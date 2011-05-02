from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.conf import settings

from nav.models import NewsSnippet

def news(req):
  limit = getattr(settings, "MAX_NEWS_SNIPPETS", 5)
  snip = NewsSnippet.objects.all()[:limit]
  return render_to_response("hdil/news.html", {"news_snippets": snip},
                            context_instance=RequestContext(req))

def about(req):
  return render_to_response("hdil/about.html", context_instance=RequestContext(req))
