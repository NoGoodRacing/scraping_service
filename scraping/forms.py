from django import forms
from .models import City, Language, Vacancy


class FindForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), to_field_name='slug', required=False,
        widget=forms.Select(attrs={'class': 'form-control'}), label='Город')
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(), to_field_name='slug', required=False,
        widget=forms.Select(attrs={'class': 'form-control'}), label='Специальность')


class VacancyForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}), label='Город')
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}), label='Специальность')

    class Meta:
        model = Vacancy
        fields = '__all__'
