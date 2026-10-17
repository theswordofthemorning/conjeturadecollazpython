# Judas J2: ¿hay un mecanismo para el régimen genérico?

16-10-2026. Rama de Claude, paso J2 de la
[Ruta de Judas Iscariote](../../RutaDeJudasIscariote.md#4-la-ruta-de-esta-rama).
Una sesión, una pregunta, salida (a) o (b). **Salida: (b).** Ninguna fuente
leída da un enunciado que pase el
[filtro de admisión](../exploracionmath20261016/EXPLORACION.md#8-filtro-de-admisión-de-una-nueva-vía)
y la prueba de fuego. Se pasa a J3b. De paso quedan una reformulación exacta
del piloto, una calibración más fina y una corrección de prioridad para
[Complejidad](../perdices20261007/COMPLEJIDAD.md#6-prioridad-y-fuentes).

## 1. Pregunta, dominio y prueba de fuego

Atajo `T(x)=x/2` si x es par y `(3x+1)/2` si es impar, sobre enteros
positivos. Clase AB: prefijos de `{1,110}^ω`. `λ(n)` es el largo del mayor
prefijo admitido de las paridades de `n, T(n), T^2(n), ...`, como en
[SALIDAS §1](../perdices20261007/SALIDAS.md#1-convenciones-y-resultados-finitos).

Pregunta única de J2: ¿hay algún teorema que impida a una órbita entera
quedarse para siempre, o más de `C·log n` pasos, en una clase de paridades de
entropía positiva con todos sus ciclos expansivos?

Prueba de fuego: el candidato no puede valer para −1 ni para −5, que se
quedan en AB para siempre (`A^ω` y `B^ω`), ni para los ciclos racionales de
la clase. Tiene que usar que n es un entero positivo.

## 2. El piloto en el formato de Yolcu–Aaronson–Heule

**Lema (prueba escrita).** Sea `n=4z-1` con z entero, de modo que n es
impar y `n=3 mod 4`. Sea

```text
G(z) = 3z/2        si z es par            (bloque A),
       (9z+1)/8    si z = 7 mod 8         (bloque B),
       sin definir si z = 1, 3 o 5 mod 8.
```

En las entradas de bloque, `z=(x+1)/4` evoluciona por G. Las salidas valen
3 si `z=1,5 mod 8` y 4 si `z=3 mod 8`. Así,

```text
λ(4z-1) = #A + 3·#B + (3 o 4),     λ(n)=0 si n es par,   λ(n)=1 si n=1 mod 4.
```

*Prueba.* Con `x=4z-1` se tiene `T(x)=6z-1`.
- Si z es par, `6z-1=3 mod 4` es la entrada siguiente, con `z'=3z/2`.
- Si z es impar, `T^2(x)=9z-1` es par y `T^3(x)=(9z-1)/2`.
  - Si `z=1 mod 4`, este valor es par: la palabra es `1100` y sale tras 3 letras.
  - Si `z=3 mod 8`, el valor es `1 mod 4`: la palabra es `11010` y sale tras 4 letras.
  - Si `z=7 mod 8`, el valor es `3 mod 4` y es la entrada siguiente, con `z'=(9z+1)/8`.

**Consecuencia.** La versión cualitativa del piloto equivale a que G se
detenga en todo entero positivo z.

**En Lean.** [JudasPiloto.lean](JudasPiloto.lean):
- `piloto_iff`: `(∀ L, Admite n L) ↔ n % 4 = 3 ∧ NoPara ((n+1)/4)`. Aquí
  `Admite` es la convención de SALIDAS §1, y `NoPara z` dice que los iterados
  de G nunca dan `none`.
- `admite_a` y `admite_b` desplazan la palabra 1 y 3 letras.
- `salida_tres` y `salida_cuatro` prueban las salidas.
- `fantasma_cero` muestra que `z=0`, es decir `n=-1`, nunca se detiene.

Sólo axiomas estándar, sin `sorry` ([evidencia](evidencia_judas_piloto.txt)). La misma salida se lee en la órbita impar:
salir de AB es visitar 1, 5 o 13 módulo 16. Desde n=3 mod 4, la salida es
`D_i+2` si el impar es 5 o 13 y `D_i+3` si es 1, con `D_i` el instante de T
en que se llega a ese impar.

**Entre Mahler y la 4.14.** Tres funciones parciales del mismo formato:

```text
Mahler (necesaria):  M(2m) = 3m,   M(4m+1) = 6m+2,   parar en 4m+3
piloto:              G(2m) = 3m,   G(8m+7) = 9m+8,   parar en 1, 3, 5 mod 8
YAH, 4.14:           H(4m) = 3m,   H(8m+7) = 9m+8,   parar en el resto
```

- **H.** Yolcu, Aaronson y Heule (§4.5, Prop. 4.15) prueban que la conjetura
  4.14 equivale a que H se detenga.
- **M.** Si existe un número Z en `[m,m+1)`, M no se detiene desde m. Es
  sólo condición necesaria (Mahler 1968, p. 317, según la
  [nota de Mahler](../mahler20261007/LEEME.md)). La forma con ⊥ es la de
  Michel (1993), anotada por Lagarias en la entrada 128 de su bibliografía.

G tiene la rama A de Mahler y la rama B de H. M y G sólo expanden; H tiene
una rama que contrae. De las conjeturas de YAH, sólo la 4.12 implica el
piloto: una órbita que se quedara en AB visitaría 7 y 1 módulo 8 (infinitas
A y B) y nunca 5.

**Como reescritura de cadenas.** [srs_piloto.py](srs_piloto.py) escribe G en
la base mixta de YAH (§3.2):
- reglas X: las nueve suyas, que llevan las cifras ternarias hasta L;
- reglas dinámicas: `f R -> 0 R`, `t t t R -> 2 2 R` y el caso suelto
  `L t t R -> L f f f R` (z=7, donde el tercer 1 es L).

El resultado, [piloto_yah.srs](piloto_yah.srs), está en el formato de la
Termination Problem Database.

*Argumento escrito:* el sistema termina desde toda cadena si y sólo si G se
detiene en todo z>=1. Una inversión es una cifra binaria con una ternaria más
a la derecha, no necesariamente al lado.
- En cada lado de cada regla, L sólo aparece al principio y R sólo al final,
  y ninguna regla crea ni borra L o R. La cadena se corta, pues, después de
  cada R y antes de cada L, y cada trozo se reescribe por separado.
- Las reglas X terminan solas (YAH), con la medida (cifras ternarias,
  inversiones) en orden lexicográfico: los seis cambios quitan una inversión
  y las tres reglas de L gastan una cifra ternaria.
- Sin L se termina con (cifras binarias, inversiones): los cambios no tocan
  las cifras binarias y quitan una inversión; `f R -> 0 R` gasta una binaria
  y `t t t R -> 2 2 R`, tres.
- Queda el trozo `L w R`. Cada regla X conserva su valor y cada dinámica le
  aplica G. Toda cifra ternaria tiene una regla X con el símbolo que la
  precede, así que en forma normal de X el trozo es binario puro. Si G está
  definida en su valor, la regla dinámica que toca está disponible; si no, el
  trozo ya está en forma normal.

Así, entre dos reglas dinámicas sólo caben finitas reglas X, y una derivación
infinita desde `L w R` da una órbita de G que no se detiene. Desde la cadena
binaria de z hay una derivación infinita exactamente cuando G no se detiene
en z.

Cotejo de las medidas ([medidas_srs.py](medidas_srs.py),
[cotejo_medidas.json](cotejo_medidas.json), unos 2 s): la cuenta exacta, regla
por regla, da que cada medida baja en todo contexto. Además, 3400 contextos al
azar y 39 741 reescrituras al azar (17 746 con X y 21 995 sin L) no dan
fallos. En el sistema completo ninguna de las dos medidas sirve: las reglas de
L suben las cifras binarias, y `f R -> 0 R` y `t t t R -> 2 2 R` suben las
ternarias. Toda la dificultad está en el cruce de las dos mitades.

Cotejo de la simulación ([cotejo_srs.json](cotejo_srs.json)): en todos los
z<2^14, con la estrategia de más a la izquierda y con una al azar, los valores
tras cada regla dinámica son la órbita de G, y la forma normal es binaria. No
hay fallos; la derivación más larga tiene 513 pasos. Es el blanco natural para
un probador automático de terminación: el usuario aprobó instalar AProVE el
17-10 ([ruta §11](../../RutaDeJudasIscariote.md#11-siguiente-paso-aprove)).

**Fantasmas.** `G(0)=0` es −1, y `G(-1)=-1` es −5. Para cada palabra
periódica de bloques, el punto fijo de las funciones afines compuestas es
`z*=β/(1-α)` con `α>1` y `β>=0`, luego `z*<=0`. G no tiene ciclos racionales
positivos. Cualquier prueba de que G se detiene tiene que usar `z>0`.

Cotejo exacto ([cotejo_j2.json](cotejo_j2.json)):
- las tres lecturas de λ (T literal, G y Siracusa módulo 16) coinciden en los
  2 097 151 naturales menores que 2^21; el máximo es 39 y su menor semilla
  es 763675;
- también coinciden en los 21 récords de J1, incluido 338203040342655 con
  λ=112;
- la conjugación `n=8m+1` entre la G de YAH y H no falla bajo 2^20;
- bajo 2^20, G coincide con M en los pares y con H en `7 mod 8`. G, H y M se
  detienen en todos esos enteros, con máximos de 28, 14 y 59 iteraciones;
- las 2046 palabras periódicas de hasta diez bloques dan puntos fijos con las
  condiciones de resto 2-ádicas y `x=4z*-1` en `[-5,-1]`.

## 3. Lectura

Cada fuente lleva su mecanismo y el punto del filtro que no supera. «Leído»
quiere decir el texto completo, salvo donde se indica otra cosa.

| Fuente | Qué prueba | Mecanismo | En el piloto |
| --- | --- | --- | --- |
| Yolcu–Aaronson–Heule (2021; JAR 2023), §4.4–4.5, leído | Visitas forzadas a {1,5}, {1,7} y a 2, 3, 4, 6 módulo 8; 4.11–4.14 abiertas | Ciclos que contraen (Prop. 4.7), un solo punto 2-ádico, interpretaciones matriciales | No: en AB todo ciclo expande y la entropía es 0,55 bits. S1 y S2 resistieron miles de horas de CPU; 4.11–4.14 no tienen prueba. Falla el punto 5. |
| Akiyama–Frougny–Sakarovitch (2008), leídos §1 y §6; Akiyama (2008), leídos los enunciados | Existen infinitos z con `{z(3/2)^n}` en `[0,1/3)∪[2/3,1)`; Mahler equivale a que ninguna palabra mínima `w(n)` evite el factor 11 | Existencia por dobles desarrollos en base 3/2 | Barrera, no prueba: no da inexistencia. Falla el punto 5. |
| Dubickas (2009), Glasgow Math. J. 51, leído | Teorema 5: si una órbita de T diverge, `P(X,n)>1,70951129·n` para todo n grande | Palomar: tramos iguales de largo m obligan a `2^m` a dividir la diferencia, y `x_n<(3/2)^n(x_0+1)` | Pasa la prueba de fuego, pero sólo da complejidad lineal. AB admite `p(n)=p(n-1)+p(n-3)`: 1873 factores de largo 19 frente a 32,5. Falla el punto 5. |
| Eliahou–Verger-Gaugry (2025), CRAS 363, leído | Para n impar, `T(n)` en base 3/2 es añadir la cifra 1; conjeturas 4.2 y 4.3 | Diccionario | Sin mecanismo. Falla el punto 1. |
| Andrieu–Eliahou–Vivion (2025), arXiv 2510.11723, leídos §1 y §3 | La normalidad de las palabras mínimas implica Mahler, Z_{p/q} con p<q², Akiyama y el problema 4/3 | Condicional: equidistribución de `⌈px/q⌉` módulo `q^k` | `⌈3x/2⌉` difiere de T en los pasos pares (3x/2 frente a x/2). La hipótesis análoga para T sería tan fuerte como la conclusión. Fallan los puntos 2 y 5. |
| Stephan (2026), GitHub, leídos §1–2 | Excluye la ventana `[2/7,5/7)` en 3/2 (Lean). Teorema D: retención finita ⇒ vacío; retención infinita ⇒ ningún certificado sin rangos | Encierro ⇒ palabra de acarreos periódica, contra Dubickas–Novikas (2005) | En el piloto las colas retenidas son todo `[1,5]` (Judas §2.3): retención infinita. Por analogía, queda fuera de los certificados; no es un teorema transferido, porque AB alterna 3/2 y 9/8. Falla el punto 3. |
| Kari–Kopra (2017), RAIRO ITA 51, leídos §4–5 | Hay uniones de medida `>=1-ε` que ninguna órbita respeta (no constructivo) | El autómata celular que multiplica por p/q es de mezcla fuerte; la trampa cubre en el instante 0 el conjunto nulo que nunca cae | La trampa se fabrica a medida. No decide una trampa fijada de antemano, como los restos de salida del piloto. Falla el punto 5. |
| Kwon (2025), arXiv 2502.10132, leídos el resumen y la introducción; Bugeaud–Dubickas (2005) | Órbitas de β-transformaciones en intervalos de largo 1/β | Pasillo sturmiano | Entropía cero. Falla el punto 3. |
| Kumar (2024), arXiv 2411.03468 | «No hay números Z enteros» | Trivial: si `N=2^k·impar`, en `n=k+1` la parte fraccionaria vale 1/2 | Retirado el 18-06-2025. Descartado. |
| Dubickas–Mossinghoff (2009), Math. Comp. 78, leído (PDF aportado por el usuario) | Prop. 3.2: el mapa se detiene si S tiene un solo resto; Prop. 3.1: que se detenga para todo S impide los `Z_{p/q}` con `p<|S|q`; no hay `Z_{3/2}` bajo 2^57 | Con un solo resto, `g_n(p-q)+t=(p/q)^n(g_0(p-q)+t)` no es entero salvo en un punto fijo; además, factores prohibidos y búsqueda | Es el mecanismo de entropía cero: el que deja sólo −1 en `A^ω` y −5 en `B^ω`. Fallan los puntos 5 y 6. |
| Flatto (1992), por DM pp. 1839–1840 | Hay a lo sumo `O(x^log2(3/2))` números Z; numerables si `q<p<q^2` | Dinámica simbólica (β-transformación) | «Pocos», no «ninguno». Falla el punto 5. **Original sin leer.** |

**El problema 4/3.** Dubickas y Mossinghoff (2009, p. 1838) preguntan si
`x ↦ ⌈px/q⌉`, iterada mientras x cae en un conjunto S de restos módulo q, se
detiene en todo entero positivo. Esperan a lo sumo `c·log_(q/|S|) x`
iteraciones. Del caso 4/3 escriben que «there is currently no promising
approach to its solution» (p. 1837). Es el mismo tipo que el piloto: órbita
determinista, restos prohibidos, entropía positiva y expansión en cada paso,
y la misma forma cuantitativa que `λ(n)<=C·log n`. Sigue abierto.

**Los dos censos siguen la misma ley.** El modelo de restos uniformes predice
que el récord bajo `2^B` dura `B/(1-h)` pasos, con h la entropía de la clase
(Judas §3.1). En Mahler, `h=log2(3/2)`. DM (Teorema 5.1 y p. 1849) hallan, para
`g_0<=2^57`, una supervivencia máxima de 137 pasos, con `g_0=9850069454682037`;
el modelo da 137,3. En el piloto, el censo AB da 112 y el modelo, 111,5. Son
dos mediciones finitas, no una prueba: en ninguno de los dos problemas se ve
estructura que separe la órbita real del azar.

## 4. Veredicto: (b)

Los mecanismos publicados que excluyen órbitas son de cuatro clases, y
ninguna llega al piloto:
1. **Contracción o un único punto 2-ádico** (YAH): en AB no hay ciclos que
   contraigan.
2. **Pasillo finito** (Flatto–Lagarias–Pollington, Bugeaud, Dubickas, Stephan):
   el encierro deja finitos supervivientes y fuerza periodicidad, que la
   aperiodicidad impide (lema 2.2 de FLP, Lema 2 de Dubickas–Novikas). En AB
   el pasillo no existe: las colas cubren `[1,5]`.
3. **Complejidad lineal** (Dubickas 2009): AB tiene complejidad exponencial.
4. **Conteo** (Mahler, Flatto, nuestro `c_L`): da «pocos», nunca «ninguno».

La Prop. 3.2 de Dubickas–Mossinghoff, con un solo resto permitido, es la
forma publicada del «único punto» de la clase 1: fija el punto, que resulta
ser un fantasma. En AB la entropía es positiva y no hay un único punto.

A eso se suman los certificados automáticos (YAH), que sólo han tenido éxito
en clases que contraen o de entropía cero. Las conjeturas de normalidad (AEV)
sólo lo cierran suponiendo algo tan fuerte como la conclusión. Kari–Kopra no
decide una trampa dada.

Calibración más fina que la de J1. El piloto cualitativo:
- equivale a que G se detenga;
- comparte la rama A con la condición de Mahler y la rama B con la H de la
  4.14;
- es consecuencia de 4.12;
- es del mismo tipo que el problema 4/3 de Dubickas–Mossinghoff y que el de
  Mahler (palabras mínimas sin 11), sin pasillo.

Todos siguen abiertos. Se confirma la expectativa J3b.

**Qué refutaría este veredicto:**
- una prueba de 4.12, de que G o H se detienen, del problema 4/3 o de Mahler;
- o un teorema de inexistencia para una trampa dada de antemano con
  retención infinita.

## 5. Prioridad: la cota de complejidad ya estaba en 2009

Dubickas, «On integer sequences generated by linear maps», Glasgow Math. J.
51 (2009) 243–252, Teorema 5: toda órbita divergente de T tiene
`P(X,n)>1,70951129·n` para n grande, con `1,7095...=log 2/log(3/2)`. Su
prueba es la de [Complejidad §4](../perdices20261007/COMPLEJIDAD.md#4-complejidad):
- mismo factor de largo m equivale a congruencia módulo 2^m;
- dos valores distintos;
- crecimiento a lo sumo `(3/2)^n`.

Tras su Teorema 3 observa que una cota así excluye las palabras sturmianas,
y conjetura complejidad `2^n`. En naturales, una órbita inyectiva tiende a
infinito, porque cada valor aparece una sola vez: su Teorema 5 cubre por eso
la cota (4) de Complejidad. Así, la cota (4) y su corolario para naturales
tienen un antecedente de 2009, anterior a De Jesus (2026).

Lo propio de Complejidad sigue siendo:
- la forma entera explícita;
- el umbral `m>=5(n+1)`;
- la versión para `3x+q` y racionales;
- la formalización en Lean.

En esta sesión se agrega la cita a COMPLEJIDAD.md. Para el registro, la
corrección de las filas `perdices_complejidad_factores` y
`perdices_racional_sturmiana` queda propuesta en
[correccion_registro.json](correccion_registro.json) y validada en copia
temporal con el generador ([verificar_correccion.py](verificar_correccion.py),
[evidencia](evidencia_correccion.json)). Sobre las 349 filas, sólo cambia el
campo `fuente` de esas dos, y el registro central queda intacto. Se integrará
junto con las altas Codex pendientes.

## 6. Evidencia, fuentes y pendientes

```powershell
python -B -X utf8 depuracion/judas20261016/cotejar_j2.py --bits 21 --bits-hermana 20 --salida depuracion/judas20261016/cotejo_j2.json
```

Unos 6 s, enteros y `Fraction`. Lee la huella de
[diagnostico_ruta.json](diagnostico_ruta.json) y no repite censos.

```powershell
python -B -X utf8 depuracion/judas20261016/srs_piloto.py --bits 14 --salida depuracion/judas20261016/cotejo_srs.json
python -B -X utf8 depuracion/judas20261016/medidas_srs.py --salida depuracion/judas20261016/cotejo_medidas.json
```

Unos 36 s y 2 s. El primero también escribe [piloto_yah.srs](piloto_yah.srs).

Tipos de afirmación:
- §2 es prueba escrita, formalizada en Lean (`piloto_iff`) y con cotejo
  exhaustivo bajo 2^21;
- la reescritura de §2 es prueba escrita, con la cuenta de cada medida regla
  por regla. La simulación bajo 2^14 y las reescrituras al azar son cotejos
  finitos, y la equivalencia con G no está en Lean;
- §3 es lectura de originales, salvo donde se indica otra cosa;
- las cifras de complejidad son conteo exacto de factores;
- los récords de supervivencia de §3 son mediciones finitas;
- nada de esta nota está en el registro.

```powershell
# desde depuracion/gao20260920/formal; unos 20 s
lake env lean ../../judas20261016/JudasPiloto.lean
```

Fuentes:
- E. Yolcu, S. Aaronson, M. J. H. Heule, [arXiv:2105.14697v3](https://arxiv.org/abs/2105.14697), §4.4–4.6.
- S. Akiyama, Ch. Frougny, J. Sakarovitch, Israel J. Math. 168 (2008) 53–91, [PDF](https://www.irif.fr/~cf/publications/IJM.pdf).
- S. Akiyama, Unif. Distrib. Theory 3 (2008) 91–99, [PDF](https://www.math.tsukuba.ac.jp/~akiyama/papers/Mahler_08-2.pdf).
- A. Dubickas, Glasgow Math. J. 51 (2009) 243–252, [doi:10.1017/S0017089508004655](https://doi.org/10.1017/S0017089508004655).
- S. Eliahou, J.-L. Verger-Gaugry, C. R. Math. 363 (2025) 329–336, [arXiv:2504.13716](https://arxiv.org/abs/2504.13716).
- M. Andrieu, S. Eliahou, L. Vivion, [arXiv:2510.11723](https://arxiv.org/abs/2510.11723).
- R. Stephan, *Confinement schemas and the reach of block certificates*, 12-09-2026, [GitHub](https://github.com/rwst/Confinement-Certificates/blob/e773310aa60d010038c3b1a02ee09dcaacce064d/paper2.pdf). Según [MathWorld](https://mathworld.wolfram.com/Z-Number.html), lo descubrieron y formalizaron Fable 5 y Opus 5, y no consta revisión independiente.
- J. Kari, J. Kopra, RAIRO ITA 51 (2017) 191–204, [arXiv:1710.05737](https://arxiv.org/abs/1710.05737).
- D. Kwon, [arXiv:2502.10132](https://arxiv.org/abs/2502.10132); N. Kumar, [arXiv:2411.03468](https://arxiv.org/abs/2411.03468), retirado.

- A. Dubickas, M. J. Mossinghoff, «Lower bounds for Z-numbers», Math. Comp. 78
  (2009) 1837–1851. Leído completo en el PDF que el usuario dejó el 16-10 en
  `Collatz Investigacion/S0025-5718-09-02211-X.pdf` (fuera de Git), con
  SHA256 `c5b856ab5ad68825537bec3e54effec8e34a46f2f73c819369d37883b08cee07`.
  La descarga automática chocó con la verificación de navegador de la AMS, y
  no se saltó.

- J. C. Lagarias, *The 3x+1 problem: an annotated bibliography (1963–1999)*,
  arXiv:math/0309224v13 (11-01-2011), en el PDF que el usuario dejó el 16-10.
  Se usaron las entradas 62 (Flatto), 117 (Mahler) y 128 (P. Michel, «Busy
  beaver competition and Collatz-like problems», Arch. Math. Logic 32 (1993)
  351–367). La entrada 117 dice «si y sólo si». El original de Mahler sólo da
  la condición necesaria: ya lo corrigió la nota de Mahler del 07-10.

**Pendiente, pedirlo al usuario:** L. Flatto, «Z-numbers and
β-transformations», Contemp. Math. 135 (1992) 181–201. No se halló copia
libre. Su contenido se conoce por la anotación de Lagarias (entrada 62), por
DM (pp. 1839–1840), por AEV y por Stephan: aplica la β-transformación de
Parry con β=3/2.

**Siguiente:** J3b sigue. El 16-10 el usuario aprobó instalar AProVE al día
siguiente. El plan, una escalera de calibración y las salidas están en la
[ruta §11](../../RutaDeJudasIscariote.md#11-siguiente-paso-aprove). TTT2 y
Matchbox quedan como contraste.
