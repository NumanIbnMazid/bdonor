
from django.urls import path, include
from .views import DonationReportTemplateView


urlpatterns = [
    path("donation/", DonationReportTemplateView.as_view(), name="report_donation")
]
