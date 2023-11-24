from django.contrib import admin

from phone_directory.models import Main, Firstname, Street, Surname, Patronymic




@admin.register(Main)
class MainAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'surname', 'patronymic', 'street', 'house', 'corpus', 'apartments', 'phone')
    fields = ('firstname', 'surname', 'patronymic', 'street', 'house', 'corpus', 'apartments', 'phone')


@admin.register(Firstname)
class FirstnameAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name',)



@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name',)



@admin.register(Surname)
class SurnameAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name',)



@admin.register(Patronymic)
class PatronymicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name',)