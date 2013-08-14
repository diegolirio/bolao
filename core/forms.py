from django.forms import ModelForm
from core.models import Aposta
from core.models import Participante
from core.models import Jogo
from django.contrib.auth.models import User

from django import forms

class ApostaForm(ModelForm):
	class Meta:
		model = Aposta
		
	def clean_resultado_a(self):
		if int(self.cleaned_data['resultado_a']) < 0:
			raise forms.ValidationError('O Resultado deve ser igual ou maior que ZERO!')
		return self.cleaned_data['resultado_a']	

	def clean_resultado_b(self):
		if int(self.cleaned_data['resultado_b']) < 0:
			raise forms.ValidationError('O Resultado deve ser igual ou maior que ZERO!')
		return self.cleaned_data['resultado_b']			

class JogoForm(ModelForm):
	class Meta:
		model = Jogo		
		
class ParticipanteForm(ModelForm):
	class Meta:
		model = Participante
		fields = ('user','apelido','ddd','telefone', 'foto')

class ParticipanteFotoForm(ModelForm):
	class Meta:
		model = Participante
		fields = ('user', 'foto')		
		
class UserNewForm(forms.ModelForm):	
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
		
	def clean_email(self):
		if self.cleaned_data['email'] == '':
			raise forms.ValidationError('Digite um email valido!')
		return self.cleaned_data['email']		
		
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

"""		
class UserEmailForm(forms.ModelForm):
	class Meta:
		model = User		
		fields = ('email')				
"""
		
# Mesma que o UserNewForm, mas sem o clean_username()		
class UserPasswordForm(forms.ModelForm):
	class Meta:
		model = User		
		fields = ('username', 'password')		
	
	confirme_a_senha = forms.CharField(max_length=30, widget=forms.PasswordInput)
	senha_atual = forms.CharField(max_length=30, widget=forms.PasswordInput)
	
	def __init__(self, *args, **kwargs):
		self.base_fields['password'].help_text = 'Informe uma senha segura'
		self.base_fields['password'].widget = forms.PasswordInput()
		super(UserPasswordForm, self).__init__(*args, **kwargs)		
		
	def clean_confirme_a_senha(self):
		if self.cleaned_data['confirme_a_senha'] != self.data['password']:
			raise forms.ValidationError('Confirmacao de senha nao confere!')
		return self.cleaned_data['confirme_a_senha']		
		
	def clean_senha_atual(self):
		user = User.objects.filter(username=self.cleaned_data['username'])[0:1].get()
		print(self.cleaned_data['senha_atual'])
		valid = user.check_password(self.cleaned_data['senha_atual'])
		if not valid:
			raise forms.ValidationError('Senha atual incorreta!')
		return self.cleaned_data['senha_atual']		
		
	def save(self, commit=True):
		usuario = super(UserPasswordForm, self).save(commit=False)
		usuario.set_password(self.cleaned_data['password'])
		if commit:
			usuario.save()
		return usuario					


		
		
		
		
