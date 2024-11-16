from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponseRedirect
from .models import Link

def scrape(request):
    if request.method == "POST":
        site = request.POST.get('site','')

        try:
            page = requests.get(site)
            page.raise_for_status()  # Ensure no HTTP errors
            soup = BeautifulSoup(page.text, 'html.parser')

            for link in soup.find_all('a'):
                link_address = link.get('href') if link.get('href') else ''
                link_text = link.string if link.string else ''
                Link.objects.create(address=link_address, name=link_text)

            return HttpResponseRedirect('/')
        except requests.RequestException as e:
            # Handle request exceptions, e.g., invalid URL or connection errors
            data = Link.objects.all()  # Retrieve existing data for rendering
            return render(request, 'myapp/result.html', {'data': data, 'error_message': str(e)})

    else:
        data = Link.objects.all()

    return render(request, 'myapp/result.html', {'data': data})

def clear(request):
    Link.objects.all().delete()
    return render(request,'myapp/result.html')
