from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
from . import scraper
import time

# Create your views here.

def index(request):
    msg = ""
    url = "https://www.vrs.de/index.php?eID=tx_vrsinfo_ass2_departuremonitor&i=10f097e955db1f293542baf07a4a13e4"
    headers = requests.utils.default_headers()
    headers.update({
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    })
    r = requests.get(url, headers)
    tries = 0
    while r.status_code != 200 and tries <= 5:
        r = requests.get(url, headers)
        tries = tries + 1
    if tries >= 5:
        msg = "Der Statuscode beträgt: " + str(r.status_code)
    raw_html = r.content
    bus_info = json.loads(raw_html)
    for i in range(0, len(bus_info["events"])):
        bus_info["events"][i]["departure"]["comes_in"] = round((bus_info["events"][i]["departure"]["timestamp"] - time.time()) / 60)

    return render(request=request,
                  template_name="bus/index.html",
                  context={"bus_info": bus_info, "msg": msg})