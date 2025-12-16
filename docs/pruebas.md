# Pruebas unitarias de la aplicación Lavadero

En este apartado se documenta el diseño, implementación y ejecución de las **pruebas unitarias** realizadas sobre la aplicación *Lavadero*, con el objetivo de verificar el correcto funcionamiento de los requisitos definidos en el enunciado de la actividad.

Las pruebas se han implementado utilizando el módulo **Unittest** de Python.

---

## 1. Objetivo de las pruebas

El objetivo principal de las pruebas unitarias es:

- Verificar el **estado inicial** del lavadero.
- Comprobar que se lanzan **excepciones** cuando se incumplen las reglas de negocio.
- Validar el **cálculo correcto de los ingresos** según las opciones seleccionadas.
- Comprobar el **flujo de fases** del lavadero en todos los escenarios posibles.
- Detectar **errores en la lógica interna** del programa para su posterior corrección.

Cada test se corresponde directamente con una **premisa del enunciado**.

---

## 2. Preparación del entorno de pruebas

Las pruebas se encuentran en la carpeta `tests` del proyecto y utilizan la siguiente estructura:

```text
tests/
 └── test_lavadero_unittest.py
