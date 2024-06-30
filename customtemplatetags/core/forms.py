from django import forms


class SampleForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "test-first-name", "placeholder": "First Name"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "test-last-name"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "test-email", "placeholder": "Enter your email"}),
            required=False
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "test-password", "placeholder": "Password"})
    )
    age = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "test-age", "placeholder": "Age"}),
        required=False
    )
    agree = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "test-agree"}),
        required=False
    )
