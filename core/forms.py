from django.forms import ModelForm
from core.models import Aposta
from core.models import Participante
from core.models import Jogo
from django.contrib.auth.models import User

from django import forms

class ApostaForm(ModelForm):
	class Meta:
		model = Aposta

class JogoForm(ModelForm):
	class Meta:
		model = Jogo		
		
class ParticipanteForm(ModelForm):
	class Meta:
		model = Participante

class UserNewForm(forms.ModelForm):
	
	senha_atual = forms.CharField(max_length=30, widget=forms.PasswordInput)
	
	class Meta:
		model = User		
		fields = ('username','email','password')
		
	confirme_a_senha = forms.CharField(max_length=30, widget=forms.PasswordInput)
  
	def __init__(self, *args, **kwargs):
		self.base_fields['password'].help_text = 'Informe uma senha segura'
		self.base_fields['password'].widget = forms.PasswordInput()
		super(UserNewForm, self).__init__(*args, **kwargs)		
		
	def clean_confirme_a_senha(self):
		if self.cleaned_data['confirme_a_senha'] != self.data['password']:
			raise forms.ValidationError('Confirmacao de senha nao confere!')
		return self.cleaned_data['confirme_a_senha']
		
	def clean_username(self):
		if User.objects.filter(username=self.cleaned_data['username']).count():
			raise forms.ValidationError('Ja existe um usuario com este username')
		return self.cleaned_data['username']
		
	def save(self, commit=True):
		usuario = super(UserNewForm, self).save(commit=False)
		usuario.set_password(self.cleaned_data['password'])
		if commit:
			usuario.save()
		return usuario
		
class UserEditForm(forms.ModelForm):
	class Meta:
		model = User		
		fields = ('username','email','first_name','last_name')
		
# Mesma que o UserNewForm, mas sem o clean_username()		
class UserPasswordForm(forms.ModelForm):
	class Meta:
		model = User		
		fields = ('username','email','password')
		
	confirme_a_senha = forms.CharField(max_length=30, widget=forms.PasswordInput)
  
	def __init__(self, *args, **kwargs):
		self.base_fields['password'].help_text = 'Informe uma senha segura'
		self.base_fields['password'].widget = forms.PasswordInput()
		super(UserPasswordForm, self).__init__(*args, **kwargs)		
		
	def clean_confirme_a_senha(self):
		if self.cleaned_data['confirme_a_senha'] != self.data['password']:
			raise forms.ValidationError('Confirmacao de senha nao confere!')
		return self.cleaned_data['confirme_a_senha']
		
	def save(self, commit=True):
		usuario = super(UserPasswordForm, self).save(commit=False)
		usuario.set_password(self.cleaned_data['password'])
		if commit:
			usuario.save()
		return usuario				
		
		
		
		
		
