from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages

class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, "pages/home.html")
