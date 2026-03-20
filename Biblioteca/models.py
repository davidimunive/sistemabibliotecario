from datetime import date

class Material:
    def __init__(self, idMaterial: int, titulo: str, anioPublicacion: int):
        self.idMaterial = idMaterial
        self.titulo = titulo
        self.anioPublicacion = anioPublicacion
        self.disponible = True

    def mostrar_info(self):
        estado = "Disponible" if self.disponible else "No disponible"
        print(f"[{self.idMaterial}] {self.titulo} ({self.anioPublicacion}) - {estado}")


class Libro(Material):
    def __init__(self, idMaterial, titulo, anioPublicacion, autor, isbn, genero):
        super().__init__(idMaterial, titulo, anioPublicacion)
        self.autor = autor
        self.isbn = isbn
        self.genero = genero

    def mostrar_info(self):
        super().mostrar_info()
        print(f" El autor es {self.autor}, su ISBN es {self.isbn} y el genero es {self.genero}")


class Revista(Material):
    def __init__(self, idMaterial, titulo, anioPublicacion, edicion, periodicidad):
        super().__init__(idMaterial, titulo, anioPublicacion)
        self.edicion = edicion
        self.periodicidad = periodicidad

    def mostrar_info(self):
        super().mostrar_info()
        print(f" Es la edicion {self.edicion} y su periodicidad es {self.periodicidad}")


class MaterialDigital(Material):
    def __init__(self, idMaterial, titulo, anioPublicacion, tipoArchivo, urlDescarga, tamanoMB):
        super().__init__(idMaterial, titulo, anioPublicacion)
        self.tipoArchivo = tipoArchivo
        self.urlDescarga = urlDescarga
        self.tamanoMB = tamanoMB

    def mostrar_info(self):
        super().mostrar_info()
        print(f" El tipo de Archivo es {self.tipoArchivo}, pesa {self.tamanoMB} MB y se descarga en {self.urlDescarga}")


class Persona:
    def __init__(self, nombre: str, idPersona: int):
        self.nombre = nombre
        self.idPersona = idPersona

    def mostrar_info(self):
        print(f"Persona: {self.nombre} (ID: {self.idPersona})")


class Usuario(Persona):
    def __init__(self, nombre, idPersona, limitePrestamos: int = 3):
        super().__init__(nombre, idPersona)
        self.limitePrestamos = limitePrestamos
        self.listaActiva = []
        self.bloqueado = False

    def mostrar_info(self):
        print(f"El usuario {self.nombre} tiene {len(self.listaActiva)} préstamos activos de {self.limitePrestamos} y está bloqueado: {self.bloqueado}")


class Bibliotecario(Persona):
    def __init__(self, nombre, idPersona):
        super().__init__(nombre, idPersona)

    def gestionar_prestamo(self, prestamo):
        print(f"Bibliotecario {self.nombre} gestionando préstamo ID {prestamo.idPrestamo}.")

    def transferir_material(self, material, sucursal_destino):
        sucursal_destino.catalogo_local.append(material)
        print(f"Material '{material.titulo}' agregado a sucursal '{sucursal_destino.nombre}'.")

class Penalizacion:
    def __init__(self, motivo: str):
        self.monto = 0.0
        self.motivo = motivo
        self.pagada = False

    def calcular_multa(self, dias_retraso: int):
        self.monto = dias_retraso * 5.0
        print(f"Multa calculada: ${self.monto:.2f} por {dias_retraso} días de retraso.")

    def bloquear_usuario(self, usuario):
        usuario.bloqueado = True
        print(f"Usuario '{usuario.nombre}' bloqueado por: {self.motivo}.")


class Prestamo:
    def __init__(self, idPrestamo, usuario, material, fechaInicio, fechaDevolucion):
        self.idPrestamo = idPrestamo
        self.usuario = usuario
        self.material = material
        self.fechaInicio = fechaInicio
        self.fechaDevolucion = fechaDevolucion
        self.penalizacion = None

        usuario.listaActiva.append(self)
        material.disponible = False

    def devolver(self, dias_retraso):
        self.material.disponible = True
        self.usuario.listaActiva.remove(self)

        if dias_retraso > 0:
            self.penalizacion = Penalizacion("Devolucion tardía")
            self.penalizacion.calcular_multa(dias_retraso)

            if dias_retraso > 7:
                self.penalizacion.bloquear_usuario(self.usuario)
        else:
            print(f"Material '{self.material.titulo}' devuelto a tiempo. Sin penalización.")

    def mostrar_info(self):
        print(f"El préstamo {self.idPrestamo} es del usuario {self.usuario.nombre} y el material es {self.material.titulo}")
        print(f"Inició el {self.fechaInicio} y debe devolverse el {self.fechaDevolucion}")

class Sucursal:
    def __init__(self, idSucursal, nombre):
        self.idSucursal = idSucursal
        self.nombre = nombre
        self.catalogo_local = []

    def mostrar_catalogo(self):
        print(f"\n Catálogo de {self.nombre} ")
        for m in self.catalogo_local:
            m.mostrar_info()

class Catalogo:
    def __init__(self, sucursales):
        self.sucursales = sucursales

    def buscar_por_autor(self, autor):
        print(f"\nBuscando por autor: '{autor}'")
        encontrado = False
        for s in self.sucursales:
            for m in s.catalogo_local:
                if isinstance(m, Libro) and m.autor.lower() == autor.lower():
                    print(f"[{s.nombre}] ", end="")
                    m.mostrar_info()
                    encontrado = True

        if not encontrado:
            print(" No se encontraron resultados.")

    def buscar_en_todas_sucursales(self, titulo):
        print(f"\nBuscando '{titulo}' en todas las sucursales:")
        encontrado = False
        for s in self.sucursales:
            for m in s.catalogo_local:
                if titulo.lower() in m.titulo.lower():
                    print(f"[{s.nombre}] ", end="")
                    m.mostrar_info()
                    encontrado = True

        if not encontrado:
            print(" No se encontraron resultados.") 