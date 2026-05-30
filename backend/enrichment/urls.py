from django.urls import path
from . import views

urlpatterns = [
    path('enrich/', views.enrich_company_api, name='enrich_company'),
    path('results/', views.list_results_api, name='list_results'),
]
