from django.http import HttpResponse

def index(request):
	return HttpResponse("<h3>Hello, world. You're at the blog index.</h3>")