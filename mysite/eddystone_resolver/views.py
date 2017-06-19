from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from .models import Beacon, EID

def index(request):
    return HttpResponse("Hello world")

def beacons(request):
    return JsonResponse([model_to_dict(beacon) for beacon in Beacon.objects.all()], safe=False)

def beacon(request, beacon_name):
    if request.method == 'GET':
        beacon = get_object_or_404(Beacon, name=beacon_name)
        return JsonResponse(model_to_dict(beacon))

def resolve_eid(request, beacon_eid):
    eid = get_object_or_404(EID, eid=beacon_eid)
    return JsonResponse(model_to_dict(eid.beacon))
