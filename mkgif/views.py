from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Animation, Image

@login_required
def index(request):
    if request.method == 'POST':
        anim = Animation.objects.create(name=request.POST['name'], user=request.user)
        for img in request.FILES.getlist('imgs'):
            Image.objects.create(animation=anim, image=img, user=request.user)

    anims = Animation.objects.filter(user=request.user)
    context = {
            'anims': anims
            }
    return render(request, 'mkgif/index.html', context)

@login_required
def details(request, pk):
    anim = get_object_or_404(Animation, pk=pk, user=request.user)
    images = Image.objects.filter(animation=pk)
    context = {
            'anim': anim,
            'images': images
            }
    return render(request, 'mkgif/details.html', context)
