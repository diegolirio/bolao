from django.forms import ModelForm
from core.models import Aposta
from core.models import Participante
from django.contrib.auth.models import User

from django import forms

class ApostaForm(ModelForm):
	class Meta:
		model = Aposta

class ParticipanteForm(ModelForm):
	class Meta:
		model = Participante

class UserForm(forms.ModelForm):
	class Meta:
		model = User		
		fields = ('username','email','password')
		confirme_a_senha = forms.CharField(max_length=30, widget=forms.PasswordInput)

		def __init__(self, *args, **kwargs):
			self.base_fields['password'].help_text = 'Informe uma senha segura'
			self.base_fields['password'].widget = forms.PasswordInput()
			super(userForm, self).__init__(*args, **kwargs)		
