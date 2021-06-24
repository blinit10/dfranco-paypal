from django.db import models
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from colorfield.fields import ColorField
import sys
from PIL import Image
from io import BytesIO
from pathlib import Path
import shutil
import hashlib
import os
from datetime import datetime
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.
def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def walk_up_folder(path, depth=1):
    _cur_depth = 1
    while _cur_depth < depth:
        path = os.path.dirname(path)
        _cur_depth += 1
    return path

# Create your models here.
class ConfiguracionGodlango(models.Model):
    inicializado = models.BooleanField(default=False)
    has_previo = models.CharField(max_length=500, blank=True, default='', verbose_name='Hash previo')

    def __str__(self):
        return 'Configuraciones de ámbito global'

    class Meta:
        verbose_name_plural = '*  Configuraciones de ámbito global'
        verbose_name = 'Configuración de ámbito global'
        app_label = 'godjango'

class Despliegue(models.Model):
    llave = models.CharField(max_length=500)
    valor = models.CharField(max_length=500)
    hora = models.TimeField(default=datetime.now())

    def __str__(self):
        return 'Despliegue'

    def save(self, *args, **kwargs):
        hash = self.llave + self.valor
        hash = hash_string(hash)
        ruta = ""
        ruta = ruta + os.path.join(os.path.dirname(os.path.dirname(__file__)))
        ruta = Path(ruta)
        ruta = walk_up_folder(ruta, 2)
        ruta = ruta + '/messages/' + hash + '.sd/'
        ruta = Path(ruta)
        if ConfiguracionGodlango.objects.all()[0].inicializado == False:
            if not os.path.exists(ruta):
                os.makedirs(ruta)
                obj = ConfiguracionGodlango.objects.all()[0]
                obj.has_previo = ruta
                obj.inicializado = True
                obj.save()
        else:
            dir_path = Path(ConfiguracionGodlango.objects.all()[0].has_previo)
            try:
                shutil.rmtree(dir_path)
            except OSError as e:
                print("Error: %s : %s" % (dir_path, e.strerror))
            if not os.path.exists(ruta):
                os.makedirs(ruta)
                obj = ConfiguracionGodlango.objects.all()[0]
                obj.has_previo = ruta
                obj.save()
        pass

    class Meta:
        verbose_name_plural = '**  Despliegues'
        verbose_name = 'Despliegue'
        app_label = 'godjango'

#principal
class Configuracion(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre del negocio')
    logo = models.ImageField(upload_to='cfg/')
    paypal = models.CharField(max_length=255, default='ARPyFdnp1H1PssVANyVuDHoRWm7MA3jwMROIjX.R.Wt43uCIYZ17LIpr')
    moneda = models.CharField(max_length=255, verbose_name='Moneda que se utilizará en la plataforma')
    porciento = models.FloatField(default=0, verbose_name='Porcentaje de comisión', help_text='Porciento extra que se le agrega al precio de cada producto')
    desc = models.TextField(verbose_name='Breve descripción de la empresa')
    color = ColorField(default='#FF0000')
    color2 = ColorField(default='#FF0000')
    instagram = models.CharField(max_length=255, verbose_name='Enlace a Instagram', help_text='Opcional', blank=True)
    facebook = models.CharField(max_length=255, verbose_name='Enlace a Facebook', help_text='Opcional', blank=True)
    telegram = models.CharField(max_length=255, verbose_name='Contacto de Telegram', help_text='Opcional', blank=True)
    whatsapp = models.CharField(max_length=255, verbose_name='Contacto de WhatsApp', help_text='Opcional', blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = '01 - Configuraciones'
        verbose_name = 'Configuración'

class Tipo(models.Model):
    tipo = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='tipos')

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = '02 - Tipos'

class Product(models.Model):
    TIPO_CHOICES = (
        ('Servicio', 'Servicio'),
        ('Producto', 'Producto'),
    )
    clasificacion = models.ForeignKey(Tipo, on_delete=models.CASCADE, verbose_name='Clasificación', null=True)
    tipo = models.CharField(choices=TIPO_CHOICES, max_length=255)
    image = models.ImageField(upload_to='productos y servicios/', verbose_name='Imagen')
    name = models.CharField(max_length=255, verbose_name='Nombre')
    price = models.FloatField(default=0, verbose_name='Precio', help_text='Opcional')
    contenido = RichTextField()
    visible = models.BooleanField(default=True)
    visitas = models.IntegerField(default=0)
    compras = models.IntegerField(default=0)
    calculado = models.BooleanField(default=False)
    __precio = None

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        self.__precio = self.price

    def save(self, *args, **kwargs):
        if self.calculado == False or self.price != self.__precio:
            self.calculado = True
            porciento = Configuracion.objects.all()[0].porciento
            iv = 0
            dv = self.price + (self.price * porciento / 100)
            if dv - int(dv) > 0:
                iv = int(dv) + 1
            else:
                iv = dv
            self.price = iv
        super(Product, self).save(*args, **kwargs)
        self.__precio = self.price

    def resumen(self):
        if len(self.contenido) > 120:
            return self.contenido[:117] + ' ...'
        return self.contenido

    class Meta:
        verbose_name_plural = '03 - Productos y servicios'
        verbose_name = 'Producto o servicio'
        ordering = ['tipo', 'id']

class ProductoPerks(models.Model):
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    contenido = models.CharField(max_length=255)

    def __str__(self):
        return self.contenido

    class Meta:
        verbose_name_plural = 'Informaciones adicionales'
        verbose_name = 'Información adicional'

class GaleriaProducto(models.Model):
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    image =  models.ImageField(upload_to='productos/', verbose_name='Imagen',help_text='Resolución recomendada 1024x768')
    titulo = models.CharField(max_length=255, blank=True, help_text='Opcional', verbose_name='Título')
    contenido = RichTextField(blank=True, help_text='Opcional')

    def __str__(self):
        return 'Imagen ' + str(self.id) + ' producto ' + self.producto.name

    class Meta:
        verbose_name_plural = 'Imágenes de productos'
        verbose_name = 'Imagen de productos'


class Historia(models.Model):
    imagen = models.ImageField(upload_to='historias/')
    titulo = models.CharField(max_length=255, verbose_name='Título')
    contenido = RichTextUploadingField(help_text='Opcional', blank=True)
    visible = models.BooleanField(default=True)
    fecha = models.DateTimeField()

    def __str__(self):
        return self.titulo

#217
    def resumen(self):
        if len(self.contenido) > 217:
            return self.contenido[:217] + ' ...'
        else:
            return self.contenido

    class Meta:
        verbose_name = 'Historia'
        verbose_name_plural = '04 - Historias'

class HistoriaCarrusel(models.Model):
    seccion = models.ForeignKey(Historia, on_delete=models.CASCADE, related_name='galeria')
    multimedia = models.CharField(max_length=700, help_text='Link del video de YouTube tipo embed')

    def __str__(self):
        return 'Archivo multimedia #' + str(self.id)

    class Meta:
        verbose_name_plural = 'Multimedias'
        verbose_name = 'Multimedia'

class Reservacion(models.Model):
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255, verbose_name='Teléfono o E-mail')
    asunto = models.CharField(max_length=255)
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = '05 - Contactos'

class Destinatario(models.Model):
    identificador = models.CharField(max_length=255, help_text='Opcional', blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        if self.identificador:
            return self.identificador + ' - ' + str(self.email)
        return str(self.email)

    class Meta:
        verbose_name_plural = '06 - Destinatarios'
        verbose_name = 'Destinatario'

class Pedido(models.Model):
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255, verbose_name='Teléfono del comprador')
    telefono2 = models.CharField(max_length=255, verbose_name='Teléfono del receptor', blank=True, null=True)
    direccion = models.CharField(max_length=255, verbose_name='Dirección a entregar', help_text='Dirección de quién lo recibe en Cuba')
    contenido = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Encargo'
        verbose_name_plural = '07 - Encargos'

#secciones
class SeccionPrincipal(models.Model):
    ENLACE_CHOICES = (
        ('productos','Ver productos'),
        ('servicios', 'Ver servicios'),
        ('blog', 'Historias'),
        ('contacto', 'Contáctenos'),
    )
    titulo = models.CharField(verbose_name='Título', max_length=255)
    subtitulo = models.CharField(verbose_name='Subtítulo', max_length=255)
    imagen = models.ImageField(upload_to='secciones/')
    enlace = models.CharField(max_length=255, choices=ENLACE_CHOICES)

    def __str__(self):
        return self.titulo + ' ' + self.subtitulo

    class Meta:
        verbose_name_plural = '01 - Sección Principal'
        verbose_name = 'Sección Principal'
        app_label = 'secciones'

class SeccionNosotros(models.Model):
    titulo = models.CharField(verbose_name='Título', max_length=255)
    imagen = models.ImageField(upload_to='secciones/')


    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = '02 - Sección Nosotros'
        verbose_name = 'Sección Nosotros'
        app_label = 'secciones'

class SeccionNosotrosPerks(models.Model):
    ALINEACION_CHOICES = (
        ('center', 'Al centro'),
        ('left', 'A la izquierda'),
        ('right', 'A la derecha'),
        ('justify', 'Justificar'),
    )
    seccion = models.ForeignKey(SeccionNosotros, on_delete=models.CASCADE, related_name='bloques')
    alineacion = models.CharField(max_length=255, choices=ALINEACION_CHOICES, default='justify', verbose_name='Alineación del párrafo')
    bloque_der = models.BooleanField(default=False, verbose_name='Bloque de texto a la derecha')
    titulo = models.CharField(max_length=300, verbose_name='Título', help_text='Opcional', blank=True)
    imagen = models.ImageField(upload_to='secciones/', verbose_name='Imagen', help_text='Opcional', blank=True, null=True)
    contenido = RichTextField(verbose_name='Contenido', help_text='Opcional', blank=True)

    def __str__(self):
        if self.titulo:
            return self.titulo
        if self.contenido:
            return self.contenido
        return 'Imagen sin texto'

    class Meta:
        verbose_name_plural = 'Bloques'
        verbose_name = 'Bloque'

class Mapa(models.Model):
    coordenadas = models.TextField()


    def __str__(self):
        return 'Coordenadas ' + str(Configuracion.objects.all()[0].nombre)

    def save(self, *args, **kwargs):
        coords = str(self.coordenadas)
        nuevas_coordenadas = coords.replace('width="600" height="450"', 'width="100%" height="600px"')

        self.coordenadas = nuevas_coordenadas
        super(Mapa, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '03 - Coordenadas'
        verbose_name = 'Coordenada'
        app_label = 'secciones'




