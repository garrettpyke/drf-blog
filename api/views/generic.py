from django.http import HttpResponse

def index(request):
	return HttpResponse("<h2>Hello, world. You're at the blog index.</h2>")