from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from lesphonefinder.models import Location

def home(request):
    try:
        ob = Location.objects.all()[0]
        CUR_LATI = ob.lati
        CUR_LONGI = ob.longi
    except:
        CUR_LATI = 40.69847032728747
        CUR_LONGI = -73.951442241668722
    
    return render_to_response('base.html', locals(), context_instance=RequestContext(request))

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

            
