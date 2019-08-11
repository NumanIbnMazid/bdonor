from django.urls import path
from .views import (PlanCreateView, priceplan_delete,
                    PlanDetailView, PlanUpdateView, PricePlanListView)

urlpatterns = [
    path('create/', PlanCreateView.as_view(), name='plan_create'),
    path('delete/', priceplan_delete, name='plan_delete'),
    path('<slug>/details/', PlanDetailView.as_view(), name='plan_details'),
    path('<slug>/update/', PlanUpdateView.as_view(), name='plan_update'),
    path('list/', PricePlanListView.as_view(), name='plan_list'),
]
