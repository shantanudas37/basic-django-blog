from urllib.parse import quote_plus
from django.shortcuts import render,get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Post
from .forms import PostForm
from django.db.models import Q


# Create your views here.
def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    if not request.user.is_authenticated():
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance= form.save(commit=False)
        print(form.cleaned_data.get("title"))
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    #if request.method == "POST":
    #    print request.POST.get("content")
    context = {
        "form": form,
    }

    return render(request, "post_form.html", context)


def post_detail(request, slug = None):                       #retrieve
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    share_content = quote_plus(instance.content)
    context = {
        "title": instance.title,
        "slug": slug,
        "instance": instance,
        "share_content": share_content
    }
    return render(request, "detail.html", context)

def post_list(request):
    # return HttpResponse("<h1>LIST</h1>")
    # queryset_list = Post.objects.filter(draft=False).filter(publish__lte= timezone.now()) #all()#.order_by("-timestamp")
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("query_s")
    if query:
        queryset_list = queryset_list.filter(Q(title__icontains=query)|
                                             Q(content__icontains=query)|
                                             Q(user__first_name__icontains=query)|
                                             Q(user__last_name__icontains=query)).distinct()
    paginator = Paginator(queryset_list, 3) # Show 25 contacts per page
    page_no='page_no'
    page = request.GET.get('page_no')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)


    context = {
            "queryset": queryset,
            "title": "List",
            "page_no": page_no,
            "today": today
        }

    # if request.user.is_authenticated():
    #     context = {
    #         "queryset": queryset,
    #          "title": "User List"
    #     }
    # else:
    #     context = {
    #         "queryset": queryset,
    #         "title": "List"
    #     }
    return render(request, "base.html", context)


def post_update(request, slug= None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance= form.save(commit=False)
        instance.save()
        messages.success(request, "<a href=''>Item</a> Saved", extra_tags="html_safe")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "content": instance.content,
        "form": form,
        "instance": instance,
        "slug": slug
    }
    return render(request, "post_form.html", context)


def post_delete(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    instance.delete()
   # messages.success(request, "Successfully Deleted")
    return redirect("posts:list")