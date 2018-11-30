from django.contrib import admin

from .models import Movie, User, StyleType, LeadRole, Country, Advertise

# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'release_time', 'country', 'length', 'mark', 'director']

@admin.register(StyleType)
class StyletypeAdmin(admin.ModelAdmin):
    list_display = ['style_type']

@admin.register(LeadRole)
class LeadRoleAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['country']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'subscribe']

@admin.register(Advertise)
class AdvertiseAdmin(admin.ModelAdmin):
    list_display = ['name', 'link', 'edit_time']

# class UserInline(admin.StackedInline):
#     model = User
#     can_delete = False
#     verbose_name_plural = 'user'
#     fields = ('username', 'email', 'is_subscribe')
#
# class UserAdmin(admin.ModelAdmin):
#     # list_display = ['username', 'email', 'is_subscribe']
#     inlines = [User]
#
# # admin.unregister(User)
# admin.register(User, UserAdmin)