SESSION_KEY = '_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'
HASH_SESSION_KEY = '_auth_user_hash'
from user.models import AnonymousUser,User
from hmac import compare_digest

from importlib import import_module
from django.utils.functional import SimpleLazyObject
from django.conf import settings

def force_bytes(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_bytes, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.
    If strings_only is True, don't convert (some) non-string-like objects.
    """
    # Handle the common case first for performance reasons.
    if isinstance(s, bytes):
        if encoding == 'utf-8':
            return s
        else:
            return s.decode('utf-8', errors).encode(encoding, errors)
    if strings_only and is_protected_type(s):
        return s
    if isinstance(s, memoryview):
        return bytes(s)
    if isinstance(s, Promise) or not isinstance(s, str):
        return str(s).encode(encoding, errors)
    else:
        return s.encode(encoding, errors)

def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        ) from err

def load_backend(path):
    return import_string(path)()

def _get_user_session_key(request,model):
    # This value in the session is always serialized to a string, so we need
    # to convert it back to Python whenever we access it.
    return model._meta.pk.to_python(request.session[SESSION_KEY])

def user(request):
    """
    Return the user model instance associated with the given request session.
    If no user is retrieved, return an instance of `AnonymousUser`.
    """
    user = None
    backend = 'mobile.backends.ModelBackend'
    model = User
    try:
        user_id = _get_user_session_key(request,model)
        backend_path = request.session[BACKEND_SESSION_KEY]
    except KeyError:
        pass
    else:
        backend = load_backend(backend)
        user = backend.get_user(user_id)
        # Verify the session
        if hasattr(user, 'get_session_auth_hash'):
            session_hash = request.session.get(HASH_SESSION_KEY)
            session_hash_verified = session_hash and compare_digest(
                force_bytes(session_hash),
                force_bytes(user.get_session_auth_hash())
            )
            if not session_hash_verified:
                request.session.flush()
                user = None

    return user or AnonymousUser()

def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = user(request)
    return request._cached_user

class AuthenticationMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        response = response or self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE%s setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")
        request.user = SimpleLazyObject(lambda: get_user(request))