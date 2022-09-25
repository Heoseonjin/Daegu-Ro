from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.

# CBV 방식 사용
# 목록
class BoardList(ListView):
    model = Post
    template_name = 'noticeboard/board_list.html'
    ordering = '-pk'


# 상세페이지
class BoardDetail(DetailView):
    model = Post
    template_name = 'noticeboard/board_detail.html'
