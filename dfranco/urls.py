"""dfranco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from principal.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('nosotros/', nosotros, name='nosotros'),
    path('categorias/', categorias, name='categorias'),
    path('productos/', productos, name='productos'),
    path('productos/<int:tipo_id>/', productos_tipo, name='productos_tipo'),
    path('producto/<int:producto_id>/', producto_detail, name='producto_detail'),
    path('servicios/', servicios, name='servicios'),
    path('servicio/<int:producto_id>/', servicio_detail, name='servicio_detail'),
    path('blog/', blog, name='blog'),
    path('blog/<int:historia_id>/', blog_detail, name='blog_detail'),
    path('contacto/', contacto, name='contacto'),
    path('carrito/', cart_detail, name='cart_detail'),
    #ajax
    path('ajax/paginate/', paginate, name='wertwe'),
    path('ajax/itemsno/', getitemsno, name='itemsno'),
    path('ajax/paginateservicios/', paginate_servicios, name='paginate_servicios'),
    path('ajax/itemsnoservicios/', getitemsno_servicios, name='itemsno_servicios'),
    path('ajax/paginate_historias/', paginate_historias, name='paginate_historias'),
    path('ajax/itemsno_historias/', getitemsno_historias, name='itemsno_historias'),
    path('cart/add/<int:id>/', cart_add_ajax, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear_ajax, name='item_clear'),
    path('cart/item_increment/<int:id>/', item_increment, name='item_increment'),
    path('cart/decrement/<int:id>/', cart_decrement_ajax, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('payment/', paypal_ipn, name='payment'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
