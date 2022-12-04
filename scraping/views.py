from django.core.paginator import Paginator
from django.shortcuts import render
from .forms import FindForm
from .models import Vacancy


def home_view(request):
    form = FindForm()
    return render(request, 'scraping/home.html', {'form': form})


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    context = {'city': city, 'language': language, 'form': form}
    if city or language:
        filt = {}
        if city:
            filt['city__slug'] = city
        if language:
            filt['language__slug'] = language
        qs = Vacancy.objects.filter(**filt)
        paginator = Paginator(qs, 10)  # Show 10 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scraping/list.html', context)
