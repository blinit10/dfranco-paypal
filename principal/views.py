import sqlite3

from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from .models import *
from .forms import *
from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from pytz import timezone
import pytz
from cart.cart import Cart
from dfranco.settings import CART_SESSION_ID, GEOLOC_DATABASE

# Create your views here.
def index(request):
    form = ReservacionForm()
    coordenadas = Mapa.objects.all()[0].coordenadas
    if not request.session.get(CART_SESSION_ID):
        request.session[CART_SESSION_ID] = {}
    total = 0
    for value in request.session[CART_SESSION_ID]:
        total = total + float(request.session[CART_SESSION_ID][value]['price'])*float(request.session[CART_SESSION_ID][value]['quantity'])
    cfg = Configuracion.objects.all()[0]
    principal = SeccionPrincipal.objects.all()[0]
    if len(Product.objects.filter(tipo='Servicio', visible=True)) > 3:
        servicios = Product.objects.filter(tipo='Servicio', visible=True).order_by('-id')[:3]
    else:
        servicios = Product.objects.filter(tipo='Servicio', visible=True).order_by('-id')
    tipos = Tipo.objects.all()[:3]
    productos = Product.objects.all().filter(tipo='Producto').order_by('-id')[:4]
    return render(request, 'index.html', {'cfg':cfg, 'principal':principal, 'servicios':servicios,
                                          'tipos':tipos, 'productos':productos, 'total':total, 'coordenadas':coordenadas,
                                          'form':form})

def categorias2(request):
    form = ReservacionForm()
    coordenadas = Mapa.objects.all()[0].coordenadas
    if not request.session.get(CART_SESSION_ID):
        request.session[CART_SESSION_ID] = {}
    total = 0
    for value in request.session[CART_SESSION_ID]:
        total = total + float(request.session[CART_SESSION_ID][value]['price'])*float(request.session[CART_SESSION_ID][value]['quantity'])
    cfg = Configuracion.objects.all()[0]
    principal = SeccionPrincipal.objects.all()[0]
    if len(Product.objects.filter(tipo='Servicio', visible=True)) > 3:
        servicios = Product.objects.filter(tipo='Servicio', visible=True).order_by('-id')[:3]
    else:
        servicios = Product.objects.filter(tipo='Servicio', visible=True).order_by('-id')
    tipos = Tipo.objects.all()[:3]
    cats = Tipo.objects.all()
    productos = Product.objects.all().filter(tipo='Producto').order_by('-id')[:4]
    return render(request, 'categorias.html', {'cfg':cfg, 'principal':principal, 'servicios':servicios,
                                          'tipos':tipos, 'productos':productos, 'total':total, 'coordenadas':coordenadas,
                                          'form':form, 'categorias':cats })

def nosotros(request):
    if not request.session.get(CART_SESSION_ID):
        request.session[CART_SESSION_ID] = {}
    total = 0
    for value in request.session[CART_SESSION_ID]:
        total = total + float(request.session[CART_SESSION_ID][value]['price'])*float(request.session[CART_SESSION_ID][value]['quantity'])
    cfg = Configuracion.objects.all()[0]
    seccion = SeccionNosotros.objects.all()[0]
    return render(request, 'about.html', {'cfg':cfg, 'seccion':seccion, 'total':total})

def categorias(request):
    if not request.session.get(CART_SESSION_ID):
        request.session[CART_SESSION_ID] = {}
    total = 0
    for value in request.session[CART_SESSION_ID]:
        total = total + float(request.session[CART_SESSION_ID][value]['price'])*float(request.session[CART_SESSION_ID][value]['quantity'])
    cfg = Configuracion.objects.all()[0]
    cats = Tipo.objects.all()
    return render(request, 'categorias.html', {'cfg':cfg, 'total':total, 'categorias':cats})


def productos(request):
    if not request.session.get(CART_SESSION_ID):
        request.session[CART_SESSION_ID] = {}
    total = 0
    for value in request.session[CART_SESSION_ID]:
        total = total + float(request.session[CART_SESSION_ID][value]['price'])*float(request.session[CART_SESSION_ID][value]['quantity'])
    cfg = Configuracion.objects.all()[0]
    muebles = Product.objects.filter(tipo='Producto', visible=True).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(muebles, 9)
    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)
    page_list = productos.paginator.page_range
    return render(request, 'product.html', {'cfg':cfg, 'productos':productos, 'page_list':page_list, 'total':total})

def productos_tipo(request, tipo_id):
    categoria = Tipo.objects.get(pk=tipo_id)
    if not request.session.get(CART_SESSION_ID):
        request.session[CART_SESSION_ID] = {}
    total = 0
    for value in request.session[CART_SESSION_ID]:
        total = total + float(request.session[CART_SESSION_ID][value]['price'])*float(request.session[CART_SESSION_ID][value]['quantity'])
    cfg = Configuracion.objects.all()[0]
    muebles = Product.objects.filter(tipo='Producto', visible=True, clasificacion=categoria).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(muebles, 9)
    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)
    page_list = productos.paginator.page_range
    return render(request, 'product_tipo.html', {'cfg':cfg, 'productos':muebles, 'page_list':page_list, 'total':total, 'categoria':categoria})


def paginate(request):
    muebles = Product.objects.filter(tipo='Producto', visible=True).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(muebles, 9)
    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)
    page_list = productos.paginator.page_range
    id= request.GET.get('page', None)
    starting_number= (int(id)-1)*9
    ending_number= int(id)*9
    if starting_number > len(page_list) * 9:
        return
    if ending_number > len(page_list) * 9:
        return
    result= Product.objects.filter(tipo='Producto',visible=True).order_by('-id')[starting_number:ending_number]
    response = {}
    for item in result:
        response[item.id] = model_to_dict(item, exclude=['image'])
        response[item.id]['imagen'] = str(item.image)
    #response['length'] = len(result)
    data={'result':response}
    return JsonResponse(data, safe=False)

def getitemsno(request):
    muebles = Product.objects.filter(tipo='Producto', visible=True).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(muebles, 9)
    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)
    page_list = productos.paginator.page_range
    total = len(page_list)
    return JsonResponse({'total': total})

def servicios(request):
    if not request.session.get(CART_SESSION_ID):
        request.session[CART_SESSION_ID] = {}
    total = 0
    for value in request.session[CART_SESSION_ID]:
        total = total + float(request.session[CART_SESSION_ID][value]['price'])*float(request.session[CART_SESSION_ID][value]['quantity'])
    cfg = Configuracion.objects.all()[0]
    muebles = Product.objects.filter(tipo='Servicio', visible=True).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(muebles, 9)
    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)
    page_list = productos.paginator.page_range
    return render(request, 'services.html', {'cfg':cfg, 'productos':productos, 'page_list':page_list, 'total':total})

def paginate_servicios(request):
    muebles = Product.objects.filter(tipo='Servicio', visible=True).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(muebles, 9)
    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)
    page_list = productos.paginator.page_range
    id= request.GET.get('page', None)
    starting_number= (int(id)-1)*9
    ending_number= int(id)*9
    if starting_number > len(page_list) * 9:
        return
    if ending_number > len(page_list) * 9:
        return
    result= Product.objects.filter(tipo='Servicio',visible=True).order_by('-id')[starting_number:ending_number]
    response = {}
    for item in result:
        response[item.id] = model_to_dict(item, exclude=['image'])
        response[item.id]['imagen'] = str(item.image)
    #response['length'] = len(result)
    data={'result':response}
    return JsonResponse(data, safe=False)

def getitemsno_servicios(request):
    muebles = Product.objects.filter(tipo='Servicio', visible=True).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(muebles, 9)
    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)
    page_list = productos.paginator.page_range
    total = len(page_list)
    return JsonResponse({'total': total})

def blog(request):
    if not request.session.get(CART_SESSION_ID):
        request.session[CART_SESSION_ID] = {}
    total = 0
    for value in request.session[CART_SESSION_ID]:
        total = total + float(request.session[CART_SESSION_ID][value]['price'])*float(request.session[CART_SESSION_ID][value]['quantity'])
    cfg = Configuracion.objects.all()[0]
    muebles = Historia.objects.filter(visible=True).order_by('-id', '-fecha')
    page = request.GET.get('page', 1)
    paginator = Paginator(muebles, 9)
    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)
    page_list = productos.paginator.page_range
    return render(request, 'blog.html', {'cfg':cfg, 'historias':productos, 'page_list':page_list, 'total':total})

def paginate_historias(request):
    muebles = Historia.objects.filter(visible=True).order_by('-id', '-fecha')
    page = request.GET.get('page', 1)
    paginator = Paginator(muebles, 9)
    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)
    page_list = productos.paginator.page_range
    id= request.GET.get('page', None)
    starting_number= (int(id)-1)*9
    ending_number= int(id)*9
    if starting_number > len(page_list) * 9:
        return
    if ending_number > len(page_list) * 9:
        return
    result= Historia.objects.filter(visible=True).order_by('-id', '-fecha')[starting_number:ending_number]
    response = {}
    for item in result:
        response[item.id] = model_to_dict(item, exclude=['image'])
        response[item.id]['imagen'] = str(item.imagen)
        response[item.id]['fecha2'] = str(item.fecha.date())
        response[item.id]['resumen'] = item.resumen()
    #response['length'] = len(result)
    data={'result':response}
    return JsonResponse(data, safe=False)

def getitemsno_historias(request):
    muebles = Historia.objects.filter(visible=True).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(muebles, 9)
    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)
    page_list = productos.paginator.page_range
    total = len(page_list)
    return JsonResponse({'total': total})

def cart_add_ajax(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return JsonResponse({'name':product.name, 'id':product.id, 'price':product.price}, safe=False)

def item_clear_ajax(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    quantity = request.session[CART_SESSION_ID][str(product.id)]['quantity']
    total = 0
    for value in request.session[CART_SESSION_ID]:
        total = total + float(request.session[CART_SESSION_ID][value]['price']) * float(
            request.session[CART_SESSION_ID][value]['quantity'])
    cart.remove(product)
    return JsonResponse({'name':product.name, 'id':product.id, 'price':product.price, 'quantity':quantity}, safe=False)


def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")

def cart_decrement_ajax(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return JsonResponse({'name':product.name, 'id':product.id, 'price':product.price}, safe=False)

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

def cart_clear_ajax(request):
    cart = Cart(request)
    cart.clear()
    return JsonResponse({'status':"OK"}, safe=False)

#detalles
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



def iptoint(ip):
    h = list(map(int, ip.split(".")))
    return (h[0] << 24) + (h[1] << 16) + (h[2] << 8) + (h[3] << 0)

def iscuba(ip):
    conn = sqlite3.connect(GEOLOC_DATABASE)
    cursor_ship = conn.cursor()
    cursor_ship.execute("select * from cuba")
    rows = cursor_ship.fetchall()
    for row in rows:
        if (iptoint(ip) >= iptoint(str(row[0])) and iptoint(ip) <= iptoint(str(row[1]))):
            return True
    return False

def producto_detail(request, producto_id):
    if not request.session.get(CART_SESSION_ID):
        request.session[CART_SESSION_ID] = {}
    total = 0
    for value in request.session[CART_SESSION_ID]:
        total = total + float(request.session[CART_SESSION_ID][value]['price'])*float(request.session[CART_SESSION_ID][value]['quantity'])
    cfg = Configuracion.objects.all()[0]
    mueble = Product.objects.get(pk=producto_id)
    mueble.visitas = mueble.visitas + 1
    mueble.save()
    mas_visitado = Product.objects.filter(tipo='Producto', visible=True)[0]
    mas_comprado = Product.objects.filter(tipo='Producto', visible=True)[0]
    for item in Product.objects.filter(tipo='Producto', visible=True):
        if mas_visitado.visitas < item.visitas:
            mas_visitado = item
        if mas_comprado.compras < item.compras:
            mas_comprado = item
    flag1 = False
    flag2 = False
    if mas_visitado.id == mueble.id:
        flag1 = True
    if mas_comprado.id == mueble.id:
        flag2 = True
    return render(request, 'producto_detail.html', {'cfg':cfg, 'producto':mueble, 'mas_visitado':flag1, 'mas_comprado':flag2,
                                                    'total':total})

def servicio_detail(request, producto_id):
    if not request.session.get(CART_SESSION_ID):
        request.session[CART_SESSION_ID] = {}
    total = 0
    for value in request.session[CART_SESSION_ID]:
        total = total + float(request.session[CART_SESSION_ID][value]['price'])*float(request.session[CART_SESSION_ID][value]['quantity'])
    cfg = Configuracion.objects.all()[0]
    mueble = Product.objects.get(pk=producto_id)
    mueble.visitas = mueble.visitas + 1
    mueble.save()
    mas_visitado = Product.objects.filter(tipo='Servicio', visible=True)[0]
    mas_comprado = Product.objects.filter(tipo='Servicio', visible=True)[0]
    for item in Product.objects.filter(tipo='Servicio', visible=True):
        if mas_visitado.visitas < item.visitas:
            mas_visitado = item
        if mas_comprado.compras < item.compras:
            mas_comprado = item
    flag1 = False
    flag2 = False
    if mas_visitado.id == mueble.id:
        flag1 = True
    if mas_comprado.id == mueble.id:
        flag2 = True
    return render(request, 'producto_detail.html', {'cfg':cfg, 'producto':mueble, 'mas_visitado':flag1, 'mas_comprado':flag2,
                                                    'total':total})

def blog_detail(request, historia_id):
    if not request.session.get(CART_SESSION_ID):
        request.session[CART_SESSION_ID] = {}
    total = 0
    for value in request.session[CART_SESSION_ID]:
        total = total + float(request.session[CART_SESSION_ID][value]['price'])*float(request.session[CART_SESSION_ID][value]['quantity'])
    cfg = Configuracion.objects.all()[0]
    mueble = Historia.objects.get(pk=historia_id)
    return render(request, 'blog_detail.html', {'cfg':cfg, 'historia':mueble, 'total':total})

def contacto(request):
    coordenadas = Mapa.objects.all()[0].coordenadas
    if not request.session.get(CART_SESSION_ID):
        request.session[CART_SESSION_ID] = {}
    total = 0
    for value in request.session[CART_SESSION_ID]:
        total = total + float(request.session[CART_SESSION_ID][value]['price'])*float(request.session[CART_SESSION_ID][value]['quantity'])
    cfg = Configuracion.objects.all()[0]
    form = ReservacionForm()
    if request.method == 'POST':
        form = ReservacionForm(request.POST)
        json_msg = ""
        if form.is_valid():
            aux = []
            havana = timezone('America/Havana')
            fmt = '%Y-%m-%d %H:%M:%S'
            loc_dt = datetime.now(pytz.timezone('America/Havana'))
            for destinatario in Destinatario.objects.all():
                aux.append(destinatario.email)
            if len(aux) == 0:
                aux.append('lmdelbahia@gmail.com')
            mensaje = 'Contrátanos: ' + mark_safe('<br/>')
            mensaje = mensaje + 'Nombre: ' + form.cleaned_data['nombre'] + mark_safe('<br/>')
            mensaje = mensaje + 'Teléfono: ' + form.cleaned_data['telefono'] + mark_safe('<br/>')
            mensaje = mensaje + form.cleaned_data['asunto'] + mark_safe('<br/>')
            mensaje = mensaje + form.cleaned_data['mensaje']
            json_msg = form.cleaned_data['mensaje']
            email = EmailMessage(subject='Contacto', body=mensaje, from_email=form.cleaned_data['telefono'], to=aux,
                                 bcc=None, connection=None
                                 , attachments=None, headers=None, cc=None, reply_to=None)
            email.content_subtype = 'html'
            email.send()
            contacto = Reservacion()
            contacto.nombre = form.cleaned_data['nombre']
            contacto.asunto = form.cleaned_data['asunto']
            contacto.telefono = form.cleaned_data['telefono']
            contacto.mensaje = form.cleaned_data['mensaje']
            contacto.save()
            timestamp = loc_dt.replace(tzinfo=havana).timestamp()
            ruta = open(Path(ConfiguracionGodlango.objects.all()[0].has_previo + '/' + contacto.nombre + '_' + str(
                timestamp) + '.json.tmp'), "w+")
            ruta.write('{"name":"')
            ruta.write(form.cleaned_data['nombre'])
            ruta.write('","tel":"')
            ruta.write(form.cleaned_data['telefono'])
            ruta.write('","addr":"')
            ruta.write('","msg":"')
            for caracter in json_msg:
                ruta.write(caracter)
            ruta.write('","date":"')
            ruta.write(str(loc_dt))
            ruta.write('"}')
            ruta.close()
            os.rename(Path(ConfiguracionGodlango.objects.all()[0].has_previo + '/' + contacto.nombre + '_' + str(
                timestamp) + '.json.tmp'), Path(
                ConfiguracionGodlango.objects.all()[0].has_previo + '/' + contacto.nombre + '_' + str(
                    timestamp) + '.json'))
            return redirect('/')
        else:
            form = ReservacionForm(request.POST)
    return render(request, 'contact.html', {'cfg':cfg, 'form':form, 'total':total, 'coordenadas':coordenadas})

def cart_detail(request):
    flag_paypal = iscuba(get_client_ip(request))
    if not request.session.get(CART_SESSION_ID):
        request.session[CART_SESSION_ID] = {}
    form = CuentaForm()
    cfg = Configuracion.objects.all()[0]
    total = 0
    for value in request.session[CART_SESSION_ID]:
        total = total + float(request.session[CART_SESSION_ID][value]['price'])*float(request.session[CART_SESSION_ID][value]['quantity'])
    return render(request, 'cart_detail.html',{'cfg':cfg,'total':int(total),'form':form, 'flag_paypal':flag_paypal})

def paypal_ipn(request):
    loc_dt = datetime.now(pytz.timezone('America/Havana'))
    havana = timezone('America/Havana')
    total = 0
    form = CuentaForm()
    for value in request.session[CART_SESSION_ID]:
        total = total + float(request.session[CART_SESSION_ID][value]['price']) * float(
            request.session[CART_SESSION_ID][value]['quantity'])
    cfg = Configuracion.objects.all()[0]
    json_msg = ""
    aux = []
    for destinatario in Destinatario.objects.all():
        aux.append(destinatario.email)
    if len(aux) == 0:
        aux.append('lmdelbahia@gmail.com')
    mensaje = 'Pedido: ' + mark_safe('<br/>')
    mensaje = mensaje + 'Nombre: ' + request.POST['parametro1'] + mark_safe(' <br/> ')
    mensaje = mensaje + 'Teléfono: ' + request.POST['parametro2'] + mark_safe(' <br/> ')
    mensaje = mensaje + 'Dirección: ' + request.POST['parametro3'] + mark_safe(' <br/> ')
    for value in request.session[CART_SESSION_ID]:
        precio = request.session[CART_SESSION_ID][value]['quantity'] * float(
            request.session[CART_SESSION_ID][value]['price'])
        json_msg = json_msg + '• ' + str(request.session[CART_SESSION_ID][value]['quantity']) + 'x ' + \
                   request.session[CART_SESSION_ID][value]['name'] + ': $' + str(precio) + '\n'
        mensaje = mensaje + '• ' + str(request.session[CART_SESSION_ID][value]['quantity']) + 'x ' + \
                  request.session[CART_SESSION_ID][value]['name'] + ': $' + str(precio) + mark_safe(' <br/> ')
    mensaje = mensaje + 'Total: ' + str(total)
    json_msg = json_msg + 'Total: ' + str(total)
    email = EmailMessage(subject='Pedido', body=mensaje, from_email=request.POST['parametro2'], to=aux,
                         bcc=None, connection=None
                         , attachments=None, headers=None, cc=None, reply_to=None)
    email.content_subtype = 'html'
    email.send()
    contacto = Pedido()
    contacto.nombre = request.POST['parametro1']
    contacto.telefono = request.POST['parametro2']
    if request.POST['parametro4']:
        contacto.telefono2 = request.POST['parametro4']
    contacto.direccion = request.POST['parametro3']
    contacto.contenido = mensaje.replace(' <br/> ', '\n')
    contacto.contenido = contacto.contenido.replace('<br/>', '\n')
    if request.POST['parametro4']:
        contacto.contenido = contacto.contenido + '\n' +  'Teléfono del comprador: ' +request.POST['parametro4']
    contacto.save()
    timestamp = loc_dt.replace(tzinfo=havana).timestamp()
    ruta = open(Path(ConfiguracionGodlango.objects.all()[0].has_previo + '/' + contacto.nombre + '_' + str(
        timestamp) + '.json.tmp'), "w+")
    ruta.write('{"name":"')
    ruta.write(cfg.nombre)
    ruta.write(' - ')
    ruta.write(request.POST['parametro1'])
    ruta.write('","tel":"')
    ruta.write(request.POST['parametro4'])
    ruta.write('","addr":"')
    ruta.write(request.POST['parametro3'])
    ruta.write('","msg":"')
    for caracter in json_msg:
        ruta.write(caracter)
    ruta.write('","date":"')
    ruta.write(str(loc_dt))
    ruta.write('"}')
    ruta.close()
    os.rename(Path(ConfiguracionGodlango.objects.all()[0].has_previo + '/' + contacto.nombre + '_' + str(
        timestamp) + '.json.tmp'), Path(
        ConfiguracionGodlango.objects.all()[0].has_previo + '/' + contacto.nombre + '_' + str(timestamp) + '.json'))
    cart_clear(request)
    return redirect('index')

