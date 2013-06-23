from django.forms import ModelForm
from core.models import Aposta
from core.models import Participante
from django.contrib.auth.models import User

class ApostaForm(ModelForm):
	class Meta:
		model = Aposta

class ParticipanteForm(ModelForm):
	class Meta:
		model = Participante

class UserForm(ModelForm):
	class Meta:
		model = User
