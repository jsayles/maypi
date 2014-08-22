from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from maypi.models import DoorCode, CodeLog

class DoorCodeAdmin(admin.ModelAdmin):
	model = DoorCode
	list_display=('created', 'user', 'code', 'start', 'end')
admin.site.register(DoorCode, DoorCodeAdmin)

class CodeLogAdmin(admin.ModelAdmin):
	model = CodeLog
	list_display=('created', 'code_entered', 'user', 'code', 'success')
admin.site.register(CodeLog, CodeLogAdmin)

admin.site.unregister(User)
class CustomUserAdmin(UserAdmin):
	model = User
	list_display=('date_joined', 'username', 'email', 'first_name', 'last_name', 'is_staff')
admin.site.register(User, CustomUserAdmin)
