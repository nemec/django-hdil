from django.contrib.messages.storage.base import BaseStorage
from django.contrib.sessions.models import Session


class CommunicatorStorage(BaseStorage):

    """
    Stores messages in the session (that is, django.contrib.sessions).
    """
    session_key = '_messages'

    def __init__(self, request, *args, **kwargs):
        assert hasattr(request, 'session'), "The session-based temporary "\
            "message storage requires session middleware to be installed, "\
            "and come before the message middleware in the "\
            "MIDDLEWARE_CLASSES list."
        super(CommunicatorStorage, self).__init__(request, *args, **kwargs)

    def _get(self, *args, **kwargs):
        """
        Retrieves a list of messages from the request's session.  This storage
        always stores everything it is given, so return True for the
        all_retrieved flag.
        """
        return self.request.session.get(self.session_key), True

    def _store(self, messages, response, *args, **kwargs):
        """
        Stores a list of messages to the request's session.
        """
        #import pdb; pdb.set_trace()
        if messages:
            for session in Session.objects.all():
              d = session.get_decoded()
              print messages
              d[self.session_key] = messages
              session.session_data = Session.objects.encode(d)
              session.save() 
        else:
            self.request.session.pop(self.session_key, None)
        return []
