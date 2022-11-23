from django.shortcuts import render
from .forms import FindForm
from .models import Vacancy


def home_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    qs = []
    if city or language:
        filt = {}
        if city:
            filt['city__slug'] = city
        if language:
            filt['language__slug'] = language
        qs = Vacancy.objects.filter(**filt)
    return render(request, 'scraping/home.html', {'object_list': qs, 'form': form})
