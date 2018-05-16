from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect 
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render


from .models import Post
from .forms import PostForm


def post_create(request):
	form = PostForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit = False)
		print(form.cleaned_data.get('title'))#comparar esta linea particular.
		instance.save()
		messages.success(request, "Post succesfully created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)


def post_detail(request, id = None):	
	instance = get_object_or_404(Post, id = id)
	context = {
		"title": instance.title,
		"instance": instance,
	}
	return render(request,"post_detail.html", context)


def post_list(request):

	queryset_list = Post.objects.all()
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
    
   


def post_update(request, id = None):
	instance = get_object_or_404(Post, id = id)
	form = PostForm(request.POST or None, instance = instance)
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
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "Succesfully Deleted")
	return redirect("posts:list")

