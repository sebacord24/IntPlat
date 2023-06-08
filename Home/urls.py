from django.urls import path
from .views import *



urlpatterns = [
    path('', HomeView, name='home'),
    path('admin/', admin, name='admin'),
    path('product/', product, name='product'),
    path('mantencion/', listar_mantenciones, name='mantencion'),
    path('mantencion/agregar_mantenimiento/', agregar_mantenimiento, name='agregar_mantenimiento'),
    path('reparacion/', reparacion, name='reparacion'),
    path('filtro_libros_nombre/', filtro_libros_nombre, name='filtro_libros_nombre'),
    path('autenticar_usuario/', autenticar_usuario, name='autenticar_usuario'),
    path('login/autenticar_usuario/', autenticar_usuario, name='autenticar_usuario'),
    path('login/', Login, name='login'),
    path('clientes_form/', clientes_form, name='clientes_form'),
    path('agregar_cliente/', agregar_cliente, name='agregar_cliente'),
    path('agregar_libro/<int:id_libro>/', agregar_libro, name='agregar_libro'),
    path('limpiar_carrito/', limpiar_carrito, name='limpiar_carrito'),
    path('carrito/', carrito, name='carrito'),
    path('pago/', pago, name='pago'),
    path('confirmacion_compra', confirmacion_compra, name='confirmacion_compra'),
]




