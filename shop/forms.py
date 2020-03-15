from django import forms
from django.core import validators
from django.contrib.auth.models import User
from shop.models import UserProfileInfo


class UserForm(forms.ModelForm):
    firstname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',}))
    verify_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    botcatcher = forms.CharField(required=False,
                                 widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)]
                                 )

    def clean(self):
        all_clean_data = super().clean()
        password = all_clean_data['password']
        vpassword = all_clean_data['verify_password']

        if password != vpassword:
            raise forms.ValidationError("Password didn't match.")

    def clean_botcatcher(self):
        botcatcher = self.cleaned_data['botcatcher']
        if len(botcatcher) > 0:
            raise forms.ValidationError("Gotcha Bot!")
        return botcatcher

    class Meta():
        model = User
        fields = ('firstname', 'lastname', 'username', 'email', 'password', 'verify_password')
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.TextInput(attrs={'class': 'form-control'})}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].label = 'Display Name'
            self.fields['email'].label = "Email Address"


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')
        widget = {'portfolio_site': forms.TextInput(attrs={'class': 'form-control'})}
