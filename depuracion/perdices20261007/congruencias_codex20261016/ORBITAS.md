# Perdices: congruencias orbitales y ventanas desde la misma semilla

16-10-2026. Continuación de [Congruencias](CONGRUENCIAS.md). Trabajo local
de Codex. Se conserva el nombre Perdices y no se reclama prioridad.

**Avance:** la cota residual ya tiene un certificado Lean desde caminos
reales A/B hasta `ceil(log2(n+5))`, sin asumir como hipótesis las
congruencias de las fronteras. Además se transporta a cualquier ventana
interior conservando la semilla inicial. No demuestra el presupuesto (P).

## 1. Enunciado y alcance

Se usa `T(x)=x/2` para x par y `(3x+1)/2` para x impar, sobre naturales;
la interpretación de interés tiene n>=1. A=1 y B=110 son paridades reales.
No se asigna ley aleatoria ni condicionamiento probabilístico.

Sean U y V palabras finitas arbitrarias de A/B, incluso vacías. Si la misma
semilla n realiza

```text
U B A^b B^c A^d B V,       b,d>=0, c>=1,
```

poner P=longitud de U en pasos de T y S=número de unos de U. Con
`delta=(8,6,8,8,7,8)`, se obtiene

```text
2^(P+b+delta(b mod 6)-1) < 3^S (n+5).                  (1)
```

No se acota el número de cambios en U ni en V. Para U vacía resulta
`b+delta(b mod 6)<=ceil(log2(n+5))`. La formalización muestra que b,d
pueden ser cero: las rachas A vacías no invalidan la desigualdad. La
optimalidad anterior para b>=1 sigue conservando sus seis familias.

**Límite:** (1) controla cada ventana con el reloj acumulado P,S. Su lado
derecho aumenta con S; no proporciona una cota uniforme sobre la longitud
total ni permite sumar los sobrecostes de ventanas solapadas. Es una
restricción necesaria para cualquier cantidad de cambios, no un cierre
del presupuesto uniforme de recargas, la salida del piloto o Collatz.

## 2. Cadena formal y derivación independiente

[PerdicesCongruenciasOrbitales.lean](PerdicesCongruenciasOrbitales.lean)
importa y recompila desde fuente el módulo orbital anterior
[Transporte impar](../PerdicesTransporteImpar.lean) y la
[tabla aritmética](PerdicesCongruencias.lean).

`Camino` enlaza fronteras mediante `2y=3x+1` para A y `8y=9x+5` para B.
Los teoremas importados `paso_a_real` y `paso_b_real` prueban su equivalencia
con los pasos de T y sus paridades. No son ecuaciones afines sin conexión
con la dinámica.

Los trece resultados nuevos separan un camino concatenado, transportan
rachas y extraen sus congruencias. En particular, si y,z,t,u son las
fronteras sucesivas de `B^a A^b B^c A^d`, con a,c>=1 y u entrada B:

```text
y+1=2^(b+2)r,        z+1=4*3^b*r,
9 | y+5,            32 | z+5.
```

La primera línea se obtiene de la racha A y `z=3 mod 8`, cancelando
potencias coprimas. Para la segunda, una racha B no vacía hace su salida
igual a 4 módulo 9; y `4 | t+5`, junto con la racha B anterior, obliga a
`32 | z+5`. Ambas divisibilidades siguen válidas cuando b o d son cero.
Así aparecen las dos congruencias de la misma r de la nota anterior.

`desde_palabra` une todo sin fronteras externas como hipótesis.
`banda_logaritmica` llega a `Nat.clog 2 (n+5)`, el techo entero del
logaritmo. La realización de las familias óptimas y el cilindro con
valuación terminal siguen teniendo prueba escrita, no formalización completa.

Para comprobar independientemente (1), llamar x a la frontera tras U.
La banda local y el encaje orbital ya probado dan

```text
2^(b+delta-1) < x+5,
2^P(x+5) <= 3^S(n+5).
```

Multiplicar la primera por `2^P>0` y encadenar prueba (1).
`ventana_desde_semilla` certifica exactamente este paso. No cambia n por x
en el enunciado final ni supone independencia entre ventanas.

## 3. Evidencia y siguiente obligación

- [Evidencia Lean](evidencia_orbitas.json) y [salida](evidencia_orbitas.txt):
  Lean 4.32.2, 29 consultas de axiomas —ocho del transporte, ocho de la tabla
  y trece nuevas—, sólo axiomas estándar, sin `sorryAx` ni avisos. Los tres
  módulos se compilan desde fuente en una carpeta temporal propia. Los
  imports directos se cotejan con Mathlib fijado; no se declara auditoría
  transitiva completa de Mathlib.
- [Contraste orbital](cotejo_ventanas.json): 1116 ventanas construidas con
  dos algoritmos independientes de cilindros y recorrido literal de T;
  1080 interiores y 620 con alguna racha A vacía. Prefijos de hasta cuatro
  bloques, c=1,2 y b,d=0,1,2; dos representantes por cilindro. También hay
  colas posteriores a la ventana. Es contraste finito, no prueba universal.
- El [alta versionada](alta_registro.json) incorpora este alcance y se
  valida con el generador central en una copia temporal; el catálogo y
  las bases originales siguen intactos.

**Continuación:** [Ventanas conjuntas](CONJUNTAS.md) descarta dos mínimos
residuales vecinos y prueba un exceso óptimo de 72 por pareja disjunta,
con cualquier número de ventanas. Falta relacionar ese exceso con el
tiempo total o la carga terminal desde n; (1) no aporta ese puente.

```powershell
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/comprobar_orbitas.py --salida depuracion/perdices20261007/congruencias_codex20261016/evidencia_orbitas.json
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/cotejar_ventanas.py --prefijo-max 4 --racha-max 2 --traslados 2 --salida depuracion/perdices20261007/congruencias_codex20261016/cotejo_ventanas.json
```
