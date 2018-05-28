from urllib.parse import quote_plus
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect 
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils import timezone


from .models import Post
from .forms import PostForm


def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise http404

	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.user = request.user
		print(form.cleaned_data.get('title'))#comparar esta linea particular.
		instance.save()
		messages.success(request, "Post succesfully created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)


def post_detail(request, slug=None):	
	instance = get_object_or_404(Post, slug = slug)
	share_string = quote_plus(instance.content)
	context = {
		"title": instance.title,
		"instance": instance,
		"share_string":share_string,
	}
	return render(request,"post_detail.html", context)


def post_list(request):

	today = timezone.now().date()
	#queryset_list = Post.objects.active()
	if request.user.is_staff or request.user.is_superuser:
		queryset_list= Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(title__icontains=query)
	

	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:

		queryset = paginator.page(page)
		
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)
	
	context = {       
		"object_list": queryset,
		"title": "List",
		"page_request:var": page_request_var
	}
	return render(request,"post_list.html", context)
    
   


def post_update(request, slug = None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise http404
	instance = get_object_or_404(Post, slug = slug)
	form = PostForm(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request, "Succesfully edited")
		return HttpResponseRedirect(instance.get_absolute_url())
	
	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}
	return render(request, "post_form.html", context)


def post_delete(request, id= None):
	if request.user.is_staff or request or not request.user.is_superuser:
		raise http404
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "Succesfully Deleted")
	return redirect("posts:list")

