from django.contrib.auth.models import User
from lesphonefinder.accounts.models import Mobile
from lesphonefinder.models import Location, ACTIVITIES, MAXIMUM_LEN_LOCATIONS
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404


"""
This generate a random id based in a id.
This function just generates 7 characters at random and then
concatenate with the current_id, so we can guarantee that the
id is unique
"""
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


"""
This function get username and identifer from GET
and it also validates if the mobile identifier is from the same user
"""

def get_details_from_mobile(request):
    identifier = request.GET['identifier']
    username = request.GET['username']
    mobile = Mobile.objects.filter(identifier=identifier)[0] # I do not care if it does not exist
    user = User.objects.filter(username=username)[0] # I dont not care if Username is invalid
    if (mobile.user != user):
        raise Exception()

    return identifier, username, mobile, user 
    


"""
This function based on the request updates the mobile's current
position.
"""
def update_location(request):
    try:
        identifier, username, mobile, user = get_details_from_mobile(request)
        lati = float(request.GET['lati'].replace(',', '.'))
        longi = float(request.GET['longi'].replace(',','.'))
        locations = Location.objects.filter(mobile=mobile)
        if (len(locations) < MAXIMUM_LEN_LOCATIONS):
            Location.objects.create(mobile=mobile, lati=lati, longi=longi)
        else:
            location = locations.order_by('modification_date')[0]
            location.lati = lati
            location.login = longi
            location.modification_date = location.modification_date.now()
            location.save()
    except:
        pass



"""
This function based on the request, receives an activity from the mobile.
And so I need to delete this activity from that mobile, because he has
already done this activity
"""
def receive_activity(request):
    try:
        identifier, username, mobile, user = get_details_from_mobile(request)
        activity = int(request.GET['activity'])
        if activity in ACTIVITIES:
            activity = Activity.objects.filter(activity=activity, mobile=mobile)[0]
            activity.delete()

    except:
        pass


