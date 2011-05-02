import simplejson as json
from django.http import HttpResponse

from session_chat.models import get_messages

# django.contrib.sessions.models.Session.objects.get(session_key="bd8fe599df17b5ca76ce563872f67759")
# req.session.session_key

def updates(req):
  django_messages = []
  if req.is_ajax():
    for message in get_messages(req):
      django_messages.append({
        "message": message.message,
        "extra_tags": message.tags,
      })
  return HttpResponse(json.dumps(django_messages), "application/javascript")

