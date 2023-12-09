from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView

from functools import reduce
from operator import and_

from phone_directory.models import Main, Firstname, Street, Surname, Patronymic
from phone_directory.forms import MainForm, SearchForm, FirstnameForm, SurnameForm, PatronymicForm, StreetForm


class GenericModelView(ListView):
    context_object_name = 'tasks'
    template_name = 'phone_dictionary/index.html'
    model = Main

    def get(self, request, *args, **kwargs):
        model_name = self.kwargs.get('model_name', 'main')
        model_mapping = {
            'main': Main,
            'firstname': Firstname,
            'surname': Surname,
            'street': Street,
            'patronymic': Patronymic,
        }
        self.model = model_mapping.get(model_name, Main)
        return super().get(request, *args, **kwargs)

    def get_template_names(self):
        return [f'phone_dictionary/{self.model.__name__.lower()}_list.html']

    def get_queryset(self):
        return self.model.objects.all()        

def delete_task(request, model_name, task_id):
    model_mapping = {
            'main': Main,
            'firstname': Firstname,
            'surname': Surname,
            'street': Street,
            'patronymic': Patronymic,
        }
    model = model_mapping.get(model_name)

    if not model:
        return redirect('index')
    
    task = get_object_or_404(model, id=task_id)
    
    if request.method == 'POST':
        task.delete()
        table_template = f'{model_name.lower()}_list'
        return redirect(reverse(table_template))

    return redirect('index')



class LineCreateView(SuccessMessageMixin, CreateView):
    success_message = 'Запись добавлена!'
    
    def get_form_class(self):
        model_name = self.kwargs.get('model_name', 'main')
        form_mapping = {
            'main': MainForm,
            'firstname': FirstnameForm,
            'surname': SurnameForm,
            'street': StreetForm,
            'patronymic': PatronymicForm,
        }
        return form_mapping.get(model_name, MainForm)

    def get_template_names(self):
        model_name = self.kwargs.get('model_name', 'main')
        return [f'phone_dictionary/{model_name.lower()}_create.html']

    def get_success_url(self):
        model_name = self.kwargs.get('model_name', 'main')
        return reverse_lazy(f'{model_name.lower()}_list')

class LineUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'phone_dictionary/edit.html'
    model = Main
    form_class = MainForm
    success_message = 'Запись обновлена!'
    success_url = reverse_lazy('main_list')


    def get_object(self):
        return get_object_or_404(Main, id=self.kwargs['id'])
    
class SearchView(View):
    template_name = 'phone_dictionary/search.html'
    results_template_name = 'phone_dictionary/search_result.html'

    def get(self, request):
        form = SearchForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SearchForm(request.POST)
        #функция post с обработкой незаполненной формы
        if form.is_valid():
            q_filters = []

            if form.cleaned_data['surname']:
                q_filters.append(Q(surname__name=form.cleaned_data['surname']))

            if form.cleaned_data['firstname']:
                q_filters.append(
                    Q(firstname__name=form.cleaned_data['firstname']))

            if form.cleaned_data['patronymic']:
                q_filters.append(
                    Q(patronymic__name=form.cleaned_data['patronymic']))

            if form.cleaned_data['street']:
                q_filters.append(Q(street__name=form.cleaned_data['street']))

            if form.cleaned_data['house']:
                q_filters.append(Q(house=form.cleaned_data['house']))

            if form.cleaned_data['corpus']:
                q_filters.append(Q(corpus=form.cleaned_data['corpus']))

            if form.cleaned_data['apartments']:
                q_filters.append(Q(apartments=form.cleaned_data['apartments']))

            if form.cleaned_data['phone']:
                q_filters.append(Q(phone=form.cleaned_data['phone']))

            if q_filters:
                combinedfilter = reduce(and_, q_filters)
                search_results = Main.objects.filter(combinedfilter)
            
            else:
                search_results = Main.objects.none()

            return render(request, self.results_template_name, {'results': search_results})
        return render(request, self.template_name, {'form': form})