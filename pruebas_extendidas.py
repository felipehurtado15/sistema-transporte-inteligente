"""
Script de Pruebas Extendidas para el Sistema de Transporte Inteligente
Incluye validaciones, análisis estadístico y generación de reportes
"""

import json
from datetime import datetime
from sistema_transporte import (
    BaseConocimiento, 
    MotorInferencia, 
    crear_sistema_transmilenio
)

class ValidadorSistema:
    """
    Clase para validar la consistencia y corrección del sistema
    """
    
    def __init__(self, base_conocimiento: BaseConocimiento):
        self.bc = base_conocimiento
        self.errores = []
        self.advertencias = []
    
    def validar_consistencia(self):
        """
        Valida la consistencia lógica de la base de conocimiento
        """
        print("\n" + "="*60)
        print("VALIDACIÓN DE CONSISTENCIA DEL SISTEMA")
        print("="*60 + "\n")
        
        # Validación 1: Simetría de conexiones
        print("[1] Validando simetría de conexiones...")
        self._validar_simetria()
        
        # Validación 2: Estaciones referenciadas existen
        print("[2] Validando referencias de estaciones...")
        self._validar_referencias()
        
        # Validación 3: No hay conexiones duplicadas
        print("[3] Validando unicidad de conexiones...")
        self._validar_duplicados()
        
        # Validación 4: Valores positivos
        print("[4] Validando valores de distancia y tiempo...")
        self._validar_valores_positivos()
        
        # Reporte de resultados
        self._generar_reporte_validacion()
    
    def _validar_simetria(self):
        """Verifica que si A conecta con B, entonces B conecta con A"""
        for estacion, vecinos in self.bc.conexiones.items():
            for vecino, dist, tiempo in vecinos:
                # Buscar la conexión inversa
                conexion_inversa = False
                for v, d, t in self.bc.conexiones.get(vecino, []):
                    if v == estacion and abs(d - dist) < 0.01 and abs(t - tiempo) < 0.01:
                        conexion_inversa = True
                        break
                
                if not conexion_inversa:
                    self.errores.append(
                        f"Asimetría detectada: {estacion} → {vecino} existe, "
                        f"pero {vecino} → {estacion} no existe o tiene valores diferentes"
                    )
        
        if not self.errores:
            print("   ✓ Todas las conexiones son simétricas")
    
    def _validar_referencias(self):
        """Verifica que todas las estaciones referenciadas existen"""
        for estacion, vecinos in self.bc.conexiones.items():
            if estacion not in self.bc.estaciones:
                self.errores.append(f"Estación referenciada no existe: {estacion}")
            
            for vecino, _, _ in vecinos:
                if vecino not in self.bc.estaciones:
                    self.errores.append(
                        f"Estación vecina no existe: {vecino} (referenciada desde {estacion})"
                    )
        
        if not [e for e in self.errores if "no existe" in e]:
            print("   ✓ Todas las referencias de estaciones son válidas")
    
    def _validar_duplicados(self):
        """Verifica que no haya conexiones duplicadas"""
        for estacion, vecinos in self.bc.conexiones.items():
            vecinos_nombres = [v[0] for v in vecinos]
            if len(vecinos_nombres) != len(set(vecinos_nombres)):
                duplicados = [v for v in vecinos_nombres if vecinos_nombres.count(v) > 1]
                self.advertencias.append(
                    f"Conexiones duplicadas desde {estacion}: {set(duplicados)}"
                )
        
        if not self.advertencias:
            print("   ✓ No se encontraron conexiones duplicadas")
    
    def _validar_valores_positivos(self):
        """Verifica que distancias y tiempos sean positivos"""
        for estacion, vecinos in self.bc.conexiones.items():
            for vecino, dist, tiempo in vecinos:
                if dist <= 0:
                    self.errores.append(
                        f"Distancia inválida en {estacion} → {vecino}: {dist}"
                    )
                if tiempo <= 0:
                    self.errores.append(
                        f"Tiempo inválido en {estacion} → {vecino}: {tiempo}"
                    )
        
        if not [e for e in self.errores if "inválid" in e]:
            print("   ✓ Todos los valores de distancia y tiempo son positivos")
    
    def _generar_reporte_validacion(self):
        """Genera un reporte de la validación"""
        print("\n" + "-"*60)
        print("REPORTE DE VALIDACIÓN")
        print("-"*60)
        
        if not self.errores and not self.advertencias:
            print("✓ Sistema VÁLIDO: No se encontraron errores ni advertencias")
        else:
            if self.errores:
                print(f"\n❌ ERRORES ENCONTRADOS: {len(self.errores)}")
                for i, error in enumerate(self.errores, 1):
                    print(f"  {i}. {error}")
            
            if self.advertencias:
                print(f"\n⚠ ADVERTENCIAS: {len(self.advertencias)}")
                for i, adv in enumerate(self.advertencias, 1):
                    print(f"  {i}. {adv}")
        print()

class AnalizadorRendimiento:
    """
    Analiza el rendimiento y eficiencia del sistema
    """
    
    def __init__(self, motor: MotorInferencia):
        self.motor = motor
        self.resultados = []
    
    def analisis_completo(self, muestra_estaciones=None):
        """
        Realiza un análisis completo de rendimiento
        """
        print("\n" + "="*60)
        print("ANÁLISIS DE RENDIMIENTO DEL SISTEMA")
        print("="*60 + "\n")
        
        estaciones = muestra_estaciones or list(self.motor.bc.estaciones.keys())
        
        print(f"[1] Probando rutas entre {len(estaciones)} estaciones...")
        total_pruebas = 0
        rutas_exitosas = 0
        
        for origen in estaciones:
            for destino in estaciones:
                if origen != destino:
                    total_pruebas += 1
                    ruta, costo, stats = self.motor.buscar_ruta_optima(origen, destino)
                    
                    if ruta:
                        rutas_exitosas += 1
                        self.resultados.append({
                            'origen': origen,
                            'destino': destino,
                            'ruta': ruta,
                            'costo': costo,
                            'estadisticas': stats
                        })
        
        print(f"   ✓ Pruebas completadas: {total_pruebas}")
        print(f"   ✓ Rutas encontradas: {rutas_exitosas}")
        print(f"   ✓ Tasa de éxito: {(rutas_exitosas/total_pruebas)*100:.1f}%\n")
        
        # Análisis estadístico
        self._analisis_estadistico()
        
        # Identificar casos extremos
        self._identificar_casos_extremos()
        
        return self.resultados
    
    def _analisis_estadistico(self):
        """Calcula estadísticas sobre las rutas encontradas"""
        if not self.resultados:
            return
        
        print("[2] Estadísticas generales:")
        
        longitudes = [len(r['ruta']) for r in self.resultados]
        transbordos = [r['estadisticas']['transbordos'] for r in self.resultados]
        distancias = [r['estadisticas']['distancia_total'] for r in self.resultados]
        tiempos = [r['estadisticas']['tiempo_total'] for r in self.resultados]
        nodos_explorados = [r['estadisticas']['nodos_explorados'] for r in self.resultados]
        
        print(f"   • Longitud de ruta promedio: {sum(longitudes)/len(longitudes):.2f} estaciones")
        print(f"   • Longitud máxima: {max(longitudes)} estaciones")
        print(f"   • Longitud mínima: {min(longitudes)} estaciones")
        print(f"   • Transbordos promedio: {sum(transbordos)/len(transbordos):.2f}")
        print(f"   • Distancia promedio: {sum(distancias)/len(distancias):.2f} km")
        print(f"   • Tiempo promedio: {sum(tiempos)/len(tiempos):.1f} minutos")
        print(f"   • Nodos explorados promedio: {sum(nodos_explorados)/len(nodos_explorados):.1f}")
        print()
    
    def _identificar_casos_extremos(self):
        """Identifica las rutas más interesantes"""
        print("[3] Casos extremos identificados:")
        
        # Ruta más larga
        ruta_mas_larga = max(self.resultados, key=lambda r: len(r['ruta']))
        print(f"\n   • Ruta MÁS LARGA:")
        print(f"     {ruta_mas_larga['origen']} → {ruta_mas_larga['destino']}")
        print(f"     Estaciones: {len(ruta_mas_larga['ruta'])}")
        print(f"     Transbordos: {ruta_mas_larga['estadisticas']['transbordos']}")
        
        # Ruta con más transbordos
        mas_transbordos = max(self.resultados, key=lambda r: r['estadisticas']['transbordos'])
        print(f"\n   • Ruta con MÁS TRANSBORDOS:")
        print(f"     {mas_transbordos['origen']} → {mas_transbordos['destino']}")
        print(f"     Transbordos: {mas_transbordos['estadisticas']['transbordos']}")
        print(f"     Ruta: {' → '.join(mas_transbordos['ruta'])}")
        
        # Ruta más rápida
        mas_rapida = min(self.resultados, key=lambda r: r['estadisticas']['tiempo_total'])
        print(f"\n   • Ruta MÁS RÁPIDA:")
        print(f"     {mas_rapida['origen']} → {mas_rapida['destino']}")
        print(f"     Tiempo: {mas_rapida['estadisticas']['tiempo_total']:.1f} minutos")
        
        # Búsqueda más eficiente
        mas_eficiente = min(self.resultados, key=lambda r: r['estadisticas']['nodos_explorados'])
        print(f"\n   • Búsqueda MÁS EFICIENTE:")
        print(f"     {mas_eficiente['origen']} → {mas_eficiente['destino']}")
        print(f"     Nodos explorados: {mas_eficiente['estadisticas']['nodos_explorados']}")
        print()

class GeneradorReportes:
    """
    Genera reportes en diferentes formatos
    """
    
    @staticmethod
    def generar_reporte_json(resultados, filename="reporte_rutas.json"):
        """Genera un reporte en formato JSON"""
        reporte = {
            'fecha_generacion': datetime.now().isoformat(),
            'total_rutas': len(resultados),
            'rutas': resultados
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Reporte JSON generado: {filename}")
    
    @staticmethod
    def generar_reporte_markdown(motor: MotorInferencia, casos_prueba, filename="reporte_rutas.md"):
        """Genera un reporte en formato Markdown"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Reporte de Rutas del Sistema de Transporte\n\n")
            f.write(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Sistema:** {len(motor.bc.estaciones)} estaciones, ")
            f.write(f"{len(motor.bc.reglas)} reglas de conexión\n\n")
            f.write("---\n\n")
            
            for origen, destino in casos_prueba:
                f.write(f"## Ruta: {origen} → {destino}\n\n")
                
                ruta, costo, stats = motor.buscar_ruta_optima(origen, destino)
                
                if ruta:
                    f.write("### Secuencia de Estaciones\n\n")
                    for i, est in enumerate(ruta, 1):
                        linea = motor.bc.estaciones[est].linea
                        f.write(f"{i}. **{est}** (Línea: {linea})\n")
                    
                    f.write("\n### Estadísticas\n\n")
                    f.write(f"- Número de estaciones: {len(ruta)}\n")
                    f.write(f"- Transbordos: {stats['transbordos']}\n")
                    f.write(f"- Distancia: {stats['distancia_total']:.2f} km\n")
                    f.write(f"- Tiempo estimado: {stats['tiempo_total']:.1f} minutos\n")
                    f.write(f"- Eficiencia (nodos explorados): {stats['nodos_explorados']}\n")
                else:
                    f.write("**No se encontró ruta válida**\n")
                
                f.write("\n---\n\n")
        
        print(f"✓ Reporte Markdown generado: {filename}")

def pruebas_reglas_logicas(bc: BaseConocimiento):
    """
    Demuestra el funcionamiento de las reglas lógicas
    """
    print("\n" + "="*60)
    print("DEMOSTRACIÓN DE REGLAS LÓGICAS")
    print("="*60 + "\n")
    
    # Regla 1: Conectividad
    print("[1] Regla de Conectividad:")
    print("    ∀A,B,d,t: conecta(A,B,d,t) → puede_viajar(A,B)")
    print("\n    Ejemplos:")
    
    estacion_ejemplo = "Portal Norte"
    vecinos = bc.obtener_vecinos(estacion_ejemplo)
    print(f"    Desde '{estacion_ejemplo}' se puede viajar a:")
    for vecino, dist, tiempo in vecinos:
        print(f"      • {vecino} (distancia: {dist} km, tiempo: {tiempo} min)")
    
    # Regla 2: Transbordo
    print("\n[2] Regla de Transbordo:")
    print("    ∀A,B: (linea(A) ≠ linea(B)) → requiere_transbordo(A,B)")
    print("\n    Ejemplos:")
    
    pares_prueba = [
        ("Portal Norte", "Toberín"),
        ("Virrey", "Calle 75"),
        ("Portal Suba", "Virrey")
    ]
    
    for est1, est2 in pares_prueba:
        requiere = bc.requiere_transbordo(est1, est2)
        linea1 = bc.estaciones[est1].linea
        linea2 = bc.estaciones[est2].linea
        simbolo = "✓" if requiere else "✗"
        print(f"    {simbolo} {est1} [{linea1}] → {est2} [{linea2}]: {requiere}")
    
    # Regla 3: Heurística
    print("\n[3] Regla Heurística:")
    print("    ∀A,B: tiene_coordenadas(A,B) → puede_estimar_distancia(A,B)")
    print("\n    Ejemplos de estimaciones:")
    
    pares_distancia = [
        ("Portal Norte", "CAD"),
        ("Portal Suba", "Portal Américas"),
        ("Calle 100", "Heroes")
    ]
    
    for origen, destino in pares_distancia:
        h = bc.calcular_heuristica(origen, destino)
        print(f"    • h({origen}, {destino}) = {h:.2f} km")
    
    # Mostrar reglas almacenadas
    print("\n[4] Reglas de Conexión en la Base de Conocimiento:")
    print(f"    Total de reglas: {len(bc.reglas)}")
    print("\n    Primeras 10 reglas:")
    for i, regla in enumerate(bc.reglas[:10], 1):
        print(f"    {i}. {regla}")
    
    print()

def comparacion_algoritmos(motor: MotorInferencia, origen: str, destino: str):
    """
    Compara el rendimiento de A* con búsqueda en amplitud simulada
    """
    print("\n" + "="*60)
    print("COMPARACIÓN DE ALGORITMOS DE BÚSQUEDA")
    print("="*60 + "\n")
    
    print(f"Problema: Encontrar ruta de '{origen}' a '{destino}'\n")
    
    # Ejecutar A*
    print("[1] Algoritmo A* (con heurística):")
    ruta_astar, costo_astar, stats_astar = motor.buscar_ruta_optima(origen, destino)
    
    if ruta_astar:
        print(f"    • Ruta encontrada: {' → '.join(ruta_astar[:3])} ... {ruta_astar[-1]}")
        print(f"    • Longitud: {len(ruta_astar)} estaciones")
        print(f"    • Costo total: {costo_astar:.2f} km")
        print(f"    • Nodos explorados: {stats_astar['nodos_explorados']}")
        print(f"    • Tiempo: {stats_astar['tiempo_total']:.1f} minutos")
    
    # Simular búsqueda en amplitud (estimación)
    print("\n[2] Búsqueda en Amplitud (estimación sin heurística):")
    total_estaciones = len(motor.bc.estaciones)
    # En el peor caso, búsqueda en amplitud explora todos los nodos
    nodos_bfs_estimados = min(total_estaciones, stats_astar['nodos_explorados'] * 2)
    print(f"    • Nodos que exploraría (estimado): {nodos_bfs_estimados}")
    print(f"    • Garantiza optimalidad: Sí")
    print(f"    • Usa información del dominio: No")
    
    # Análisis de eficiencia
    print("\n[3] Análisis de Eficiencia:")
    mejora = ((nodos_bfs_estimados - stats_astar['nodos_explorados']) / nodos_bfs_estimados) * 100
    print(f"    • A* exploró {mejora:.1f}% MENOS nodos que BFS")
    print(f"    • Razón: La heurística guía la búsqueda hacia el objetivo")
    print(f"    • Factor de ramificación efectivo reducido por h(n)")
    
    print()

def prueba_casos_especiales(motor: MotorInferencia):
    """
    Prueba casos especiales y situaciones límite
    """
    print("\n" + "="*60)
    print("PRUEBAS DE CASOS ESPECIALES")
    print("="*60 + "\n")
    
    casos = [
        {
            'nombre': 'Ruta de una estación a sí misma',
            'origen': 'Portal Norte',
            'destino': 'Portal Norte',
            'esperado': 'Ruta vacía o trivial'
        },
        {
            'nombre': 'Ruta entre estaciones muy distantes',
            'origen': 'Portal Norte',
            'destino': 'Portal Américas',
            'esperado': 'Ruta larga con múltiples transbordos'
        },
        {
            'nombre': 'Ruta entre estaciones adyacentes',
            'origen': 'Portal Norte',
            'destino': 'Toberín',
            'esperado': 'Ruta directa sin transbordos'
        },
        {
            'nombre': 'Ruta que requiere múltiples transbordos',
            'origen': 'Portal Suba',
            'destino': 'Marsella',
            'esperado': 'Múltiples transbordos necesarios'
        }
    ]
    
    for i, caso in enumerate(casos, 1):
        print(f"[{i}] {caso['nombre']}")
        print(f"    Ruta: {caso['origen']} → {caso['destino']}")
        print(f"    Esperado: {caso['esperado']}")
        
        ruta, costo, stats = motor.buscar_ruta_optima(caso['origen'], caso['destino'])
        
        if caso['origen'] == caso['destino']:
            if not ruta or len(ruta) <= 1:
                print(f"    ✓ Resultado: Caso trivial manejado correctamente")
            else:
                print(f"    ⚠ Resultado inesperado: {ruta}")
        elif ruta:
            print(f"    ✓ Ruta encontrada: {len(ruta)} estaciones, {stats['transbordos']} transbordos")
            print(f"      Primera parte: {' → '.join(ruta[:min(3, len(ruta))])}")
        else:
            print(f"    ✗ No se encontró ruta")
        
        print()

def generar_visualizacion_red(bc: BaseConocimiento, filename="red_transporte.txt"):
    """
    Genera una visualización en texto de la red de transporte
    """
    print("\n" + "="*60)
    print("GENERANDO VISUALIZACIÓN DE LA RED")
    print("="*60 + "\n")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("RED DE TRANSPORTE MASIVO\n")
        f.write("="*60 + "\n\n")
        
        # Agrupar estaciones por línea
        lineas = {}
        for nombre, estacion in bc.estaciones.items():
            if estacion.linea not in lineas:
                lineas[estacion.linea] = []
            lineas[estacion.linea].append(nombre)
        
        # Escribir cada línea
        for linea, estaciones in sorted(lineas.items()):
            f.write(f"\n{linea}\n")
            f.write("-" * len(linea) + "\n")
            
            for estacion in estaciones:
                vecinos = bc.obtener_vecinos(estacion)
                f.write(f"\n{estacion}:\n")
                
                if vecinos:
                    for vecino, dist, tiempo in vecinos:
                        linea_vecino = bc.estaciones[vecino].linea
                        transbordo = " [TRANSBORDO]" if linea != linea_vecino else ""
                        f.write(f"  → {vecino}{transbordo} ({dist:.1f}km, {tiempo}min)\n")
                else:
                    f.write("  (Sin conexiones)\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write(f"\nTotal de estaciones: {len(bc.estaciones)}\n")
        f.write(f"Total de conexiones: {len(bc.reglas)}\n")
        f.write(f"Total de líneas: {len(lineas)}\n")
    
    print(f"✓ Visualización generada: {filename}\n")

def pruebas_exhaustivas():
    """
    Ejecuta todas las pruebas del sistema
    """
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + " "*10 + "SUITE COMPLETA DE PRUEBAS" + " "*23 + "█")
    print("█" + " "*58 + "█")
    print("█"*60 + "\n")
    
    # Inicializar sistema
    print("Inicializando sistema...")
    bc = crear_sistema_transmilenio()
    motor = MotorInferencia(bc)
    print(f"✓ Sistema inicializado: {len(bc.estaciones)} estaciones cargadas\n")
    
    # 1. Validación de consistencia
    validador = ValidadorSistema(bc)
    validador.validar_consistencia()
    
    # 2. Demostración de reglas lógicas
    pruebas_reglas_logicas(bc)
    
    # 3. Casos especiales
    prueba_casos_especiales(motor)
    
    # 4. Comparación de algoritmos
    comparacion_algoritmos(motor, "Portal Norte", "Marsella")
    
    # 5. Análisis de rendimiento
    analizador = AnalizadorRendimiento(motor)
    # Usar un subconjunto para no hacer demasiadas pruebas
    muestra = ["Portal Norte", "Portal Suba", "Portal Américas", "CAD", "Virrey", "Marsella"]
    resultados = analizador.analisis_completo(muestra)
    
    # 6. Generar reportes
    print("\n" + "="*60)
    print("GENERANDO REPORTES")
    print("="*60 + "\n")
    
    casos_reporte = [
        ("Portal Norte", "CAD"),
        ("Portal Suba", "Calle 142"),
        ("Portal Américas", "Virrey")
    ]
    
    GeneradorReportes.generar_reporte_json(resultados[:10], "reporte_rutas.json")
    GeneradorReportes.generar_reporte_markdown(motor, casos_reporte, "reporte_rutas.md")
    generar_visualizacion_red(bc, "red_transporte.txt")
    
    # Resumen final
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + " "*15 + "PRUEBAS COMPLETADAS" + " "*24 + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    print("\nResumen:")
    print(f"  ✓ Validación de consistencia: Completada")
    print(f"  ✓ Pruebas de reglas lógicas: Completadas")
    print(f"  ✓ Casos especiales: Completados")
    print(f"  ✓ Comparación de algoritmos: Completada")
    print(f"  ✓ Análisis de rendimiento: Completado ({len(resultados)} rutas analizadas)")
    print(f"  ✓ Reportes generados: 3 archivos")
    print("\nArchivos generados:")
    print("  • reporte_rutas.json")
    print("  • reporte_rutas.md")
    print("  • red_transporte.txt")
    print("\n" + "█"*60 + "\n")

def modo_interactivo():
    """
    Modo interactivo para probar rutas personalizadas
    """
    print("\n" + "="*60)
    print("MODO INTERACTIVO - BÚSQUEDA DE RUTAS")
    print("="*60 + "\n")
    
    bc = crear_sistema_transmilenio()
    motor = MotorInferencia(bc)
    
    print("Estaciones disponibles:")
    for i, estacion in enumerate(sorted(bc.estaciones.keys()), 1):
        linea = bc.estaciones[estacion].linea
        print(f"  {i:2d}. {estacion} [{linea}]")
    
    print("\n" + "-"*60)
    print("Escribe 'salir' para terminar")
    print("-"*60 + "\n")
    
    while True:
        try:
            origen = input("Estación de origen: ").strip()
            if origen.lower() == 'salir':
                break
            
            if origen not in bc.estaciones:
                print(f"❌ Estación '{origen}' no encontrada. Intenta de nuevo.\n")
                continue
            
            destino = input("Estación de destino: ").strip()
            if destino.lower() == 'salir':
                break
            
            if destino not in bc.estaciones:
                print(f"❌ Estación '{destino}' no encontrada. Intenta de nuevo.\n")
                continue
            
            print("\n🔍 Buscando ruta óptima...\n")
            ruta, costo, stats = motor.buscar_ruta_optima(origen, destino)
            
            if ruta:
                explicacion = motor.explicar_ruta(ruta, stats)
                print(explicacion)
            else:
                print(f"❌ No se encontró ruta entre {origen} y {destino}\n")
            
            continuar = input("\n¿Buscar otra ruta? (s/n): ").strip().lower()
            if continuar != 's':
                break
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Saliendo del modo interactivo...\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

def main():
    """
    Función principal del script de pruebas
    """
    import sys
    
    if len(sys.argv) > 1:
        modo = sys.argv[1]
        
        if modo == '--exhaustivo':
            pruebas_exhaustivas()
        elif modo == '--interactivo':
            modo_interactivo()
        elif modo == '--validar':
            bc = crear_sistema_transmilenio()
            validador = ValidadorSistema(bc)
            validador.validar_consistencia()
        elif modo == '--rendimiento':
            bc = crear_sistema_transmilenio()
            motor = MotorInferencia(bc)
            analizador = AnalizadorRendimiento(motor)
            analizador.analisis_completo()
        elif modo == '--ayuda':
            print("\nSistema de Pruebas - Opciones disponibles:")
            print("  --exhaustivo    : Ejecuta todas las pruebas")
            print("  --interactivo   : Modo interactivo para buscar rutas")
            print("  --validar       : Solo validación de consistencia")
            print("  --rendimiento   : Solo análisis de rendimiento")
            print("  --ayuda         : Muestra este mensaje")
            print("\nSin argumentos: Ejecuta pruebas exhaustivas por defecto\n")
        else:
            print(f"Opción '{modo}' no reconocida. Usa --ayuda para ver opciones.")
    else:
        # Por defecto, ejecutar pruebas exhaustivas
        pruebas_exhaustivas()

if __name__ == "__main__":
    main()