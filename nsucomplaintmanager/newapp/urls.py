from re import template
from django.contrib import admin
from django.urls import path
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from newapp import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.UserView.as_view(), name='home'),
    path('registration/',views.RegistrationView.as_view(), name='registration'),
    path('lodge/',views.LodgeView.as_view(), name='lodge'),
    path('info/', views.information, name='info'),
    path('userprofile/', views.UserProfileView.as_view(), name='userprofile'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('complaints/', views.ComplaintsView, name='complaints'),
    path('reviews/', views.ReviewsView, name='review'),
    path('det-review/<int:pk>', views.DetailedReviewView.as_view(), name='det-review'),
    path('chng-reviewer/<int:pk>', views.ChangeReviewerView.as_view(), name='chng-reviewer'),

    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='newapp/passwordchange.html',
    form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),

    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='newapp/passwordchangedone.html'),name='passwordchangedone'),
    
    path('accounts/login/', auth_views.LoginView.as_view(template_name='newapp/login.html', 
    authentication_form=LoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='newapp/password_reset.html', form_class=MyPasswordResetForm),
    name='password_reset'),

    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='newapp/password_reset_done.html'),
    name='password_reset_done'),

    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='newapp/password_reset_complete.html'),
    name='password_reset_complete'),

    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='newapp/password_reset_confirm.html',
    form_class=MySetPasswordForm), name='password_reset_confirm'),

    # #API
    # path('API/student/',views.StudentList.as_view()),
    # path('API/user/',views.UserList.as_view()),
    # path('API/faculty/',views.FacultyList.as_view()),
    # path('API/employee/',views.EmployeeList.as_view()),
    # path('API/complaint/',views.ComplaintsList.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)