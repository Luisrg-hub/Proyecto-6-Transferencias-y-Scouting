"""Proyecto final: Simulación y evaluación de jugadores de fútbol usando SimPy."""
import random
import csv
import simpy
import matplotlib.pyplot as plt


def cargar_jugadores_desde_csv(ruta):
    jugadores = []
    with open(ruta, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            nombre = fila['Nombre']
            rol = fila['Rol']
            precio = int(fila['Precio'])
            jugadores.append(Jugador(nombre, rol, precio))
    return jugadores

# Clase con los datos del jugador y su simulación
class Jugador:
    def __init__(self, nombre, rol, precio):
        self.nombre = nombre
        self.rol = rol    # Defensa o Ataque
        self.precio = precio
        self.historial = []
    #Función que simula cada partido
    def simular_partido(self, env):
        """Simula un partido de fútbol para cada jugador."""
        while True:
            minutos_jugados = random.randint(45, 90)
            if self.rol == "Defensa":
                intentos = random.randint(10, 15)
                intentos_exitosos = random.randint(0, intentos)
                self.historial.append({
                    'minutos': minutos_jugados,
                    'defensas': intentos,
                    'defensas_exitosas': intentos_exitosos,
                    'ataques': 0,
                    'ataques_exitosos': 0
                })
            else: #Si el rol es Ataque
                intentos = random.randint(10, 15)
                intentos_exitosos = random.randint(0, intentos)
                self.historial.append({
                    'minutos': minutos_jugados,
                    'defensas': 0,
                    'defensas_exitosas': 0,
                    'ataques': intentos,
                    'ataques_exitosos': intentos_exitosos
                })
            yield env.timeout(1)  # Simula el paso del tiempo en el partido

#Simula los partidos a jugar por cada persona
def simular_partidos_jugadores(jugadores, num_partidos=10):
    """Simula varios partidos para una lista de jugadores."""
    env = simpy.Environment()
    procesos = []
    for jugador in jugadores:
        procesos.append(env.process(jugador.simular_partido(env)))
    env.run(until=num_partidos)
    return jugadores

def evaluar_jugador(jugador):
    total_minutos = sum(p['minutos'] for p in jugador.historial)
    if jugador.rol == "Defensa":
        total_intentos = sum(p['defensas'] for p in jugador.historial)
        total_exitos = sum(p['defensas_exitosas'] for p in jugador.historial)
    else:
        total_intentos = sum(p['ataques'] for p in jugador.historial)
        total_exitos = sum(p['ataques_exitosos'] for p in jugador.historial)

    efectividad = total_exitos / total_intentos if total_intentos > 0 else 0
    costo_por_efectividad = jugador.precio / efectividad if efectividad > 0 else float('inf')
    
    return {
        'Nombre': jugador.nombre,
        'Rol': jugador.rol,
        'Precio': jugador.precio,
        'Efectividad': round(efectividad, 2),
        'Minutos Jugados': total_minutos,
        'Costo/Efectividad': round(costo_por_efectividad, 2)
    }

def comparar_jugadores (jugadores):
    """Compara varios jugadores y devuelve una lista ordenada por costo"""
    evaluaciones = [evaluar_jugador(j) for j in jugadores]
    atacantes = sorted(
        [e for e in evaluaciones if e['Rol'] == 'Ataque'],
        key=lambda x: (x['Costo/Efectividad'], -x['Minutos Jugados'])
    )
    defensores = sorted(
        [e for e in evaluaciones if e['Rol'] == 'Defensa'],
        key=lambda x: (x['Costo/Efectividad'], -x['Minutos Jugados'])
    )
    return atacantes, defensores

def mostrar_resultados(lista, titulo):
    """Imprime resultados en forma de tabla"""
    print(f"\n{titulo}\n")
    print(f"{'Nombre':<12}{'Rol':<10}{'Precio':<10}{'Efectividad':<12}{'Minutos':<10}{'Costo/Efect':<15}")
    print("-" * 70)
    for r in lista:
        # Manejar caso de inf para impresión
        costo_efect = r['Costo/Efectividad']
        if costo_efect == float('inf'):
            costo_str = "Inf"
        else:
            costo_str = f"{costo_efect:.2f}"
        print(f"{r['Nombre']:<12}{r['Rol']:<10}{r['Precio']:<10.0f}{r['Efectividad']:<12.2f}{r['Minutos Jugados']:<10}{costo_str:<15}")

# --- FUNCIONES DE VISUALIZACIÓN AÑADIDA ---
def graficar_ranking(atacantes, defensores):
    """Genera gráficos de barras del costo por efectividad."""
    # Preparar datos para atacantes
    atac_finitos = [a for a in atacantes if a['Costo/Efectividad'] != float('inf')]
    def_finitos = [d for d in defensores if d['Costo/Efectividad'] != float('inf')]
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    
    # Atacantes
    if atac_finitos:
        nombres_atac = [e['Nombre'] for e in atac_finitos]
        costo_efect_atac = [e['Costo/Efectividad'] for e in atac_finitos]
        bars1 = axs[0].bar(nombres_atac, costo_efect_atac, color='tomato', alpha=0.8, edgecolor='black')
        axs[0].set_title("Costo por Unidad de Efectividad - Atacantes")
        axs[0].set_ylabel("Costo / Efectividad")
        max_val = max(costo_efect_atac) if costo_efect_atac else 1
        axs[0].set_ylim(0, max_val * 1.15)
        for bar, val in zip(bars1, costo_efect_atac):
            axs[0].text(bar.get_x() + bar.get_width()/2, val + max_val*0.03, f"${val:,.0f}", ha='center', fontweight='bold')
    else:
        axs[0].text(0.5, 0.5, 'Sin datos', ha='center', va='center', transform=axs[0].transAxes)
    
    # Defensores
    if def_finitos:
        nombres_def = [e['Nombre'] for e in def_finitos]
        costo_efect_def = [e['Costo/Efectividad'] for e in def_finitos]
        bars2 = axs[1].bar(nombres_def, costo_efect_def, color='skyblue', alpha=0.8, edgecolor='black')
        axs[1].set_title("Costo por Unidad de Efectividad - Defensores")
        axs[1].set_ylabel("Costo / Efectividad")
        max_val = max(costo_efect_def) if costo_efect_def else 1
        axs[1].set_ylim(0, max_val * 1.15)
        for bar, val in zip(bars2, costo_efect_def):
            axs[1].text(bar.get_x() + bar.get_width()/2, val + max_val*0.03, f"${val:,.0f}", ha='center', fontweight='bold')
    else:
        axs[1].text(0.5, 0.5, 'Sin datos', ha='center', va='center', transform=axs[1].transAxes)
    
    plt.tight_layout()
    plt.show()

def graficar_efectividad_vs_precio(todos):
    """Gráfico de dispersión: Precio vs Efectividad."""
    validos = [j for j in todos if j['Efectividad'] > 0]
    if not validos:
        return
    
    atacantes = [j for j in validos if j['Rol'] == 'Ataque']
    defensores = [j for j in validos if j['Rol'] == 'Defensa']
    
    plt.figure(figsize=(9, 6))
    
    if atacantes:
        plt.scatter([j['Precio'] for j in atacantes], [j['Efectividad'] for j in atacantes],
                    label='Atacantes', color='red', s=120, edgecolor='black')
        for j in atacantes:
            plt.text(j['Precio'] + 15000, j['Efectividad'] + 0.008, j['Nombre'], fontweight='bold')
    
    if defensores:
        plt.scatter([j['Precio'] for j in defensores], [j['Efectividad'] for j in defensores],
                    label='Defensores', color='blue', s=120, edgecolor='black')
        for j in defensores:
            plt.text(j['Precio'] + 15000, j['Efectividad'] + 0.008, j['Nombre'], fontweight='bold')
    
    plt.title("Relación entre Precio y Efectividad por Jugador")
    plt.xlabel("Precio ($)")
    plt.ylabel("Efectividad")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

# --- FIN DE FUNCIONES AÑADIDAS ---

if __name__ == "__main__":
    jugadores = cargar_jugadores_desde_csv("jugadores.csv")
    simular_partidos_jugadores(jugadores, num_partidos=10)
    atacantes, defensores = comparar_jugadores(jugadores)
    mostrar_resultados(atacantes, "Ranking de Atacantes")
    mostrar_resultados(defensores, "Ranking de Defensores")
    
    # --- AÑADIDO: Visualización gráfica ---
    todos = atacantes + defensores
    graficar_ranking(atacantes, defensores)
    graficar_efectividad_vs_precio(todos)