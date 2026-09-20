# Análisis del repositorio — 20-09-2026

El frente vigente tiene verificaciones reproducibles y declara correctamente sus
límites. No contiene una prueba completa de `phi=1` ni de Collatz. Los principales
riesgos operativos están en los scripts históricos: ejecución al importar,
reconstrucción destructiva de una base y aritmética de ancho fijo sin validar el
dominio. Esta revisión documenta los hallazgos; no modifica esos programas.

## Alcance y método

Base revisada: commit `a0bf045`, rama `main`. Se ejecutó `git fetch origin` y se
comprobó el estado antes de añadir este informe. El único cambio local previo era
`.claude/`, sin seguimiento; se conserva sin inspeccionarlo ni modificarlo.

Se inventariaron los **716 archivos versionados**: 210 Python, 78 Lean, 340 TXT,
34 JSON, 25 Markdown, 21 ZIP, tres SQLite y otros cinco archivos. Los Python suman
55.064 líneas. El análisis sintáctico cubrió los 210 Python y la lectura JSON
cubrió los 34 archivos de esa extensión, sin errores.

La lectura detallada se concentró en el motor, transiciones, frente matemático,
persistencia, controles y puntos de riesgo detectados. No se leyó cada línea de
los 716 archivos ni se recertificó cada afirmación histórica. Las transcripciones
comprimidas no se descomprimieron; las bases de conversaciones y trayectorias se
consultaron sólo para esquema y conteos. No se ejecutaron los censos grandes ni
se consultó el estado remoto actual de OEIS.

## Organización y coherencia

| Área | Función y valoración |
|---|---|
| `collatz.py`, `main.py` | Motor y CLI del mapa clásico. El agotamiento del tope se informa como inconcluso y conserva el prefijo verificado. |
| `estratoscadena.py`, `subrenovacionc.py` | Cadena simbólica del mapa atajo y conteos enteros. Tienen entrada explícita, límites de estados y protección frente a ejecución al importar. |
| `depuracion/frente20260910/` | Notas, implementaciones exactas y certificados del frente actual. Distingue medición, prueba escrita y formalización parcial. |
| `registroafirmaciones.py`, `guardarafirmaciones.py` | Fuente literal histórica más migración versionada. El reemplazo del catálogo es atómico y comprueba integridad. El generador aún se ejecuta al importarlo. |
| `guardarrespuestas.py` | Captura literal, idempotencia y reversión del lote ante conflictos. Sus controles pasaron. |
| `depuracion/py`, `depuracion/lean`, `revision*`, raíz histórica | Implementaciones independientes, sondas y evidencia de revisiones. Deben conservarse; no forman una biblioteca importable de manera indiscriminada. |
| `archivo/`, `transcripciones/`, salidas | Evidencia histórica. Sus conclusiones se interpretan con el estado y registro vigentes. |

El catálogo coincide con su generador y registro del 17-09: **216 afirmaciones,
85 correcciones, 20 constantes, 52 nodos, 84 dependencias y ocho claves actuales**.
Sus estados son 119 «demostrado», 82 «medido», ocho «conjeturado» y siete
«refutado». Son etiquetas del catálogo, no 119 pruebas nuevamente auditadas aquí.
`respuestas.db` contiene 1.957 mensajes; `hilos.db`, 11 hilos y 1.111 pasos.

## Hallazgos por prioridad

### Alta: reconstrucción destructiva y dependiente del directorio actual

En [guardarhilos.py](../../guardarhilos.py), `ARCHIVO = "hilos.db"` (línea 90)
apunta al directorio de ejecución. Las líneas 255–258 eliminan el archivo
existente antes de crear la base nueva; el commit llega en la línea 327.
Una excepción entre ambas operaciones deja perdido el archivo anterior.
Además, todo ese bloque se ejecuta al importar el módulo.

No se ejecutó ese generador ni se simuló el fallo sobre datos reales. El riesgo
se deduce directamente del flujo de escritura. La reparación prioritaria es
encapsular la ejecución, declarar la ruta y construir/validar un temporal antes
del reemplazo, siguiendo el mecanismo ya usado por `registroafirmaciones.py`.

### Media: importaciones que lanzan trabajo considerable

Hay **181 Python con bucles, bloques `with` o `try` en el nivel superior**, y
184 sin guardia `if __name__ == '__main__'`. Estas cifras son indicadores
estructurales, no una afirmación de que todos ejecuten censos caros.

Dos casos confirmados son [clasesfusion.py](../../clasesfusion.py), con
`K_MAX=32` y el barrido en la línea 301, y
[atacacst2.py](../../atacacst2.py), con límite predeterminado `10**8` y bucle
global en la línea 53. Importarlos para reutilizar una función lanza también
el experimento. Conviene proteger primero los módulos que se reutilicen,
conservando sus implementaciones independientes y parámetros históricos.

### Media: desbordamiento silencioso al ampliar el contador NumPy

En [clasesparalelo.py](../../clasesparalelo.py), líneas 43–48, el estado usa
`np.int64` y evalúa `3*v+1` sin comprobar desbordamiento. Un único residuo basta
para reproducir el problema; no hace falta enumerar `2**40` clases:

```python
from clasesparalelo import salto_y_paridad
print(int(salto_y_paridad([2**40 - 1], 40)[0][0]))
```

Devuelve `-3983235605438928864`; la iteración independiente con enteros Python
devuelve `12157665459056928800`. Para este residuo, los 40 pasos son impares y
el resultado exacto es `3**40-1`. Los controles del mismo tipo en k=1,2,3,32,39
coincidieron.

El objetivo configurado es **k=32**: el testigo no invalida sus resultados
almacenados. Sí demuestra que la función no admite ampliaciones arbitrarias
sin validar cotas de los valores intermedios o cambiar de representación.

### Baja: reproducibilidad y orientación documental

No hay `lean-toolchain` versionado ni archivo de bloqueo de dependencias Python.
`requirements.txt` sólo fija versiones mínimas. El `lean` del sandbox no
encontró configuración; la instalación del usuario, comprobada con autorización,
es **Lean 4.32.2**. Conviene fijar esa versión para facilitar la reproducción.

El [LEEME histórico de depuración](../LEEME.md) aún llama a `veredictos.jsonl`
«el registro que manda»; el estado vigente advierte correctamente que sus IDs
no se trasladan directamente al catálogo actual. Hace falta una remisión visible
al registro vigente, conservando el texto histórico. La cifra de 84 correcciones
en el informe del 13-09 es histórica; hoy son 85. El encabezado de
`estratoscadena.py` también conserva signos `?` en lugar de algunas tildes.

## Evaluación matemática

El mapa de investigación es `T(x)=x/2` para x par y `(3x+1)/2` para x impar;
el CLI utiliza el clásico. `a(n)` cuenta clases balanceadas módulo `2**n`;
su incremento nuevo es `a(n)-2*a(n-1)`. La transición usa la paridad del ancla,
no necesariamente la del menor, y conserva el signo de c en la torre.

Las notas de Mangostas y Gacelas justifican por escrito el reloj interior y
la cola uniforme de una excursión desde `(2,c0)`, con bits justos independientes
y salida en la primera llegada a k=1. Esa salida no es la fusión del par.
Los ingredientes Lean revisados no formalizan todo el ensamblaje probabilístico.

La derivación del control de W en `Matematica.md`, §4, está planteada como una
condición suficiente pendiente. Controlar `Pi_tau*u0` no controla el sumando
`W_tau`. Asimismo, Erizas descarta una contracción uniforme en todas las escalas;
no descarta por ello una ruta a escala fija. No apareció en los controles
ejecutados una contradicción nueva con estos límites declarados.

Las obligaciones siguen siendo:

1. **P1:** integrar los tramos k=0,1 con las excursiones interiores y declarar
   los tiempos de reinicio y la dependencia del estado inicial.
2. **P2:** probar la ventana uniforme de W en la salida bajo el condicionamiento
   especificado, o refutarla con una familia de arranques.
3. **P3:** controlar los arranques reales y la suma de riesgos condicionales.

No se convirtió un barrido finito en prueba universal, ni se adoptó el reloj
O(n) que la revisión 12 había inferido de una media medida.

## Verificación realizada en esta sesión

- Los 210 Python y 34 JSON pasan lectura sintáctica.
- Pasan `verificar_motor.py`, `verificar_registro.py` y `verificar_matematica.py`:
  incluyen 1.001 trayectorias, fallos de persistencia simulados, topes y bordes,
  y comparación directa/simbólica de estratos en n=1..13.
- Pasan los cinco Python del frente: invariantes, balance, obstrucción, rachas
  y transferencia. Incluyen 200 balances exactos, 33.371 celdas de rachas y
  contraste de la descomposición afín en 1.536 palabras, entre otros controles.
- Compilan ocho Lean: `cadenakc`, `cabras`, `conejas` y los cinco del frente.
  Sus 71 salidas de `#print axioms` no contienen `sorryAx`; sólo aparecen los
  axiomas estándar o ausencia de axiomas. No se recompilaron los otros 70 Lean.
- Existen los destinos de los 35 enlaces locales encontrados en nueve notas
  de orientación y del frente; no se validaron las anclas internas.
- Se reprodujo el desbordamiento descrito, con un cálculo entero independiente.

El control de estratos lee el verificador del repositorio vecino `zootheorem`;
esta revisión no constituye una auditoría integral de ese segundo repositorio.
No se regeneraron bases, sobrescribieron salidas históricas, hicieron envíos a
OEIS ni publicaron cambios. La evidencia capturada del frente se conserva en
[evidencia.json](evidencia.json).
