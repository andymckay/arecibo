from django.contrib import admin

from error.models import Error, Group


class ErrorAdmin(admin.ModelAdmin):
    pass


class GroupAdmin(admin.ModelAdmin):
    pass


admin.site.register(Error, ErrorAdmin)
admin.site.register(Group, GroupAdmin)
