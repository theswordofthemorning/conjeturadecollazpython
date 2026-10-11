# Perdices: pisos futuros, reinicios y la semilla que falta conservar

10-10-2026. Continúa [Cola](COLA.md). Quedan formalizadas la cota
exponencial desde un piso futuro y la extracción de reinicios de fuga
pura. También queda en Lean la equivalencia

```text
Collatz <-> MuroB y ausencia de circuitos no triviales.
```

**No se demuestra MuroB ni se excluyen esos circuitos.** La combinación
de anchura sublineal y congruencia admite prefijos arbitrariamente
largos con semillas variables. Ese control no construye un cohete.
Se conserva el nombre Perdices; no se reclama prioridad matemática.

## 1. Mapa, dominio y cuantificadores

Atajo T sobre naturales: n/2 para n par, (3n+1)/2 para n impar.
`x_j=T^j(n)`, `S_k=#{j<k:x_j impar}`, `P_k=3^S_k/2^k`,
`I_k=1/P_k`, `R_k=x_k/P_k`. Los índices cuentan pasos de T.
No hay ley aleatoria ni condicionamiento probabilístico.

Para los resultados infinitos se supone n>0 e inyectividad de
`j -> x_j` sobre todos los naturales. [Colisiones](COLISIONES.md)
da `P_k -> infinito` y `R_k -> ξ` real finito. La cola de
[Cola](COLA.md) es `t_k=ξ P_k-x_k>=1`.

Un **piso futuro** en k es una cota inferior válida para x_(k+j)
para todo j>=0. Verificarla hasta un corte no certifica esa hipótesis.
Tampoco un mínimo sobre un intervalo finito es necesariamente un
mínimo de toda la cola infinita.

## 2. Sumar desde el piso, sin perder el resto

La cuenta de Colisiones, válida para cualquier conjunto finito A
de valores de una órbita inyectiva, es

```text
#{a en A: a<2^(100r)} <= 3*2^(99r).
```

El anillo `[2^(100r),2^(100(r+1)))` aporta a lo sumo
`3*2^99*2^(-r)` a la suma de 1/a. Si todos los a de A son
>=2^(100m), una inducción finita sobre d prueba

```text
(sum_{a en A, a<2^(100(m+d))} 1/a)*2^(m+d) + 3*2^100
    <= 3*2^100 * 2^d.                                  (1)
```

El caso d=0 tiene suma vacía. En cada paso se añade exactamente
un anillo; se conserva el resto geométrico. Todo conjunto finito
cabe en algún corte, de modo que su suma es <=3*2^100/2^m.
Pasar a prefijos de la órbita usa su inyectividad, y pasar a la
serie infinita usa sumas parciales no negativas acotadas.

Por tanto, si x_j>=2^(100m) para todo j>=k,

```text
sum_{j>=k} 1/x_j <= 3*2^100/2^m,
t_k <= x_k [exp(2^100/2^m)-1].                          (2)
```

En Lean se prueba la suma infinita desde el origen; aplicarla a
la órbita reiniciada da la primera expresión de (2). El traslado
normalizado y el de su límite están formalizados explícitamente:

```text
R_(k+j)(n) = I_k(n) R_j(x_k),
ξ(n) = I_k(n) ξ(x_k),
t_k(n) = ξ(x_k)-x_k.                                   (3)
```

La prueba del traslado del supremo usa monotonía y cotas en ambos
sentidos. Para la segunda expresión de (2), se aplica
`1+u<=exp(u)` al producto corrector de la órbita reiniciada y se
resta x_k. Positividad e inyectividad se trasladan también.

**(1)–(3) están formalizados.** Para FugaPura n>=2^(100m),
el piso n nunca se cruza y se obtiene
`ξ(n)-n<=n[exp(2^100/2^m)-1]`. Elegir el mayor m da
`O(n^(99/100))`, con constante uniforme entre esas semillas
hipotéticas. La traducción a esta notación asintótica conserva la
prueba escrita de [Cola, §5](COLA.md#5-lo-que-sí-da-cuantitativamente-la-cuenta-de-colisiones);
no se añade un lema Lean sobre potencias reales o Big-O.

## 3. Reinicios grandes sin usar el muro A

Como I_k>0 e I_k->0, cada cola `k>=K` alcanza su máximo de I.
Prueba formal: elegir J tras el cual I_j<I_K; tomar el máximo
en `[K,max(K,J)]`. También domina todos los índices posteriores.

En ese índice u,

```text
I_(u+j) = I_u I_j(x_u) <= I_u,
```

luego `I_j(x_u)<=1` para todo j. Es decir, x_u es FugaPura.
La órbita inyectiva acaba sobre cualquier cota de valores, por lo
que se puede imponer simultáneamente u>=K y x_u>M. Esto enlaza
la extracción y (2) para pisos arbitrariamente altos.

El argumento de mínimo del pronóstico ya figuraba condicionalmente
en [CasaTablero](../casa20261004/CasaTablero.lean),
`fuga_de_minimo` y la primera rama de `rasgo_cohete_o_planeador`.
Aquí se escribe con el inverso y se elimina la alternativa del
planeador mediante Colisiones. **No hace falta MuroA.** La semilla
inicial puede incluso haber cruzado antes: basta la inyectividad.

## 4. Qué controla exactamente el muro B

`MuroB` exige que todo n>=2 tenga algún P_k<1. Si hubiera una
órbita positiva inyectiva, la sección anterior produciría un
reinicio x_u>=2 de fuga pura, en contradicción con MuroB.
Recíprocamente, si MuroB falla, CasaRetrato ya prueba que la fuga
pura resultante es inyectiva. Así,

```text
MuroB <-> ninguna órbita positiva es inyectiva.           (4)
```

Para una iteración determinista, repetir un valor vuelve periódico
todo el futuro. Por ello (4) identifica al muro B con excluir las
órbitas positivas con infinitos valores distintos. Un circuito no trivial,
sí cruza el pronóstico: MuroB no lo excluye.

Si además no hay circuitos no triviales, una órbita positiva que
no llegase a 1 no podría repetir valores; sería inyectiva y
contradiría (4). La conversión entre atajo y mapa clásico ya está
formalizada en CasaPlano. Esto da

```text
Collatz <-> MuroB y (para todo x, no Circuito x).          (5)
```

(4)–(5) están en Lean. La grieta divergente no es un tercer caso
independiente de no divergencia: produce reinicios de fuga pura.
**Sigue sin excluirse**, porque MuroB sigue abierto. Del mismo
modo, la grieta del mínimo de un circuito exige excluir ese circuito.
La equivalencia reorganiza lo pendiente; no prueba ninguna de las
dos condiciones del lado derecho.

## 5. La anchura y la congruencia no se contradicen por prefijo

Para una palabra de longitud L, s unos y aditivo B, escribir
`A=3^s`, `M=2^L` y `M y=A n+B`. Con `θ=ξ-n`, la cola final t
satisface `M t=A θ-B`. Si t>=1 y θ<=W(n), necesariamente

```text
B+M <= A W(n).                                         (6)
```

El lema algebraico está en Lean. La congruencia de la semilla sigue
siendo `A n+B=0 mod M`: (6) no añade otra congruencia independiente.
Para comprobar si ambas pueden dar una contradicción uniforme a
longitud finita, considerar para todo L>=2

```text
n_L=2^L-1,       palabra 1^L,
x_j=3^j 2^(L-j)-1,       0<=j<=L,
θ_L=1+(2/3)^L,           ξ_L=n_L+θ_L.                    (7)
```

La fórmula de x_j se verifica por inducción: es impar para j<L
y el paso impar da la siguiente fórmula. Por tanto S_j=j y
P_j=(3/2)^j>=1. En cada corte j<=L,

```text
A_j=3^j, M_j=2^j, B_j=3^j-2^j,
M_j x_j=A_j n_L+B_j,
ξ_L P_j-x_j=1+(2/3)^(L-j), entre 1 y 2.                 (8)
```

En el corte L, n_L es el representante mínimo de su clase. Además
`θ_L^100<=n_L^99`: basta θ_L<=2, n_L>=3 y `2^100<3^99`.
Incluso una anchura sublineal con constante 1 sería compatible
con estos prefijos. La cota exponencial de (2) también lo es:
si n_L>=2^(100m), `n_L*(2^100/2^m)>=2^100>θ_L`, y
`exp(u)-1>=u`.

(7)–(8) tienen prueba escrita y cotejo exacto, sin formalización
orbital completa de la familia en este módulo. **ξ_L es un
parámetro del prefijo, no el límite orbital de n_L.** Tampoco
afirmamos que n_L sea FugaPura. Varía n_L, y sus representantes
en la palabra infinita de unos son `r_j=2^j-1`: no se estabilizan
en ningún natural fijo; su límite 2-ádico es -1.

El control descarta una contradicción que sólo mire, para cada
longitud por separado, la congruencia y la anchura disponibles.
No descarta una prueba que use conjuntamente todos los cortes de
una misma semilla positiva.

**Continuación ejecutada:** [Repeticiones](REPETICIONES.md) obtiene
un presupuesto entero para repetir un bloque desde una única semilla
y localiza el defecto que aparece al cambiar de bloque. Usa el
levantamiento de [Semilla](SEMILLA.md); no excluye las concatenaciones
variables. Siguiente: controlar esas cancelaciones, empezando por
la transición explícita `1`/`110`. Recuperar sólo FugaPura reformularía
MuroB; mejorar otra vez la anchura no cubre ese paso.

## 6. Verificación y conservación

[PerdicesMinimos.lean](PerdicesMinimos.lean): 20 lemas nuevos.

| Tramo | Certificados principales |
|---|---|
| Presupuesto desde un piso | `suma_desde_hasta`, `suma_finita_piso`, `suma_orbital_piso`, `suma_infinita_piso` |
| Producto y traslado | `normalizado_piso`, `estatura_piso`, `estatura_traslado`, `cola_traslado`, `cola_piso`, `fuga_piso` |
| Reinicios y reducción | `maximo_futuro`, `fuga_del_maximo`, `reinicio_grande`, `reinicio_con_cota`, `muroB_iff_sin_inyectivas`, `collatz_iff_cruce_sin_circuitos` |
| Congruencia | `intervalo_afin`, sólo el enlace algebraico (6) |

[comprobar_minimos.py](comprobar_minimos.py) audita 24 módulos
previos y compila sólo el nuevo: 25 módulos, 295 consultas.
Lean 4.32.2, Mathlib fijado y únicamente axiomas estándar; sin
avisos ni pruebas incompletas. [Evidencia](evidencia_minimos.json),
[salida](evidencia_minimos.txt). Revisión humana pendiente.

[cotejar_minimos.py](cotejar_minimos.py), enteros y Fraction:

- n=1..128, corte 64: 202 mínimos finitos y 296 identidades de
  traslado, con órbitas reiniciadas calculadas independientemente.
  Esos mínimos no certifican ninguna afirmación sobre todo el futuro.
- 129 pisos y cortes d=0..32: 4257 controles del presupuesto y
  resto geométrico, incluido el corte vacío.
- L=2..256: 255 prefijos de (7), congruencias en todos los cortes,
  cola entre 1 y 2 y la desigualdad entera θ^100<=n^99. Se incluyen
  los cambios de anillo L=99,100,101 y 199,200,201.
- La comparación con la exponencial usa su cota racional inferior,
  sin aproximaciones flotantes. No se mide una órbita infinita.

[Resultado](cotejo_minimos.json). No se repiten censos históricos.

Al cerrar este bloque, el [registro](../coherencia20260913/registro.json)
actualizó la evidencia de `perdices_cola_minimos` y añadió
`perdices_minimos_reinicios` y `perdices_minimos_compatibilidad`:
310 afirmaciones, 204 demostradas,
86 medidas, 12 conjeturadas y ocho refutadas. La segunda alta tiene
el alcance escrito de §5, no una certificación Lean de toda la familia.
`guardarafirmaciones.py` regenera la base; el
[verificador](../coherencia20260913/verificar_registro.py) confirma
catálogo, atomicidad y captura literal en bases temporales. Se conserva
el resto del registro y no se modifica `respuestas.db`.

```powershell
python -B -X utf8 depuracion/perdices20261007/comprobar_minimos.py --compilados "$env:TEMP/perdices_cruce_20261010" --salida depuracion/perdices20261007/evidencia_minimos.json
python -B -X utf8 depuracion/perdices20261007/cotejar_minimos.py --nmax 128 --pasos 64 --mmax 128 --lmax 256 --salida depuracion/perdices20261007/cotejo_minimos.json
```

Si faltan objetos previos, reproducir primero [Cola](COLA.md).
