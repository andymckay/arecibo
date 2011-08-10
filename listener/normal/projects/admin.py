from django.contrib import admin

from projects.models import Project, ProjectURL


class ProjectAdmin(admin.ModelAdmin):
    pass


class ProjectURLAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectURL, ProjectURLAdmin)
