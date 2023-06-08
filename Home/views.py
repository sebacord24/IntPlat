from django.db import connection, connections
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import base64
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .models import *
from django.contrib.auth import authenticate, login
from Home.Carrito import Carrito

# Create your views here.

def HomeView(request):
    data = {
        'libros': listado_libros()
    }
    return render(request, 'Home/index.html', data) 

def Register(request):
    return render(request, 'Home/register.html')
def Login(request):
    return render(request, 'Home/login.html')

def admin(request):
    return render(request, 'Home/admin.html')

def clientes_form(request):
    return render(request, 'Home/clientes_form.html')



def product(request):
    return render(request, 'Home/product.html')

def mantencion(request):
    return render(request, 'Home/mantencion.html')

def reparacion(request):
    return render(request, 'Home/reparacion.html')


def listado_libros():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("listarlibros", [out_cur])

    lista = []
    for fila in out_cur:
        imagen = fila[8]
        if imagen is not None:
            imagen_data = str(base64.b64encode(imagen.read()), 'utf-8')
        else:
            imagen_data = None

        data = {
            'data': fila,
            'imagen': imagen_data
        }

        lista.append(data)

    return lista


def listado_libros_busqueda_nombre(busqueda):
    with connection.cursor() as cursor:
        cursor.callproc("listarlibros_busqueda_nombre", [busqueda])
        rows = cursor.fetchall()
        lista = [row[1] for row in rows] 
    return lista

def listado_libros_busqueda_categoria(busqueda):
    with connection.cursor() as cursor:
        cursor.callproc("listarlibros_busqueda_categoria", [busqueda])
        rows = cursor.fetchall()
        lista = [row[6] for row in rows] 
    return lista

def filtro_libros_nombre(request):
    busqueda = request.GET.get('busqueda', '') 
    libros = listado_libros_busqueda_nombre(busqueda)
    return render(request, 'Home/index.html', {'libros': libros})

def filtro_libros_categoria(request):
    busqueda = "TIPO_LIBRO"  
    lista = listado_libros_busqueda_categoria(busqueda)
    return render(request, 'lista_libros.html', {'libros': lista})




def agregar_mantenimiento(request):
    if request.method == 'POST':
        id_mantencion = request.POST['id_mantencion']
        fec_mantencion = request.POST['fec_mantencion']

        # Obtener una conexión a la base de datos Oracle
        with connection.cursor() as cursor:
            # Ejecutar el procedimiento almacenado
            cursor.callproc('AGREGAR_MANTENIMIENTO', [id_mantencion, fec_mantencion])

    # Redirigir a la vista ListarMante para obtener la lista actualizada de mantenciones
    return redirect('/mantencion/')

def listar_mantenciones(request):
    # Obtener la lista de mantenciones
    lista = obtener_lista_mantenciones()

    # Pasar la lista como contexto a la plantilla
    data = {
        'mantencion': lista
    }
    
    return render(request, 'Home/mantencion.html', data)

def obtener_lista_mantenciones():
    # Obtener la lista de mantenciones desde la base de datos
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_SERVICIOS_MANTENCION", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

def agregar_cliente(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        direccion = request.POST['direccion']
        rut = request.POST['rut']
        pr_nombre = request.POST['pr_nombre']
        seg_nombre = request.POST['seg_nombre']
        ap_paterno = request.POST['ap_paterno']
        ap_materno = request.POST['ap_materno']
        email = request.POST['email']
        fec_nac = request.POST['fec_nac']
        celular = request.POST['celular']
        password = request.POST['password']

        # Conectar a la base de datos Oracle y ejecutar el procedimiento almacenado
        with connection.cursor() as cursor:
            try:
                # Llamar al procedimiento almacenado
                cursor.callproc('sp_agregar_cliente', [
                    direccion, rut, pr_nombre, seg_nombre,
                    ap_paterno, ap_materno, email, fec_nac, celular, password
                ])
                messages.success(request, 'Cliente agregado exitosamente.')
                return redirect('agregar_cliente')
            except Exception as e:
                messages.error(request, 'Error al agregar el cliente. Por favor, inténtalo nuevamente.')
                print(str(e))

    # Renderizar el formulario de creación de cliente
    return render(request, 'Home/clientes_form.html')



def autenticar_usuario(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        password = request.POST.get('password')

        try:
            django_cursor = connection.cursor()
            cursor = django_cursor.connection.cursor()

            with connection.cursor() as cursor:
                # Ejecutar el procedimiento almacenado
                resultado = cursor.var(str)
                cursor.callproc('autenticar_usuario', [rut, password, resultado])

                # Obtener el resultado del procedimiento almacenado
                resultado = resultado.getvalue()

                if resultado == '1':
                    # Autenticación exitosa
                    user = authenticate(request, username=rut, password=password)
                    login(request, user)
                    messages.success(request, 'Inicio de sesión exitoso.')
                    return redirect('home')
                elif resultado == '0':
                    # Rut no registrado
                    messages.error(request, 'El rut no está registrado. Regístrate antes de iniciar sesión.')
                elif resultado == '-1':
                    # Error en el procedimiento
                    messages.error(request, 'Error al autenticar el usuario. Por favor, inténtalo nuevamente.')
        
        except Exception as e:
            # Error en el procedimiento almacenado
            messages.error(request, 'Error al autenticar el usuario. Por favor, inténtalo nuevamente.')

    return render(request, 'Home/login.html')


def agregar_libro(request, id_libro):
    libro = Libro.objects.get(id_libro=id_libro)
    carrito = Carrito(request)
    carrito.agregar(libro)
    return redirect("carrito")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar_carrito()
    return redirect("carrito")

def carrito(request):
    carrito = Carrito(request)
    total = carrito.calcular_total()
    total_paypal = str(total)

    context = {
        'carrito': carrito,
        'total': total,
        'total_paypal': total_paypal,
    }

    return render(request, 'Home/carrito.html', context)

def pago(request):
    carrito = Carrito(request)
    total = carrito.calcular_total()
    total_paypal = str(total)

    context = {
        'carrito': carrito,
        'total': total,
        'total_paypal': total_paypal,
    }
    return render(request, 'Home/paypal.html', context)

def confirmacion_compra(request):
    carrito = Carrito(request)
    id_compra = None  # Declarar el ID de la compra como None inicialmente

    # Obtener los productos del carrito
    total_productos = carrito.cantidad_total()
    total_pago = carrito.calcular_total()
    id_cliente = request.user.id
    estado = 'Comprado'  # Define el estado deseado de la compra

    try:
        # Crear una instancia de Compra
        compra = Compra(total_productos=total_productos, total_pago=total_pago, id_cliente_id=id_cliente, estado=estado)
        compra.save()

        # Limpiar el carrito
        carrito.limpiar_carrito()
        return redirect("carrito")

    except Exception as e:
        print(e)
        # Manejo del error al confirmar la compra
        messages.error(request, 'Error al confirmar la compra. Por favor, inténtalo nuevamente.')
        return redirect("carrito")