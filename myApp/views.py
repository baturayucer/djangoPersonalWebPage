from django.shortcuts import render
from myApp.models import Users
from . import forms
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView , View

# Create your views here.


def index(request):
    return render(request, 'myApp/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def aboutus(request):
    return render(request, 'myApp/aboutus.html')


class userLogin(TemplateView):

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account is not active')
        else:
            print('Someone tried to login and failed')
            print(f'username: {username}')
            return HttpResponse('invalid login credentials')

    def get(self, request, *args, **kwargs):
        return render(request, 'myApp/user_login.html')


class formView(View):
    form = forms.UserForm

    def post(self, request, *args, **kwargs):
        form = forms.UserForm(request.POST)

        if form.is_valid():
            try:
                cli_addr = request.META.get('REMOTE_ADDR')

                try:
                    record = Users.objects.get(email=form.cleaned_data['email'])
                    return render(request, 'myApp/errorpage.html')
                except Users.DoesNotExist:
                    user = form.save(commit=False)
                    user.set_password(user.password)
                    user.save()
                    return render(request, 'myApp/successpage.html', context={'username': form.cleaned_data['username']})
            except Exception as a:
                return render(request, 'myApp/errorpage.html')
        else:
            return HttpResponse('Form is not valid')

    def get(self, request, *args, **kwargs):
        form = self.form
        if request.user.is_authenticated:
            return render(request, 'myApp/logoutFirst.html')
        else:
            return render(request, 'myApp/register.html', context={'form': form})










