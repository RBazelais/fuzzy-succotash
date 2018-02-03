from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime
from django.utils.timezone import now

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserValidator(models.Manager):
	def AddUser(self, name, email, password, confirm):
		errors = []
		if len(name) < 1:
			errors.append("You must have a name")
		else:	
			for char in name:
				if str(char).isdigit():
				 	errors.append("No numbers in the name fields") 
		if len(password) < 8:
			errors.append("Password must be at least 8 characters long")
		else:
			hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())			
		if not EMAIL_REGEX.match(email):
			errors.append("Please enter a valid email address")
		else:	
			emails = User.objects.filter(email=email)
			if len(emails) != 0:	
				errors.append("This email already exists")
		if password != confirm:
			errors.append("Passwords must match")
		if len(errors) > 0:
			return errors	
		else:
			new_user = User.objects.create(name=name, email=email, password=hashed)
			return new_user	
	def login(self, email, password):
		users = User.objects.filter(email=email)
		if len(users) == 0:
			return "Invalid email"
		elif bcrypt.checkpw(password.encode(), users[0].password.encode()) == False:
			return "Incorrect password"
		else:	
			return users[0]	

class User(models.Model):
	name = models.CharField(max_length=255)
	# username = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	# birthday = models.DateTimeField(default=datetime.now(), blank=True)
	objects = UserValidator()


class ItemValidator(models.Manager):
	def add_product(self, name, created_by):
		errors = []
		user = User.objects.get(id=name)
		created_by = User.objects.get(id=created_by)
		# created_at = datetime.now().strptime("%Y-%m-%D")

		if len(name) < 1:
			errors.append("Must have a name")
		if len(Item.objects.filter(name=name)) > 0:
			errors.append("Item has already been added!")
		if len(errors) > 0:
			return errors
		else:
			user = User.objects.get(id=created_by)
			new_product = Item.objects.create(name=name, created_by=user)
			return new_product

	def add_item(self, id, add_this):
		user = User.objects.get(id=id)
		item = Item.objects.get(id=add_this)
		# Item.added_to_list.add(user)
		# Item.save()
		return user		
	
	def remove_item(self, id, remove_this):
		user = User.objects.get(id=id)
		item = Item.objects.get(id=remove_this)
		# Item.added_to_list.add(user)
		return user		

class Item(models.Model):
	name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	added_to_list = models.ManyToManyField(User, related_name="added_item")
	# created_by(user) to product
	created_by = models.ForeignKey(User)
	objects = ItemValidator()