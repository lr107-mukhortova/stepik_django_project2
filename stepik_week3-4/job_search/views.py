from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView
from .models import Vacancy, Company, Speciality


class VacancyView(TemplateView):
    template_name = 'job_search/vacancy.html'

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        context['vacancy'] = get_object_or_404(Vacancy, pk=context['vacancy_pk'])
        context['vacancies_count'] = Vacancy.objects.count()
        return context


class MainView(TemplateView):
    template_name = 'job_search/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['companies'] = Company.objects.annotate(num_vacancies=Count('vacancies'))
        context['specialities'] = Speciality.objects.annotate(num_vacancies=Count('vacancies'))
        return context


class VacanciesView(ListView):
    template_name = 'job_search/vacancies.html'
    context_object_name = 'vacancies'
    model = Vacancy

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacanciesView, self).get_context_data(**kwargs)
        context['title'] = "Все вакансии"  # Тайтл в темплэйт
        return context


class VacanciesByCategoryView(ListView):
    template_name = 'job_search/vacancies.html'
    model = Vacancy
    context_object_name = 'vacancies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacanciesByCategoryView, self).get_context_data(**kwargs)
        category = get_object_or_404(Speciality, code=self.kwargs['category'])
        context['title'] = category.title  # Тайтл в темплэйте.
        return context

    def get_queryset(self):
            category = self.kwargs['category']
            speciality = get_object_or_404(Speciality, code=category)
            return Vacancy.objects.filter(specialty=speciality)


class CompanyView(TemplateView):
    template_name = 'job_search/company.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['company'] = get_object_or_404(Company, pk=context['company_pk'])
        context['companies_count'] = Company.objects.count()
        return context


# обработка ошибок
def custom_handler404(request, exception):
    return HttpResponseNotFound('Ресурс не найдет!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
