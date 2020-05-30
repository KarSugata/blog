from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200)
    class meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']