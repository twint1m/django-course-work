from django.urls import path, include
from . import views
from .views import product_page
# Django rest_framework imports
from rest_framework import routers
from .views import CategoryApi, StockApi, ProductReviewApi, ProductApi, UserInfoApi


app_name = 'webshop'

router = routers.DefaultRouter()
router.register(r'api/category', CategoryApi)
router.register(r'api/stock', StockApi)
router.register(r'api/product-review', ProductReviewApi)
router.register(r'api/product', ProductApi)
router.register(r'api/user-info', UserInfoApi)

urlpatterns = [
    # path('', views.Home.as_view(), name='home'),
    path('', views.MainPage.as_view(), name='main_page'),
    path('main/', views.MainPage.as_view(), name='main_page'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('remove_review/', views.remove_review, name='remove_review'),
    path('buy/', views.buy_product, name='buy_product'),     
    path('filter/', views.ProductFilter.as_view(), name='filter'),
    path('shop/', views.ShopPage.as_view(), name='shop_page'),
    path('shop/<category_slug>', views.CategoryPage.as_view() , name='category_page'),
    path('shop/<category_slug>/<product_slug>', views.ProductPage.as_view(), name='product_page'),
    path('profile/<username>', views.UserProfile.as_view(), name='profile'),
    path('category/<slug:category_slug>/<slug:product_slug>/', product_page, name='product_page'),
    path('', include(router.urls)),
    path('api/user-info/<str:username>/', UserInfoApi.as_view({'get': 'retrieve'}), name='user-info'),
]
