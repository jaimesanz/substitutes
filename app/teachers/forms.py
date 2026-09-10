from django import forms

from .models import Certificate, TeacherProfile


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        exclude = ["user", "created_at", "updated_at"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
            "availability_notes": forms.TextInput(),
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "available_from": forms.DateInput(attrs={"type": "date"}),
            "subjects": forms.CheckboxSelectMultiple(),
            "preferred_comunas": forms.SelectMultiple(attrs={"size": 8}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to non-checkbox/select-multiple fields.
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                continue
            css = "form-select" if isinstance(widget, (forms.Select, forms.SelectMultiple)) else "form-control"
            widget.attrs.setdefault("class", css)


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ["doc_type", "name", "file"]
        widgets = {
            "doc_type": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
