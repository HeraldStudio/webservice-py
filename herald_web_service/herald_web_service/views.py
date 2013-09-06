from django.http import HttpResponse

def home(request):
    return HttpResponse("web-service-py homepage")
