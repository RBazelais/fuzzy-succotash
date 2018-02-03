from django.shortcuts import render, redirect
from .models import *
# from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    # user = User.objects.get(id=request.session['user_id'])
    # context = {
    #     'session_user': user,
    #     'all_users' : User.objects.exclude(user),
    #     'all_items' : Item.objects.all(),
    # }	
    return render(request, "index.html")

def process(request):
	if request.method == 'POST':
		new_user = User.objects.AddUser(
			request.POST['name'], 
			request.POST['email'],
			request.POST['password'],
			request.POST['confirm']
			)
		# print new_user
		if type(new_user) is list:
			for error in new_user:
				messages.add_message(request, messages.ERROR, error)
			return redirect('/')
		else:
			request.session['user_id'] = new_user.id
			return redirect("/users/{}".format(new_user.id)) 
	else:
		return redirect("/") 		

def login(request):	
	if request.method == 'POST':
		login = User.objects.login(
			request.POST['email'],
			request.POST['password']
			)
		if type(login) is unicode:
			messages.add_message(request, messages.ERROR, login)
			return redirect('/')
		else:
			request.session['user_id'] = login.id
			return redirect("/users/{}".format(login.id))
		return redirect("/")
	else:
		return redirect("/")	

# @login_required
def logout(request):
	request.session.clear()	
	return redirect('/')		

def create(request):
	if 'user_id' not in request.session:
		return redirect('/')
	else:	
		user = User.objects.get(id=request.session['user_id'])
		return render(request, "create_item.html", {'user' : user})
	return redirect('/')	

# @login_required
def open_app(request):
	if 'user_id' not in request.session:
		return redirect('/')
	else:	
		user = User.objects.get(id=request.session['user_id'])
		print "user.id: " + str(user.id)
		print "any string..."
		return render(request, "dashboard.html", {'user' : user})

# @login_required
def user_dash(request, id):
	if 'user_id' not in request.session:
		return redirect('/')
	else:	
		user = User.objects.get(id=id)
		return render(request, "dashboard.html", {'user' : user})

# @login_required
def add_item(request):
    user = Item.objects.get(id=id)
    Item.attendees.add(request.user)
    return redirect('/dashboard')

# @login_required
def remove_item(request):
    result = Item.objects.remove_item(
        request.session['user_id'],
        request.POST['remove_this'],
        )
    return redirect('/dashboard')

# @login_required
def add_product(request):
    # print request.POST['created_by']
    new_item = Item.objects.add_product(
        sender=request.session['user_id'], 
        receiver=request.POST['created_by']
    )
    return redirect('/dashboard')
