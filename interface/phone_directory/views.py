from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy

from functools import reduce
from operator import and_

from phone_directory.models import Main
from phone_directory.forms import MainForm, SearchForm


class IndexView(TemplateView):
    template_name = 'phone_dictionary/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Main.objects.all()
        return context


def delete_task(request, task_id):
    task = get_object_or_404(Main, id=task_id)
    
    if request.method == 'POST':
        task.delete()
        return redirect('index')

    return redirect('index')



class LineCreateView(SuccessMessageMixin, CreateView):
    template_name = 'phone_dictionary/add.html'
    form_class = MainForm
    success_message = 'Запись добавлена!'
    success_url = reverse_lazy('index')


class LineUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'phone_dictionary/edit.html'
    model = Main
    form_class = MainForm
    success_message = 'Запись обновлена!'
    success_url = reverse_lazy('index')


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

            if q_filters:
                combinedfilter = reduce(and_, q_filters)
                search_results = Main.objects.filter(combinedfilter)
            else:
                search_results = Main.objects.none()

            return render(request, self.results_template_name, {'results': search_results})
        return render(request, self.template_name, {'form': form})