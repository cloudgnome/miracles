from django.utils.crypto import constant_time_compare
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.middleware.csrf import rotate_token
from user.signals import user_logged_in, user_login_failed
from django.conf import settings
from django.utils.module_loading import import_string
from user.models import User
from django.contrib.auth.hashers import check_password
from django.utils import timezone
import re

SESSION_KEY = '_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'
HASH_SESSION_KEY = '_auth_user_hash'
REDIRECT_FIELD_NAME = 'next'

def _get_user_session_key(request):
    # This value in the session is always serialized to a string, so we need
    # to convert it back to Python whenever we access it.
    return User._meta.pk.to_python(request.session[SESSION_KEY])

def load_backend(path):
    return import_string(path)()

def _get_backends(return_tuples=False):
    backends = []
    for backend_path in ['user.backends.ModelBackend']:
        backend = load_backend(backend_path)
        backends.append((backend, backend_path) if return_tuples else backend)
    if not backends:
        raise ImproperlyConfigured(
            'No authentication backends have been defined. Does '
            'AUTHENTICATION_BACKENDS contain anything?'
        )
    return backends

def login(request, user, backend=None):
    """
    Persist a user id and a backend in the request. This way a user doesn't
    have to reauthenticate on every request. Note that data set during
    the anonymous session is retained when the user logs in.
    """
    session_auth_hash = ''
    if user is None:
        user = request.user
    if hasattr(user, 'get_session_auth_hash'):
        session_auth_hash = user.get_session_auth_hash()

    if SESSION_KEY in request.session:
        if _get_user_session_key(request) != user.pk or (
                session_auth_hash and
                not constant_time_compare(request.session.get(HASH_SESSION_KEY, ''), session_auth_hash)):
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()

    try:
        backend = backend or user.backend
    except AttributeError:
        backends = _get_backends(return_tuples=True)
        if len(backends) == 1:
            _, backend = backends[0]
        else:
            raise ValueError(
                'You have multiple authentication backends configured and '
                'therefore must provide the `backend` argument or set the '
                '`backend` attribute on the user.'
            )
    else:
        if not isinstance(backend, str):
            raise TypeError('backend must be a dotted import path string (got %r).' % backend)

    request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
    request.session[BACKEND_SESSION_KEY] = backend
    request.session[HASH_SESSION_KEY] = session_auth_hash
    if hasattr(request, 'user'):
        request.user = user

    rotate_token(request)
    user_logged_in.send(sender=user.__class__, request=request, user=user)

def _clean_credentials(credentials):
    """
    Clean a dictionary of credentials of potentially sensitive info before
    sending to less secure functions.
    Not comprehensive - intended for user_login_failed signal
    """
    SENSITIVE_CREDENTIALS = re.compile('api|token|key|secret|password|signature', re.I)
    CLEANSED_SUBSTITUTE = '********************'
    for key in credentials:
        if SENSITIVE_CREDENTIALS.search(key):
            credentials[key] = CLEANSED_SUBSTITUTE
    return credentials

def authenticate(request=None,value=None, password=None, **credentials):
    user = User.objects.filter(email=value).first()

    if user and check_password(password, user.password):
        user.last_login = timezone.now()
        return user

    user_login_failed.send(sender=__name__, credentials=_clean_credentials(credentials), request=request)

    return None