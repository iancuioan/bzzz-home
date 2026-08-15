from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserFeedback

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Există deja un cont cu acest email.")
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Parolă', widget=forms.PasswordInput)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = UserFeedback
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Scrie aici părerea ta...',
                'class': 'form-control'
            })
        }