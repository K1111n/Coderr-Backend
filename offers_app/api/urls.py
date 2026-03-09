# Third-party imports
from django.urls import path

# Local imports
from offers_app.api.views import BaseInfoView, OfferDetailItemView, OfferDetailView, OfferListCreateView

urlpatterns = [
    path('offers/', OfferListCreateView.as_view(), name='offer-list-create'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
    path('offerdetails/<int:pk>/', OfferDetailItemView.as_view(), name='offer-detail-item'),
    path('base-info/', BaseInfoView.as_view(), name='base-info'),
]
