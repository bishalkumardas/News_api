from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'', views.NewsViewSet)
# router.register(r'news', views.NewsViewSet) #as I am already giving news in path url I don't need news

urlpatterns = [
    path('', views.view_comments, name='view_comments'),
    path('create/', views.create_comment, name='create_comment'),
    path('news/', include(router.urls), name='view_news'),
    path('review/', views.Comment, name='view_news'),
    # path('<int:pk>', views.single_comment, name='single_comment'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)