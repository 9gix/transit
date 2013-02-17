from django.views.generic import TemplateView


class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        return super(HomeView, self).get_context_data(**kwargs)
    template_name = 'home.html'
