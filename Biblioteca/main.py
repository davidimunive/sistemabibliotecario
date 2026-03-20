from models import *
from datetime import date, timedelta

def mostrar_menu():
    print("\n" + "="*40)
    print("SISTEMA BIBLIOTECA DIGITAL")
    print("="*40)
    print("1. Ver catálogo completo (por sucursal)")
    print("2. Buscar material por título")
    print("3. Buscar libros por autor")
    print("4. Realizar préstamo")
    print("5. Devolver material")
    print("6. Ver estado de usuario")
    print("0. Salir")
    return input("Seleccione una opción: ")

def inicializar_datos():
    s1 = Sucursal(1, "Sede Central")
    s2 = Sucursal(2, "Sede Norte")
    
    libros = [
    Libro(1, "Python for Data Analysis", 2017, "Wes McKinney", "978-1491957660", "Data Science"),
    Libro(2, "Clean Code", 2008, "Robert C. Martin", "978-0132350884", "Software Engineering"),
    Libro(3, "The Pragmatic Programmer", 1999, "David Thomas", "978-0201616224", "Software Engineering"),
    Libro(4, "Introduction to Algorithms", 2009, "Thomas H. Cormen", "978-0262033848", "Computer Science"),
    Libro(5, "Design Patterns", 1994, "Erich Gamma", "978-0201633610", "Software Engineering"),
    Libro(6, "Deep Learning", 2016, "Ian Goodfellow", "978-0262035613", "Artificial Intelligence"),
    Libro(7, "The Mythical Man-Month", 1975, "Frederick Brooks", "978-0201835953", "Software Engineering"),
    Libro(8, "Structure and Interpretation of Computer Programs", 1984, "Harold Abelson", "978-0262510875", "Computer Science"),
    Libro(9, "Python Crash Course", 2015, "Eric Matthes", "978-1593276034", "Programming"),
    Libro(10, "JavaScript: The Good Parts", 2008, "Douglas Crockford", "978-0596517748", "Web Development")
]

    revistas = [Revista(i+20, f"IEEE Software Vol {i}", 2024, i, "Mensual") for i in range(1, 11)]

    materiales_digitales = [
    MaterialDigital(41, "Dataset: Housing Prices", 2024, "CSV", "https://www.kaggle.com/datasets/housing-prices", 12.5),
    MaterialDigital(42, "Manual de Python básico", 2023, "PDF", "https://docs.python.org/3/tutorial/", 5.2),
    MaterialDigital(43, "Plantilla de presupuesto 2025", 2025, "Excel", "https://templates.office.com/presupuesto", 0.85),
    MaterialDigital(44, "Presentación de ventas Q1", 2024, "PowerPoint", "https://slideshare.net/ventas-q1-2024", 12.7),
    MaterialDigital(45, "Video tutorial programación", 2023, "MP4", "https://youtu.be/programacion-123", 156.0),
    MaterialDigital(46, "Ebook: Marketing digital", 2022, "EPUB", "https://archive.org/details/marketing-digital", 1.8),
    MaterialDigital(47, "Podcast: IA en negocios", 2025, "MP3", "https://spotify.com/episode/ia-negocios", 28.5),
    MaterialDigital(48, "Logo empresa vectorial", 2024, "PNG", "https://images.unsplash.com/logo-empresa", 0.45),
    MaterialDigital(49, "Documento API REST", 2023, "Word", "https://docs.google.com/document/api-rest", 2.3),
    MaterialDigital(50, "Curso diseño gráfico", 2024, "ZIP", "https://coursera.org/curso-diseno-grafico", 890.0)
]
    
    s1.catalogo_local = libros[:5] + revistas[:5] + materiales_digitales[:5]
    s2.catalogo_local = libros[5:] + revistas[5:] + materiales_digitales[5:]
    
    return [s1, s2], Usuario("David Isaac", 2026), Bibliotecario("Admin", 1), Catalogo([s1, s2])

def ejecutar():
    sucursales, usuario, biblio, catalogo = inicializar_datos()
    prestamos_globales = []

    while True:
        opc = mostrar_menu()
        
        if opc == "1":
            for s in sucursales:
                print(f"\n--- {s.nombre} ---")
                for m in s.catalogo_local:
                    m.mostrar_info()
        
        elif opc == "2":
            t = input("Ingrese título a buscar: ")
            res = catalogo.buscar_en_todas_sucursales(t)
            for s_nom, m in res:
                print(f"[{s_nom}] {m.mostrar_info()}")
        
        elif opc == "3":
            a = input("Ingrese autor: ")
            res = catalogo.buscar_por_autor(a)
            for s_nom, m in res:
                print(f"[{s_nom}] {m.mostrar_info()}")

        elif opc == "4":
            if usuario.bloqueado:
                print(" Usuario bloqueado por multas pendientes.")
                continue
            id_m = int(input("Ingrese ID del material a prestar: "))
            material_encontrado = None
            for s in sucursales:
                for m in s.catalogo_local:
                    if m.idMaterial == id_m and m.disponible:
                        material_encontrado = m
                        break
            
            if material_encontrado:
                p = Prestamo(len(prestamos_globales)+1, usuario, material_encontrado, date.today(), date.today() + timedelta(days=7))
                prestamos_globales.append(p)
                biblio.gestionar_prestamo(p)
                print(f"Prestamo exitoso: {material_encontrado.titulo}")
            else:
                print("Material no disponible o ID incorrecto.")

        elif opc == "5":
            if not usuario.listaActiva:
                print("No tienes préstamos activos.")
                continue
            print("Tus préstamos:")
            for i, p in enumerate(usuario.listaActiva):
                print(f"{i}. {p.material.titulo}")
            
            idx = int(input("Seleccione el índice a devolver: "))
            retraso = int(input("Días de retraso (0 para a tiempo): "))
            
            p_dev = usuario.listaActiva.pop(idx)
            p_dev.material.disponible = True
            
            if retraso > 0:
                pen = Penalizacion("Entrega tardía")
                multa = pen.calcular_multa(retraso)
                print(f" Penalización generada: ${multa}")
                if retraso > 5:
                    pen.bloquear_usuario(usuario)
                    print(" El usuario ha sido bloqueado.")
            else:
                print("Devolución exitosa sin cargos.")

        elif opc == "6":
            estado = "BLOQUEADO" if usuario.bloqueado else "ACTIVO"
            print(f"Usuario: {usuario.nombre} | ID: {usuario.idPersona} | Estado: {estado}")
            print(f"Préstamos actuales: {len(usuario.listaActiva)} / {usuario.limitePrestamos}")

        elif opc == "0":
            break

if __name__ == "__main__":
    ejecutar()