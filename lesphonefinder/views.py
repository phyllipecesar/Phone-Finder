# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from lesphonefinder.models import Location
from lesphonefinder.accounts.models import Mobile
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.models import Site
from lesphonefinder.accounts.forms import UserCreateForm 
from django.utils.translation import ugettext
from lesphonefinder.utils import validate_captcha, update_location
from lesphonefinder.settings import STATIC_PREFIX
from threading import *

"Phone Finder it is an app that allows the user to know the location of his mobile"

lang_message = { 
    'PORTUGUESE': {
        'INFO_PHONE_FINDER':u"""Phone Finder é um aplicativo que permite o usuário saber a localização do seu celular via web a partir do GPS do seu aparelho.
Além disso o aplicativo possibilita acesso remoto ao seu celular, isto é, quando você não estiver encontrando seu celular e o mesmo estiver no silencioso, você não precisa perder seu tempo procurando pela sua residência. Você pode ativar pelo nosso website que o seu telefone toque algum tipo de alarme, facilitando a busca do aparelho!
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


"""
This is the home view, it has two possibilities, if the user is logged in and if not.
If the user is logged in, the template automatically will the renderize the register option.
And I also receive here the POST method, so I need to check if the POST was from for example the
register or login way.
Basically home, is just the home, with login option and register.

"""    

def home(request):
    danilo_locations = Location.objects.filter(mobile__user__username='danilopmn')

    intro_message = ugettext("""Phone Finder is an app that allows you to track your cellphone through its GPS feature. 
Moreover, you can via this app remotely control your cellphone, say, if you can't find it and it is in the silent mode, 
there is no need to waste time trying to find it in every corner of your home, just use Phone Finder to activate an alarm in the device to ease your search!
Wait, there's more! If your cellphone is stolen, you can use Phone Finder to make your cellphone take pictures every 10 minutes
 and store it in our database, so that you can help the police catch the thieves red-handed!""")
    #print current_site.domain, current_site.name, current_site
    user = request.user

    #intro_message = lang_message['PORTUGUESE']['INFO_PHONE_FINDER']
  
    if not user.is_active:
        registration_form = UserCreateForm(prefix="registration")

    if not user.is_active and request.method == 'POST':
        if request.POST.has_key('registration-username'):
            try:
                privatekey = '6LeqdM4SAAAAAFxk7YzPB2JDlc0I5J4VUdT2u6Of'
                remoteip  = request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get('REMOTE_ADDR')
                
                try:

                    challenge = request.POST['recaptcha_challenge_field']
                    response  = request.POST['recaptcha_response_field']
                except:
                    challenge = ""
                    response = ""
                registration_form = UserCreateForm(request.POST, prefix="registration")
                if registration_form.is_valid():
                    if validate_captcha(privatekey, remoteip, challenge, response):
                        registration_user = registration_form.save(commit=False)
                        registration_user.save()                        
                        user = authenticate(username=request.POST['registration-username'], password=request.POST['registration-password1'])
                        login(request, user)
                        
                    else:
                        reg_captcha = ugettext("Invalid captcha.")
            except:
                pass
        else:
            try:
                form_username = request.POST['username']
                form_password = request.POST['password']
                user = authenticate(username=form_username, password=form_password)
                
                if user is not None:
                    if user.is_active:
                        login(request, user)
                else:

                    if not form_username or not form_password:
                        
                        login_error = ugettext("Username or password can not be blank.")
                    else:
                        login_error = ugettext("Username and password mismatches.")
                   
            except:
                pass
    
    return render_to_response('base.html', locals(), context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return redirect( STATIC_PREFIX )

def view_mobile_map(request, mobile_id):
    mobile = get_object_or_404(Mobile, pk=mobile_id)
    user = request.user
    """if mobile.user != user:
        raise Http404("User is not the same.")
    """
    locations = Location.objects.filter(mobile=mobile)
    
    return render_to_response('accounts/map_display.html', locals(), context_instance=RequestContext(request))

    


class UpdateLocation(Thread):
    def __init__(self, request):
        Thread.__init__(self)
        self.request = request

    def run(self):
        update_location(self.request)
        
def update(request):
    UpdateLocation(request).start()
    return HttpResponse("")

            
