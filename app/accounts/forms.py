from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class EmailAuthenticationForm(AuthenticationForm):
    """Login form that labels the username field as 'correo'."""

    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"autofocus": True, "class": "form-control"}),
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class BaseRegistrationForm(UserCreationForm):
    """Shared registration form; subclasses set the role."""

    role = User.Roles.APPLICANT
    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name = forms.CharField(label="Apellido", max_length=150, required=False)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.role
        if commit:
            user.save()
        return user


class ApplicantRegistrationForm(BaseRegistrationForm):
    role = User.Roles.APPLICANT


class SchoolRegistrationForm(BaseRegistrationForm):
    role = User.Roles.SCHOOL
