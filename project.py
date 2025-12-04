import numpy as np

class Futbolista:
    def __init__(self, nombre, edad, posicion, precio, rendimiento_esperado, variacion):
        self.nombre = nombre
        self.edad = edad
        self.posicion = posicion
        self.precio = precio
        self.rendimiento_esperado = rendimiento_esperado
        self.variacion = variacion

    # Rendimiento generado con D. Normal
    def simular_rendimiento(self, cantidad=100):
        return np.random.normal(self.rendimiento_esperado, self.variacion, cantidad)


def calcular_rentabilidad(futbolista, cantidad=100):
    # Simulamos el rendimiento del jugador
    rendimientos = futbolista.simular_rendimiento(cantidad)
    # Promedio
    promedio = np.mean(rendimientos)
    # Calculamos el costo por unidad de rendimiento
    costo_por_unidad = futbolista.precio / promedio if promedio > 0 else float('inf')

    # Devolvemos los resultados en un diccionario
    return {
        'Nombre': futbolista.nombre,
        'Edad': futbolista.edad,
        'Posición': futbolista.posicion,
        'Precio': futbolista.precio,
        'Rendimiento Promedio': round(promedio, 2),
        'Costo por Unidad': round(costo_por_unidad, 2)
    }

def comparar_futbolistas(lista_futbolistas):
    # Evaluamos la rentabilidad de cada futbolista
    resultados = [calcular_rentabilidad(f) for f in lista_futbolistas]

    # Ordenamos por costo por unidad (más rentable primero)
    resultados.sort(key=lambda x: x['Costo por Unidad'])
    return resultados

def mostrar_tabla(resultados):
    print("\nComparativa de jugadores según el costo/unidad\n")
    print(f"{'Nombre':<12}{'Edad':<6}{'Posición':<10}{'Precio':<12}{'Rendimiento':<18}{'Costo/Unidad':<15}")
    print("-" * 80)
    for r in resultados:
        print(f"{r['Nombre']:<12}{r['Edad']:<6}{r['Posición']:<10}{r['Precio']:<12.0f}{r['Rendimiento Promedio']:<18.2f}{r['Costo por Unidad']:<15.2f}")

# Main
if __name__ == "__main__":
    futbolistas = [
        Futbolista("Carlos", 24, "Delantero", 12000000, 18, 4),
        Futbolista("Luis", 27, "Portero", 9000000, 14, 3),
        Futbolista("Raúl", 22, "Defensa", 6000000, 8, 2)
    ]

    resultados = comparar_futbolistas(futbolistas)
    mostrar_tabla(resultados)
