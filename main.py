class Producto:
    def __init__(self, nombre, precio, stock):
        self.Nombre = nombre
        self.Precio = precio
        self.Stock = stock
        
    def mostrarProducto(self):
        print(f"Nombre: {self.Nombre}, Precio: {self.Precio}, Stock: {self.Stock}.")
        
    def devolverPrecio(self):
        print(f"{self.Precio}€")
        
    def actualizarStock(self, nuevoStock):
        self.Stock += nuevoStock
        return self.Stock
        
    def hayDisponible(self, cantidad):
        if cantidad > self.Stock:
            return False
        else:
            return True   
        
    
class Cliente:
    def __init__(self, nombre):
        self.Nombre = nombre
        self.Carrito = list()
        self.TicketsCompra = dict()
        self.MembresiaVIP = False
        self.NumeroTicket = 1
        
    def agregarProducto(self, producto, cantidad):
        if producto.hayDisponible(cantidad) == True:
            self.Carrito.append((producto, cantidad))
            print("Producto añadido al carrito.")
        else:
            print("No hay suficiente stock del producto.")


    def mostrarCarrito(self):
        if len(self.Carrito) == 0:
            print("El carrito está vacío.")
        else:
            for tupla in self.Carrito:
                print(f"Nombre del producto: {tupla[0].Nombre}, Cantidad de producto: {tupla[1]}")
        
    def calcularTotalCarro(self):
        costoTotal = 0
        for tupla in self.Carrito:
            precioProducto = tupla[0].Precio
            costoTotal += (tupla[1] * precioProducto)
        return costoTotal
            
    def vaciarCarrito(self):
        self.Carrito = list()
        
    def comprar(self):
        self.TicketsCompra[f"Ticket {self.NumeroTicket}."] = self.Carrito
        self.NumeroTicket += 1

        for tupla in self.Carrito:
            tupla[0].Stock -= tupla[1]

    
        print("Compra realizada. Aquí está tu ticket:\n")
        print(f"Ticket {self.NumeroTicket - 1}:")
        for producto, cantidad in self.Carrito:
            print(f"- {producto.Nombre}: {cantidad} unidades a {producto.Precio}€ cada una.")
        print(f"Total: {self.calcularTotalCarro()}€\n")

        self.vaciarCarrito()
        
        
    def darseAltaBajaVIP(self):
        if self.MembresiaVIP == True:
            self.MembresiaVIP = False
        else:
            self.MembresiaVIP = True
        
    def totalGastado(self):
        totalGastado = 0
        for ticket in self.TicketsCompra:
            for tupla in self.TicketsCompra[ticket]:
                totalGastado += tupla[0].Precio * tupla[1]
        return totalGastado
        
    def mostrarCliente(self):
        if self.MembresiaVIP == True:
            esVIP = "Si"
        else:
            esVIP = "No"
        print(f"Nombre: {self.Nombre}, Cliente VIP: {esVIP}, Dinero total gastado: {self.totalGastado()}")        



class Tienda:
    def __init__(self, nombre):
        self.Nombre = nombre
        self.Clientes = list()
        self.Productos = list()

    def agregarCliente(self, cliente):
        self.Clientes.append(cliente)
        print("El cliente se ha registrado en la tienda.")

    def agregarProducto(self, producto):
        self.Productos.append(producto)
        print("El producto se ha registrado en la tienda.")
        
    def mostrarClientes(self):
        for cliente in self.Clientes:
            cliente.mostrarCliente()          

    def buscarCliente(self, nomCliente):
        for cliente in self.Clientes:
            if cliente.Nombre.lower() == nomCliente.lower():
                return cliente
        return False

    def buscarProducto(self, nomProducto):
        for producto in self.Productos:
            if producto.Nombre.lower() == nomProducto.lower():
                return producto
        return False
    
    def clienteTop(self):
        if not self.Clientes:
            print("No hay clientes registrados en la tienda.")
            return False

        clienteMaximo = max(self.Clientes, key=lambda c: c.totalGastado(), default=None)

        if clienteMaximo and clienteMaximo.totalGastado() > 0:
            print(f"El cliente top es {clienteMaximo.Nombre} con un gasto total de {clienteMaximo.totalGastado()}€.")
        else:
            print("Ningún cliente ha realizado compras todavía.")
            return False

           
    def procesarCompra(self, nomCliente):
        for cliente in self.Clientes:
            if cliente.Nombre == nomCliente:
                cliente.comprar()

                
    def mostrarProductos(self):
        listaTuplas = []
        for producto in self.Productos:
            listaTuplas.append((producto.Nombre, producto.Precio, producto.Stock))
        print(listaTuplas)


#FUNCIÓN MOSTRAR MENÚ
# Función que imprime el menú y sera llamada por main donde, depende del número introducido, llama a una función o a otra. 

def mostrarMenu():
    print("""
        TIENDA GAME
        
1. Registrar producto
2. Registrar cliente
3. Agregar producto al carrito de un cliente
4. Mostrar el carrito de un cliente
5. Mostrar informacion de la tienda
6. Procesar compra de un cliente
7. Modificar informar de un cliente
8. Salir
          """)
    
def registrarProducto(tienda):
    nombreUsu = input("Introduce el nombre del producto a registrar: ")
       
    if tienda.buscarProducto(nombreUsu) == False:
        precioUsu = float(input("Introduce el precio del producto a registrar: "))
        stockUsu = int(input("Introduce el stock inicial del producto a registrar: "))

        tienda.agregarProducto(Producto(nombreUsu, precioUsu, stockUsu))

    else:
        print("El producto ya se encuentra registrado en la tienda.")


def registrarCliente(tienda):
    respuestas = ["s", "n"]
    nombreUsu = input("Introduce el nombre del cliente a registrar: ")
    

    if tienda.buscarCliente(nombreUsu) == False:
        VIPUsu = input("Quieres darte de alta como cliente VIP?(s/n): ").lower()
        while VIPUsu not in respuestas:
            VIPUsu = input("ERROR - Introduce una opción correcta(s/n): ").lower()
        if VIPUsu == "s":
            print("El cliente será VIP.")
            tienda.agregarCliente(Cliente(nombreUsu))
            cliente = tienda.buscarCliente(nombreUsu)
            cliente.darseAltaBajaVIP()
        else:
            print("El cliente no será VIP.")
            tienda.agregarCliente(Cliente(nombreUsu))
    else: 
        print("El cliente ya se encuentra registrado en la tienda.")

        

def agregarProductoCarritoCliente(tienda):
    productoUsu = input("Introduce el nombre del producto a agregar al carrito: ")
    if tienda.buscarProducto(productoUsu) == False:
        print("El producto no se encuentra registrado en la tienda.")
    else:
        clienteUsu = input("Introduce el nombre del cliente del carrito: ")
        if tienda.buscarCliente(clienteUsu) == False:
            print("El cliente no se encuentra registrado en la tienda.")
        else:
            producto = tienda.buscarProducto(productoUsu)
            cliente = tienda.buscarCliente(clienteUsu)
            cliente.agregarProducto(producto, 1)

def mostrarCarritoCliente(tienda):
    clienteUsu = input("Introduce el nombre del cliente del que quieres mostrar su carrito: ")

    if tienda.buscarCliente(clienteUsu) == False:
        print("El cliente no se encuentra registrado en la tienda.")
    else:
        cliente = tienda.buscarCliente(clienteUsu)
        cliente.mostrarCarrito()

def mostrarInformacionTienda(tienda):
    tienda.mostrarProductos()
    print("Clientes: ")
    tienda.mostrarClientes()
    tienda.clienteTop()


def procesarCompraCliente(tienda):
    clienteUsu = input("Introduce el nombre del cliente del que quieres procesar la compra: ")
    if tienda.buscarCliente(clienteUsu) == False:
        print("El cliente no se encuentra registrado en la tienda.")
    else:
        tienda.procesarCompra(clienteUsu)

def modificarInformacionCliente(tienda):
    respuestas = ["s", "n"]
    clienteUsu = input("Introduce el nombre del cliente que quieres modificar:")
    if tienda.buscarCliente(clienteUsu) == False:
        print("El cliente no se encuentra registrado en la tienda.")
    else:
        preguntaNombre = input("Deseas cambiar el nombre del cliente?(s/n): ").lower()
        while preguntaNombre not in respuestas:
            preguntaNombre = input("ERROR - Introduce una respuesta correcta(s/n): ").lower()
        if preguntaNombre == "s":
            nuevoNombre = input("Introduce el nuevo nombre: ")
            for cliente in tienda.Clientes:
                if cliente.Nombre == clienteUsu:
                    cliente.Nombre = nuevoNombre
            print(f"Se ha modificado el nombre.\nCliente: {cliente.Nombre}")
        else:
            print("No se ha modificado el nombre.")

        preguntaVIP = input("Desea cambiar el estado de la membresía VIP?(s/n): ").lower()
        while preguntaVIP not in respuestas:
            preguntaVIP = input("ERROR - Introduce una respuesta correcta(s/n): ").lower()
        if preguntaVIP == "s": 
            for cliente in tienda.Clientes:
                if cliente.Nombre == clienteUsu:
                    cliente.darseAltaBajaVIP()
            print(f"Se ha modificado el estado de la membresía VIP.\nCliente: {cliente.Nombre}")
        else:
            print("No se ha modificado el estado de la membresía VIP.")


    

def menu(tienda):
    while True:
        mostrarMenu()
        opcionUsu = int(input("Introduce una opcion(1-8): "))
        while opcionUsu not in range(1,9):
            opcionUsu = int(input("ERROR - Introduce una opcion correcta(1-8): "))

        match opcionUsu:
            case 1:
                registrarProducto(tienda)
            case 2:
                registrarCliente(tienda)
            case 3:
                agregarProductoCarritoCliente(tienda)
            case 4:
                mostrarCarritoCliente(tienda)
            case 5:
                mostrarInformacionTienda(tienda)
            case 6:
                procesarCompraCliente(tienda)
            case 7:
                modificarInformacionCliente(tienda)
            case 8:
                break

tienda1 = Tienda("GAME")

menu(tienda1)