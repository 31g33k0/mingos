from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect


class LoginView(TemplateView):
    template_name = "auth/login.html"

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/api')
        else:
            return HttpResponse('Invalid login')
