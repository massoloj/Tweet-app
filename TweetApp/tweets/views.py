from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.shortcuts import render
from user_profile.models import UserProfile
from tweets.models import Tweet, HashTag, UserFollower
from tweets.forms import TweetForm, SearchForm, LoginForm
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, redirect
from django.template import Context
from django.template import RequestContext
from django.http import HttpResponse
import json

class Index(View):
	def get(self, request):
		params = {}
		params["name"] = "Django"
		return render(request, 'base.html', params)

	def post(self, request):
		return HttpResponse('I am called from a post Request')

class Profile(LoginRequiredMixin, View):
	"""User Profile page reachable from /user/<username> URL"""
	def get(self, request, username):
		TWEET_PER_PAGE = 5
		params = dict()
		userProfile = UserProfile.objects.get(username=username)
		try:
			userFollower = UserFollower.objects.get(user=userProfile)
			#if userFollower.followers.filter(username=request.user.username).exists():
			params["following"] = True
		except:
		#else:
			params["following"] = False
			form = TweetForm(initial={'country': 'Global'})
			search_form = SearchForm()
			tweets = Tweet.objects.filter(user=userProfile).order_by('-created_date')
			paginator = Paginator(tweets, TWEET_PER_PAGE)
			page = request.GET.get('page')
			try:
				tweets = paginator.page(page)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				tweets = paginator.page(1)
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page
				#of results.
				tweets = paginator.page(paginator.num_pages)
			params["tweets"] = tweets
			params["profile"] = userProfile
			params["form"] = form
			params["search"] = search_form
		return render(request, 'profile.html', params)
		
	def post(self, request, username):
		follow = request.POST['follow']
		user = User.objects.get(username= request.user.username)
		userProfile = User.objects.get(username=username)
		userFollower = UserFollower.objects.get_or_create(user=userProfile)
		if follow =='true':
			#follow user
			userFollower.followers.add(user)
		else:
			#unfollow user
			userFollower.followers.remove(user)
		return HttpResponse(json.dumps(""),	content_type="application/json")


class PostTweet(View):
	"""Tweet Post form available on page /user/<username> URL"""
	def post(self, request, username):
		form = TweetForm(self.request.POST)
		if form.is_valid():
			user = User.objects.get(username=username)
			tweet = Tweet(text=form.cleaned_data['text'],
							user=user,
							country=form.cleaned_data['country'])
			tweet.save()
			words = form.cleaned_data['text'].split(" ")
			for word in words:
				if word[0] == "#":
					hashtag = HashTag.objects.get_or_create(name=word[1:]),
					hashtag.tweet.add(tweet)
		return HttpResponseRedirect('/user/'+username)

class HashTagCloud(View):
	"""Hash Tag page reachable from /hastag/<hashtag> URL"""
	def get(self, request, hashtag):
		params = dict()
		hashtag = HashTag.objects.get(name=hashtag)
		params["tweets"] = hashtag.tweet
		return render(request, 'hashtag.html', params)

class Search(View):
	"""Search all tweets with query /search/?query=<query> URL"""
	def get(self, request):
		form = SearchForm()
		params = dict()
		params["search"] = form
		return render(request, 'search.html', params)
	
	def post(self, request):
		form = SearchForm(request.POST)
		if form.is_valid():
			query = form.cleaned_data['query']
			tweets = Tweet.objects.filter(text__icontains=query)
			context = Context({"query": query, "tweets": tweets})
			return_str = render_to_string('partials/_tweet_search.html', context)
			return HttpResponse(json.dumps(return_str), content_type="application/json")
		else:
			HttpResponseRedirect("/search")

class MostFollowedUsers(View):
	def get(self, request):
		userFollowers = UserFollowers.objects.order_by('-count')
		params = dict()
		params['userFollowers'] = userFollowers
		return render(request, 'users.html', params)


class UserRedirect(View):
	def get(self, request):
		return HttpResponseRedirect('/user/'+ request.user.username)

class UserLogin(View):
	def get (self, request):
		form = LoginForm()
		params = dict()
		params["login"] = form
		return render(request, 'registration/login.html', params)
		
	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']
		form = LoginForm(data=request.POST)
		user = authenticate(username=username, password=password)
		if form.is_valid():
			if user is not None:
				if user.is_active:
					django_login(request, user)
					return HttpResponseRedirect('/user/'+ user.username)
				else:
					return HttpResponse("Your account is disabled.")
			else:
				print ("Invalid login details: {0}, {1}".format(username, password))
				return HttpResponse("Invalid login details supplied." + username + password)
		else:
			print ("Invalid form details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid form details supplied." + username + password)

class UserLogout(View):
	"""
	Log out view
	"""
	def get (self, request):
		django_logout(request)
		return redirect('/')
