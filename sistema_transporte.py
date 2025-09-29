"""
Sistema Inteligente de Rutas en Transporte Masivo
Basado en Reglas Lógicas y Búsqueda Heurística A*
"""

import heapq
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
import json

@dataclass
class Estacion:
    """Representa una estación en el sistema de transporte"""
    nombre: str
    linea: str
    latitud: float
    longitud: float
    
    def __hash__(self):
        return hash(self.nombre)
    
    def __eq__(self, other):
        return self.nombre == other.nombre

class BaseConocimiento:
    """
    Base de conocimiento del sistema de transporte.
    Utiliza reglas lógicas para representar conexiones y características.
    """
    
    def __init__(self):
        self.estaciones: Dict[str, Estacion] = {}
        self.conexiones: Dict[str, List[Tuple[str, float, float]]] = {}
        self.reglas = []
        
    def agregar_estacion(self, nombre: str, linea: str, lat: float, lon: float):
        """
        Agrega una estación al sistema.
        Regla implícita: SI existe una estación ENTONCES es accesible
        """
        estacion = Estacion(nombre, linea, lat, lon)
        self.estaciones[nombre] = estacion
        if nombre not in self.conexiones:
            self.conexiones[nombre] = []
    
    def agregar_conexion(self, origen: str, destino: str, distancia: float, tiempo: float):
        """
        Regla: SI estacion_A conecta_con estacion_B 
               ENTONCES se puede viajar de A a B
        La conexión es bidireccional en este sistema
        """
        if origen in self.estaciones and destino in self.estaciones:
            # Conexión de ida
            self.conexiones[origen].append((destino, distancia, tiempo))
            # Conexión de vuelta (sistema bidireccional)
            self.conexiones[destino].append((origen, distancia, tiempo))
            
            # Registrar regla
            regla = f"conecta({origen}, {destino}, {distancia}, {tiempo})"
            self.reglas.append(regla)
    
    def requiere_transbordo(self, est1: str, est2: str) -> bool:
        """
        Regla: SI estacion_A.linea != estacion_B.linea 
               ENTONCES requiere_transbordo(A, B)
        """
        if est1 in self.estaciones and est2 in self.estaciones:
            return self.estaciones[est1].linea != self.estaciones[est2].linea
        return False
    
    def obtener_vecinos(self, estacion: str) -> List[Tuple[str, float, float]]:
        """
        Regla: SI conecta(A, B, d, t) ENTONCES es_vecino(B, A)
        Retorna lista de (estacion_destino, distancia, tiempo)
        """
        return self.conexiones.get(estacion, [])
    
    def calcular_heuristica(self, origen: str, destino: str) -> float:
        """
        Función heurística: distancia euclidiana entre coordenadas.
        Regla: SI hay coordenadas ENTONCES se puede estimar distancia
        Esta heurística es admisible (nunca sobreestima el costo real)
        """
        if origen not in self.estaciones or destino not in self.estaciones:
            return float('inf')
        
        est_o = self.estaciones[origen]
        est_d = self.estaciones[destino]
        
        # Distancia euclidiana aproximada (en km)
        lat_diff = (est_d.latitud - est_o.latitud) * 111  # 1 grado lat ≈ 111 km
        lon_diff = (est_d.longitud - est_o.longitud) * 111 * 0.85  # ajuste por latitud
        
        return (lat_diff**2 + lon_diff**2)**0.5

class MotorInferencia:
    """
    Motor de inferencia que aplica el algoritmo A* con la base de conocimiento.
    Implementa búsqueda heurística informada.
    """
    
    def __init__(self, base_conocimiento: BaseConocimiento):
        self.bc = base_conocimiento
        
    def buscar_ruta_optima(self, origen: str, destino: str) -> Tuple[List[str], float, Dict]:
        """
        Implementación del algoritmo A* para encontrar la ruta óptima.
        
        A* combina:
        - g(n): costo real desde el origen hasta el nodo n
        - h(n): estimación heurística desde n hasta el destino
        - f(n) = g(n) + h(n): función de evaluación total
        
        Regla de decisión: SI f(n) es mínima ENTONCES explorar nodo n
        """
        
        # Verificar que origen y destino existen
        if origen not in self.bc.estaciones or destino not in self.bc.estaciones:
            return [], float('inf'), {}
        
        # Cola de prioridad: (f_score, g_score, nodo_actual, camino)
        cola_prioridad = [(0, 0, origen, [origen])]
        
        # Conjunto de nodos visitados
        visitados: Set[str] = set()
        
        # Registro de costos para cada nodo
        g_scores = {origen: 0}
        
        # Estadísticas para análisis
        estadisticas = {
            'nodos_explorados': 0,
            'transbordos': 0,
            'distancia_total': 0,
            'tiempo_total': 0
        }
        
        while cola_prioridad:
            # Regla: Seleccionar el nodo con menor f_score
            f_actual, g_actual, nodo_actual, camino = heapq.heappop(cola_prioridad)
            
            # Condición de terminación: SI nodo_actual == destino ENTONCES éxito
            if nodo_actual == destino:
                # Calcular estadísticas finales
                estadisticas['nodos_explorados'] = len(visitados)
                estadisticas['distancia_total'] = g_actual
                
                # Contar transbordos
                for i in range(len(camino) - 1):
                    if self.bc.requiere_transbordo(camino[i], camino[i+1]):
                        estadisticas['transbordos'] += 1
                
                # Calcular tiempo total
                tiempo_total = 0
                for i in range(len(camino) - 1):
                    for vecino, dist, tiempo in self.bc.obtener_vecinos(camino[i]):
                        if vecino == camino[i+1]:
                            tiempo_total += tiempo
                            break
                estadisticas['tiempo_total'] = tiempo_total
                
                return camino, g_actual, estadisticas
            
            # Regla: SI nodo ya fue visitado ENTONCES omitir
            if nodo_actual in visitados:
                continue
                
            visitados.add(nodo_actual)
            estadisticas['nodos_explorados'] += 1
            
            # Explorar vecinos
            # Regla: PARA CADA vecino conectado EVALUAR si mejora el camino
            for vecino, distancia, tiempo in self.bc.obtener_vecinos(nodo_actual):
                if vecino in visitados:
                    continue
                
                # Calcular costo tentativo
                # Incluimos penalización por transbordo
                penalizacion_transbordo = 2.0 if self.bc.requiere_transbordo(nodo_actual, vecino) else 0
                g_tentativo = g_actual + distancia + penalizacion_transbordo
                
                # Regla: SI nuevo costo < costo anterior ENTONCES actualizar
                if vecino not in g_scores or g_tentativo < g_scores[vecino]:
                    g_scores[vecino] = g_tentativo
                    h_score = self.bc.calcular_heuristica(vecino, destino)
                    f_score = g_tentativo + h_score
                    
                    nuevo_camino = camino + [vecino]
                    heapq.heappush(cola_prioridad, (f_score, g_tentativo, vecino, nuevo_camino))
        
        # No se encontró ruta
        return [], float('inf'), estadisticas
    
    def explicar_ruta(self, ruta: List[str], estadisticas: Dict) -> str:
        """
        Genera una explicación en lenguaje natural de la ruta encontrada.
        Aplica reglas de presentación del conocimiento.
        """
        if not ruta:
            return "No se encontró una ruta válida entre las estaciones especificadas."
        
        explicacion = f"\n{'='*60}\n"
        explicacion += "RUTA ÓPTIMA ENCONTRADA\n"
        explicacion += f"{'='*60}\n\n"
        
        explicacion += f"Origen: {ruta[0]} (Línea {self.bc.estaciones[ruta[0]].linea})\n"
        explicacion += f"Destino: {ruta[-1]} (Línea {self.bc.estaciones[ruta[-1]].linea})\n\n"
        
        explicacion += "Secuencia de estaciones:\n"
        for i, estacion in enumerate(ruta, 1):
            linea = self.bc.estaciones[estacion].linea
            explicacion += f"  {i}. {estacion} [{linea}]"
            
            if i < len(ruta):
                sig_estacion = ruta[i]
                if self.bc.requiere_transbordo(estacion, sig_estacion):
                    explicacion += f" → TRANSBORDO a línea {self.bc.estaciones[sig_estacion].linea}"
            explicacion += "\n"
        
        explicacion += f"\n{'='*60}\n"
        explicacion += "ESTADÍSTICAS DEL VIAJE\n"
        explicacion += f"{'='*60}\n"
        explicacion += f"Número de estaciones: {len(ruta)}\n"
        explicacion += f"Transbordos requeridos: {estadisticas['transbordos']}\n"
        explicacion += f"Distancia aproximada: {estadisticas['distancia_total']:.2f} km\n"
        explicacion += f"Tiempo estimado: {estadisticas['tiempo_total']:.1f} minutos\n"
        explicacion += f"Nodos explorados por el algoritmo: {estadisticas['nodos_explorados']}\n"
        
        return explicacion

def crear_sistema_transmilenio():
    """
    Crea un sistema ejemplo basado en TransMilenio de Bogotá.
    Define la base de conocimiento con estaciones y conexiones reales.
    """
    bc = BaseConocimiento()
    
    # Línea Troncal Caracas (simplificada)
    bc.agregar_estacion("Portal Norte", "Troncal Caracas", 4.7656, -74.0467)
    bc.agregar_estacion("Toberín", "Troncal Caracas", 4.7532, -74.0464)
    bc.agregar_estacion("Calle 142", "Troncal Caracas", 4.7241, -74.0511)
    bc.agregar_estacion("Alcalá", "Troncal Caracas", 4.7110, -74.0532)
    bc.agregar_estacion("Calle 100", "Troncal Caracas", 4.6858, -74.0549)
    bc.agregar_estacion("Virrey", "Troncal Caracas", 4.6656, -74.0569)
    
    # Línea Troncal NQS (simplificada)
    bc.agregar_estacion("Portal Suba", "Troncal NQS", 4.7462, -74.0832)
    bc.agregar_estacion("Suba Calle 95", "Troncal NQS", 4.7279, -74.0834)
    bc.agregar_estacion("Calle 75", "Troncal NQS", 4.6771, -74.0613)
    bc.agregar_estacion("Heroes", "Troncal NQS", 4.6531, -74.0633)
    bc.agregar_estacion("CAD", "Troncal NQS", 4.6437, -74.0641)
    
    # Línea Troncal Américas (simplificada)
    bc.agregar_estacion("Portal Américas", "Troncal Américas", 4.6172, -74.1413)
    bc.agregar_estacion("Pradera", "Troncal Américas", 4.6294, -74.1291)
    bc.agregar_estacion("Marsella", "Troncal Américas", 4.6376, -74.1156)
    bc.agregar_estacion("Zona Industrial", "Troncal Américas", 4.6445, -74.1069)
    
    # Estaciones de transbordo
    bc.agregar_estacion("Centro Memoria", "Transbordo", 4.6569, -74.0611)
    
    # Conexiones Troncal Caracas
    bc.agregar_conexion("Portal Norte", "Toberín", 1.5, 3)
    bc.agregar_conexion("Toberín", "Calle 142", 3.2, 6)
    bc.agregar_conexion("Calle 142", "Alcalá", 1.8, 4)
    bc.agregar_conexion("Alcalá", "Calle 100", 2.8, 5)
    bc.agregar_conexion("Calle 100", "Virrey", 2.3, 4)
    
    # Conexiones Troncal NQS
    bc.agregar_conexion("Portal Suba", "Suba Calle 95", 2.1, 4)
    bc.agregar_conexion("Suba Calle 95", "Calle 75", 5.8, 10)
    bc.agregar_conexion("Calle 75", "Heroes", 2.8, 5)
    bc.agregar_conexion("Heroes", "CAD", 1.2, 3)
    bc.agregar_conexion("CAD", "Centro Memoria", 0.8, 2)
    
    # Conexiones Troncal Américas
    bc.agregar_conexion("Portal Américas", "Pradera", 1.7, 3)
    bc.agregar_conexion("Pradera", "Marsella", 1.9, 4)
    bc.agregar_conexion("Marsella", "Zona Industrial", 1.5, 3)
    bc.agregar_conexion("Zona Industrial", "Centro Memoria", 1.2, 3)
    
    # Conexiones entre líneas (transbordos)
    bc.agregar_conexion("Virrey", "Calle 75", 1.5, 8)  # Transbordo con tiempo de espera
    bc.agregar_conexion("Virrey", "Centro Memoria", 1.8, 5)
    
    return bc

def main():
    """
    Función principal que demuestra el sistema inteligente.
    """
    print("="*60)
    print("SISTEMA INTELIGENTE DE RUTAS - TRANSPORTE MASIVO")
    print("Basado en Reglas Lógicas y Algoritmo A*")
    print("="*60)
    
    # Crear base de conocimiento
    print("\n[1] Inicializando base de conocimiento...")
    bc = crear_sistema_transmilenio()
    print(f"✓ Base de conocimiento creada: {len(bc.estaciones)} estaciones")
    print(f"✓ Reglas de conexión definidas: {len(bc.reglas)}")
    
    # Crear motor de inferencia
    print("\n[2] Inicializando motor de inferencia...")
    motor = MotorInferencia(bc)
    print("✓ Motor de inferencia A* listo")
    
    # Ejemplos de búsqueda de rutas
    casos_prueba = [
        ("Portal Norte", "CAD"),
        ("Portal Suba", "Calle 142"),
        ("Portal Américas", "Virrey"),
        ("Toberín", "Marsella")
    ]
    
    print("\n[3] Ejecutando búsquedas de rutas óptimas...\n")
    
    for origen, destino in casos_prueba:
        print(f"\n🔍 Buscando ruta: {origen} → {destino}")
        print("-" * 60)
        
        ruta, costo, estadisticas = motor.buscar_ruta_optima(origen, destino)
        
        if ruta:
            explicacion = motor.explicar_ruta(ruta, estadisticas)
            print(explicacion)
        else:
            print(f"❌ No se encontró ruta entre {origen} y {destino}\n")
    
    # Mostrar algunas reglas de la base de conocimiento
    print("\n" + "="*60)
    print("EJEMPLOS DE REGLAS EN LA BASE DE CONOCIMIENTO")
    print("="*60)
    print("\nPrimeras 5 reglas de conexión:")
    for i, regla in enumerate(bc.reglas[:5], 1):
        print(f"{i}. {regla}")
    
    print("\n✓ Sistema ejecutado exitosamente")

if __name__ == "__main__":
    main()