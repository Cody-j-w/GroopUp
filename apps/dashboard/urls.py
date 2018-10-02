from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^register_user$', views.register_user),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^user/(?P<username>\w+)$', views.user),
    url(r'^settings$', views.settings),
    url(r'^game_finder$', views.game_finder),
    url(r'^game/(?P<id>\d+)$', views.game),
    url(r'^user_edit$', views.user_edit),
    url(r'^email_edit$', views.email_edit),
    url(r'^pass_edit$', views.pass_edit),
    url(r'^avatar_edit$', views.avatar_edit),
    url(r'^avatar_change$', views.avatar_change),
    url(r'^desc_edit$', views.desc_edit),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)