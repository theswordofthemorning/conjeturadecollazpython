# Ocelotas aplicada a ciclos: calibración contra Hercher — 12-10-2026

## Qué se demuestra

[OcelotasCiclos.lean](OcelotasCiclos.lean), teorema `ciclo_exige`:
si la CST vale para toda palabra con a lo sumo R rachas (`CSTHasta R`, la
forma de `descenso_contador`), entonces todo ciclo del atajo T con
`T^[L] n = n`, `L ≥ 1` y todos sus puntos ≥ 2 tiene **más de R rachas
impares**, contadas sobre el ciclo (`rachasCiclicas`). Esas rachas son los
m mínimos locales de Simons–de Weger y de Hercher. El recuento no depende
del punto de partida (`rotar`).

Prueba, en palabras:
1. Sea m el mínimo del ciclo: ningún punto del ciclo baja de m.
2. Tras una vuelta, 3^S · m ≤ 2^L · m, y 3^S ≠ 2^L por paridad; luego el
   coeficiente 3^S/2^L ya es menor que 1. Hay un primer cruce k ≤ L.
3. Si la palabra hasta k tuviera ≤ R rachas, la CST daría T^k(m) < m:
   imposible. Así que tiene más de R.
4. El predecesor de m en el ciclo es par: si fuera impar, m = (3p+1)/2 > p.
   Por eso contar desde m da exactamente el recuento cíclico, y la palabra
   hasta k es un prefijo suyo.

Instancias, cada una en su archivo (las carpetas de compilados repiten
módulos y no se mezclan):

| Archivo | Hipótesis | Resultado |
|---|---|---|
| [OcelotasCiclosVeinticuatro.lean](OcelotasCiclosVeinticuatro.lean) | LMN | ningún ciclo con ≤ 24 rachas |
| [OcelotasCiclosCuarentaYDos.lean](OcelotasCiclosCuarentaYDos.lean) | LMN + censo propio 3·10^11 | ≤ 42 |
| [OcelotasCiclosCuarentaYSeis.lean](OcelotasCiclosCuarentaYSeis.lean) | LMN + censo propio 7·10^11 | ≤ 46 |
| [OcelotasCiclosOchentaYUno.lean](OcelotasCiclosOchentaYUno.lean) | LMN + Rozier–Terracol 5.4 | ≤ 81 |

Los cinco compilan sin errores; `#print axioms` da sólo `propext`,
`Classical.choice` y `Quot.sound`. Compilación manual con `lake env lean -R`,
LEAN_PATH = compilados propios + la carpeta de extensión del cierre +
`ocelotas_auditado_20261003`.

Auditados el 12-10 sobre las carpetas de compilados de cada cierre, con la
misma herramienta que auditó ese cierre (evidencia_ciclos_*.json y .txt):

| Instancia | Auditor | Compilados | Reutilizados | Consultas |
|---|---|---|---|---|
| 24 | comprobar_extension_paralela.py | 2 | 650 | 26024 |
| 42 | comprobar_extension_persistente.py | 2 | 20 | 98 |
| 46 | comprobar_extension_persistente.py | 2 | 19 | 98 |
| 81 | comprobar_extension_persistente.py | 2 | 14 | 135 |

Los compilados son OcelotasCiclos y la instancia; sin sorryAx. En la carpeta
de 24 se lanzó primero, por error, el auditor persistente, que reescribió su
manifiesto; se restauró desde evidencia_veinticuatro_lean.json tras comprobar
que los 650 objetos coincidían con sus huellas.

## Calibración

Datos leídos en los PDF de `Collatz Investigacion/` (Hercher 2023, JIS 26,
art. 23.3.5; Simons–de Weger v1.44, 2010):

| Fuente | Verificación usada | Excluye m-ciclos con |
|---|---|---|
| Simons–de Weger 2005 | — | m ≤ 67 |
| Simons–de Weger 2010 | X0 = 5·2^60 ≈ 5,8·10^18 | m ≤ 75 |
| Mismo método con X0 nuevo (según Hercher) | X0 = 695·2^60 ≈ 8,0·10^20 | m ≤ 82 |
| Hercher 2023 (pesos) | X0 = 695·2^60 | m ≤ 91 |
| **Ocelotas (aquí)** | CST hasta 2,8·10^19 (Rozier–Terracol) | **m ≤ 81** |

Lectura: con una verificación entre las de 2010 y 2023, y usando los pesos
de Hercher, el número cae entre 75 y 91. **No contradice la literatura.**
No es un resultado nuevo: Hercher ya cubre más. Es una comprobación de
coherencia del método, no una prueba de que el método sea correcto.

Diferencias que impiden una comparación exacta:
- Hercher supone que las órbitas hasta X0 convergen; aquí se supone la CST
  hasta 2,8·10^19, que es una afirmación distinta.
- El primer cruce sólo ve un prefijo del ciclo; Hercher usa el ciclo
  entero (la suma de todas sus rachas), lo que le da más fuerza.

## Registro

Afirmación `ocelotas_ciclos_calibracion_lean` en `registro.json` (12-10), y
relación ocelotas → sin_circuitos en el mapa.
