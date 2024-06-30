from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserAccount

class UserRegistrationForm(UserCreationForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    email=forms.CharField(widget=forms.EmailInput(attrs={'id':'required'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'id': 'required'}))
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email','image']
    
    def save(self,commit=True):
        our_user=super().save(commit=True)
        if commit==True:
            image=self.cleaned_data.get('image')
            UserAccount.objects.create(
                user=our_user,
                image=image
            )
        return our_user