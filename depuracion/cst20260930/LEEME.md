# CST por número de rachas: Ocelotas — 30-09-2026

Bloque 4 del [plan por sesiones](../transversal20260927/PLAN_SESIONES_20260928.md),
que la [segunda opinión](../transversal20260927/SEGUNDA_OPINION_20260928.md)
proponía como frente principal. El objetivo candidato era el caso de dos rachas
impares, y está cerrado.

**Revisión posterior:** [extensión exacta hasta diez rachas](REVISION_RACHAS.md),
bajo `RhinEntera`, con prueba escrita, criba entera y cotejo independiente.
El [cierre en Lean](CIERRE_LEAN.md) certifica la criba, el descenso finito
y el teorema `ocelotas_diez` para palabras reales `Palabra`, con Rhin
explícita. La [interfaz del contador](CONTADOR_LEAN.md) extrae esa palabra
y prueba `cst_contador`: primer descenso = primer cruce hasta diez rachas.
El teorema original de dos rachas se conserva abajo.

**Teorema (Ocelotas, bajo `RhinEntera`).** Sea `T(n) = n/2` (par), `(3n+1)/2` (impar), y sea
`k = τ(n)` el primer cruce del coeficiente: `3^{S_j} ≥ 2^j` para `1 ≤ j < k` y
`3^{S_k} < 2^k`, donde `S_j` cuenta los pasos impares entre los j primeros. Si
`n ≥ 2` y su palabra de paridad de longitud k es `1^a 0^b 1^c 0^d` (dos rachas
impares, `a, b, c, d ≥ 1`), entonces `T^k(n) < n`. Por tanto, la conjetura CST
de Terras, `t(n) = τ(n)`, vale para todas esas n, con exponentes sin cota.

La prueba usa la cota de Rhin (1987) para `|k log 2 − q log 3|` y dos cálculos
finitos. Está formalizada en Lean ([Ocelotas.lean](Ocelotas.lean)); la única
hipótesis externa es la forma entera de Rhin, que figura explícita en el
enunciado.

## Literatura (sesión 1)

- La conjetura CST es de Terras (1976), y el nombre, de Lagarias. Rozier y
  Terracol la verifican para `n <= 2,8·10^19` (arXiv:2502.00948v5, corolario
  5.4; publicado en Discrete Math. 2026).
- Su apéndice A excluye las sucesiones paradójicas con un solo máximo local
  (una racha): el argumento elemental trata el caso acíclico, y el cíclico usa
  la exclusión conocida de circuitos mediante teoría trascendente.
  Su observación 5.5, sugerida por
  Simons, propone estudiar CST por número de máximos locales, como Simons y de
  Weger (2005) hicieron con los ciclos.
- Una búsqueda rápida no encontró el caso de dos máximos para CST. El
  preprint arXiv:2605.13886 (Niu, retirado) no lo trata. **La novedad no está
  certificada.**

## Prueba escrita

Notación: `q = a + c`, `P = 3^q`, `Δ = 2^k − P`, `y_i` los valores al final de
cada racha.

1. **Primer cruce.** El prefijo de longitud `a + b` tiene a impares, así que
   `2^{a+b} ≤ 3^a`; el de longitud `k − 1`, q impares, así que `2^{k−1} ≤ P`; y
   `P < 2^k`. Las dos primeras son estrictas por paridad.
2. **Tramos.** En una racha impar, `T(y) + 1 = 3(y+1)/2`; en una par, `T(y) = y/2`.
   Por tanto `2^a (y_1 + 1) = 3^a (n+1)`, `2^b y_2 = y_1`,
   `2^c (y_3 + 1) = 3^c (y_2 + 1)` y `2^d y_4 = y_3`, con `y_4 = T^k(n)`.
3. **Identidad.** `2^k T^k(n) = P n + B`, con
   `B = 3^c (3^a − 2^a) + 2^{a+b} (3^c − 2^c) < 2P`, porque `2^{a+b} < 3^a`.
4. **Fallo.** `T^k(n) ≥ n ⟺ Δ n ≤ B`.
5. **Congruencias.** Como `2^a` y `3^a` son coprimos, `2^a ∣ n + 1`, luego
   `n ≥ 2^a − 1`. Del mismo modo `2^c ∣ y_2 + 1`, y
   `2^{a+b} y_2 + 2^a = 3^a (n+1)`.
6. **Núcleo** (`nucleo`). Sean `u = 2^a` y `v = 2^c`. De 4 y 5 salen
   `u Δ < 3P` y `u v Δ < 2·3^a·P`. Como `3^a < u²`, queda
   `2^q Δ³ < 18·27^q`.
7. **Rhin.** Para `2^{k−1} ≤ 3^q < 2^k`, `Λ = k log 2 − q log 3 ∈ (0, log 2]`, y
   Rhin da `Λ ≥ k^{−13,3}` (`H = max(k, q) = k ≥ 2`). Entonces
   `Δ = P(e^Λ − 1) ≥ PΛ ≥ P k^{−14}`: es la forma entera `RhinEntera`. Con 4 da
   `n < 2k^14`. De ahí `2^a ≤ 2k^14`, `2^c < 3k^28` y `P < 36 k^84`, así que
   `2^k < 2P < 72 k^84`. Como `72 k^84 < 2^k` para `k ≥ 1024` (`poli_exp`),
   resulta `k <= 1023` y `q <= 645`.
8. **Primer cálculo** (`finito_q`). Para cada `q <= 645`, con
   `k = ⌊log2 3^q⌋ + 1` (el único posible, `k_de_q`), vale una de dos: o bien
   `18·27^q <= 2^q Δ³`, que contradice 6, o bien `k <= 27` y `2·3^q <= 51 Δ`.
   En el segundo caso, `Δn <= B < 2P <= 51 Δ` da `n <= 50`. El test por q sólo
   deja pasar q = 0, 1, 2, 3, 4, 5, 6, 8, 10 y 17.
9. **Segundo cálculo** (`finito_n`). CST para `2 <= n <= 50` con `τ(n) <= 27`.

El caso más ajustado de toda la familia es `n = 39`, con palabra `1^3 0^1 1^2 0^2`,
`k = 8` y `T^8(39) = 38`.

## Formalización

[Ocelotas.lean](Ocelotas.lean): Lean 4.32.2 con la Mathlib del proyecto de Gao;
se compila con `lake env lean` en unos 30 s ([registro](lean_local.txt)).

- `ocelotas` depende de `propext`, `Classical.choice` y `Quot.sound`.
- Los dos cálculos finitos se hacen en el núcleo con `decide +kernel` y dependen
  sólo de `propext`.
- Definiciones en el enunciado: `T`, `S`, `PrimerCruce` (τ(n) = k),
  `DosRachas` (palabra `1^a 0^b 1^c 0^d`) y `RhinEntera`.
- Los `#guard` finales comprueban `T^8(39) = 38` y el primer cruce de 39 en 8.

**Lean certifica el enunciado, no su interpretación**, y la hipótesis
`RhinEntera` se apoya en un teorema publicado con demostración asistida por
ordenador (Rhin, *Approximants de Padé et mesures effectives
d'irrationalité*, Progr. Math. 71, 1987). El mismo resultado se usa en la
literatura de ciclos. `RhinEntera` se comprobó además numéricamente, con enteros
exactos, para `q <= 20000`.

## Cotejos independientes

- [dos_rachas.py](dos_rachas.py) ([salida](dos_rachas_salida.txt)) usa la cota
  de Rhin literal, que da `k <= 492`, y una mil veces más conservadora, que da
  `k <= 539`. Recorre las 3.803.188 ternas con `k <= 539`, con el menor
  representante de cada clase (`r = −B·3^{−q} mod 2^k`): no hay ningún
  contraejemplo, y el menor cociente `Δ n_min / B` es 2,02, en `n = 39`.
- [cotejo_dos_rachas.py](cotejo_dos_rachas.py) ([salida](cotejo_dos_rachas_salida.txt))
  hace dos comprobaciones. La primera toma 20.000 ternas al azar, construye el
  representante bit a bit con la identidad de Terras y lo itera directamente:
  la palabra, el primer cruce y el descenso cuadran. La segunda barre todos los
  `n < 2^22` y encuentra 306.857 semillas de dos rachas (211 ternas) y
  1.496.791 de una: la caracterización cuadra y todas descienden.
- [supervivientes.py](supervivientes.py) ([salida](supervivientes_salida.txt)):
  con la forma entera de Rhin y los filtros de congruencia, de las 13.328.215
  ternas con `k <= 819` sólo sobreviven 5, todas con `k <= 8`, y sus menores
  representantes (11, 219, 39, 175 y 79) descienden.

## Alcance

- Cubre todas las n cuya palabra hasta τ(n) tiene exactamente dos rachas
  impares, a cualquier escala. Es una familia infinita de clases y de enteros.
  Recupera, como control, el caso de una racha de Rozier–Terracol en el
  barrido, pero no lo formaliza.
- No demuestra CST en general, ni Collatz. Bajo `RhinEntera`, el caso de dos
  rachas excluye contraejemplos con menos de tres; la extensión escrita
  posterior eleva ese mínimo a once; Lean ya lo prueba mediante el contador
  directo de rachas, bajo Rhin.
- El método (Rhin, congruencias de cada racha, un test por q y un cálculo
  final pequeño) es el de Simons y de Weger para ciclos, trasladado al
  descenso.

## Extensión exacta y siguiente paso

La [revisión](REVISION_RACHAS.md) desarrolla la prueba general y sustituye
el cálculo aproximado por `3^5 < 2^8`, racionales y comparaciones enteras.
Para hasta diez rachas, bajo `RhinEntera`, obtiene `k < 131072`; la criba
deja 888 valores de q y obliga a `n <= 11214`. Todas esas semillas
descienden en su primer cruce. El cotejo independiente usa otra criba,
con 1023 supervivientes, y obtiene el mismo límite.

Evidencia: [certificador](certificar_rachas.py),
[certificado](certificado_10_rachas.json),
[cotejo](cotejar_certificado_rachas.py), [salida](cotejo_10_rachas.json) y
[núcleo Lean](OcelotasRachas.lean) ([compilación](lean_revision_rachas.txt)).
La [segunda tanda](TRAYECTORIAS_LEAN.md) formaliza desde la palabra real las
congruencias, la cota aditiva y **k<131072 bajo Rhin**, además de la interfaz
con la criba ([Lean](OcelotasTrayectorias.lean),
[compilación](lean_trayectorias.txt)).
La [tercera tanda](FINITO_LEAN.md) certifica el descenso para cada
2<=n<=11214, sin Rhin, y demuestra el ensamblaje con una condición
aritmética explícita ([Lean](OcelotasFinito.lean), [compilación](lean_finito.txt)).
La [cuarta tanda](CIERRE_LEAN.md) demuestra esa condición para
1<=q<=82696 y cierra el ensamblaje: `ocelotas_diez` ya no recibe `hcriba`.
Siete módulos compilaron sin `sorryAx` ([registro](lean_cierre.txt)).
La [quinta tanda](CONTADOR_LEAN.md) construye `Palabra` desde el contador
canónico y prueba que no hay descenso antes del cruce. Ocho módulos
compilan sin `sorryAx` ([registro](lean_contador.txt)).
**Siguiente:** auditar el rango y las constantes de Rhin contra la fuente
original y estudiar su descarga en Lean; revisión humana pendiente.

Se conservan los estudios preliminares [r_rachas.py](r_rachas.py)
([salida](r_rachas_salida.txt)) y [r_rachas_fino.py](r_rachas_fino.py)
([salida](r_rachas_fino_salida.txt), [r=17,...,20](r_rachas_fino_17_20.txt)),
como exploración. Su aritmética aproximada no certifica redondeo dirigido.
Los barridos anteriores [hasta 2^22](verificar_r_rachas_salida.txt) y
[hasta 2^23](verificar_r_rachas_23_salida.txt) se preservan; la salida
`verificar_r_rachas_29_salida.txt` vacía no acredita un cálculo terminado.

## Reproducir

```text
python -B -X utf8 dos_rachas.py           # unos 25 s
python -B -X utf8 cotejo_dos_rachas.py    # unos 65 s
python -B -X utf8 supervivientes.py       # unos 25 s
```

Desde `depuracion/gao20260920/formal`:

```text
lake env lean ../../cst20260930/Ocelotas.lean
```
