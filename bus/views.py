from django.shortcuts import render
from django.http import HttpResponse
from . import scraper

# Create your views here.

def index(request):
    scraper.give_bus_times()
    busliste = zip(scraper.linien, scraper.zeiten)
    return render(request=request,
                  template_name="bus/index.html",
                  context={"linien": busliste, "msg": scraper.msg})