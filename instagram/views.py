from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Tag, Post

@login_required
def index(request):
    return render(request, "instagram/index.html", {

    })


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
            return redirect(post)
    else:
        form = PostForm()
    return render(request, 'instagram/post_form.html', {
        'form': form,
    })

def post_edit(request):
    pass

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "instagram/post_detail.html", {
        'post': post,
    })

def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count() # 실제 DB에 COUNT 쿼리를 날림.
    # len(post_list) <- 이렇게 하면, post_list 전체를 다 가져와서 메모리에 얹은 후, 메모리 상 리스트의 갯수를 변환.
    return render(request, "instagram/user_page.html", {
        "page_user": page_user,
        "post_list": post_list,
        "post_list_count": post_list_count,
    })