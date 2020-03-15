from django import forms
from django.core import validators

class djangopay(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    dob = forms.DateField(label = "DOB")
    cardnumber =forms.IntegerField(label = "Card Number")

    botcatcher = forms.CharField(required=False,
                                 widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)]
                                 )
    fields = ('email','dob','cardnumber')
    widgets = {'email': forms.TextInput(attrs={'class': 'form-control'}),
               'dob': forms.TextInput(attrs={'class': 'form-control'})}

    def clean_botcatcher(self):
        botcatcher = self.cleaned_data['botcatcher']
        if len(botcatcher) > 0:
            raise forms.ValidationError("Gotcha Bot!")
        return botcatcher