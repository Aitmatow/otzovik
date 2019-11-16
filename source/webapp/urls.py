from django.urls import path
from .views import IndexView, ProductView, ProductCreateView, ProductUpdateView, ProductDeleteView, ReviewCreateView, \
    ReviewDeleteView, ReviewUpdateView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/<int:pk>/', ProductView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete', ProductDeleteView.as_view(), name='product_delete'),
    path('review/create/<int:pk>', ReviewCreateView.as_view(), name='review_create'),
    path('review/<int:pk>/update/<int:id>', ReviewUpdateView.as_view(),name='review_update'),
    path('review/<int:pk>/delete/<int:id>', ReviewDeleteView.as_view(),name='review_delete')
]
