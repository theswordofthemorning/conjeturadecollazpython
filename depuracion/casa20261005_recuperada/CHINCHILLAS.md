# Chinchillas: Korec y el ahorro de potencia

05-10-2026. Ruta B, a continuación del [retrato del fugitivo](CORZAS.md).
Todo está demostrado en Lean 4.32.2 sin hipótesis externas, con axiomas
estándar: [CasaKorec.lean](CasaKorec.lean) y
[CasaPotencia.lean](CasaPotencia.lean).

## Korec (1994): casi todo número baja por debajo de `n^c`

Mapa: el atajo `T(n)=n/2` si n es par y `(3n+1)/2` si es impar. Para
`p ≤ q` con `3^q < 4^p`, sea `altos p q N` el conjunto de los `n < N`
cuya órbita nunca baja de `n^(p/q)`, es decir, `n^p ≤ T^j(n)^q` para todo
j.

| Teorema | Enunciado |
|---|---|
| `korec` | si `3^q < 4^p` y `p ≤ q`, la proporción de `altos p q N` entre los `n < N` tiende a 0 |
| `korec_cuatro_quintos` | caso `c = 4/5`: casi todo número baja por debajo de `n^0,8` |
| `korec_cerca_del_umbral` | caso `c = 191/241 ≈ 0,79253`, a menos de 5·10⁻⁵ del umbral |
| `allouche` | caso `c = 0,87`; Allouche (1979) lo probó para `c > 0,869` |

`3^q < 4^p` equivale a `p/q > log 3/log 4 ≈ 0,79248`. Entre dos reales
siempre hay un racional, así que `korec` cubre todo exponente real
`c > log 3/log 4`. Ese es el teorema de Korec. El enunciado con potencias
reales no está escrito en Lean porque esta instalación no tiene
compilados los módulos de logaritmos de Mathlib. Con `p = q` se recupera
«casi todo número baja de sí mismo» (Terras 1976, Everett 1977).

### Cómo se prueba, en palabras

- **Varianza binomial.** `momento_dos`:
  `∑_{r<2^K} (2 S_K(r) − K)² = K 2^K`. Se prueba por inducción con
  `suma_transferencia`. Cada residuo módulo `2^(K+1)` es `2s` (sin
  subida) o `2s+1`; este último sube una vez y sigue en `3s+2`, que
  recorre todos los residuos módulo `2^K`.
- **Chebyshev.** `cota_chebyshev`: a lo sumo `K 2^K/(2t)²` residuos
  tienen `2 S_K ≥ K + 2t`. Con `k = 2(E+1)m` pasos y umbral `(E+2)m`,
  la proporción de residuos con demasiadas subidas es a lo sumo
  `(E+1)/(2m)` (`cota_muchas`).
- **Bajar de una potencia.** `baja_de_potencia` es la cota superior de
  Terras (`cota_superior`): si `S_k(n) ≤ s`, `n ≥ 3^(k−s)` y
  `2^q 3^(sq) n^(q−p) ≤ 2^(kq)`, entonces `T^k(n)^q < n^p`.
- **La cuenta.** `korec_cota`: `m · #altos ≤ (E+2) N` cuando
  `2^k ≤ N` y se cumple la condición de potencias. Se elige E con
  `3^((E+2)q) < 4^((E+1)p)` (`potencias_ganan`) y
  `m = log_{4^(E+1)} N`, y la proporción queda por debajo de
  `(E+2)/m → 0`.

### La barrera de los métodos 2-ádicos

Con k ≈ log₂ n pasos se gastan todos los bits de n. Un número típico
tiene cerca de k/2 subidas, y entonces
`T^k(n) ≈ n (√3/2)^k = n^(log 3/log 4)`. Repartir los pasos en etapas no
mejora el exponente: cada paso gasta un bit y, en promedio, multiplica
por `√3/2`. En el cotejo, para n en `[2^19, 2^20)`, la mediana de
`log T^20(n) / log n` es 0,788. Bajar de ese exponente exige información
3-ádica, como en Tao (2019).

### No es una cota práctica

La prueba es asintótica. Para `c = 4/5`, el primer N que cubre tiene unos
117 438 dígitos ([cotejo](cotejo_korec.json)). El teorema dice que la
proporción tiende a 0, no cuándo se hace pequeña.

## Ahorro de potencia: los que nunca bajan son a lo sumo `14,5 N^0,969`

| Teorema | Enunciado |
|---|---|
| `fugitivos_potencia` | para `N ≥ 2`, `#fugitivos(N)^20 < (2N)^19`: menos de `(2N)^0,95` fugitivos bajo N |
| `noDescienden_potencia` | para `N ≥ 2`, `#noDescienden(N)^32 < 5^32 · 3^31 · N^31`: menos de `14,5 N^(31/32)` números bajo N nunca bajan de sí mismos |
| `fallasCST_potencia` | para `N ≥ 2`, la conjetura CST de Terras falla en menos de `14,5 N^(31/32)` números bajo N |
| `contraejemplo_minimo_no_baja` | el menor contraejemplo de Collatz, si existe, nunca baja de sí mismo |
| `potencia_de_bloques` | la misma cota para toda propiedad *bloqueable*: si `n ≥ 3^J` la tiene, su pronóstico no cruza en el paso J |
| `bloques_tres` | `#{n < 3^J : P n} ≤ 5 (3ρ)^J`, con `3ρ ≈ 2,898` |

El menor contraejemplo, si existe, está en un conjunto con a lo sumo
`14,5 N^0,969` elementos bajo N. Lo mismo vale para las fallas de CST
(`fallasCST_iff`: primer cruce k sin bajar en el paso k), es decir, CST
vale para casi todo n con ahorro de potencia. Ambas cotas son más fuertes
que la densidad 0 de Terras y Everett, que no da ninguna potencia.

- **Fugitivos.** Si `n < N ≤ 2^K`, n es su propio residuo módulo `2^K`.
  Un fugitivo es entonces un residuo sin cruce a los K pasos
  (`fugitivos_en_sinCruce`), y hay a lo sumo `((1+√3)/√2)^K` de ellos.
  El exponente `log₂((1+√3)/√2) ≈ 0,94998` cumple
  `((1+√3)/√2)^20 < 2^19` (`razon_fugitivos`). Difiere en 3·10⁻⁵ de la
  entropía `H(log 2/log 3) ≈ 0,94996`, el exponente óptimo de Chernoff
  para ese umbral.
- **Los que nunca bajan y las fallas de CST.** En el bloque
  `[3^J, 3^(J+1))` todo número es `≥ 3^J`. Si no baja, su pronóstico
  tampoco cruza en el paso J (`desciende_de_grande`). Una falla de CST
  tiene su primer cruce después de J (`fallaCST_bloqueable`). En los dos
  casos la propiedad es bloqueable, y el bloque aporta a lo sumo
  `6 (3ρ)^J` (`bloque_paso`). Al sumar los bloques sale `5 (3ρ)^J`, y
  `(3ρ)^32 < 3^31` (`razon_potencia`).

En los datos ([cotejo](cotejo_potencia.json)), los candidatos del bloque
J = 10 son 20 297, frente a la cota por residuos 30 448 y la cota final
`6 (3ρ)^10 ≈ 250 497`. Por órbitas directas, bajo `3^11 = 177 147` sólo
0 y 1 nunca bajan y sólo 0 y 1 fallan en CST, y todo número tiene primer
cruce. Las cotas acotan contraejemplos
posibles, no observados.

## Bajo LMN: el exponente baja a 0,95

[CasaLMN.lean](CasaLMN.lean). Toma como hipótesis explícita `LMNEntera`,
la forma entera del corolario de Laurent–Mignotte–Nesterenko (1995):
`3^q ≤ (2^k − 3^q) 2^(19(t+33)²)` cuando `2^k ≤ 2·3^q`, `3^q < 2^k` y
`k < 2^(t+1)`. Es el enunciado de `OcelotasLMN.cola_lmn_entera`, que lo
deduce de `LMNDebil` en la carpeta de CST. Ese enlace usa logaritmos
reales y no se compila en esta instalación. La hipótesis es un argumento
de los teoremas, no un axioma.

| Teorema | Enunciado |
|---|---|
| `falla_acotada` | una falla de CST `n ≥ 2` con primer cruce k cumple `n 2^(k−1) < 3^k 2^(19(t+33)²)` |
| `falla_tardia` | si además `n ≥ 2^125000`, entonces `2n < 2^k`: el primer cruce llega después de `log₂ n + 1` pasos |
| `fallasCST_lmn_potencia` | por encima de `2^125000`, las fallas de CST bajo N cumplen `#^20 < 3^20 (2N)^19` |
| `noDescienden_lmn_potencia` | por encima de `2^125000`, los que nunca bajan bajo N cumplen `#^20 < 4^20 (2N)^19` |

**Cómo se prueba.** Sea `D = 2^k − 3^q`.

1. **La cota de la falla.** La desigualdad de la grieta (`CasaDomino`)
   da `D n < 3^k`. Como el último paso del cruce es par
   (`cruce_justo`), `2^(k−1) ≤ 3^q`, y LMN da `3^q ≤ D 2^E`. Juntando
   las tres, `n 2^(k−1) < 3^k 2^E`.
2. **Cruce largo.** Si `2n ≥ 2^k` y `k ≥ 2^17`, de ahí sale
   `4^k < 3^k 2^(E+2)`. Eso contradice `tres_cuatro_k`, probado por
   inducción en t desde un caso base comprobado en el núcleo con
   `decide +kernel`.
3. **Cruce corto.** Si `k < 2^17`, la misma cota obliga a
   `n < 2^125000` (`tres_dos_k`).
4. **La cuenta.** Por encima de `2^125000`, una falla bajo `2^K` es un
   residuo sin cruce a los K pasos (`falla_en_sinCruce`), y vale la
   cuenta de los fugitivos.

Bajo LMN, los candidatos a menor contraejemplo grandes son tan raros como
los fugitivos: exponente `0,95` en vez de `31/32`. La cota `2^125000` es
holgada. En `k ≤ 3000`, el peor `log₂(3^q/D)` real es 10, frente a los
36 784 que permite la hipótesis ([cotejo](cotejo_lmn.json)).

## Contraste independiente

Todo con enteros exactos y órbitas directas, sin la recursión de las
pruebas Lean:

- [cotejar_korec.py](cotejar_korec.py) ([salida](cotejo_korec.json)):
  - `momento_dos` y `cota_chebyshev` para K ≤ 18 (190 casos);
  - el conteo por residuos (273 casos) y `cota_muchas` (67 casos);
  - `baja_de_potencia` en barrido exhaustivo de n < 2000, k ≤ 20 y
    `p ≤ q ≤ 4` (79 960 casos con las hipótesis);
  - `condicion` en el peor caso N (384 casos);
  - el umbral efectivo y la ilustración de la barrera.
- [cotejar_potencia.py](cotejar_potencia.py) ([salida](cotejo_potencia.json)):
  - las tres constantes en `ℤ[√3]`;
  - `c_K^20 < 2^(19K)` para K ≤ 20;
  - los bloques J ≤ 10;
  - las órbitas directas bajo `3^11`, también para las fallas de CST.
- [cotejar_lmn.py](cotejar_lmn.py) ([salida](cotejo_lmn.json)):
  - las dos bases gigantes con enteros de Python (márgenes de 6897 y
    2707 bits);
  - el paso de inducción para t ≤ 10⁵;
  - `cruce_justo` en 99 999 primeros cruces;
  - la holgura de `LMNEntera` para k ≤ 3000.

## Evidencia y reproducción

[comprobar_fugitivo.py](comprobar_fugitivo.py) compila desde las fuentes,
en una carpeta temporal nueva y sin cachés, los ocho módulos de Ocelotas
que importa `CasaPlano` y los ocho módulos de la casa, con CasaKorec y
CasaPotencia incluidos ([evidencia](evidencia_fugitivo.json)). Desde la
raíz:

```text
python -B -X utf8 depuracion/casa20261004/comprobar_fugitivo.py --salida depuracion/casa20261004/evidencia_fugitivo.json
python -B -X utf8 depuracion/casa20261004/cotejar_korec.py --hasta 18 --salida depuracion/casa20261004/cotejo_korec.json
python -B -X utf8 depuracion/casa20261004/cotejar_potencia.py --salida depuracion/casa20261004/cotejo_potencia.json
```

## Límites

- Nada aquí afirma Collatz, Wu 1 («casi todo número llega a 1») ni que
  los conjuntos acotados sean vacíos o finitos.
- CasaLMN depende de `LMNEntera`; el resto de esta nota no usa
  hipótesis externas.
- Los teoremas de Korec (1994) y Allouche (1979) son conocidos; sus citas
  son de memoria, como en el resumen de Lagarias, y falta cotejar los
  originales. El ahorro
  de potencia sale directamente del conteo de Chernoff y puede estar en la
  literatura; no se ha cotejado. Lo propio es la formalización. No se
  reclama prioridad.
- Revisión humana pendiente. Lean certifica los enunciados, no su
  interpretación.
