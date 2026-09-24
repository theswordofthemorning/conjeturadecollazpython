# Cigarras — dónde empiezan a decir algo CF_H y CF_F

24-09-2026. La primera obligación al retomar era demostrar, «para m>=10»,

    P(sigma>h y K_(C_m)(h)<N) <= 3/N+66/h+1/(4h^3).      (*)

Precisión que importa: **(*) por sí sola es sustantiva en cualquier `m`**,
también en `m=10`; acota un suceso concreto y no contiene el número de
ensayos. Lo que se vacía es el ensamblaje al que sirve. La descomposición
de `Guardias_finitas.md`, con `1+J_F(W_m+2)<=N`, da

    P(sigma>h) <= P(sigma>h y K_(C_m)(h)<N) + (1-p_m)^(J_F)

y es ese lado derecho el que hay que vigilar: si `J_F = 0` el segundo
sumando vale 1 y la conclusión no dice nada por buena que sea (*).

Verificador: [`parametros_cff.py`](parametros_cff.py), salida en
[`parametros_cff_salida.txt`](parametros_cff_salida.txt). Enteros de
precisión arbitraria y `Fraction`; ningún flotante en las desigualdades.

## Lo que sí queda confirmado

Todas las identidades declaradas en `Ventana_armonica.md` §4 se reproducen
exactamente desde las definiciones de §3, para `m` de 10 a 1000:

    r = m0 = 24m+4        T_m = 768m+128        Q_m = T_m+1

El término `3/N` también sale exacto. Con `H3` instanciada en `n=N^4`,
`L=N^2`, `a=4m+2`, `s=6m`, el coste por excursión es

    1/L + (L-1)/n + n*2^(-s) = 1/N^2 + (N^2-1)/N^4 + 1/N^2 <= 3/N^2

comprobado como fracción exacta, y la unión de `N` excursiones da `3/N`
sin holgura perdida. El encaje temporal `N*d <= h` equivale a
`10m+3 <= 2^m` y se cumple desde `m=6`, así que ahí `m>=10` sobra.

Las tres condiciones aritméticas de §3 —`n^2>=8Q`, `T>=1024` y
`4(T+1)*61^T <= 62^T`— se cumplen en todo el rango probado.

## El problema: el número de ensayos es cero

`J_F = floor((N-1)/(W_m+2))` con `W_m = H_m + D_m`, donde `H_m` es la `H`
de la ventana aplicada a `c0 = C_m = 9h^4`. Los tamaños no se parecen:

| m | W_m | N = 2^m | J_F |
|---:|---:|---:|---:|
| 10 | 2 154 318 682 768 | 1 024 | **0** |
| 30 | 20 613 218 634 000 | 1 073 741 824 | **0** |
| 45 | 48 672 159 515 712 | 35 184 372 088 832 | **0** |
| 46 | 50 851 179 349 056 | 70 368 744 177 664 | 1 |
| 60 | 86 367 469 271 184 | 1 152 921 504 606 846 976 | 13 349 |

**Primer `m` con `J_F >= 1`: m = 46.** Por debajo, un solo bloque de ensayo
es más largo que el presupuesto entero de entradas admisibles, `J_F = 0`,
y el término `(1-p_m)^(J_F)` vale exactamente 1. Ninguna de las dos piezas
es falsa; el ensamblaje acota una probabilidad por algo que supera 1.

Lo mismo le pasa a CF_H, que se enuncia igualmente «para m>=10»: usa
`D_m+2` en vez de `W_m+2`, y aun así **el primer `m` con `J_H >= 1` es 19**,
porque `D_m = 250000` ya en `m=10`.

## Dónde empieza a ser útil de verdad

Que haya un ensayo no basta; hace falta que `J*p` sea grande, con
`p_m = 2^(-D_m)/(4*Q_m)`. En logaritmo base 2,

    log2(J_F * p_m) = log2(J_F) - D_m - log2(4*Q_m)

y `D_m` ronda el millón mientras `log2(J_F)` es del orden de `m`:

| m | D_m | log2(J_F) | log2(J_F·p_m) |
|---:|---:|---:|---:|
| 46 | 304 704 | 0 | −304 721 |
| 1 000 | 440 896 | 945 | −439 972 |
| 100 000 | 678 976 | 99 931 | −579 073 |
| 300 000 | 746 496 | 299 928 | −446 597 |

**Primer `m` con `J_F * p_m > 1`: m = 802 923**, donde `D_m = 802 816`.

Esto no rompe nada: `D_m` crece como `log^2(m)` y `m` acaba superándolo,
luego `J_F*p_m -> infinito` y el límite sigue en pie. Y es coherente con
lo que el propio laboratorio ya usaba: `Ventana_armonica.md` §4 calcula
sus parámetros en `m = 1 000 000`, que es justo por encima de este umbral.

## Consecuencia para el trabajo pendiente

El «m>=10» de los enunciados es un artefacto heredado de las identidades
de parámetros, donde sí vale. Formalizar (*) con esa hipótesis no está mal
—(*) es sustantiva—; lo que no se puede es cerrar el ensamblaje con ella y
darlo por bueno, porque el resultado compilaría sin decir nada. Los
umbrales a declarar en el ensamblaje son:

- `m >= 19` para que CF_H tenga al menos un ensayo;
- `m >= 46` para que CF_F tenga al menos uno;
- `m >= 802923` para que el término de ensayos de CF_F baje de 1.

Ninguno de estos números cambia la ruta ni la conclusión buscada. Cambian
la hipótesis que hay que escribir en el enunciado, y avisan de que
cualquier contraste numérico del protocolo en `m` pequeño está mirando
un régimen donde la cota es trivial por construcción.

## Lo que esto no es

No es una demostración de la cota pendiente, ni la toca. Es aritmética de
parámetros: comprueba las identidades declaradas y localiza el rango de
validez útil. La desigualdad de `Guardias_finitas.md` sigue sin demostrarse.
