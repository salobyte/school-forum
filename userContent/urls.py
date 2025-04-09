from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/home/', permanent=False)), 
    path('home/', views.HomeView.as_view(), name='home'),
    path('student_signup/', views.CreatingStudentView.as_view(), name='student_signup'),
    path('login/', views.login_view.as_view(), name = "login"),
    path('logout/', views.logout_view, name = "logout"),
    path('post/<int:post_id>/', views.SoloPostView.as_view(), name = 'view_post'),
    path('post/delete_post/<int:post_id>/', views.post_delete, name = 'delete_post'),
    path('post/like_post/<int:post_id>/', views.post_like, name = 'like_post'),
    path('post/delete_reply/<int:post_id>/<int:pk>', views.reply_delete, name = 'delete_reply'),
    path('post/like_reply/<int:post_id>/<int:pk>', views.reply_like, name = 'like_reply'),
    path('profiles/<int:user_id>', views.ProfileView.as_view(), name = 'profile'),
    path('profiles/settings/<int:user_id>', views.ProfileSettingsView.as_view(), name = 'profile_settings')
    ]

