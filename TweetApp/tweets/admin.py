from django.contrib import admin
from tweets.models import Tweet, HashTag, UserFollower

class TweetAdmin(admin.ModelAdmin):
	list_display = ('user', 'text', 'created_date')
	list_filter = ('user', )
	ordering = ('-created_date', )
	search_fields = ('text', )

admin.site.register(Tweet, TweetAdmin)
admin.site.register(HashTag)
admin.site.register(UserFollower)