from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .forms import FindForm, VacancyForm
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


def vacancy_detail(request, pk=None):
    # vac_object = Vacancy.objects.get(pk=pk)
    vac_object = get_object_or_404(Vacancy, pk=pk)
    return render(request, 'scraping/vacancy_detail.html', {'object': vac_object})


class VacancyDetail(DetailView):
    queryset = Vacancy.objects.all()
    template_name = 'scraping/vacancy_detail.html'
    # context_object_name = 'object'


class VacancyList(ListView):
    model = Vacancy
    template_name = 'scraping/list.html'
    form = FindForm()
    paginate_by = 10


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['language'] = self.request.GET.get('language')
        context['form'] = self.form

        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        if city or language:
            filt = {}
            if city:
                filt['city__slug'] = city
            if language:
                filt['language__slug'] = language
            qs = Vacancy.objects.filter(**filt).select_related('city', 'language')
        return qs


class VacancyCreateView(CreateView):
    model = Vacancy
    # fields = '__all__'
    form_class = VacancyForm
    template_name = 'scraping/create.html'
    success_url = reverse_lazy('home')


class VacancyUpdateView(UpdateView):
    model = Vacancy
    # fields = '__all__'
    form_class = VacancyForm
    template_name = 'scraping/create.html'
    success_url = reverse_lazy('home')


class VacancyDelete(DeleteView):
    model = Vacancy
    template_name = 'scraping/delete.html'
    success_url = reverse_lazy('home')

    # def get(self, request, *args, **kwargs): # without template_name
    #     messages.success(request, 'Запись успешно удалена')
    #     return self.post(request, *args, **kwargs)
