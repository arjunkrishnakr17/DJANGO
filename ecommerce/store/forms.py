from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class customform(UserCreationForm):
    class meta:
        model=User
        fields=("username","password1","password2","name","email")