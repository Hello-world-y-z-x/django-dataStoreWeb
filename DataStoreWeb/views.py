from django.shortcuts import render

# Create your views here.
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.conf import settings
from .models import File, AccessLog
from pathlib import Path


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('file_list')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def file_list(request):
    qs = File.objects.order_by('-uploaded_at')
    # 仅保留那些磁盘上确实存在的文件
    existing = [f for f in qs if Path(f.file.path).exists()]
    return render(request, 'list.html', {'files': existing})

@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        new_file = File(file=request.FILES['file'], uploaded_by=request.user)
        new_file.save()
        AccessLog.objects.create(user=request.user, file=new_file, action='upload')
        return redirect('file_list')
    return render(request, 'upload.html')

@login_required
def download_file(request, file_id):
    f = get_object_or_404(File, pk=file_id)
    path = f.file.path
    if os.path.exists(path):
        AccessLog.objects.create(user=request.user, file=f, action='download')
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(path)}"'
            return response
    raise Http404("File not found")
