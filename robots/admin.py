from django.contrib import admin

from robots.models import Robot


class RobotListAdmin(admin.ModelAdmin):
    list_display = ('id','created', 'serial', 'model', 'version')
    list_display_links = ('id', )
    list_filter = ('model', 'version')

admin.site.register(Robot, RobotListAdmin)


# Register your models here.
