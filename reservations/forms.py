from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class CustomPasswordChangeForm(PasswordChangeForm):
    pass

class UpdateUserForm(forms.ModelForm):
    birthdate = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    street_address = forms.CharField(max_length=255, required=True)
    zip_code = forms.CharField(max_length=10, required=True)
    state = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'birthdate', 'street_address', 'zip_code', 'state')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['birthdate'].initial = self.instance.profile.birthdate
            self.fields['street_address'].initial = self.instance.profile.street_address
            self.fields['zip_code'].initial = self.instance.profile.zip_code
            self.fields['state'].initial = self.instance.profile.state

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.profile.birthdate = self.cleaned_data['birthdate']
        user.profile.street_address = self.cleaned_data['street_address']
        user.profile.zip_code = self.cleaned_data['zip_code']
        user.profile.state = self.cleaned_data['state']
        user.profile.save()
        return user
