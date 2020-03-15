from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.generic import TemplateView,ListView, DetailView,CreateView, UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class AboutView(TemplateView): # about메뉴를 보여주는 view
    template_name = 'blog/about.html'

class PostListView(ListView): # Post list를 보여주는 view
    model=Post

    def get_queryset(self): # 지금까지 publish된 post들을 내림차순으로 가져온다.
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date') # lte=less than equal. 오름차순으로 나타내고 싶으면 published_date앞의 -를 지우면 된다.

class PostDetailView(DetailView): # Post detail을 보여주는 view
    model=Post

class CreatePostView(LoginRequiredMixin, CreateView): # Post를 만드는 view. login이 필요한 view를 처리할 때 LoginRequiredMixin을 사용한다.
    login_url='/login/' # login이 기본적으로 요구된다.
    redirect_field_name='blog/post_detail.html' # post_detail.html로 연결된다.
    form_class=PostForm # 사용할 form. (form에 class로 정의되어 있다.)
    model=Post # 사용할 model은 Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list') # 성공하면 어디로 갈 것인지 경로를 지정한다. generic view의 경우, 타이밍 문제 때문에 reverse_lazy를 사용한다.

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_draft_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST) # CommentForm에 입력한 값을 form이라는 변수에 저장한다.
        if form.is_valid(): # form이 유효하다면
            comment = form.save(commit=False) # comment에 form의 내용을 저장하고
            comment.post = post # comment모델의 comment에 post의 값을 저장한다.
            comment.save() # comment를 저장하고
            return redirect('post_detail', pk=post.pk) # 저장한 comment를 가지고 있는 post의 detail로 이동한다.
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})

# login이 요구되는 함수들

@login_required # @login_required는 아래의 함수를 실행하려면 로그인이 요구된다는 의미이다.
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk) # get_object_or_404는 첫번째 인자로 model을 받고 두번째 인자로는 키워드를 받는데, 존재하지 않을 경우는 Http404예외가 발생한다.
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment=get_object_or_404(Comment, pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
