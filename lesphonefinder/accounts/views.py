# Create your views here.
from django.http import HttpResponse
from lesphonefinder.accounts.models import Mobile
from django.contrib.auth.models import User
from lesphonefinder.utils import generate_random_id

"""
This view register a mobile it takes from GET:
username, password -> So I need to validate.
Name and description of the phone
This only will return HttpResponse to the mobile see what happenned.
invalid-username (the username or password mismatch)
invalid-name (invalid phone name)
invalid-description ( invalid phone description )
"""
def register_mobile(request):

    if not request.GET.has_key('name'):
        return HttpResponse("invalid-name")
    name = request.GET['name']
    
    if not request.GET.has_key('description'):
        return HttpResponse("invalid-description")
    
    description = request.GET['description']
    
    if not request.GET.has_key('username') or not request.GET.has_key('password'):
        return HttpResponse("invalid-username")
    
    username = request.GET['username']
    password = request.GET['password']
    
    user = User.objects.filter(username=username)

    if len(user) == 0:
        return HttpResponse("invalid-username")

    user = user[0]
    
    if not user.check_password(password):
        return HttpResponse("invalid-password")

    try:
        print dir(Mobile.objects)
        mobile = Mobile.objects.create(user=user, name=name, description=description, identifier='k')
        
        print generate_random_id(mobile.id)
        print mobile.id

        mobile.identifier = generate_random_id(mobile.id)
        mobile.save()
        
        return HttpResponse(str(mobile.identifier))
    except:
        try:
            print mobile
            mobile.delete()
            
        except:
            pass
        return HttpResponse("unexpected-error")
    

