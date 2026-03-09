# Third-party imports
from django.urls import path

# Local imports
from reviews_app.api.views import ReviewDetailView, ReviewListCreateView

urlpatterns = [
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
