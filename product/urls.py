from django.urls import path

from . import views

app_name = 'product'
urlpatterns = [
    path('product-list/', views.ProductListView.as_view(), name='product-list'),
    path('product/<str:pk>', views.ProductDetailView.as_view(), name='product-detail'),

    path('add-favorite/<str:pk>', views.AddFavoriteView.as_view(), name='add-favorite'),
    path('remove-fav/<str:pk>', views.RemoveFavoriteView.as_view(), name='remove-favorite'),
    path('favorite-list/', views.FavoriteListView.as_view(), name='favorite-list'),

    path('add-comparison/<str:pk>', views.AddCompareView.as_view(), name='add-comparison'),
    path('remove-comparison/<str:pk>', views.RemoveComparisonView.as_view(), name='remove-comparison'),
    path('comparison-list/', views.CompareListView.as_view(), name='comparison-list'),
    path('get-csv/', views.export_products_csv, name='export_products_csv'),
]
