from django.urls import path

# пути в приложении adboard
from .views import start, RulesView, AdsList, ResponsesList, AdCreate, AdView, AdEdit, AdDelete


urlpatterns = [
   path('', start),
   path('rules/', RulesView.as_view()),

   path('ads', AdsList.as_view(), name='ads_list'),
   path('ad/<int:pk>', AdView.as_view(), name='ad'),  # имя совпадает со view'шкой, надо ли его указывать здесь?
                                                      # Какое в приоритете?
   path('ad/add/', AdCreate.as_view(), name='ad_create'),  # Внимательно с заглавными!
   path('ad/<int:pk>/update/', AdEdit.as_view(), name='ad_edit'),
   path('ad/<int:pk>/delete/', AdDelete.as_view(), name='ad_delete'),

   # path('responses', ResponsesList.as_view(), name='responses_list'),  # список к конкретному Ad
]
