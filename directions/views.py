from django.views.generic import View
from django.shortcuts import render

class DirectionView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'directions/index.html')
