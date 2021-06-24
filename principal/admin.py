from django.contrib import admin, messages
from .models import *
# Register your models here.
#inlines
class GaleriaProductoInline(admin.StackedInline):
    model = GaleriaProducto
    extra = 0

class ProductoPerksInline(admin.StackedInline):
    model = ProductoPerks
    extra = 0

class SeccionNosotrosPerksInline(admin.StackedInline):
    model = SeccionNosotrosPerks
    extra = 0

class HistoriaCarruselInline(admin.StackedInline):
    model = HistoriaCarrusel
    extra = 0

#model admins
class DespliegueAdmin(admin.ModelAdmin):

    def response_add(self, request, obj, post_url_continue=None):
        msg = "Despliegue realizado con exito"
        self.message_user(request, msg, level=messages.SUCCESS)
        return self.response_post_save_add(request, obj)

class ProductoAdmin(admin.ModelAdmin):
    list_filter = ['tipo', 'visible']
    inlines = [ProductoPerksInline, GaleriaProductoInline]

class SeccionNosotrosAdmin(admin.ModelAdmin):
    inlines = [SeccionNosotrosPerksInline]

class HistoriaAdmin(admin.ModelAdmin):
    inlines = [HistoriaCarruselInline]

#register
#***
admin.site.register(ConfiguracionGodlango)
admin.site.register(Despliegue, DespliegueAdmin)
#***
#principal
admin.site.register(Configuracion)
admin.site.register(Product, ProductoAdmin)
admin.site.register(Tipo)
admin.site.register(Historia, HistoriaAdmin)
admin.site.register(Reservacion)
admin.site.register(Pedido)
admin.site.register(Destinatario)
#secciones
admin.site.register(SeccionPrincipal)
admin.site.register(SeccionNosotros, SeccionNosotrosAdmin)
admin.site.register(Mapa)