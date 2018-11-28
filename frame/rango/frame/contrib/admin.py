from django.contrib import admin
from .models import User, SToken, Trash,YConstant



class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'is_activated',
                    'name', 'create_time', 'update_time')
    ordering = ('-update_time',)


admin.site.register(User, UserAdmin)



class STokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'user', 'host', 'create_time')
    fields = ('user', 'host')
    ordering = ('-create_time',)


admin.site.register(SToken, STokenAdmin)



class TrashAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'content', 'comment', 'create_time')
    ordering = ('-create_time',)


admin.site.register(Trash, TrashAdmin)



class ConstantAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'description')
    ordering = ('key',)


admin.site.register(YConstant, ConstantAdmin)
