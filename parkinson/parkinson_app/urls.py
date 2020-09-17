from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "parkinson_app"
urlpatterns = [
    path('', views.landing_page, name="landing_page"),
    path('login', views.login_page, name="login"),
    path('signup', views.signup_page, name="signup"),
    path('home', views.home_page, name="home"),
    path('help', views.help_page, name="help"),
    path('faqs', views.faq_page, name="faq"),
    path('complete-profile', views.complete_profile, name="complete_profile"),
    path('edit-profile', views.edit_profile_page, name="edit_profile"),
    path('update-password', views.update_password, name="update_password"),
    path('new-test', views.new_test_page, name="new_test"),
    path('upload-profile-pic', views.upload_profile_pic, name="upload_profile_pic"),
    path('what-is-parkinsons', views.what_is_parkinson_page, name="what_is_parkinson"),
    path('logout', views.logout_view, name="logout"),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)