from django.forms import ModelForm
from core.models import Aposta

class ApostaForm(ModelForm):
	class Meta:
		model = Aposta
