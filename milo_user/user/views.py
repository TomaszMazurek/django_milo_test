from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import MiloAddForm, MiloUpdateForm
from .models import MiloUser
from .utils import is_fizz_buzz, get_age


def milo_user_list_view(request):
    users = MiloUser.objects.all()
    user_attributes = []

    for i, user in enumerate(users):
        user_attributes.append({"fizzbuzz": is_fizz_buzz(user), "eligible": get_age(user)})

    user_data = zip(users, user_attributes)
    return render(request, "user/list.html", {"users": user_data})


def milo_user_view(request, name):
    return render(request, "user/detail.html", {"user": MiloUser.objects.get(username=name)})


def milo_user_add_view(request):
    if request.method == 'POST':
        form = MiloAddForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.birthDate = form.cleaned_data.get('birthDate')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = MiloAddForm()
    return render(request, 'user/add.html', {'form': form})


def milo_user_delete_view(request, name):
    MiloUser.objects.get(username=name).delete()
    return HttpResponseRedirect('/')


def milo_user_update_view(request, name):
    if request.method == 'POST':
        form = MiloUpdateForm(request.POST, instance=MiloUser.objects.get(username=name))
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.birthDate = form.cleaned_data.get('birthDate')
            user.number = form.cleaned_data.get('number')
            user.save()
            return redirect('/')
    else:
        user_old = MiloUser.objects.get(username=name)
        form = MiloUpdateForm(instance=MiloUser.objects.get(username=name))
        initial = form["username"]
        values = initial
    return render(request, "user/update.html", {"form": form, "user": MiloUser.objects.get(username=name)})
