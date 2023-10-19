# shop_api/urls.py
from django.contrib import admin
from django.urls import include, path

# shop_api/urls.py
from django.contrib import admin
from django.urls import include, path
from product.views import CategoryList

urlpatterns = [
    path('', CategoryList.as_view(), name='root'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('product.urls')),
]

