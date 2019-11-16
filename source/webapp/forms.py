from django import forms
from django.contrib.auth.models import User

from webapp.models import Review, Product


class ReviewForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=User.objects.all(),label='Автор', required=True, empty_label=None)
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label='Товар', required=True, empty_label=None)
    class Meta:
        model = Review
        exclude = []

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating<1 or rating>5:
            raise forms.ValidationError('Оценка должна быть от 1 - 5!')
        return rating

