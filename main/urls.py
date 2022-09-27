from django.urls import path
from .views import *
from django.contrib.auth.views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', loginPage, name='login'),
    path('register/', registerPage, name='register'),
    path('check-valid-name/', check_name, name='check-name'),
    path('logout/', logoutUser, name='logout'),
    path('create-post/', createPost, name='create-post'),
    path('post/<int:pk>/', postDetail, name='post'),
    path('update-post/<int:pk>/', updatePost, name='update-post'),
    path('delete-post/<int:pk>/', deletePost, name='delete-post'),
    path('p/<slug:slug>/', userProfile, name='profile'),
    path('favorite/<slug:slug>/', favoritePost, name='favorite'),
    path('update-user/', updateUser, name='update-user'),
    path('delete-comment/<int:pk>/', deleteComment, name='delete-comment'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/',PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',PasswordResetCompleteView.as_view(),name='password_reset_complete')
]