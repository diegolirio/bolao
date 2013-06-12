from django.shortcuts import render_to_response
from django.shortcuts import redirect

def home(request):
	#return render_to_response('_base.html', {'template': 'rancking.html'})
	return redirect('/rancking/1/')
