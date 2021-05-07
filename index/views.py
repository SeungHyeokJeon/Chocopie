from django.shortcuts import render

# Create your views here.
def index(request):
    context = {'check':False}
    if request.session.get('access_token'):
        context['check'] = True
    return render(request, 'index/index.html', context)