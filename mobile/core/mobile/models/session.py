"""
This module allows importing AbstractBaseSession even
when django.contrib.sessions is not in INSTALLED_APPS.
"""
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


class BaseSessionManager(models.Manager):
    def encode(self, session_dict):
        """
        Return the given session dictionary serialized and encoded as a string.
        """
        session_store_class = self.model.get_session_store_class()
        return session_store_class().encode(session_dict)

    def save(self, session_key, session_dict, expire_date):
        s = self.model(session_key, self.encode(session_dict), expire_date)
        if session_dict:
            s.save()
        else:
            s.delete()  # Clear sessions with no data.
        return s


@python_2_unicode_compatible
class AbstractBaseSession(models.Model):
    session_key = models.CharField(_('session key'), max_length=40, primary_key=True)
    session_data = models.TextField(_('session data'))
    expire_date = models.DateTimeField(_('expire date'), db_index=True)

    objects = BaseSessionManager()

    class Meta:
        abstract = True
        verbose_name = _('session')
        verbose_name_plural = _('sessions')

    def __str__(self):
        return self.session_key

    @classmethod
    def get_session_store_class(cls):
        raise NotImplementedError

    def get_decoded(self):
        session_store_class = self.get_session_store_class()
        return session_store_class().decode(self.session_data)


class SessionManager(BaseSessionManager):
    use_in_migrations = True

class Session(AbstractBaseSession):
    """
    Django provides full support for anonymous sessions. The session
    framework lets you store and retrieve arbitrary data on a
    per-site-visitor basis. It stores data on the server side and
    abstracts the sending and receiving of cookies. Cookies contain a
    session ID -- not the data itself.

    The Django sessions framework is entirely cookie-based. It does
    not fall back to putting session IDs in URLs. This is an intentional
    design decision. Not only does that behavior make URLs ugly, it makes
    your site vulnerable to session-ID theft via the "Referer" header.

    For complete documentation on using Sessions in your code, consult
    the sessions documentation that is shipped with Django (also available
    on the Django Web site).
    """
    objects = SessionManager()

    @classmethod
    def get_session_store_class(cls):
        return SessionStore

    # class Meta(AbstractBaseSession.Meta):
    #     db_table = 'django_session'import logging


from django.contrib.sessions.backends.base import (
    CreateError, SessionBase, UpdateError,
)
from django.core.exceptions import SuspiciousOperation
from django.db import DatabaseError, IntegrityError, router, transaction
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.functional import cached_property


class SessionStore(SessionBase):
    """
    Implements database session store.
    """
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

    @classmethod
    def get_model_class(cls):
        # Avoids a circular import and allows importing SessionStore when
        # django.contrib.sessions is not in INSTALLED_APPS.
        return Session

    @cached_property
    def model(self):
        return self.get_model_class()

    def load(self):
        try:
            s = self.model.objects.get(
                session_key=self.session_key,
                expire_date__gt=timezone.now()
            )
            return self.decode(s.session_data)
        except (self.model.DoesNotExist, SuspiciousOperation) as e:
            if isinstance(e, SuspiciousOperation):
                logger = logging.getLogger('django.security.%s' % e.__class__.__name__)
                logger.warning(force_text(e))
            self._session_key = None
            return {}

    def exists(self, session_key):
        return self.model.objects.filter(session_key=session_key).exists()

    def create(self):
        while True:
            self._session_key = self._get_new_session_key()
            try:
                # Save immediately to ensure we have a unique entry in the
                # database.
                self.save(must_create=True)
            except CreateError:
                # Key wasn't unique. Try again.
                continue
            self.modified = True
            return

    def create_model_instance(self, data):
        """
        Return a new instance of the session model object, which represents the
        current session state. Intended to be used for saving the session data
        to the database.
        """
        return self.model(
            session_key=self._get_or_create_session_key(),
            session_data=self.encode(data),
            expire_date=self.get_expiry_date(),
        )

    def save(self, must_create=False):
        """
        Saves the current session data to the database. If 'must_create' is
        True, a database error will be raised if the saving operation doesn't
        create a *new* entry (as opposed to possibly updating an existing
        entry).
        """
        if self.session_key is None:
            return self.create()
        data = self._get_session(no_load=must_create)
        obj = self.create_model_instance(data)
        using = router.db_for_write(self.model, instance=obj)
        try:
            with transaction.atomic(using=using):
                obj.save(force_insert=must_create, force_update=not must_create, using=using)
        except IntegrityError:
            if must_create:
                raise CreateError
            raise
        except DatabaseError:
            if not must_create:
                raise UpdateError
            raise

    def delete(self, session_key=None):
        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key
        try:
            self.model.objects.get(session_key=session_key).delete()
        except self.model.DoesNotExist:
            pass

    @classmethod
    def clear_expired(cls):
        cls.get_model_class().objects.filter(expire_date__lt=timezone.now()).delete()
