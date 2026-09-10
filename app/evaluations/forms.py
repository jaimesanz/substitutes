from django import forms

from .models import Evaluation


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ["status", "rating", "notes"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
            "rating": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating is not None and not (1 <= rating <= 5):
            raise forms.ValidationError("El puntaje debe estar entre 1 y 5.")
        return rating
