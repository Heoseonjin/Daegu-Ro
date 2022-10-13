from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Category, Post, Comment
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.

# CBV 방식 사용
# 목록
class BoardList(ListView):
    model = Post
    template_name = 'noticeboard/board_list.html'
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(BoardList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


# 상세페이지
class BoardDetail(DetailView):
    model = Post
    template_name = 'noticeboard/board_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BoardDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm        
        return context

# 카테고리 페이지
def category_page(request, slug):
    # category = Category.objects.get(slug=slug)

    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request, 
        'noticeboard/board_list.html', 
        {
            # 'board_list':Post.objects.filter(category=category), 
            'post_list': post_list,
            'categories': Category.objects.all(), 
            'no_category_post_count' : Post.objects.filter(category=None).count(), 
            'category':category,
        }
    )

# 입력폼
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category']

    # 관리자만 post 허용
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    # 자동으로 author 필드 채우기
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/board/')

# 게시글 수정
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'category']

    template_name = 'noticeboard/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


# 댓글 수정
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

# 댓글 삭제
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

# 검색 기능
class PostSearch(BoardList):
    # 검색 결과를 한 페이지에 다 보여주기 위해 none 지정
    paginate_by = None

    # objects.all과 동일
    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(Q(title__contains=q)).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'

        return context