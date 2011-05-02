from django.contrib.sessions.models import Session

from django.conf import settings
from django.utils.encoding import force_unicode, StrAndUnicode

def add_message(request, message, session, extra_tags='', fail_silently=False):
    """
    Attempts to add a message to the request using the 'messages' app.
    """
    if hasattr(request, '_messages'):
        return request._messages.add(message, session, extra_tags)
    if not fail_silently:
        raise MessageFailure('You cannot add messages without installing '
                    'session_chat.middleware.MessageMiddleware')


def get_messages(request):
    """
    Returns the message storage on the request if it exists, otherwise returns
    an empty list.
    """
    if hasattr(request, '_messages'):
        return request._messages
    else:
        return []


class Message(StrAndUnicode):
    """
    Represents an actual message that can be stored in any of the supported
    storage classes (typically session- or cookie-based) and rendered in a view
    or template.
    """

    def __init__(self, message, session, extra_tags=None):
        self.message = message
        self.extra_tags = extra_tags
        self.session = session

    def _prepare(self):
        """
        Prepares the message for serialization by forcing the ``message``
        and ``extra_tags`` to unicode in case they are lazy translations.

        Known "safe" types (None, int, etc.) are not converted (see Django's
        ``force_unicode`` implementation for details).
        """
        self.message = force_unicode(self.message, strings_only=True)
        self.extra_tags = force_unicode(self.extra_tags, strings_only=True)

    def __eq__(self, other):
        return isinstance(other, Message) and self.message == other.message

    def __unicode__(self):
        return force_unicode(self.message)

    def _get_tags(self):
        extra_tags = force_unicode(self.extra_tags, strings_only=True)
        if extra_tags:
            return extra_tags
        return ''
    tags = property(_get_tags)

class ChatStorage(object):
    """
    This is the base backend for temporary message storage.

    This is not a complete class; to be a usable storage backend, it must be
    subclassed and the two methods ``_get`` and ``_store`` overridden.
    """

    msg_key = '_messages'

    def __init__(self, request, *args, **kwargs):
        assert hasattr(request, 'session'), "The session-based temporary "\
            "message storage requires session middleware to be installed, "\
            "and come before the message middleware in the "\
            "MIDDLEWARE_CLASSES list."
        self.request = request
        self._queued_messages = []
        self.used = False
        self.added_new = False

    def __len__(self):
        return len(self._loaded_messages) + len(self._queued_messages)

    def __iter__(self):
        self.used = True
        if self._queued_messages:
            self._loaded_messages.extend(self._queued_messages)
            self._queued_messages = []
        return iter(self._loaded_messages)

    def __contains__(self, item):
        return item in self._loaded_messages or item in self._queued_messages

    @property
    def _loaded_messages(self):
        """
        Returns a list of loaded messages, retrieving them first if they have
        not been loaded yet.
        """
        if not hasattr(self, '_loaded_data'):
            messages, all_retrieved = self._get()
            self._loaded_data = messages or []
        return self._loaded_data

    def _get(self, *args, **kwargs):
        """
        Retrieves a list of messages from the request's session.  This storage
        always stores everything it is given, so return True for the
        all_retrieved flag.
        """
        session = Session.objects.get(session_key = self.request.session.session_key)
        d = session.get_decoded()
        return d.get(self.msg_key, []), True

    def _store(self, messages, response, *args, **kwargs):
        """
        Stores a list of messages to the request's session.
        """
        if messages:
            for message in messages:
              session = Session.objects.get(session_key = message.session)
              d = session.get_decoded()
              if not self.msg_key in d:
                d[self.msg_key] = []
              d[self.msg_key].append(message)
              session.session_data = Session.objects.encode(d)
              session.save() 
        else:
            self.request.session.pop(self.msg_key, None)
        return []

    def _prepare_messages(self, messages):
        """
        Prepares a list of messages for storage.
        """
        for message in messages:
            message._prepare()

    def update(self, response):
        """
        Stores all unread messages.

        If the backend has yet to be iterated, previously stored messages will
        be stored again. Otherwise, only messages added after the last
        iteration will be stored.
        """
        self._prepare_messages(self._queued_messages)
        if self.used:
            return self._store(self._queued_messages, response)
        elif self.added_new:
            messages = self._loaded_messages + self._queued_messages
            return self._store(messages, response)

    def add(self, message, session, extra_tags=''):
        """
        Queues a message to be stored.

        """
        if not message:
            return
        # Add the message.
        self.added_new = True
        message = Message(message, session, extra_tags=extra_tags)
        self._queued_messages.append(message)

