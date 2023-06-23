import sqlite3


class Ley:
    def __init__(self, Nro_Registro, Tipo_Normativa, Nro_Normativa, Fecha, Descripcion, Categoria, Jurisdiccion, Organo_Legislativo, Palabras_Clave):
        self.Nro_Registro = Nro_Registro
        self.Tipo_Normativa = Tipo_Normativa
        self.Nro_Normativa = Nro_Normativa
        self.Fecha = Fecha
        self.Descripcion = Descripcion
        self.Categoria = Categoria
        self.Jurisdiccion = Jurisdiccion
        self.Organo_Legislativo = Organo_Legislativo
        self.Palabras_Clave = Palabras_Clave


class BaseDatos:
    def __init__(self):
        self.conexion = sqlite3.connect("ProyectoFinal2.0")
        self.cursor = self.conexion.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Leyes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Nro_Registro TEXT,
                Tipo_Normativa TEXT,
                Nro_Normativa INTEGER,
                Fecha TEXT,
                Descripcion TEXT,
                Categoria TEXT,
                Jurisdiccion TEXT,
                Organo_Legislativo TEXT,
                Palabras_Clave TEXT
            )"""
        )

    def crear_ley(self, ley):
        self.cursor.execute(
            """INSERT INTO Leyes (Nro_Registro, Tipo_Normativa, Nro_Normativa, Fecha, Descripcion, Categoria, Jurisdiccion, Organo_Legislativo, Palabras_Clave)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                ley.Nro_Registro,
                ley.Tipo_Normativa,
                ley.Nro_Normativa,
                ley.Fecha,
                ley.Descripcion,
                ley.Categoria,
                ley.Jurisdiccion,
                ley.Organo_Legislativo,
                ",".join(ley.Palabras_Clave),
            ),
        )

        self.conexion.commit()
        print("La ley se ha creado correctamente.")

    def leer_leyes(self):
        self.cursor.execute("SELECT * FROM Leyes")
        leyes = self.cursor.fetchall()
        for ley in leyes:
            print("ID:", ley[0])
            print("Número:", ley[1])
            print("Tipo de normativa:", ley[2])
            print("Número de normativa:", ley[3])
            print("Fecha:", ley[4])
            print("Descripción:", ley[5])
            print("Categoría:", ley[6])
            print("Jurisdicción:", ley[7])
            print("Órgano legislativo:", ley[8])
            print("Palabras clave:", ley[9])
            print()
    
        if not leyes:
            print("No hay Leyes registradas.")

    def actualizar_ley(self, id_ley, Nro_Registro, Tipo_Normativa, Nro_Normativa, Fecha, Descripcion, Categoria, Jurisdiccion, Organo_Legislativo, Palabras_Clave):
        self.cursor.execute(
            """UPDATE Leyes
            SET Nro_Registro = ?,
                Tipo_Normativa = ?,
                Nro_Normativa = ?,
                Fecha = ?,
                Descripcion = ?,
                Categoria = ?,
                Jurisdiccion = ?,
                Organo_Legislativo = ?,
                Palabras_Clave = ?
            WHERE id = ?""",
            (
                Nro_Registro,
                Tipo_Normativa,
                Nro_Normativa,
                Fecha,
                Descripcion,
                Categoria,
                Jurisdiccion,
                Organo_Legislativo,
                ",".join(Palabras_Clave),
                id_ley,
            ),
        )

        self.conexion.commit()
        print("La ley se ha actualizado correctamente.")

    def eliminar_ley(self, id_ley):
        self.cursor.execute("DELETE FROM Leyes WHERE id = ?", (id_ley,))
        self.conexion.commit()
        print("La ley se ha eliminado correctamente.")

    def consultar_ley(self, Nro_Normativa=None, Palabras_Clave=None):
        query = "SELECT * FROM Leyes WHERE "
        parameters = []

        if Nro_Normativa:
            query += "Nro_Normativa = ? "
            parameters.append(Nro_Normativa)

        if Palabras_Clave:
            if Nro_Normativa:
                query += "AND "
            query += "Palabras_Clave LIKE ?"
            parameters.append("%{}%".format(Palabras_Clave))

        self.cursor.execute(query, tuple(parameters))
        Leyes = self.cursor.fetchall()

        if Leyes:
            for ley in Leyes:
                print(ley)
        else:
            print("No se encontraron Leyes que coincidan con los criterios de búsqueda.")

    def cerrar_conexion(self):
        self.conexion.close()


def main():
    base_datos = BaseDatos()

    while True:
        print("\n=== ADMINISTRADOR DE Leyes ===")
        print("1. Crear Ley")
        print("2. Leer Leyes")
        print("3. Actualizar Ley")
        print("4. Eliminar Ley")
        print("5. Consultar Ley")
        print("6. Salir")

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            print("Ingrese los datos de la ley:")
            Nro_Registro = input("Número de registro: ")
            Tipo_Normativa = input("Tipo de normativa (Ley, Decreto, Resolución u Otro): ")
            Nro_Normativa = int(input("Número de normativa: "))
            Fecha = input("Fecha de publicación (DD/MM/AAAA): ")
            Descripcion = input("Descripción: ")
            Categoria = input("Categoría (Laboral, Penal, Civil, Comercial, Familia y sucesiones, Agrario y ambiental, Minería, Derecho informático u Otro): ")
            Jurisdiccion = input("Jurisdicción (Nacional, Provincial u Otro): ")
            Organo_Legislativo = input("Órgano legislativo (Congreso de la Nación, Legislación de Córdoba u Otro): ")
            Palabras_Clave = input("Palabras clave (separadas por comas): ").split(",")

            ley = Ley(
                Nro_Registro,
                Tipo_Normativa,
                Nro_Normativa,
                Fecha,
                Descripcion,
                Categoria,
                Jurisdiccion,
                Organo_Legislativo,
                Palabras_Clave,
            )

            base_datos.crear_ley(ley)

        elif opcion == "2":
            base_datos.leer_leyes()

        elif opcion == "3":
            print("Ingrese los nuevos datos de la ley:")
            id_ley = int(input("ID de la ley a actualizar: "))
            Nro_Registro = input("Número de ley: ")
            Tipo_Normativa = input("Tipo de normativa (Ley, Decreto, Resolución u Otro): ")
            Nro_Normativa = int(input("Número de normativa: "))
            Fecha = input("Fecha de publicación (DD/MM/AAAA): ")
            Descripcion = input("Descripción: ")
            Categoria = input("Categoría (Laboral, Penal, Civil, Comercial, Familia y sucesiones, Agrario y ambiental, Minería, Derecho informático u Otro): ")
            Jurisdiccion = input("Jurisdicción (Nacional, Provincial u Otro): ")
            Organo_Legislativo = input("Órgano legislativo (Congreso de la Nación, Legislación de Córdoba u Otro): ")
            Palabras_Clave = input("Palabras clave (separadas por comas): ").split(",")

            base_datos.actualizar_ley(
                id_ley,
                Nro_Registro,
                Tipo_Normativa,
                Nro_Normativa,
                Fecha,
                Descripcion,
                Categoria,
                Jurisdiccion,
                Organo_Legislativo,
                Palabras_Clave,
            )

        elif opcion == "4":
            id_ley = int(input("ID de la ley a eliminar: "))
            base_datos.eliminar_ley(id_ley)

        elif opcion == "5":
            print("Ingrese los criterios de búsqueda:")
            Nro_Normativa = input("Número de normativa (opcional): ")
            Palabras_Clave = input("Palabras clave (opcional): ")

            base_datos.consultar_ley(Nro_Normativa, Palabras_Clave)

        elif opcion == "6":
            base_datos.cerrar_conexion()
            break

        else:
            print("Opción inválida. Por favor, ingrese una opción válida.")


if __name__ == "__main__":
    main()
