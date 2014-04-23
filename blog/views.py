from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse

from blog.models import Post

def index(request):
	"""
		Index page for the blog
	"""
	posts = Post.objects.all().order_by("-created")
	paginator = Paginator(posts, 2)
	
	try:
		page = int(request.GET.get("page", '1'))
	except ValueError:
		page = 1

	try:
		posts = paginator.page(page)
	except (Invalid, EmptyPage):
		posts = paginator.page(paginator.num_pages)

	return render_to_response("blog/list.html", dict(posts=posts, user=request.user))
