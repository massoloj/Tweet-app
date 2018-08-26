from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from tweets.views import Index, Profile, PostTweet, HashTagCloud, Search, MostFollowedUsers, UserLogin, UserLogout, UserRedirect

admin.autodiscover()

urlpatterns = [
	url(r'^$', Index.as_view()),
	url(r'^user/(\w+)/$', Profile.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^user/(\w+)/post/$', PostTweet.as_view()),
    url(r'^hashTag/(\w+)/$', HashTagCloud.as_view()),
    url(r'^search/$', Search.as_view()),
    url(r'^profile/$', UserRedirect.as_view()),
    url(r'^mostFollowed/$', MostFollowedUsers.as_view()),
    url(r'^login/$', UserLogin.as_view()),
	url(r'^logout/$', UserLogout.as_view()),
    url(r'^invite/$', Invite.as_view()),
    url(r'^invite/accept/(\w+)/$', InviteAccept.as_view()),
]