# Auditoría del traslado: una semilla fija y muchos segmentos

10-10-2026. Bloque 1 de la [ruta](../casa20261004/RUTA_20261010.md).

Se cotejó el teorema 3.2 de Rozier–Terracol, [v5, §3](https://arxiv.org/html/2502.00948v5#S3):
un entero `n≥2` sin descenso produce infinitos segmentos paradójicos
desde múltiplos `2^k n`. El artículo usa aproximaciones de potencias
por debajo de 1. La reconstrucción siguiente trabaja directamente con
el numerador afín y usa una tolerancia ligeramente distinta. Es una
comprobación del resultado externo, sin atribución de novedad.

## Convenciones y diccionario

`T(x)=x/2` si x es par, `(3x+1)/2` si es impar, sobre enteros positivos.
`x_j=T^j(n)` y `S_j` cuenta las entradas impares antes de j; j cuenta
pasos del atajo. Un segmento es el par `(m,L)`, con `m>2`, `L≥1`,
`3^S_L(m)<2^L` y `T^L(m)≥m`. No hay ley aleatoria ni condicionamiento.

| Hipótesis | Traducción en la casa |
|---|---|
| `x_j≥n` para todo j | `¬ CasaPlano.Desciende n`; j=0 es automático. |
| No hay cruce de coeficiente | `CasaPlano.FugaPura n`; implica la hipótesis anterior. |
| Hay cruce, pero nunca descenso | `CasaGrieta.Grieta n`, añadiendo `n≥2`. |
| `n≥2` y nunca descenso | En realidad `n>2` e impar, pues todo par positivo baja en un paso. |

Cohete y planeador intermitente están dentro de fuga pura. Por ello
el traslado alcanza los tres obstáculos; no necesita la sexta raíz,
LMN, una ley de mezcla ni las altas recuperadas del 05-10.

## Reconstrucción independiente

Supongamos `n≥2` y `x_j≥n` para todo j. Hay infinitas entradas impares:
si desde cierto punto todo fuese par, las divisiones sucesivas por 2
harían caer un entero positivo por debajo de n. Por tanto existe,
para cada a≥1, el primer tiempo `j_a` con `S_j=a`.

Escribamos `A=3^a`, `V=2^b`. Se eligen infinitos pares positivos con

```text
1 - 1/(2(n+1)) < A/V < 1.                         (1)
```

La existencia procede de aproximar `log 2/log 3` por convergentes
inferiores: su error es positivo y menor que `1/b²`, de donde
`b log 2-a log 3 → 0+`. La irracionalidad se sigue de que
`3^a=2^b` es imposible con a,b positivos. Éste es el ingrediente
de aproximación diofántica; no se certifica en el módulo Lean nuevo.

Para el prefijo hasta `j=j_a`, sea B su numerador aditivo. Si sus unos
ocurren en `t_0<…<t_(a-1)`, entonces

```text
B = Σ_(i=0)^(a-1) 2^t_i 3^(a-1-i)
  ≥ Σ_(i=0)^(a-1) 2^i 3^(a-1-i) = 3^a - 2^a.     (2)
```

Aquí `t_i≥i`; la última suma se obtiene telescopando tras multiplicar
por `3-2`. Independientemente, la composición de las ramas da
`2^j x_j=A n+B`. Se distinguen dos casos:

- **j≥b.** `A<2^b≤2^j` y `x_j≥n`: `(n,j)` es paradójico.
- **j<b.** Tomar `k=b-j`, `m=2^k n`, `L=b`. Los k pasos iniciales
  son pares y `T^b(m)=x_j`. Como `A<V` implica `a<b`, tenemos
  `2^a≤V/2`. Usando (1) y (2),

```text
2^j x_j ≥ A(n+1)-2^a
        > V(n+1)-V/2-2^a ≥ V n.
```

Así `x_j>2^(b-j)n=m`, y el coeficiente del segmento es `A/V<1`.
La definición exige sólo `≥`; esta rama da desigualdad estricta.

## Infinitud y conservación de hipótesis

La franja (1) está por encima de 1/2. Para un a fijo contiene a lo
sumo un b, pues aumentar b en uno divide la razón por 2. Los infinitos
pares tienen entonces infinitos a distintos. Cada segmento construido
tiene exactamente a entradas impares. Si dos pares produjeran el mismo
`(m,L)`, tendrían el mismo a y luego el mismo b. Los segmentos son
distintos aunque puedan compartir inicio; no se demuestra que haya
infinitos inicios distintos.

Si `k>0`, la nueva semilla m baja ya en su primer paso. **No es una
grieta.** La propiedad que se conserva es que, después de los k ceros,
se recorre un prefijo de la órbita del mismo n, cuyos valores son ≥n.
No se conserva «todos los valores son ≥m». En una fuga pura necesariamente
`j_a<b`: el caso contrario daría un cruce para n.

Finalmente, si Collatz fallara, el mínimo de una órbita que no llega
a 1 sería un `n>2` que nunca desciende. El traslado le asociaría una
familia infinita. Esto justifica la reducción externa a finitud global,
sin demostrar dicha finitud. No se presupone CST.

## Alcance de la verificación

Prueba escrita auditada mediante (1)–(2), composición afín y distinción
de casos. [Jinetas.lean](Jinetas.lean) certifica álgebra de palabras y
congruencias, y ejemplos concretos; **no formaliza el teorema de traslado,
los convergentes ni el enlace universal entre su palabra y el mapa T**.
El [ensayo](LEEME.md) examina qué añade el margen modular a esta reducción.
