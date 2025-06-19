from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=10)

    class Meta:
        model = Account
        fields = ("email", "username", "first_name", "last_name", "phone_number", "password1", "password2")


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("email", "password")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password. Please try again.")
            if not user.is_active:
                raise forms.ValidationError("This account is inactive. Please contact support.")

        return cleaned_data


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("email", "first_name", "last_name")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email field cannot be empty.")
        if Account.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(f'Email "{email}" is already in use.')
        return email.lower()  # Kuhakikisha email inawekwa kwa lowercase

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class RainfallUploadForm(forms.Form):
    file = forms.FileField(label='Upload Excel file')