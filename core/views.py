from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.conf import settings
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core import serializers
from django.contrib.sessions.models import Session

import os.path
import random
import string
import simplejson as json

import nav
from forms import UploadFileForm
from models import Image
from session_chat.models import add_message

def index(req):
  i = Image.objects.get_weighted_random_object()
  form = UploadFileForm()
  if not i:
    return render_to_response("hdil/empty.html", {"form":form},
                              context_instance=RequestContext(req))

  return render_to_response("hdil/index.html", {"image": i, "form":form},
                            context_instance=RequestContext(req))


def submit(req, img_id):
  if req.method == "POST":
    try:
      i = Image.objects.get(pk=img_id)
      vote = int(req.POST["vote"])
      if vote > 0:
        i.score += 1
      i.votecount += 1

      max_votes = getattr(settings, 'MAX_VOTES', 5)
      if i.votecount >= max_votes:
        add_message(req, str(i), i.session);
        i.delete()
        os.remove(os.path.join(getattr(settings, "MEDIA_ROOT", "/media/"),
                                i.filename))
      else:
        i.save()
    except (ValueError, KeyError, Image.DoesNotExist):
      pass
  return HttpResponseRedirect(reverse('index'))


def upload(req):
  if req.method == "POST":
    form = UploadFileForm(req.POST, req.FILES)
    if form.is_valid():
      path = getattr(settings, "MEDIA_ROOT", "/media/")
      while True:
        fname = "".join(random.choice(string.ascii_letters)
                        for _ in range(0,5)) + ".jpg" # TODO correct extension
        if not os.path.exists(os.path.join(path, fname)):
          break
      try:
        dst = open(os.path.join(path, fname), 'wb+')
        for chunk in req.FILES["file"].chunks():
          dst.write(chunk)
        dst.close()
      except IOError, e:
        print e

      i = Image(filename=fname, score=0, votecount=0,
                session = req.session.session_key)
      i.save()
  else:
    form = UploadFileForm()
  return HttpResponseRedirect(reverse('index'))
