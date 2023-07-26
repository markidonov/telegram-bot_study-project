from django.contrib import admin
from .models import Client, Message, Order


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_id', 'name']
    list_filter = ['name']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'text', 'created_at']
    list_filter = ['client']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'command', 'answer']
    list_filter = ['command']
