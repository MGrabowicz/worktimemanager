from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import wtmUser


class BlogUserInline(admin.StackedInline):
    model = wtmUser
    can_delete = False
    verbose_name_plural = 'employee'

class UserAdmin(BaseUserAdmin):
    inlines = (BlogUserInline,)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(wtmUser)