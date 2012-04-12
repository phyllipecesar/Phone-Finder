# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from lesphonefinder.models import Location
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.contrib.auth import login, authenticate
lang_message = { 
    'PORTUGUESE': {
        'INFO_PHONE_FINDER':u"""Phone Finder é um aplicativo que permite o usuário saber a localização do seu celular via web a partir do GPS do seu aparelho.<br />
Além disso o aplicativo possibilita acesso remoto ao seu celular, isto é, quando você não estiver encontrando seu celular e o mesmo estiver no silencioso, você não precisa perder seu tempo procurando pela sua residência. Você pode ativar pelo nosso website que o seu telefone toque algum tipo de alarme, facilitando a busca do aparelho!<br />
Além do mais, se o seu telefone foi roubado você pode ativar o modo de tirar fotos automaticamente, isto é, a cada 10 minutos o aparelho irá tirar uma foto e enviar para nosso website, assim você pode tentar reconhecer o local, ou até mesmo os suspeitos.""",
        'LOGIN_ERROR_BLANK':u"Usuário e senha não podem ser vazios.",
        'LOGIN_ERROR':u"Usuário ou senha inválido.",
        
        },
    
    'ENGLISH': {
        'INFO_PHONE_FINDER':u"""
""",
        'LOGIN_ERROR_BLANK':"Username and password can't be blank.",
        'LOGIN_ERROR':"Username or password mismatches.",
        }
}

    
def home(request):
    user = request.user

    if not user.is_active:
        try:
            form_username = request.POST['username']
            form_password = request.POST['password']
            user = authenticate(username=form_username, password=form_password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            else:
                if request.POST.has_key('username') or request.POST.has_key('password'):
                    login_error = lang_message['PORTUGUESE']['LOGIN_ERROR_BLANK']
                else:
                    login_error = lang_message['PORTUGUESE']['LOGIN_ERROR']
        except:
            pass
                
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
        lati = float(request.GET['lati'].replace(",","."))
        longi = float(request.GET['longi'].replace(",","."))
        
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

            
