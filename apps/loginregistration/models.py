from __future__ import unicode_literals
from django.shortcuts import redirect
import re, bcrypt
from django.db import models


class UserManager(models.Manager):
	def register(self, data):
		errors = []
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		namecheck = re.compile(r"[0-9]+")

		if re.search(namecheck, data['first']):
			errors.append('First name cannot contain numbers')
		elif len(data['first']) < 1:
			errors.append('Please fill out first name')
		elif len(data['alias']) < 1:
			errors.append('Please fill out alias')
		if len(data['emailadd']) < 1:
			errors.append('Please fill out email')
		elif not EMAIL_REGEX.match(data['emailadd']):
			errors.append('Not valid email')
		if len(data['pw']) < 8:
			errors.append('Password must be longer than 8 characters')
		if data['pw'] != data['pwcheck']:
			errors.append("PASSWORDS DON'T MATCH")

		response = {}
		if errors:
			response['created'] = False
			response['errors'] = errors
		else:
			pw_hash = bcrypt.hashpw(data['pw'].encode(), bcrypt.gensalt())
			newuser = User.objects.create(first_name = data['first'], alias = data['alias'], email_address = data['emailadd'], pwhash = pw_hash)
			response['created'] = True
			response['newuser'] = newuser
			response['id'] = newuser.id
			response['firstname'] = newuser.first_name

		return response

	def login(request, data):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		errors = []
		loginresponse = {} 
		
		email = User.objects.filter(email_address = data['loginemail'])
		password = data['loginpw'].encode()

		if not email:
			errors.append('Email does not exist in database')
		else:
			if bcrypt.hashpw(password, email[0].pwhash.encode()) == email[0].pwhash:
				loginresponse['created'] = True
				loginresponse['user'] = email[0]
				loginresponse['id'] = email[0].id
				loginresponse['first_name'] = email[0].first_name
			else:
				errors.append('Password does not work with provided email')
		
		if errors:
			loginresponse['created'] = False
			loginresponse['errors'] = errors
	
		return loginresponse


class User(models.Model):
	first_name = models.CharField(max_length = 100)
	alias = models.CharField(max_length = 100)
	email_address = models.CharField(max_length = 100)
	pwhash = models.CharField(max_length = 100)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()
# Create your models here.
