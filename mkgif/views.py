from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Animation, Image
from pathlib import Path

@login_required
def index(request):
    if request.method == 'POST':
        anim = Animation.objects.create(name=request.POST['name'], user=request.user)
        for img in request.FILES.getlist('imgs'):
            Image.objects.create(animation=anim, image=img, user=request.user)
        anim.enqueue({})
        return redirect(f'/details/{anim.pk}')

    anims = Animation.objects.filter(user=request.user)
    # for anim in anims:
    #     anim.loading = Path.exists(f'media/{anim.pk}/out.git')

    context = {
            'anims': anims
            }
    return render(request, 'mkgif/index.html', context)

@login_required
def details(request, pk):
    anim = get_object_or_404(Animation, pk=pk, user=request.user)
    
    if request.method == 'DELETE':
        if anim.user == request.user:
            anim.remove()
        else:
            raise PermissionDenied()
        return HttpResponse()

    images = Image.objects.filter(animation=pk)
    path = f'media/{anim.pk}/out.gif'
    loading = not Path(path).exists()
    context = {
            'anim': anim,
            'images': images,
            'loading': loading,
            'url': f'/{path}',
            }
    return render(request, 'mkgif/details.html', context)

@login_required
def gif(request, pk):
    anim = get_object_or_404(Animation, pk=pk, user=request.user)
    path = f'media/{anim.pk}/out.gif'
    if Path(path).exists():
        context = { 'url': f'/{path}' }
        return render(request, 'mkgif/snippets/gif.html', context)
    else:
        return HttpResponseNotFound()