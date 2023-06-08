class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    def agregar (self, libro):
        id = str(libro.id_libro)
        if id not in self.carrito.keys():
            self.carrito[id] = {
                "libro_id": libro.id_libro,
                "nombre_libro": libro.nombre_libro,
                "precio": libro.precio,
                "cantidad": 1,
                "total": libro.precio,
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["precio"]
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    
    def limpiar_carrito(self):
        self.session["carrito"] = {}
        self.session.modified = True


    def calcular_total(self):
        total = 0
        for item in self.carrito.values():
            subtotal = item['precio'] * item['cantidad']
            total += subtotal
        return total

    def cantidad_total(self):
        cantidad = 0
        for item in self.carrito.values():
            cantidad += item['cantidad']
        return cantidad