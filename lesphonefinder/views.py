# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from lesphonefinder.models import Location
from django.contrib.auth.models import User
from django.core.context_processors import csrf

def home(request):
    try:
        ob = Location.objects.all()[0]
        CUR_LATI = ob.lati
        CUR_LONGI = ob.longi
    except:
        CUR_LATI = 40.69847032728747
        CUR_LONGI = -73.951442241668722
    
    return render_to_response('base.html', locals(), context_instance=RequestContext(request))


def validate(stra):
    for i in stra:
        if ord(i) >= ord('a') and ord(i) <= ord('z'):
            continue
        if ord(i) >= ord('A') and ord(i) <= ord('Z'):
            continue
        if ord(i) >= ord('0') and ord(i) <= ord('9'):
            continue
        return False
    return True
def register(request):
    user = request.user
    c = {}
    c.update(csrf(request))
    if user.is_active:
        error = u'Você já está registrado'
    else:
        try:
            username = request.POST['username']
            password = request.POST['password']
            
            if not validate(username):
                error = u"Username contém caracteres especiais!"
            elif not validate(password):
                error = u"Password contém caracteres especiais!"
            elif not username:
                error = u"Não pode ser nulo"
            elif not password:
                error = u"Password não pode ser nulo"
            else:
                try:
                    User.objects.create(username=username, password=password)
                    return redirect("/")
                except:
                    error = u"Usuario ja existe"
                

        except:
           pass

    return render_to_response('accounts/register.html', locals(), context_instance=RequestContext(request))
def update(request):
    try:
        lati = float(request.GET['lati'])
        longi = float(request.GET['longi'])
        print lati, longi
        print Location.objects.all()
        try:
            ob = Location.objects.all()[0]
        except:
            Location.objects.create(lati=lati, longi=longi)
            ob = Location.objects.all()[0]
        ob.lati = lati
        ob.longi = longi
        ob.save()
    except:
        pass
    return HttpResponse("")

            
