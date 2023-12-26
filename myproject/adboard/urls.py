from django.urls import path

# пути в приложении adboard
from .views import *


urlpatterns = [
   path('', start),
   path('rules/', RulesView.as_view()),

   path('ads', AdsList.as_view(), name='ads_list'),
   path('ad/<int:pk>', AdView.as_view(), name='ad'),
   path('ad/add/', AdCreate.as_view(), name='ad_create'),
   path('ad/<int:pk>/edit/', AdEdit.as_view(), name='ad_edit'),
   path('ad/<int:pk>/delete/', AdDelete.as_view(), name='ad_delete'),

   path('responses', ResponsesList.as_view(), name='responses_list'),
   path('response/<int:pk>', ResponseView.as_view(), name='response'),
   path('response/add/', ResponseCreate.as_view(), name='response_create'),
   path('response/<int:pk>/edit/', ResponseEdit.as_view(), name='response_edit'),
   path('response/<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),
]
