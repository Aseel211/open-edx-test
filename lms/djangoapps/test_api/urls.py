from django.urls import include, path, re_path
from .views import ClientGreetingAPI
urlpatterns = [
    path('greet', ClientGreetingAPI.as_view(),
         name='greet'
         ),
]