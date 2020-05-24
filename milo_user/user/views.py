import csv
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .forms import MiloAddForm, MiloUpdateForm
from .models import MiloUser
from .utils import is_fizz_buzz, get_age


def milo_user_list_view(request):
    users = MiloUser.objects.all()
    user_attributes = []
    for user in users:
        user_attributes.append({"fizzbuzz": is_fizz_buzz(user), "eligible": get_age(user)})

    user_data = zip(users, user_attributes)
    return render(request, "user/list.html", {"users": user_data})

    
def milo_user_view(request, name):
    user = MiloUser.objects.get(username=name)
    return render(request, "user/detail.html", {"user": user,
                                                "fizzbuzz": is_fizz_buzz(user),
                                                "eligible": get_age(user)})


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
        form = MiloUpdateForm(instance=MiloUser.objects.get(username=name))
    return render(request, "user/update.html", {"form": form, "user": MiloUser.objects.get(username=name)})


def milo_user_csv_view(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csv_file.csv"'
    writer = csv.writer(response)
    users = MiloUser.objects.all()
    writer.writerow(["Username", "Birthday", "Eligible", "Random Number", "BizzFuzz"])

    for user in users:
        writer.writerow([user.username, user.birthDate, get_age(user), user.number, is_fizz_buzz(user)])

    return response
