from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render
from datetime import datetime, timedelta, time
from django.views.decorators.csrf import csrf_exempt
#
from django.conf import settings
from authApp.models import  User
from accessApp.models import Vehicle, Access
#
#
from imutils.video import VideoStream
import imagezmq
import socket
import time
import cv2
import glob
import os
#
@login_required
def home_page(request):
    hasPerm = False
    if request.user.has_perm('accessApp.view_access'):
        hasPerm = True

    today = datetime.now().date()
    #today = datetime.combine(today, time())

    if hasPerm:
        users = User.objects.all()
        vehicles = Access.objects.filter(exit__isnull=True)
        last_accesses = Access.objects.filter(entrance__gte=today).order_by('-created')[:10]
        accesses = Access.objects.filter(entrance__gte=today).order_by('-created')
    else:
        users = [request.user]
        vehicles = Access.objects.filter(vehicle__user=request.user, exit__isnull=True)
        last_accesses = Access.objects.filter(entrance__gte=today, vehicle__user=request.user).order_by('-created')[:10]
        accesses = Access.objects.filter(entrance__gte=today, vehicle__user=request.user).order_by('-created')

    context = {
        'users': users,
        'vehicles': vehicles,
        'accesses': accesses,
        'last_accesses': last_accesses,
        'page_name': 'Dashboard',
        'menu_dashboard': 'active',
    }
    return render(request, 'home/index.html', context)

def send_images(request):
    #ip = args["ip"]
    #ip = '192.168.2.111'

    #sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(ip))

    #vs = VideoStream(src=0).start()
    #time.sleep(2.0)
    #while True:
    #   frame = vs.read()
    #    sender.send_image('pi-client', frame)
    #    cv2.imshow('Frame', frame)

    response = render_to_response('home/sendImages.html')
    response.status_code = 403
    return response

@csrf_exempt
def save_image(request):
    if request.method == 'POST':
        # save it somewhere
        f = open(settings.MEDIA_ROOT + '/webcamimages/someimage.jpg', 'wb')
        f.write(request.body)
        f.close()

        #ip = '192.168.2.105'
        ip = '192.168.43.172'
        sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(ip))
        frame = cv2.imread(settings.MEDIA_ROOT + '/webcamimages/someimage.jpg')
        sender.send_image('pi-client', frame)
        # return the URL
        return HttpResponse('http://localhost:8008/'+settings.MEDIA_ROOT + '/webcamimages/someimage.jpg')
    else:
        return HttpResponse('no data')
def handler403(request, *args, **argv):
    response = render_to_response('errors/403.html')
    response.status_code = 403
    return response

def handler404(request, *args, **argv):
    response = render_to_response('errors/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render_to_response('errors/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
