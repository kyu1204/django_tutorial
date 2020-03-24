from django.urls import path
from .views import PredictView, KospiView, ReportView, PredictRateView, HitDateView

urlpatterns = [
    path('predict/', PredictView.as_view()),
    path('kospi/', KospiView.as_view()),
    path('report/', ReportView.as_view()),
    path('rate/', PredictRateView.as_view()),
    path('hit-date/', HitDateView.as_view()),
]
