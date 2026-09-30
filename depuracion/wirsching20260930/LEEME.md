# Wirsching: bloque 3, sesión 1 — 30-09-2026

Bloque 3 del [plan por sesiones](../transversal20260927/PLAN_SESIONES_20260928.md):
revisar el programa de Wirsching (2003) y el preprint de Tavares (2026),
aislar el control por residuos pendiente e intentar una instancia limitada.

**Resultado.** El eslabón abierto es la condición aritmética (⋆3). Para la
densidad basta (⋆1). En su forma literal, con la ventana centrada en `k = ℓ`,
falla en todos los niveles calculados, `2 ≤ ℓ ≤ 16`. En cada nivel hay clases
módulo `3^ℓ` sin ningún camino con ℓ pasos impares y ℓ pares. El entero
positivo 34 es una de ellas en todos esos niveles. La dispersión de las
cuentas crece con ℓ como en una cascada multiplicativa en su punto crítico
de `L²`. Si un mismo 3-ádico fuera malo en infinitos niveles, la conjetura 2
de Wirsching sería falsa tal como está escrita. Hasta `ℓ = 16`, los conjuntos
de candidatos no se vacían.

## Fuentes leídas

- G. J. Wirsching, *On the problem of positive predecessor density in 3n+1
  dynamics*, DCDS 9 (2003) 771–787. Se leyó entera la versión preliminar del
  autor (`posden.pdf`, de su página en Bielefeld; 18 págs.).
- R. A. Tavares, *Wirsching's Positive-Predecessor-Density Program: Proofs of
  Conjectures 1 and 3*, arXiv:2608.27617v1 (27-08-2026), sin arbitrar. Se
  leyeron la introducción, el §3 (la cadena), el §4 (conjetura 1) y los §§11–12.
  No se auditaron los §§5–10, que son el análisis de φ y de Berg–Krüppel.

## La cadena y lo que queda

Mapa del atajo `T`. La función Elka `e_ℓ(k,a)` cuenta los caminos
`b → … → a` con k pasos `n/2` y ℓ pasos `(3n+1)/2`. Depende de `a mod 3^ℓ` y su
media de Haar sobre las unidades es `ē_ℓ(k) = C(k+ℓ,k) / (2·3^{ℓ−1})`. La
ventana es `A_δ = {(k_ℓ) : |k_ℓ − ℓ| ≤ δ√ℓ}`.

| Eslabón | Enunciado | Estado |
|---|---|---|
| Teorema 1 | (⋆1) ⇒ densidad positiva uniforme de predecesores | Wirsching |
| Conjetura 1 | (⋆2) ⇒ (⋆1) | Tavares, teorema 4.3 |
| Teorema 2 | (⋆3) ⇒ (⋆2) | Wirsching; prueba en Tavares §3 |
| Conjetura 2 | (⋆4) ⇒ (⋆3) | **abierta** |
| Conjetura 3 | (⋆5) y (⋆5) ⇒ (⋆4) | Tavares, teoremas 10.1 y 11.1 (µ = 1/3) |

Se separan así las tres piezas que pedía el plan:

- **Operador límite.** `W3`, su densidad invariante φ y (⋆4). No contienen
  información por residuo: Tavares cierra esta parte.
- **Control por residuos.** (⋆3) para los generadores `g_ℓ`, o (⋆1) para
  `e_ℓ`: `e_ℓ(k_ℓ,a) ≥ µ·ē_ℓ(k_ℓ)` para toda unidad a y todo `(k_ℓ) ∈ A_δ`.
  Es lo único abierto.
- **Densidad de los predecesores reales.** El teorema 1 pasa de (⋆1) para el
  entero a a la cota `≥ c/a`.

**Reformulación exacta** ([reformulacion.py](reformulacion.py)):

```text
e_ℓ(k, a) = #{ 0 ≤ d_0 ≤ … ≤ d_{ℓ−1} ≤ k :  Σ_{i<ℓ} (3/2)^i · 2^{−d_i} ≡ 2a  (mod 3^ℓ) }.
```

Es una suma de Syracuse con huecos arbitrarios, evaluada en una clase fija.
Añadir pasos pares al principio del camino conserva su extremo, así que
`e_ℓ(k+1,a) ≥ e_ℓ(k,a)`. También `g_ℓ ≤ e_ℓ`, porque `e_ℓ = p_ℓ * g_ℓ` con
`p_ℓ(0) = 1`. Por tanto, un cero de `e` es también un cero de `g`.

## Instancia limitada: cálculos exactos

Todos son finitos y en enteros. El coste mínimo es
`c_ℓ(a) = min{k : e_ℓ(k,a) > 0}`, y el exceso es `c_ℓ(a) − ℓ`.

1. **Hay ceros en `k = ℓ` en todos los niveles** ([costo.py](costo.py),
   [salida](costo_salida.txt)). Número de unidades con `c_ℓ > ℓ`:
   2, 7, 20, 58, … y 1.963.154 en `ℓ = 16`. Su fracción baja del 37 % al
   6,8 %, pero su número crece. El exceso máximo es 4 o 5 en todos los
   niveles hasta 16.
2. **El entero 34.** No tiene ningún predecesor con ℓ impares y a lo sumo ℓ
   pares para `2 ≤ ℓ ≤ 16`. Sus excesos son 2, 2, 3, 2, 2, 1, 2, 2, 3, 2, 3, 2,
   2, 2, 1. Lo confirman dos métodos independientes: la programación dinámica
   sobre residuos y una búsqueda en profundidad sobre enteros
   ([predecesores_34.py](predecesores_34.py), [salida](predecesores_34_salida.txt)).
   Aun en `k = ℓ + 3` la cuenta es mínima: `e_16(19, 34) = 9` frente a una
   media de 141,5. Al 7 le pasa lo mismo para `4 ≤ ℓ ≤ 13`, y es positivo desde
   `ℓ = 14`.
3. **La dispersión crece** ([dispersion.py](dispersion.py),
   [salida](dispersion_salida.txt)). Con `r = e/ē` y peso uniforme en las
   unidades, `M2 = E[r²]` en `k = ℓ` pasa de 1,67 a 2,71 para ℓ = 2..14, a unas
   0,075 por nivel. En `k = ℓ + ⌊√ℓ⌋` pasa de 1,32 a 1,84. La mediana baja
   despacio (0,72 en ℓ = 14) y el 10 % más cargado reúne el 41 % de la masa.
4. **Conjuntos encajados.** `S_ℓ` son las clases malas en todos los niveles
   de `[8, ℓ]` ([densidad_malos.py](densidad_malos.py), [salida](densidad_malos_salida.txt),
   [reformulacion.py](reformulacion.py)). Sus tamaños son 1.217, 2.841, …,
   1.247.348 en `ℓ = 16`. Cada clase conserva de media entre 2,3 y 2,4
   elevaciones malas, con tasa `#S_ℓ/(3·#S_{ℓ−1})` entre 0,76 y 0,81, que baja
   despacio. Los conjuntos malos no cortan todas las clases módulo `3^m`: en
   `m = 4` faltan 7 de 54.
5. **Cotejos.** `elka.py` compara la recurrencia con la enumeración de todas
   las palabras (`ℓ ≤ 7`) y con `Σ_a e = C(k+ℓ,k)` ([salida](elka_salida.txt)).
   La reformulación monótona coincide con la recurrencia para `ℓ, k ≤ 6`.

## Lectura

**Reducción (demostrada, elemental).** Si un 3-ádico `a*` cumple
`e_ℓ(ℓ, a*) = 0` para infinitos ℓ, entonces:

- con `k_ℓ = ℓ`, que está en `A_δ` para todo δ,
  `lim inf e_ℓ(ℓ,a*)/ē_ℓ(ℓ) = 0`, y (⋆1) falla en `a*` para todo δ y µ, tanto
  en la lectura global como en la de cada unidad;
- (⋆3) también falla, porque `g ≤ e`;
- si (⋆4) es cierta (Tavares, teorema 11.1), la conjetura 2 es falsa tal como
  está escrita sobre `Z_3^×`.

Los `S_ℓ` son cerrados y abiertos y están encajados. Si ninguno es vacío, por
compacidad existe un `a*` malo en todo nivel `ℓ ≥ 8`. Hasta `ℓ = 16` no se
vacían, y crecen.

**Heurística de cascada (no demostrada).** Hacia atrás,
`r_ℓ(a) = Σ_j w_j · r_{ℓ−1}(hijo_j)`, con `w_j ≈ 3·2^{−(j+1)}` sobre los j
admisibles. El hijo es un múltiplo de 3 en un tercio de los casos. Así:

- `E[Σ w_j · [vivo]] = 1`, que es la normalización;
- `E[Σ w_j² · [vivo]] = 1` exactamente: la cascada está en el punto crítico
  de `L²`, y su varianza crece linealmente, como la `M2` medida;
- `E[Σ w log w] = log(3/4) < 0`: el límite no es degenerado, pero tiene cola
  pesada de índice 2.

Como heurística, esto predice que `r_ℓ(a)` converge a un límite positivo para
casi toda a, pero sin cota inferior uniforme en a. La lectura global de
(⋆1), que es la que Wirsching necesita para su constante uniforme, fallaría;
la lectura por unidad podría valer para casi toda a.

**Para el laboratorio.** El cruce 3 (Wu 1 equivale a Collatz) sólo necesita
densidad positiva de los predecesores de cada entero, sin uniformidad. El
argumento del teorema 1 sigue funcionando con una ventana desplazada,
`k − ℓ ∈ [C, C + δ√ℓ]`, y µ dependiente del entero a. Lo que falta es una cota
inferior local de la suma de Syracuse en una clase fija: un teorema local
límite. El decaimiento de Fourier de Tao (`n^{−A}`) no llega a eso.

## Decisión y candidatas

La sesión entrega una obstrucción precisa a la cadena literal: ceros exactos
en todos los niveles calculados, y una reducción limpia de la refutación de
la conjetura 2 a que los `S_ℓ` no se vacíen. Esto cambia la valoración: la
conjetura 2 no es una ruta prometedora hacia la densidad. La versión útil para
el laboratorio es por entero y con ventana desplazada.

Candidatas, sin demostrar:

- **W1.** Demostrar que `S_ℓ ≠ ∅` para todo ℓ, o construir `a*`. Refutaría la
  conjetura 2 tal como está escrita. Evidencia: los `S_ℓ` hasta 16.
- **W2.** Formular (⋆1′): ventana desplazada y µ(a) por entero. Medir
  `e_ℓ(k,a)/ē_ℓ(k)` para enteros pequeños en `k − ℓ ∈ [C, C + √ℓ]`.

## Sesión 2 (30-09): W2 medida y candidatos a W1

**W2, ventana desplazada en enteros fijos** ([ventana_desplazada.py](ventana_desplazada.py),
[salida](ventana_desplazada_salida.txt)). Una búsqueda sobre enteros, sin
residuos, da la tabla completa `e_i(c,a)` para `i <= 21`. Se mide el mínimo de
`r = e/ē` en `k − ℓ ∈ [6, 6 + ⌊√ℓ⌋]`, por encima de todo exceso medido. Para
los ocho enteros probados ese mínimo baja despacio entre `ℓ = 6` y `ℓ = 21`:

| a | 5 | 7 | 11 | 13 | 17 | 34 | 43 | 56248 |
|---|---|---|---|---|---|---|---|---|
| ℓ = 6 | 0,80 | 0,42 | 1,30 | 1,09 | 1,49 | 0,31 | 0,61 | 0,26 |
| ℓ = 21 | 0,49 | 0,23 | 0,82 | 0,95 | 1,20 | 0,117 | 0,46 | 0,056 |

En 7, 34 y 43 el descenso se frena en los últimos niveles; en 5 y 11, no.
Es compatible con límites positivos a los que se llega despacio (la cascada
no degenerada) y también con un decaimiento lento. No decide W2.

**Candidatos racionales a W1** ([racionales_malos.py](racionales_malos.py),
[salida](racionales_malos_salida.txt)). De los racionales `p/q` con
`|p| <= 400` y `q <= 40`, 399 son malos en todos los niveles de `[8, 16]`, y
muchos en todos los de `[2, 16]`. Por ejemplo, `347/2` y `−49/20` terminan con
exceso 3, y el entero negativo −164 cuelga del ciclo de −17. Para `q` impar,
el árbol hacia atrás de `p/q` es el de predecesores de p en la dinámica
`3x+q`, cuya heurística genérica predice un coste por paso menor que 1 a la
larga. Son candidatos a estudiar, no una prueba.

**Decisión del bloque.** La obstrucción precisa cambia la valoración: la
cadena de Wirsching tal como está escrita no es una ruta prometedora hacia
Wu 1. Su versión útil (W2) equivale a un teorema local límite para la suma de
Syracuse en clases fijas, fuera del alcance de las herramientas conocidas. W1
es una pregunta matemática interesante, que refutaría una conjetura
publicada, pero no está en el camino hacia Wu 1. **Se cierra Wirsching tras
dos sesiones y el siguiente bloque es CST.** W1 y W2 quedan registradas como
candidatas.

## Reproducir

Desde esta carpeta, todo en menos de 5 minutos:

```text
python -B -X utf8 elka.py
python -B -X utf8 costo.py
python -B -X utf8 dispersion.py
python -B -X utf8 densidad_malos.py
python -B -X utf8 predecesores_34.py
python -B -X utf8 reformulacion.py
python -B -X utf8 ventana_desplazada.py
python -B -X utf8 racionales_malos.py
```

Los PDF leídos no se suben; están en la página de Wirsching y en arXiv.
