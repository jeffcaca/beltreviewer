from __future__ import unicode_literals
from django.shortcuts import redirect
import re, bcrypt
from django.db import models
from ..loginregistration.models import User




class AllManager(models.Manager):
	def formvalidate(self, data):
		print "form validation"
		errors = []
		if len(data['review']) < 1:
			errors.append('Please fill out a book review')

		bookcheck = Book.objects.filter(name = data['booktitle'])
		if bookcheck:
			errors.append('Book already exists in database')
		if len(data['booktitle']) < 1:
			errors.append('Please fill out a book title')

		authorcheck = Author.objects.filter(name = data['author'])
		if authorcheck:
			errors.append('Author already exists in database')

		if len(data['author']) < 1:
			errors.append('Please fill out a author or select an author')
		
		
		response = {}
		if errors:
			response['passed'] = False
			response['errors'] = errors
		else:
			response['passed'] = True

		return response

	def reviewvalidate(self, data):

		if len(data['description']) < 1:
			errors.append('Please fill out a description')
		reviewresponse = {}
		if errors:
			reviewresponse['passed'] = False
			reviewresponse['errors'] = errors
		else:
			reviewresponse['passed'] = True
		return reviewresponse

	def authorcreate(self, data):
		newauthor = Author.objects.create(name = data['author'])
	def bookcreate(self, data):
		author = Author.objects.get(name = data['author'])
		newbook = Book.objects.create(name = data['booktitle'], author = author)
	
	def reviewcreate(self, data, user_id):
		user = User.objects.get(id = user_id)
		book = Book.objects.get(name = data['booktitle'])
		newreview = Review.objects.create(description = data['review'], rating = data['rating'], book=book, user=user)

	def justreviewcreate(self, data, user_id, id):
		user = User.objects.get(id = user_id)
		book = Book.objects.get(name = id )
		newreview = Review.objects.create(description = data['description'], rating = data['rating'], book=book, user=user)
		

class Author(models.Model):
	name = models.CharField(max_length = 100)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = AllManager()

class Book(models.Model):
	name = models.CharField(max_length = 100)
	author = models.ForeignKey(Author, related_name="bookauthor")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = AllManager()
	#reviewbooks #for review in reviewbooks    this would display all the reviews for the book if nested in for book in books
class Review(models.Model):
	book = models.ForeignKey(Book, related_name = "reviewbooks")
	user = models.ForeignKey(User, related_name = "reviewusers")
	description = models.TextField(max_length = 500)
	rating = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = AllManager()

