from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import UserCreationForm, UserChangeForm
from .models import *

class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email','is_staff', 'is_active', 'is_superuser','is_doctor','is_patient')
    list_filter = ('email', 'is_staff', 'is_active', 'is_superuser',
                   'is_doctor', 'is_patient')
    fieldsets = (
        (None, {'fields': ('email', 'password','age','address','profile_image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 
         'is_doctor','is_patient')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'age', 'address', 'password1', 'password2', 'age', 'address', 'profile_image', 'is_staff', 'is_active', 'is_superuser', 'is_doctor', 'is_patient')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, UserAdmin)
admin.site.register(CovidTestImage)
admin.site.register(CovidResultData)
# admin.site.register(OtherReports)
admin.site.unregister(Group)