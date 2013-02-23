from django.views.generic import TemplateView
from transit.models import Bus


class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['buses'] = Bus.all()
        return context
    template_name = 'home.html'
