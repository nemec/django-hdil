import simplejson as json
from django.contrib import messages

class AjaxMessaging(object):

  def process_response(self, request, response):
    if request.is_ajax():
      if response['Content-Type'] in ["application/javascript",
                                      "application/json"]:
        try:
          content = json.loads(response.content)
        except ValueError:
          return response

        

    return response
