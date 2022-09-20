from .models import Project,Tag
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def paginatProjects(request,projects,results):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)
    # اندازه ریزالت بسته بندی کن
    try:
        projects = paginator.page(page)
    # دسته ای که خواسته شده رو نشون بده

    except PageNotAnInteger:
        # میگه اگ پیجی که گفت عدد نبود این کار رو بکن
        page = 1
        projects = paginator.page(page)

    except EmptyPage:
        # اگر چنین پیجی خارج از رنج بود اخرین دسته رو نشون بده
        page = paginator.num_pages
        projects = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1 : 
        leftIndex = 1
    
    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages

    custom_range = range(leftIndex,rightIndex+1)
    return custom_range,projects


def searchProjects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags  = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query)|
        Q(description__icontains=search_query)|
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )
    return projects, search_query
