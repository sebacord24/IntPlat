# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Administrador(models.Model):
    id_admin = models.FloatField(primary_key=True)
    rut = models.CharField(max_length=12)
    pr_nombre = models.CharField(max_length=30)
    seg_nombre = models.CharField(max_length=30)
    ap_paterno = models.CharField(max_length=30)
    ap_materno = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    fec_nac = models.CharField(max_length=30)
    sucursal_id_sucursal = models.ForeignKey('Sucursal', models.DO_NOTHING, db_column='sucursal_id_sucursal')

    class Meta:
        managed = False
        db_table = 'administrador'


class Bodega(models.Model):
    id_bodega = models.IntegerField(primary_key=True)
    direccion = models.CharField(max_length=50)
    sucursal_id_sucursal = models.OneToOneField('Sucursal', models.DO_NOTHING, db_column='sucursal_id_sucursal')

    class Meta:
        managed = False
        db_table = 'bodega'


class Cliente(models.Model):
    id_cliente = models.FloatField(primary_key=True)
    direccion = models.CharField(max_length=255)
    rut = models.CharField(max_length=12)
    pr_nombre = models.CharField(max_length=30)
    seg_nombre = models.CharField(max_length=30)
    ap_paterno = models.CharField(max_length=30)
    ap_materno = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    fec_nac = models.CharField(max_length=30)
    celular = models.CharField(max_length=50, blank=True, null=True)
    pass_field = models.CharField(db_column='pass', max_length=100)  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'cliente'


class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    total_productos = models.IntegerField()
    total_pago = models.IntegerField()
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)
    estado = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'compra'


class Libro(models.Model):
    id_libro = models.IntegerField(primary_key=True)
    nombre_libro = models.CharField(max_length=50)
    stock = models.IntegerField()
    precio = models.IntegerField()
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    bodega_id_bodega = models.ForeignKey(Bodega, models.DO_NOTHING, db_column='bodega_id_bodega')
    tipo_libro = models.CharField(max_length=30, blank=True, null=True)
    autor = models.CharField(max_length=30, blank=True, null=True)
    img = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'libro'


class Mantencion(models.Model):
    id_mantencion = models.IntegerField(primary_key=True)
    fec_mantencion = models.DateField()

    class Meta:
        managed = False
        db_table = 'mantencion'


class Pago(models.Model):
    id_pago = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=255)
    fec_transaccion = models.DateField()

    class Meta:
        managed = False
        db_table = 'pago'


class Sucursal(models.Model):
    id_sucursal = models.IntegerField(primary_key=True)
    nombre_sucursal = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'sucursal'


class Tecnico(models.Model):
    id_tecnico = models.IntegerField(primary_key=True)
    rut = models.CharField(max_length=12)
    pr_nombre = models.CharField(max_length=30)
    seg_nombre = models.CharField(max_length=30)
    ap_paterno = models.CharField(max_length=30)
    ap_materno = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    fec_nac = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tecnico'

class Carrito(models.Model):
    id_carrito = models.IntegerField(primary_key=True)
    libro = models.ForeignKey(Libro, models.CASCADE)
    cantidad = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total = self.libro.precio * self.cantidad
        super(Carrito, self).save(*args, **kwargs)
    
    class Meta:
        db_table = 'carrito'
