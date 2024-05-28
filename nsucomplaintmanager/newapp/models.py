from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser


#  Custom User Manager
position = (
    ('admin','admin'),
    ('Student','Student'),
    ('Faculty','Faculty'),
    ('Employee','Employee')
)
class UserManager(BaseUserManager):
  def create_user(self, email, name, position, password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name=name,
          position=position,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, position, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
          name=name,
          position=position,
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name = models.CharField(max_length=200)
  position = models.CharField(choices=position,default='Choose One',max_length=30)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name', 'position']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200)
    student_id = models.CharField(max_length=15)

    def __str__(self):
        return str(self.user)

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200)
    faculty_initial = models.CharField(max_length=20)

    def __str__(self):
        return str(self.user)

Sector_Choices = (
    ('Administratio','Administration'),
    ('Accounts','Accounts'),
    ('Security','Security'),
    ('Cleaning','Cleaning'),
    ('Helper','Helper'),
    ('Canteen','Canteen')
)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=80)
    sector = models.CharField(choices=Sector_Choices,default='Choose one',max_length=30)
    employee_id = models.CharField(max_length=15)

    def __str__(self):
        return str(self.user)

Status_Choices = (
    ('Accepted','Accepted'),
    ('Processing','Processing'),
    ('Reviewed','Reviewed')
)
accused_status = (
    ('Student','Student'),
    ('Faculty','Faculty'),
    ('Employee','Employee')
)

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complainer = models.EmailField(max_length=50) 
    accused = models.EmailField(max_length=50)
    accused_status = models.CharField(choices=accused_status, default='choose one', max_length=30)
    reviewer = models.EmailField(max_length=50)
    statement = models.TextField(max_length=250)
    comment = models.TextField(max_length=250, default="No comment yet")
    upload = models.FileField()
    publish_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=Status_Choices,default='Pending',max_length=30)