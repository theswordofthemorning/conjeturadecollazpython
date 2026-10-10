# Jinetas: el acarreo rompe el orden del margen

10-10-2026. Primer ensayo ejecutado de la
[ruta aritmética](../casa20261004/RUTA_20261010.md).

**Continuación ejecutada:** [prefijos de una misma semilla](PREFIJOS.md).
El intervalo de candidatos se anida correctamente, pero en el primer
cruce vuelve exactamente a CST. Se certifica el límite del mecanismo;
la decisión vigente es volver al balance, sin ampliar los censos.

**Resultado:** el intercambio `01→10` reduce siempre el término aditivo,
pero puede crear o destruir una paradoja al cambiar la semilla admisible.
El acarreo modular explica exactamente el cambio. El relleno de ceros
del traslado tampoco aporta por sí solo una congruencia nueva sobre la
semilla original. Queda cerrado el intento de usar esas dos operaciones
solas como exclusión; no se cierra ningún muro de Collatz.

El [traslado](TRASLADO.md) quedó auditado por escrito. La
[conciliación](CONCILIACION.md) separa las evidencias necesarias de los
avances locales anteriores. «Jinetas» identifica esta ficha y sus lemas
elementales: se consultaron el índice histórico, su catálogo y el registro
activo antes de asignar el nombre; no se afirma prioridad en la literatura.

## Dominio y criterio exacto

Atajo `T(n)=n/2` si n es par y `(3n+1)/2` si es impar, n positivo.
La palabra `w=w_0…w_(L-1)` se lee en orden temporal, con 0 par y 1 impar;
`L≥1` cuenta pasos, s sus unos, `M=2^L`, `A=3^s`, `D=M-A`.
Las cantidades siguientes son enteras; no hay muestreo, ley aleatoria
ni hipótesis de independencia.

```text
M T^L(u) = A u+B(w),                 u realiza la palabra w;
r(w) = -B(w) A^(-1) mod M,           0≤r<M;
u_min(w) = r + M max(0, ceil((3-r)/M)).
```

La biyección clásica de paridades garantiza una clase por palabra.
También puede verse inductivamente: la congruencia final determina
el primer bit módulo 2; al retirar su rama deja la congruencia de la
cola módulo `2^(L-1)`. La inversa de A existe por ser impar.

Para `u>2` de esa clase, el segmento es paradójico exactamente cuando
`D>0` y `Du≤B`. El margen es `F_w(u)=Du-B`; por tanto una palabra con
`D>0` admite alguna paradoja si y sólo si `F_w(u_min)≤0`. Sus semillas
son exactamente `u_min+tM`, con

```text
0≤t≤floor((floor(B/D)-u_min)/M).
```

Si el extremo superior es negativo, no hay ninguna. No se identifica
r con una semilla mayor que 2 cuando `r=0,1,2`.

## Prueba del intercambio y su acarreo

Escribir `w=a 01 b`, `w'=a 10 b`, `i=longitud(a)`,
`p=unos(a)`, `q=unos(b)`, `s=p+1+q`. La composición de ramas da

```text
B(a b)=3^unos(b) B(a)+2^longitud(a) B(b).
B(w')=B(w)-2^i 3^q.                                      (3)
```

La monotonía de B ya aparece en Rozier–Terracol,
[v5, definición 2.2 y lema 2.3](https://arxiv.org/html/2502.00948v5#S2).
Aquí se sigue además el representante modular y el margen.

Definir `H=2^(L-i)` y `h=(3^(p+1))^(-1) mod H`, con `0<h<H`.
Como L-i≥2, esta inversa es un entero positivo. De (3),

```text
r' ≡ r+2^i h mod M,
c = floor((r+2^i h)/M) ∈ {0,1},
r' = r+2^i h-cM.                                         (4)
```

En efecto, `A(r'-r)≡2^i 3^q mod M`. Cancelando `2^i` y después
el factor impar `3^q`, queda `3^(p+1)(r'-r)/2^i≡1 mod H`.
Esto también muestra que i,p,L fijan el desplazamiento; el sufijo
interviene en el valor inicial r y en q.

Al combinar (3) y (4) se obtiene, sin estimación,

```text
F_w'(r')-F_w(r) = 2^i [D(h-cH)+3^q].                    (5)
```

Si `D>0` y no hay acarreo, el cambio es estrictamente positivo.
Con acarreo es no positivo exactamente cuando `3^q≤D(H-h)`.
Es un criterio uniforme en L, **condicionado al acarreo**, no una
exclusión de una familia de posibles contraejemplos.

Para las semillas mínimas mayores que 2, escribir `u_min=r+eM` y
`u'_min=r'+e'M`. A (5) se añade `DM(e'-e)`. Omitir esta corrección
en los residuos 0,1,2 cambia el problema. Para un intercambio L≥2,
e,e' están en `{0,1}`.

## Contraejemplo a ordenar sólo por el término aditivo

Las tres palabras siguientes tienen L=8, s=5 y D=13; en ellas r=u_min.
Cada fila se obtiene de la anterior mediante un único `01→10`.

| Palabra | Semilla | B | T^8(semilla) | Margen `13u-B` | Paradoja |
|---|---:|---:|---:|---:|---|
| `00111101` | 188 | 908 | 182 | 1536 | No |
| `01011101` | 18 | 746 | 20 | -512 | Sí |
| `10011101` | 189 | 665 | 182 | 1792 | No |

En el primer intercambio i=1, h=43, H=128, c=1 y el margen cambia
en −2048. En el segundo i=0, h=171, H=256, c=0 y cambia en +2304.
Por ello ni el margen ni la existencia de una paradoja son monótonos
en ese orden. Los mismos tres testigos refutan las dos orientaciones
globales de monotonía. **No refutan el lema 2.3 del artículo**, que
habla únicamente del término aditivo, ni descartan transformaciones
que añadan condiciones para controlar el residuo y todos los prefijos.

## Lo que conserva el relleno de ceros

Para `w*=0^k w`, la composición y la congruencia dan exactamente

```text
B(w*)=2^k B(w),     r(w*)=2^k r(w),
T^(L+k)(2^k n)=T^L(n).
```

La segunda igualdad usa `0≤r<2^L`, luego `0≤2^k r<2^(L+k)`.
La congruencia del segmento ampliado se cancela:

```text
2^(L+k) | 3^s (2^k n)+2^k B
    si y sólo si 2^L | 3^s n+B.
```

Y el criterio de paradoja para la semilla **fija** trasladada es

```text
3^s < 2^(L+k),     (2^(L+k)-3^s)n ≤ B,
```

o `3^s < 2^(L+k) ≤ 3^s+B/n`. Sigue faltando acotar esa familia
compatible de prefijos de un mismo n. El relleno no introduce una
criba de congruencias adicional: la segunda condición usa el margen
original con el nuevo coeficiente. No se confunde `2^k n` con el menor
representante de su clase, ni se afirma que esas semillas nunca bajen.

## Verificación y alcance formal

[verificar_intercambio.py](verificar_intercambio.py) compara la recurrencia
de B y la inversa modular con una tabla construida por iteración directa
de todas las semillas `0≤r<2^L`. El conteo de segmentos se coteja además
recorriendo todas las semillas positivas hasta el máximo umbral B/D,
con criterio calculado desde la órbita. [Salida exacta](cotejo.json):

- L=1…12: 8190 palabras y 20481 intercambios; 16561 con D>0,
  de los cuales 9262 sin acarreo y 7299 con él.
- 16380 controles de levantamientos y 32760 de relleno, k=0…3.
- Cinco pares `(inicio,longitud)` paradójicos dentro de ese horizonte.
  El número es un conteo finito, no una cota global.
- Bordes: cero impares, r=0,1,2, L=1, margen nulo en el ciclo de
  5n+1 desde 13, n=1, n=2, D<0 y el fijo negativo −1.

[Jinetas.lean](Jinetas.lean) certifica la composición, (3), (5), los dos
criterios de signo, la identidad de congruencia bajo sus hipótesis
algebraicas, la cancelación del relleno y los tres testigos por
evaluación del mapa. La existencia de la inversa, la biyección general
de paridades, la selección del representante con c y el traslado
infinito se justifican por escrito aquí o en [TRASLADO.md](TRASLADO.md);
no se presentan como formalizados por este módulo.

Comandos desde la raíz:

```text
python -B -X utf8 depuracion/jinetas20261010/verificar_intercambio.py --longitud-maxima 12 --salida depuracion/jinetas20261010/cotejo.json
python -B -X utf8 depuracion/jinetas20261010/comprobar_lean.py --salida depuracion/jinetas20261010/evidencia_lean.json
```

Lean 4.32.2; [evidencia](evidencia_lean.json) con huellas, salida y
`#print axioms`. No se recompilan los censos ni los módulos de la casa;
el archivo nuevo depende sólo de Mathlib fijado. Revisión humana pendiente.

## Decisión al terminar este bloque

No ampliar el barrido ni construir una inducción sobre el orden de B:
el ejemplo anterior invalida esa monotonía. Los lemas algebraicos son
herramientas de control, no la restricción nueva que pedía la ruta.
El ensayo `01/10` queda cerrado como mecanismo suficiente por sí solo.

**Acción propuesta al cerrar este primer ensayo:** antes de otro experimento, formular una reducción
que actúe sobre la familia `0^k w_j(n)` de un mismo n y conserve
`T^t(n)≥n` en todos los prefijos utilizados. Su primer entregable debe
ser un invariante adicional y una condición terminal incompatible con
no descender. Si sólo recupera (5), la congruencia cancelada o el
criterio afín, volver al balance sin presentarlo como avance hacia una
exclusión universal. La finitud de los segmentos sigue abierta.

**Resultado de esa acción:** [PREFIJOS.md](PREFIJOS.md) construye el
intervalo exacto, prueba la redundancia de sus restricciones antes del
primer cruce y distingue una rama infinita de una semilla fija.
No apareció el invariante adicional: se aplica la cláusula de volver
al balance. El siguiente trabajo queda delimitado al final de esa nota.
