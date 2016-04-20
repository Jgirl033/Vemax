from django.contrib import admin
import models


# Register your models here.
class InformationAdmin(admin.ModelAdmin):
    list_display = ('uid', 'username')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('uid', 'cid', 'content')


class UserRelationshipAdmin(admin.ModelAdmin):
    list_display = ('user_uid', 'friend_uid', 'relationship', 'degree')


admin.site.register(models.Users)
admin.site.register(models.Information, InformationAdmin)
admin.site.register(models.Profiles, ProfileAdmin)
admin.site.register(models.UserRelationship, UserRelationshipAdmin)
admin.site.register(models.Classify)
admin.site.register(models.Friend)
