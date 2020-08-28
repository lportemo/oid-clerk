from django.urls import path

import clerk.views

urlpatterns = [
    path('craft', clerk.views.craft),
    path('check', clerk.views.check),
]
