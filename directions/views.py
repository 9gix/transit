from django.views.generic import View
from django.shortcuts import render
from directions.forms import DirectionForm

class DirectionView(View):
    def get(self, request, *args, **kwargs):
        form = DirectionForm()
        return render(request, 'directions/index.html', locals())
