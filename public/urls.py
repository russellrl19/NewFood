from django.conf.urls import url
from django.views.generic import RedirectView


from . import api
from . import views

urlpatterns = [

    # pages
    # url(r'^photos/add/(\d+)/tag/?$', views.tag_photo, name="tag_photo"),
    # url(r'^photos/add/?$', views.add_photo, name="add_photo"),
    # url(r'^photos/view/(\d+)/?$', views.view_photo, name="view_photo"),
    # url(r'^search/?$', views.search_filters, name="search_filters"),
    # url(r'^search/results/?$', views.search_results, name="search_results"),
    # url(r'^people/add/?$', views.add_identity, name="add_identity"),
    # url(r'^help/?$', views.help, name="help"),
    # url(r'^my_profile/?$', views.my_profile, name="my_profile"),
    # url(r'^public_profile/(?P<username>\w+)/$', views.public_profile, name="public_profile"),

    url(r'^login/?$', views.login_page, name='index'),
    url(r'^logout/?$', views.logout_page, name='index'),
    url(r'^register/?$', views.register_page, name='index'),

    url(r'^$', views.index, name='index'),
    url(r'^index/?$', RedirectView.as_view(url='index')),

]
