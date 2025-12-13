from django.urls import path
from . import views as v
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # ---------- AUTH ----------
    path('', v.signup, name='signup'),
    path('login/', v.login_view, name='login'),
    path('logout/', v.logout_view, name='logout'),

    # ---------- MAIN PAGES ----------
    path('home/', v.home, name='home'),
    path('profile/', v.profile, name='profile'),   # Profile + My Posts

    # ---------- BLOG ----------
    path('new/', v.new_post, name='new_post'),
    path('post/<int:id>/', v.blog_detail, name='blog_detail'),
    path('post/<int:id>/edit/', v.edit_post, name='edit_post'),
    path('post/<int:id>/delete/', v.delete_post, name='delete_post'),
]

# ---------- MEDIA FILES ----------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
