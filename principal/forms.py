from .models import *
from django.forms import *

class ReservacionForm(ModelForm):
    class Meta:
        model = Reservacion
        fields = '__all__'

class CuentaForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ('nombre', 'telefono', 'telefono2','direccion',)