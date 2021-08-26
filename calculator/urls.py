from django.urls import path
from . import views

urlpatterns = [
   path('', views.Intro),
   path("jobs/", views.Jobs.as_view()),
   path('universities/', views.Universities.as_view()),
   path('universities/<int:pk>', views.UniversityById.as_view()),
   path('jandu/', views.JandU.as_view()),
   path('salary/', views.Salaries.as_view()),
   path('calculations/', views.PayOffEstimate.as_view()),
]
