from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import UserLoginForm


def login_view(request):
    form = UserLoginForm(request.POST or None)
    next_ = request.GET.get('next')
    if form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username.strip(),
                            password=password.strip())
        login(request, user)
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or '/'
        return redirect(redirect_path)
    return render(request, 'accounts/login.html', context={'form': form, })


def logout_view(request):
    logout(request)
    return redirect('fakecsv:data_schema_list')
