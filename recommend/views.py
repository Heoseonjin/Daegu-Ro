from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Category, Recommend

# Create your views here.
# 목록
class RecommendList(ListView):
    model = Recommend
    template_name = 'recommend/recommend.html'

    def get_context_data(self, **kwargs):
        context = super(RecommendList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Recommend.objects.filter(category=None).count()
        return context


# 상세페이지
class RecommendDetail(DetailView):
    model = Recommend
    template_name = 'recommend/recommend_detail.html'



# def recommend(request):
#     recommend = Recommend.objects.all()

#     return render(request, 'recommend/recommend.html', {'recommend': recommend})

# 카테고리 페이지
def category_page(request, slug):
    # category = Category.objects.get(slug=slug)

    if slug == 'no_category':
        category = '미분류'
        recommend_list = Recommend.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        recommend_list = Recommend.objects.filter(category=category)


    return render(
        request, 
        'recommend/recommend.html', 
        {
            # 'recommending':Recommend.objects.filter(category=category),
            'recommend_list': recommend_list,
            'categories':Category.objects.all(), 
            'no_category_post_count': Recommend.objects.filter(category=None).count(), 
            'category':category,
        }
    )