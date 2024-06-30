from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['body']

    def clean(self):
        cleaned_data = super().clean()
        user = self.cleaned_data.get('user')
        book = self.cleaned_data.get('book')

        if user and book:
            if user not in book.borrower.all():
                raise forms.ValidationError("Only the borrower of the book can write a review.")
        
        return cleaned_data