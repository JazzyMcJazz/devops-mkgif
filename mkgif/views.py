from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Animation, File
from pathlib import Path

@login_required
def index(request):
    if request.method == 'POST':
        anim = Animation.objects.create(name=request.POST['gif_name'], user=request.user)
        paths = []
        for file in request.FILES.getlist('files'):
            newfile = File.objects.create(animation=anim, file=file, user=request.user)
            paths.append(newfile.file.path)

        # Clean up on isle 7 (rqworker removes files after processing anyway)
        File.objects.filter(animation=anim).delete()

        video_path = paths[0]
        type = request.POST["type"]
        size = request.POST['size']
        fps = request.POST['fps']
        size = request.POST['size']
        
        anim.enqueue({ 
            'type': type, 
            'video_path': video_path,
            'fps': fps, 
            'size': size,
        })

        return redirect(f'/details/{anim.pk}')

    anims = Animation.objects.filter(user=request.user)
    context = { 'anims': anims }

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
    
    path = f'media/{anim.pk}/out.gif'
    loading = not Path(path).exists()
    context = {
            'anim': anim,
            'loading': loading,
            'url': f'/{path}',
            }
    
    return render(request, 'mkgif/details.html', context)

@login_required
def gif(request, pk):
    anim = get_object_or_404(Animation, pk=pk, user=request.user)
    path = f'media/{anim.pk}/out.gif'

    # Access Controll
    if anim.user != request.user:
        return PermissionDenied()
    
    if Path(path).exists():
        context = { 'url': f'/{path}' }
        return render(request, 'mkgif/snippets/gif.html', context)
    else:
        return HttpResponseNotFound()
    
@login_required
def image_form(request):
    return render(request, 'mkgif/snippets/image_form.html')

@login_required
def video_form(request):
    return render(request, 'mkgif/snippets/video_form.html')