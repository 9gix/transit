from django.views.generic import TemplateView
from django.shortcuts import render
from directions.forms import DirectionForm

class DirectionView(TemplateView):
    template_name = 'directions/index.html'
    def get_context_data(self, **kwargs):
        context = super(DirectionView, self).get_context_data(**kwargs)
        params = self.request.GET
        if params.get('go') == 'Find Bus':
            direction_from = params.get('direction_from')
            direction_to = params.get('direction_to')

        context['buses'] = []
        context['form'] = DirectionForm()
        return context
