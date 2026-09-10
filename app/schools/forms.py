from django import forms

from .models import School, SchoolInvitation


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ["name", "rbd", "phone", "region", "comuna"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "rbd": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "region": forms.Select(attrs={"class": "form-select"}),
            "comuna": forms.Select(attrs={"class": "form-select"}),
        }


class InvitationForm(forms.ModelForm):
    class Meta:
        model = SchoolInvitation
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@colegio.cl"}),
        }
