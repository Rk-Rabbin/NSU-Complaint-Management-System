from django.contrib import admin
from newapp.models import User, Student, Faculty, Employee, Complaint
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
  # The fields to be used in displaying the User model.
  # These override the definitions on the base UserModelAdmin
  # that reference specific fields on auth.User.
  list_display = ('id', 'email', 'name', 'position', 'is_admin')
  list_filter = ('is_admin',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('name', 'position')}),
      ('Permissions', {'fields': ('is_admin',)}),
  )
  # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
  # overrides get_fieldsets to use this attribute when creating a user.
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'name', 'position', 'password1', 'password2'),
      }),
  )
  search_fields = ('email',)
  ordering = ('email', 'id')
  filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)

@admin.register(Student)
class StudentModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'student_id']

@admin.register(Faculty)
class FacultyModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'faculty_initial']

@admin.register(Employee)
class EmployeeModelAdmin(admin.ModelAdmin):
    list_display = ['user','name', 'sector', 'employee_id']

@admin.register(Complaint)
class ComplaintModelAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'complainer', 'accused', 'accused_status', 'reviewer', 'statement','comment', 'upload', 'publish_date', 'status']