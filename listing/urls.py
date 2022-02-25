from django.urls import path

from . import views

urlpatterns = [
    path('manage/', views.ManageListingView.as_view()),
    path('detail/', views.ListingDetailView.as_view()),
    path('get-list/', views.ListingsView.as_view()),
    path('search/', views.SearchListingsView.as_view()),
]
