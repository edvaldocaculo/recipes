from django import forms


class LoginForms(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your username',
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password',
        }),

    )
