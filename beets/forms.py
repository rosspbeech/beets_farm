from django import forms
from django.core.validators import FileExtensionValidator

from beets.models import Beet, Persona, UserProfile, User


class PersonaForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter your chosen persona.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    about = forms.CharField(help_text="Tell us about this persona.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Persona
        fields = ('name', 'about')


class BeetForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the name of the Beet")
    about = forms.CharField(help_text="Tell us about this beautiful beet")
    plays = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    sound_file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['mp3'])])


    class Meta:
        model = Beet
        exclude = ('persona', )



class UserForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)