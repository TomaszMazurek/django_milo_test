from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import MiloUser


class AddUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )
    number = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = MiloUser
        fields = ('username', 'birthDate', 'number')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MiloUser
        fields = (
            'username', 'birthDate', 'number', 'is_active', 'is_admin'
        )

    def clean_password(self):
        # Password can't be changed in the admin
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UpdateUserForm
    add_form = AddUserForm

    list_display = ('username', 'birthDate', 'number', 'is_admin')
    list_filter = ('is_admin', )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('birthDate', 'number')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username', 'birthDate', 'number', 'password1',
                    'password2'
                )
            }
        ),
    )
    search_fields = ('username', 'birthDate', 'number')
    ordering = ('username', 'birthDate', 'number')
    filter_horizontal = ()


admin.site.register(MiloUser, UserAdmin)
