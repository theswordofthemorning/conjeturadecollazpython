# Alpacas: rachas arbitrariamente largas de la misma altura (Garner 1985)

26-09-2026. **Demostrado en Lean** (`GarnerEnunciado.conjetura_garner`), con
axiomas `propext`, `Classical.choice` y `Quot.sound`. **Pendiente de revisión
humana**, como la conjetura de Gao de la que depende.

## Enunciado

Mapa clásico `C(n)=n/2` si n es par, `3n+1` si es impar. Se usan las
definiciones de Gao (1993, pág. 262):

- `height(n)` es el mínimo k con `C^k(n)=1`;
- el tiempo total de parada `σ∞(n)` es «el número de divisiones por 2
  hasta llegar a 1».

**Teorema (Alpacas).** Para cada L y cada N hay un `n>=N` tal que los L+1
consecutivos `n, n+1, …, n+L` tienen todos la misma altura y el mismo
tiempo total de parada.

Es la conjetura (2) de Garner, según la bibliografía anotada de Lagarias
(entrada 72): «arbitrarily long runs of integers of the same height occur».
Gao la recoge con altura y `σ∞` iguales y la atribuye a Garner y a Penning:
«It has been conjectured that there exist arbitrarily long sets of
consecutive numbers of the same height and the same σ∞(n) [1, 5]».

En Lean ([GarnerEnunciado.lean](../gao20260920/formal/GarnerEnunciado.lean)):

```lean
def C (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else 3 * n + 1
def altura (n h : ℕ) : Prop := C^[h] n = 1 ∧ ∀ k, k < h → C^[k] n ≠ 1
def mitades (n h : ℕ) : ℕ := ((Finset.range h).filter (fun k => C^[k] n % 2 = 0)).card
def FormaGarner : Prop :=
  ∀ L N : ℕ, ∃ n h s : ℕ, N ≤ n ∧ ∀ i, i ≤ L → altura (n + i) h ∧ mitades (n + i) h = s
theorem conjetura_garner : FormaGarner
```

Con `altura n h`, `mitades n h` es exactamente `σ∞(n)`. Tres `#guard` del
mismo archivo recalculan con estas definiciones los ejemplos de Gao:

| Racha | Altura | `σ∞` |
|---|---|---|
| 943 a 949 | 36 | 26 |
| 7083 a 7099 (Penning) | 57 | 40 |
| 57346 a 57370 | 78 | 54 |

Si alguno no coincidiera, el archivo no compilaría.

## Prueba

Atajo `T(x)=x/2` o `(3x+1)/2`. Para `r<2^t`, Terras (1976) da
`T^t(2^t·u+r)=3^a·u+A` para todo `u>=0`. Aquí a es el número de pasos
impares de r en t pasos y `A=T^t(r)`. El par `(r,r+1)` está *fusionado por
clases hasta t* si r y r+1 tienen la misma `(a,A)`. En Lean es
`canon (iter t ⟨r,r+1,0,0⟩) = .fusion`.

1. **Casi todos los pares están fusionados.** Sea `S_t` el conjunto de
   `r<2^t` con el par fusionado. `TejonasGao.transporte` da `|S_t|=2^t·P_t`,
   con `P_t=P(σ<=t)`, y `MartasGao.martas` da `P_t -> 1`. Es la prueba de la
   conjetura de Gao ([Martas](../gao20260920/Martas.md),
   [Tejonas](../gao20260920/Tejonas.md)).
2. **Un bloque por cota de unión** (`bloque`, `bloque_fusion`). Sean `K=L+1`
   y t con `1-P_t<=1/(2(K+1))` y `2K²<2^t`. Si ningún r tuviera
   `r, r+1, …, r+K-1` en `S_t`, cada `r<2^t` tendría un `i<K` con `r+i` fuera
   de `S_t`. La aplicación `r -> r+i` es inyectiva y cae en
   `[0,2^t+K) \ S_t`. De ahí
   `2^t <= K(2^t+K-|S_t|) <= K·2^t/(2(K+1)) + K² < 2^t/2 + 2^t/2`,
   una contradicción. Hay, pues, un r con los K pares
   `(r+i, r+i+1)`, `i<K`, fusionados, y además `r+i<2^t`.
3. **Valor común** (`fusion_sx`, `canon_modulo`, cadena `hcad`). Para cada
   `u>=0`, el residuo de `2^t·u+r+i` es `r+i`. Por eso el par
   `(2^t·u+r+i, 2^t·u+r+i+1)` está fusionado en el paso t. Encadenando los
   pares, los `n_i=2^t·u+r+i`, con `i=0..L+1`, tienen el mismo número a de
   impares y el mismo valor `T^t(n_i)=3^a·u+A` (`iter_rep`, `hafin`).
4. **`a>=1` y `3∤A`** (`sp_impar`, `tres`). Uno de r y r+1 es impar, así que
   su primer paso es impar, y a es común. Tras un paso impar, `(3x+1)/2` no
   es múltiplo de 3, y dividir por 2 un par no múltiplo de 3 da otro no
   múltiplo de 3. Por tanto `A=T^t(r)` no es múltiplo de 3.
5. **2 es raíz primitiva módulo `3^a`** (`cuatro`, `dos_genera`,
   `dos_genera_grande`).
   - `4^(3^k)=1+3^(k+1)·e` con `3∤e`, por inducción elevando al cubo.
   - Si `3^(k+1) | 2^m-c`, alguno de m, `m+2·3^k` y `m+4·3^k` sirve módulo
     `3^(k+2)`, porque `j`, `j+ce` y `j+2ce` son distintos módulo 3.
   - Sumando múltiplos de `2·3^k` se obtiene m tan grande como se quiera.

   Se toma `m>=A+3^a·N+3` con `3^a | 2^m-A`, y `u=(2^m-A)/3^a`, que cumple
   `u>N`.
6. **Misma altura y mismas mitades** (`orbita`, `altura_potencia`). Sea
   `n=2^t·u+r>=u>N`.
   - t pasos del atajo son `t+a` pasos clásicos, porque un paso impar
     `(3x+1)/2` son dos, `3x+1` y luego `/2`. En ellos hay exactamente t
     mitades. Así, cada `n+i` vale `2^m` en el paso clásico `t+a`.
   - Nadie llegó antes a 1: si no, en el paso `t+a` estaría en el ciclo
     `{1,2,4}`, y `2^m>=8`.
   - Luego bajan juntos por `2^m, 2^(m-1), …, 1`.

   Todos tienen altura `t+a+m` y `σ∞=t+m`. ∎

**Qué no dice.** La prueba da la existencia, no un tamaño útil. El t de la
prueba viene del ritmo de Martas, que es pésimo: `J_F·p_m>1` sólo desde
m=802923 ([Cigarras](../gao20260924/Cigarras.md)). El cómputo, en cambio,
halla t pequeños (tabla de abajo). Tampoco dice nada de la llegada a 1 de
otros números: la altura de estas rachas se conoce porque su valor común es
una potencia de 2.

## Las otras conjeturas de Garner (1985)

- **(1) La mayoría tiene la altura de un vecino.** Sigue abierta en la forma
  literal, con alturas finitas: haría falta saber que casi todos llegan a 1.
  Con alturas en `ℕ∪{∞}` saldría de Gao: un encuentro en `<=log2 n` pasos
  iguala las alturas. No está formalizado.
- **Caracterización por bloques y cadenas.** Refutada por Elia y Tucker
  (Integers 15, 2015, arXiv:1511.09141): el primer contraejemplo es
  3067–3068, y hay una familia infinita.

## Validación

- Lean 4.32.2, Mathlib fijada. [Alpacas.lean](../gao20260920/formal/Alpacas.lean)
  y `GarnerEnunciado.lean` compilan sin `sorry`. `#print axioms` da sólo
  `propext`, `Classical.choice` y `Quot.sound`, y `leanchecker` sale con
  código 0 en los dos. La evidencia, con hashes, está en
  [evidencia_gao_lean.json](../gao20260920/evidencia_gao_lean.json).
- [verificar_alpacas.py](verificar_alpacas.py) es independiente del sondeo
  ([salida](verificar_alpacas_salida.txt)). Calcula las clases por
  recurrencia en t, cotejada con la iteración directa para `t<=10`. Obtiene
  m subiendo de `3^k` a `3^(k+1)`, como la prueba. Construye así rachas de
  L+1 consecutivos para `L=1..22` y t hasta 20. Iterando de verdad, todas
  tienen altura `t+a+m` y `σ∞=t+m`, también con el m siguiente del
  período. Además comprueba:
  - que el orden de 2 módulo `3^k` es `2·3^(k-1)` para `k<=9`;
  - las 8 filas de la tabla 1 de Gao, enteras;
  - 37 muestras de la 35654-upla de Gao desde `2^500+1`.

  Es un control finito, no una prueba.
- [sondeo_rachas.py](sondeo_rachas.py), del plan: mismos resultados con otro
  código.

## Novedad

Revisado el 26-09:

- las bibliografías anotadas de Lagarias (1963–1999 y 2000–2009);
- Gao (1993), que el usuario aportó;
- Wu (1992, 1993, 1995) y Wu–Huang (2001), según sus resúmenes;
- Elia–Tucker (2015);
- OEIS A078441 y A277109;
- el resumen de Frinkle et al. (J. Supercomputing 81, 2025);
- una búsqueda web.

Todos tratan las rachas largas como cómputo o como conjetura. Lo probado es:

- Penning, Gao (lema 1) y Wu: una racha de largo L da infinitas del mismo
  largo;
- Wu–Huang: familias infinitas de pares.

No se halló prueba de rachas de todo largo. El 11-10, zbMATH (API, por
título y por citas a Garner 1985: Elia–Tucker 2015, LaDue 2018 y Wu 1992)
tampoco la registra. Faltan MathSciNet y los textos completos de Garner
(1985), DOI 10.1016/S0012-365X(85)80020-0, y de Frinkle et al.

Nombre: *alpacas*, libre en este repositorio y en zootheorem (consultado
el 26-09; Ovejas, Suricatas y Queltehues ya existían).
