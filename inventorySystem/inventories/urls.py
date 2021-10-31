from django.urls import path
from .views import inventoryList, per_product_view, update, delete, add_product, dashboard

urlpatterns = [
    path("", inventoryList, name="inventorylist"),
    path("per_product_view/<int:pk>/", per_product_view, name="per_product"),
    path("product_update/<int:pk>/", update, name="product_update"),
    path("delete/<int:pk>/", delete, name="product_delete"),
    path("add/", add_product, name="product_add"),
    path("dashboard/", dashboard, name="dashboard"),
]

