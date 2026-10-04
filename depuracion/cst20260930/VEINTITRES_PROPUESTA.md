# Ocelotas: preparación de 23 rachas sin Rozier–Terracol

Preparación del 03-10-2026. **Cierre de 23 aceptado a las 23:59:59**,
cotejado el 04-10: [resultado y auditoría final](VEINTITRES_LEAN.md).
Amplía [22 rachas](VEINTIDOS_LEAN.md), bajo LMN, manteniendo el
certificado interno hasta 4912740. La vía de
[77](SETENTA_Y_SIETE_LEAN.md) utiliza además Rozier–Terracol.

## Mapa y objetivo

Se usa T(n)=n/2 si n es par y (3n+1)/2 si es impar, n>=2.
Para un primer cruce finito k, q cuenta las entradas impares en los
primeros k pasos y las rachas son sus bloques maximales. Se demuestra
T^k(n)<n cuando hay como máximo 23 rachas, bajo `LMN23`.
No se afirma existencia universal del primer cruce ni llegada a 1.
No hay ley probabilística ni ampliación del censo existente.

## Tabla y cola: cotejo exacto

El [preparador](preparar_veintitres_lean.py) usa las cotas de logaritmos
de 55 decimales ya formalizadas. Produce la
[tabla de 43 intervalos](preparacion_veintitres_lean.json), para
q<19362882631. El [cotejador independiente](cotejar_veintitres_lean.py)
no importa el preparador; contrasta con series racionales de atanh,
potencias enteras, techos y la recurrencia con `Fraction`.
El [cotejo inicial](cotejo_tabla_veintitres_lean.json) comprobó sólo la
tabla. El [cotejo completo](cotejo_veintitres_lean.json) ya enlaza ambas
ventanas contrastadas por separado:

- 35 filas remiten a n<=4912740, con certificado Lean previo.
- Seis filas se excluyen por la criba numérica.
- Dos filas requieren los certificados por prefijos descritos abajo.
- Cola certificada: R=23, A=82528, c=5, H=34. Se verificaron exactamente
  las desigualdades del [criterio paramétrico](COLA_PARAMETRICA.md).
  El corte en q supera 2^34, de modo que q<k enlaza con esa cola.

El preparador antiguo, de menor precisión logarítmica, no pudo
certificar un signo en este rango. No se modificó: la propuesta nueva
usa la precisión ya disponible. Ese fallo de cálculo no era un
contraejemplo matemático.

## Ventanas finitas

Los extremos son inclusivos; ambas ventanas empiezan en 4912741.
Se usa criba afinada y combustible 128. **Las ventanas se solapan.**

| Ventana | Última semilla | q mínimo | Estado |
|---|---:|---:|---|
| Baja | 6276058 | 79335 | Cotejo independiente y certificado Lean completos |
| Alta | 356547672 | 190537 | Cotejo independiente y cadena Lean completa aceptados |

La [ventana baja](prefijos_23_bajo_1m.json) cerró 528949 nodos,
39815 hojas no vacías y 1363318 semillas, con profundidad máxima 60.
El [cotejo independiente](cotejo_prefijos_23_bajo.json) reconstruyó
las órbitas y verificó cotas, cobertura disjunta y huella de las hojas.
Se [generaron](generacion_OcelotasVeintitresPrefijosBajo.json) 28 partes
Lean, 453 subárboles y 452 uniones. El
[ensamblaje de la ventana](OcelotasVeintitresPrefijosBajo.lean) terminó
con código 0, sesión 7013: [35 módulos compilados y 477 consultas](evidencia_prefijos_23_bajo.json),
sólo axiomas estándar, 27 módulos de base reutilizados por huellas.
Sus objetos persisten en la caché `ocelotas_veintitres_20261003`.

En la alta se conservan los intentos de
[un millón](prefijos_23_alto_1m.json) y
[ocho millones](prefijos_23_alto_8m.json) de nodos. Ambos agotaron
el presupuesto antes de cubrir la ventana. Un agotamiento de
presupuesto no es un fallo de CST.

La [exploración ampliada](prefijos_23_alto_64m.json) terminó con código 0:
12368501 nodos, 2189377 hojas no vacías y 351634932 semillas cubiertas,
sin pendientes, con profundidad máxima 60; 107,928 segundos medidos.
El [contraste independiente](cotejo_prefijos_23_alto.json), sesión
92970, terminó con código 0 y sin discrepancias.
Se [generaron](generacion_OcelotasVeintitresPrefijosAlto.json) 62 partes,
11270 subárboles y 11269 uniones, con hasta 2000 nodos por subárbol y
200000 evaluados por módulo. Se verificaron todas las huellas y la
conservación del número de nodos. La sesión 72927 terminó con código 0:
[primera parte aceptada](evidencia_prefijos_23_alto_piloto.json), un
módulo compilado, seis reutilizados y 229 consultas estándar.
La sesión **27647** terminó de comprobar `OcelotasVeintitres` completo
con código 0 en la misma caché: [evidencia final](evidencia_veintitres_lean.json).
Al [cerrar la tanda](CIERRE_TANDA_20261003.md) se dejó esa ejecución
activa y se guardó una [foto parcial del avance](avance_veintitres_cierre_20261003.json).
La salida `.txt` estuvo fuera del commit mientras cambiaba; ahora está
completa y acompaña al JSON final.

Están aceptados la [tabla Lean](OcelotasVeintitresTabla.lean), en
tres partes, y el [ensamblaje de 23](OcelotasVeintitres.lean).
Las cuatro fuentes de tabla se reprodujeron byte a byte desde su
[generador](generar_veintitres_lean.py) y compilaron con la ventana alta.

La [cota con descuento por racha](DESCUENTO_RACHAS_LEAN.md) se formalizó
por separado y reduce los nodos de esta ventana en exploración. El
ensamblaje de 23 conserva la criba anterior, cuyo cotejo está completo.

## Reproducción y siguiente paso

```text
python -B -X utf8 depuracion/cst20260930/preparar_veintitres_lean.py --logaritmos depuracion/cst20260930/logaritmos_55_propuesta.json --salida depuracion/cst20260930/preparacion_veintitres_lean.json
python -B -X utf8 depuracion/cst20260930/cotejar_veintitres_lean.py --certificado depuracion/cst20260930/preparacion_veintitres_lean.json --salida depuracion/cst20260930/cotejo_tabla_veintitres_lean.json
python -B -X utf8 depuracion/cst20260930/explorar_prefijos_racionales.py --inicio 4912741 --limite 356547672 --q-min 190537 --rachas 23 --combustible 128 --criba afinada --max-nodos 64000000 --salida depuracion/cst20260930/prefijos_23_alto_64m.json
```

Cadena persistente terminada; huellas y consultas finales cotejadas.
El cierre se incorpora al registro como afirmación demostrada bajo
sus hipótesis explícitas. No se inicia una extensión automática a 24.
Revisión humana y prioridad pendientes.
