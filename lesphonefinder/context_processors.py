from lesphonefinder.settings import STATIC_PREFIX
def static_prefix(request):
    return { 'STATIC_PREFIX': STATIC_PREFIX }
