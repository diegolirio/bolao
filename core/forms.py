from django.forms import ModelForm
from core.models import Aposta
from core.models import Participante

class ApostaForm(ModelForm):
	class Meta:
		model = Aposta

class ParticipanteForm(ModelForm):
	class Meta:
		model = Participante
