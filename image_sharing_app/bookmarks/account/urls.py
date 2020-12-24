from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # Login custom
    # path('login/', views.user_login, name='login'),
    # Login view url from auth generic views
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # Logout view url
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Password Change view url
    # path('password_change/', auth_views.PasswordChangeView.as_view(),
    #  name='password_change'),
    # Password change done view url
    #  path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
    #     name='password_change_done'),
    # Password reset view url (request to reset password)
    # path('password_reset/', auth_views.PasswordResetView.as_view(),
    #     name='password_reset'),
    # Password reset done view (confirms that an email has been sent)
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
    #     name='password_reset_done'),
    # Password reset view (here is where you reset password)
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
    #     name='password_reset_confirm'),
    # Password reset done view (confirms that password has been successfully reset
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
    #     name='password_reset_complete'),


    # Dashboard view url
    path('', views.dashboard, name='dashboard'),
    # Solely Performs the functions of the above url patterns
    path('', include('django.contrib.auth.urls')),
    ##                                              ##
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('user/', views.user_list, name='user_list'),
    path('user/follow/', views.user_follow, name='user_follow'),
    path('user/<username>/', views.user_detail, name='user_detail'),
]
