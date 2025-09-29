# Sistema Inteligente de Rutas en Transporte Masivo

Sistema inteligente basado en conocimiento que utiliza reglas lógicas y el algoritmo de búsqueda heurística A* para encontrar rutas óptimas en sistemas de transporte masivo.

## 📋 Tabla de Contenidos

- [Video Demostrativo](#video-demostrativo)
- [Descripción](#descripción)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Fundamentos Teóricos](#fundamentos-teóricos)
- [Pruebas](#pruebas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Colaboradores](#colaboradores)

## 📹 Video Demostrativo
https://sistema-transporte-inteligente.netlify.app/

## 🎯 Descripción

Este proyecto implementa un sistema inteligente que resuelve el problema de búsqueda de rutas óptimas en redes de transporte masivo. El sistema combina tres pilares fundamentales de la inteligencia artificial:

1. **Representación del Conocimiento**: Utiliza reglas lógicas para modelar las características del sistema de transporte (estaciones, conexiones, líneas, distancias y tiempos).

2. **Motor de Inferencia**: Implementa el algoritmo de búsqueda A* con heurística admisible para encontrar rutas óptimas garantizadas.

3. **Base de Conocimiento**: Estructura modular que permite agregar, modificar y consultar información del sistema de transporte de manera eficiente.

El sistema está diseñado para ser genérico y puede adaptarse a cualquier sistema de transporte masivo simplemente modificando la base de conocimiento.

## ✨ Características

### Funcionalidades Principales

- ✅ Búsqueda de rutas óptimas entre cualquier par de estaciones
- ✅ Consideración de múltiples factores: distancia, tiempo y transbordos
- ✅ Heurística admisible basada en distancia euclidiana
- ✅ Explicaciones detalladas en lenguaje natural de las rutas encontradas
- ✅ Estadísticas completas de cada búsqueda (nodos explorados, eficiencia)
- ✅ Validación automática de consistencia de la base de conocimiento
- ✅ Penalización configurable por transbordos
- ✅ Soporte para redes de transporte complejas con múltiples líneas

### Características Avanzadas

- 🔍 Modo interactivo para consultas personalizadas
- 📊 Análisis de rendimiento y estadísticas
- 📝 Generación de reportes en múltiples formatos (JSON, Markdown, TXT)
- 🎯 Identificación de casos extremos y rutas interesantes
- ⚡ Comparación entre diferentes algoritmos de búsqueda
- 🔐 Validación de consistencia lógica de reglas

## 📦 Requisitos

### Requisitos del Sistema

- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows, Linux, macOS
- **Memoria RAM**: Mínimo 256 MB
- **Espacio en Disco**: Mínimo 10 MB

### Dependencias

El proyecto utiliza únicamente bibliotecas estándar de Python:
- `heapq`: Para la cola de prioridad del algoritmo A*
- `typing`: Para anotaciones de tipos
- `dataclasses`: Para estructuras de datos
- `json`: Para generación de reportes
- `datetime`: Para marcas temporales

**No se requieren instalaciones adicionales** de paquetes externos.

## 🚀 Instalación

### Paso 1: Clonar el Repositorio

```bash
# Clonar desde GitHub/GitLab
git clone https://github.com/felipehurtado15/sistema-transporte-inteligente.git

# Navegar al directorio
cd sistema-transporte-inteligente
```

### Paso 2: Verificar la Instalación de Python

```bash
# Verificar versión de Python
python --version

# O en algunos sistemas:
python3 --version
```

Debe mostrar Python 3.8 o superior.

### Paso 3: Verificar los Archivos

Asegúrate de tener los siguientes archivos:
```
sistema-transporte-inteligente/
├── sistema_transporte.py          # Código principal del sistema
├── pruebas_extendidas.py          # Suite completa de pruebas
├── README.md                      # Este archivo
├── DOCUMENTACION.pdf              # Documento de pruebas y análisis
└── requirements.txt               # Archivo vacío (sin dependencias externas)
```

## 💻 Uso

### Uso Básico

Para ejecutar el sistema con los casos de prueba predefinidos:

```bash
python sistema_transporte.py
```

Esto ejecutará automáticamente varios casos de prueba y mostrará:
- Inicialización del sistema
- Búsqueda de rutas entre diferentes pares de estaciones
- Explicaciones detalladas de cada ruta
- Estadísticas de rendimiento

### Pruebas Exhaustivas

Para ejecutar todas las pruebas de validación y análisis:

```bash
python pruebas_extendidas.py --exhaustivo
```

Esto ejecutará:
- Validación de consistencia de la base de conocimiento
- Demostración de reglas lógicas
- Casos especiales y límite
- Comparación de algoritmos
- Análisis de rendimiento
- Generación de reportes

### Modo Interactivo

Para buscar rutas personalizadas de forma interactiva:

```bash
python pruebas_extendidas.py --interactivo
```

El sistema te pedirá ingresar estaciones de origen y destino, y mostrará la ruta óptima.

### Otras Opciones

```bash
# Solo validar consistencia
python pruebas_extendidas.py --validar

# Solo análisis de rendimiento
python pruebas_extendidas.py --rendimiento

# Ver todas las opciones disponibles
python pruebas_extendidas.py --ayuda
```

## 🏗️ Arquitectura del Sistema

### Componentes Principales

```
┌─────────────────────────────────────────────┐
│         Interfaz de Usuario                 │
│  (Consultas, Resultados, Explicaciones)     │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│         Motor de Inferencia                 │
│      (Algoritmo A* + Lógica)                │
│  • Búsqueda Heurística                      │
│  • Aplicación de Reglas                     │
│  • Generación de Explicaciones              │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│       Base de Conocimiento                  │
│  • Estaciones (Nodos)                       │
│  • Conexiones (Aristas)                     │
│  • Reglas Lógicas                           │
│  • Metadatos (líneas, coordenadas)          │
└─────────────────────────────────────────────┘
```

### Clase: BaseConocimiento

Representa el conocimiento del sistema de transporte mediante:
- **Estaciones**: Objetos con nombre, línea y coordenadas
- **Conexiones**: Grafo dirigido (bidireccional) con pesos
- **Reglas**: Expresiones lógicas de conectividad

**Métodos principales:**
```python
agregar_estacion(nombre, linea, lat, lon)    # Agregar nueva estación
agregar_conexion(origen, destino, dist, t)   # Definir conexión
requiere_transbordo(est1, est2)              # Evaluar regla de transbordo
obtener_vecinos(estacion)                     # Consultar conectividad
calcular_heuristica(origen, destino)          # Función h(n)
```

### Clase: MotorInferencia

Implementa el algoritmo A* y la lógica de razonamiento:

**Algoritmo A***:
```
f(n) = g(n) + h(n)

donde:
  g(n) = costo real acumulado desde origen hasta n
  h(n) = estimación heurística de n hasta destino
  f(n) = función de evaluación total
```

**Métodos principales:**
```python
buscar_ruta_optima(origen, destino)  # Encuentra mejor ruta
explicar_ruta(ruta, estadisticas)    # Genera explicación
```

### Flujo de Ejecución

1. **Inicialización**: Carga de estaciones y conexiones en la base de conocimiento
2. **Consulta**: Usuario especifica origen y destino
3. **Inferencia**: Motor aplica A* con reglas lógicas
4. **Resultado**: Sistema retorna ruta óptima con explicación
5. **Análisis**: Estadísticas de la búsqueda y eficiencia

## 📚 Fundamentos Teóricos

### Algoritmo A*

A* es un algoritmo de búsqueda informada que combina las ventajas de:
- **Búsqueda en amplitud**: Garantía de optimalidad
- **Búsqueda voraz**: Eficiencia mediante heurística

**Propiedades Matemáticas:**

1. **Completitud**: Si existe solución, A* la encuentra
2. **Optimalidad**: Si h(n) es admisible, A* encuentra la solución óptima
3. **Eficiencia**: A* expande el mínimo número de nodos necesario

**Admisibilidad de la Heurística:**

Nuestra heurística (distancia euclidiana) es admisible porque:
```
∀n: h(n) ≤ h*(n)
```
donde h*(n) es el costo real óptimo. La línea recta es siempre el camino más corto.

### Representación mediante Reglas Lógicas

El sistema utiliza lógica de primer orden para representar conocimiento:

**Regla de Conectividad:**
```
∀A,B,d,t: conecta(A,B,d,t) → puede_viajar(A,B)
```

**Regla de Transbordo:**
```
∀A,B: (linea(A) ≠ linea(B)) → requiere_transbordo(A,B)
```

**Regla Heurística:**
```
∀A,B: tiene_coordenadas(A,B) → puede_estimar_distancia(A,B)
```

### Complejidad Computacional

- **Tiempo**: O((V + E) log V) con cola de prioridad
  - V: número de estaciones
  - E: número de conexiones

- **Espacio**: O(V) para estructuras de datos auxiliares

## 🧪 Pruebas

### Casos de Prueba Incluidos

El sistema incluye múltiples casos de prueba que validan:

1. **Rutas simples**: Sin transbordos, directas
2. **Rutas con transbordos**: Cambios de línea necesarios
3. **Rutas largas**: Múltiples estaciones y transbordos
4. **Casos límite**: Origen = Destino, estaciones no conectadas
5. **Eficiencia**: Comparación con búsqueda no informada

### Ejecutar Pruebas

```bash
# Suite completa
python pruebas_extendidas.py --exhaustivo

# Pruebas específicas
python pruebas_extendidas.py --validar
python pruebas_extendidas.py --rendimiento
```

### Reportes Generados

Las pruebas generan automáticamente:
- `reporte_rutas.json`: Resultados en formato JSON
- `reporte_rutas.md`: Documentación en Markdown
- `red_transporte.txt`: Visualización de la topología

## 📁 Estructura del Proyecto

```
sistema-transporte-inteligente/
│
├── sistema_transporte.py          # Sistema principal
│   ├── class Estacion
│   ├── class BaseConocimiento
│   ├── class MotorInferencia
│   └── def crear_sistema_transmilenio()
│
├── pruebas_extendidas.py          # Suite de pruebas