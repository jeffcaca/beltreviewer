
from django.shortcuts import render, HttpResponse, redirect
from .models import Book, Author, Review
from django.contrib import messages
from ..loginregistration.models import User
from django.core.urlresolvers import reverse
from django.conf.urls.static import static


def index(request):
	if "id" not in request.session:
		return redirect(reverse('login:index'))
	this_user = User.objects.get(id = request.session['id'])
	context = {
	'users': User.objects.all(),
	'this_user': this_user,
	'books': Book.objects.all(),
	'authors': Author.objects.all(),
	'reviews': Review.objects.all(),
	'users': User.objects.all(),
	}

	return render(request, 'books/index.html', context)

def addbook(request):
	context = {
	'authors': Author.objects.all()
	}
	return render(request, 'books/addbook.html', context)

def addbookreview(request):

	if request.method == "POST":
		
		allvalidate = Book.objects.formvalidate(request.POST)

		if allvalidate['passed']:
			author = Author.objects.authorcreate(request.POST)
			book = Book.objects.bookcreate(request.POST)
			review = Review.objects.reviewcreate(request.POST, request.session['id'])
			return redirect(reverse('books:index'))
		else:
			for error in allvalidate['errors']:
				messages.error(request, error)
			return redirect(reverse('books:addbook'))

def viewbook(request, id):
	context = {
	'book':	Book.objects.get(id = id),
	'author': Author.objects.get(id = id),
	'reviews': Review.objects.filter(book = id)
	}

	return render(request, 'books/book.html', context)


def showuser(request, id):
	context = {
	'user': User.objects.get(id = id)

	}

	user = User.objects.get(id = id)
	print user.first_name
	return render(request, 'books/user.html', context)

def addreview(request):
	
	if request.POST == "POST":
		print "got here"
		reviewvalidate = Review.objects.reviewvalidate(request.POST)
		if reviewvalidate['passed']:
			review = review.objects.justreviewcreate(request.POST, request.session['id'])
			return redirect(reverse('books:index'))
		else:
			for error in reviewvalidate['errors']:
				messages.error(request, error)

			return redirect(reverse('books:viewbook'))
	