from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Tag


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list()) #m2m은 post 저장하고 해야함. pk가 필요하기 때문. post와 관계를 별도 테이블에 매핑함.
            messages.success(request, "포스트를 생성하였습니다.")
            return redirect("/")
    else:
        form = PostForm()
    return render(request, 'instagram/post_form.html', {
        'form': form,
    })

def post_edit(request):
    pass
