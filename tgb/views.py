from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Message, Client, Order
from .forms import CreateUserForm, CommandForm
from .permissions import admin_only
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pandas as pd


@login_required(login_url='login')
def message_list(request):
    template = 'tgbot/message_list.html'
    sort_name = request.GET.get('sort')
    if sort_name != None:
        object_list = Message.objects.filter(
            client__name=sort_name).order_by('created_at')
    else:
        object_list = Message.objects.all().order_by('created_at')    
    clients = Client.objects.all()
    context = {'object_list': object_list,
               'clients': clients}
    return render(request, template, context)


@admin_only
def add_command(request, template):
    data = request.POST.copy()
    form = CommandForm(data)
    if form.is_valid():
        form.save() 
        form = CommandForm()
    else:
        messages.info(request, 
                      'Внимательно впишите имя команды. Оно должно '
                      'состоять из одного слова без пробелов, цифр '
                      'и символов(только !английские! буквы и знак "_")')    
    return form    


@admin_only
def update_command(request, pk):
    success_update = False
    get_order = Order.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommandForm(request.POST, instance=get_order)
        if form.is_valid():
            form.save()
            success_update = True
    template = 'tgbot/dashboard.html'
    context = {
        'get_article': get_order,
        'update':True,
        'form':CommandForm(instance=get_order),
        'success_update':success_update}
    return render(request, template, context)
    

@admin_only
def delete_command(request, pk):
    get_order = Order.objects.get(pk=pk)
    get_order.delete()
    return redirect(reverse('dash'))        


@login_required(login_url='login')
def dashboard(request):
    if not request.user.is_staff:
        messages.info(request, 'Только Админы могут просматривать Дашборд')
        return redirect('clients')
    template = 'tgbot/dashboard.html'
    form = CommandForm()
    # Данные о количестве пользователей и запросов
    dicty = {'Активные диалоги' : [Client.objects.all().count()],
            'Количество запросов' : [Message.objects.all().count()],}
    df1 = pd.DataFrame(dicty)
    
    # Топ запросов
    req = Message.objects.values_list('text').order_by('text')
    dict_ray = dict()
    score=0
    def count_func(dict_ray, score, ind, quest, req):
        if len(dict_ray) == 3:
            score+=1
            for elem in dict_ray:
                if dict_ray[elem]<[score]:
                    del dict_ray[elem]
                    dict_ray[quest] = [score]
                    break
                              
        if len(dict_ray)>=0 and len(dict_ray) < 3:
            score +=1             
            dict_ray[req[ind]] = [score]
            
        return dict_ray
    
    for ind, quest in enumerate(req):
        try:
            if req[ind+1]==quest:
                score +=1
                continue
            else:
                count_func(dict_ray, score, ind, quest, req)
                score=0
                continue
        except:
            count_func(dict_ray, score, ind, quest, req)
            score=0
            continue

    df2 = pd.DataFrame(dict_ray)
    
    list_commands = Order.objects.all().order_by('id')
    
    if request.method == 'POST':
        add_command(request, template)
        return redirect('dash')
    
    context = {'df1': df1.to_html,
                'df2': df2.to_html,
                'form': form,
                'list_commands': list_commands,}
    return render(request, template, context)


def register(request):
    if request.user.is_authenticated:
        return redirect('clients')
    else:
        template = 'tgbot/register.html'
        form = CreateUserForm()
        if request.method == 'POST':
            data = request.POST.copy()
            form = CreateUserForm(data)
            if form.is_valid():
                form.save() 
                form = CreateUserForm()
                return redirect('login')     
        context={'form': form}
        return render(request, template, context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('clients')
    else:
        template = 'tgbot/login.html'
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,
                                username=username,
                                password=password)
            if user is not None:
                login(request, user)
                return redirect('clients')
            else:
                messages.info(request, 'Неверно введены имя или пароль')
                    
        context={}
        return render(request, template, context)


def logout_user(request):
    logout(request)
    messages.info(request, 'Вы вышли из профиля')
    return redirect('login')



