from django.contrib.auth.models import User
from lesphonefinder.accounts.models import Mobile
from lesphonefinder.models import Location

def generate_random_id(current_id):
    new_id = ""
    possibilities = [ chr(i) for i in range(ord('a'), ord('z') ) ] + [ chr(i) for i in range(ord('A'), ord('Z')+1) ] + [ chr(i) for i in range(ord('0'), ord('9') + 1) ]
    len_max = 7
    from random import randint
    for i in xrange(len_max):

        new_id += possibilities[randint(0, len(possibilities)-1)]
    return new_id + str(current_id)

def validate_captcha(privatekey, remoteip, challenge, response):
    

    from httplib2 import Http
    
    body_val = {
                'privatekey':str(privatekey),
                'remoteip':str(remoteip),
                'challenge':str(challenge),
                'response':str(response),
                }

    headers = {
                'Content-type': 'application/x-www-form-urlencoded', 
                'Accept': 'text/plain'
                }

    from urllib import urlencode
    
    response, content = Http().request("http://www.google.com/recaptcha/api/verify", "POST", headers=headers, body=urlencode(body_val))

    return 'true' in content


def update_location(request):
    try:
        identifier = request.GET['identifier']
        username = request.GET['username']
        
        lati = float(request.GET['lati'].replace(",","."))
        longi = float(request.GET['longi'].replace(",","."))
        
        mobile = Mobile.objects.filter(identifier=identifier)[0] # I do not care if it does not exist
        
        user = User.objects.filter(username=username)[0] # I dont not care if Username is invalid
        
        if (mobile.user != user):
            raise Exception()
        
        Location.objects.create(mobile=mobile, lati=lati, longi=longi)
    except:
        pass
