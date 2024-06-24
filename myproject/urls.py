"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from product import views
from myproject import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('',views.addData, name="addData"),
    path('admin/',admin.site.urls),
    # path('shipment/',views.addData),
    path('register/',views.UserRegistrationView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    # path('sendlisting/',views.sendListing),
    path('displayshipments/<int:id>',views.displayshipments),
    path('displayquotes/<int:id>',views.display_quotes),
    path('searchshipment/',views.filterShipment),
    path('quotepage/',views.store_quote),
    path('t/register/',views.shipper_temp),
    path('searchshipment/<int:id>', views.sendListing),
    path('addshipment/', views.AddShipmentData.as_view(), name='add-new-shipment'),
    path('shipment/<int:id>/', views.AddShipmentData.as_view(), name='shipment-update'),
    path('t/history/<int:id>/<str:status>', views.display_history_trans),
    path('translisting', views.translisting),
    path('translisting/confirmed',views.confirm_shipment),
    path('deleteorder/<int:id>/<int:user_id>',views.deleteorder),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)