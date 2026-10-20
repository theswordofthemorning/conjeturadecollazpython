# Perdices: ensayo del denominador de la palabra completa

19-10-2026. Continúa [Compensación relativa](COMPENSACION_RELATIVA.md).
Se mantiene Perdices; no se reclama prioridad. **Este ensayo no obtiene
una cota nueva del reloj universal.** Identifica por qué una congruencia
global concreta tampoco basta como estimación de tamaño.

## 1. Pregunta y criterio exacto

Atajo T sobre enteros positivos: n/2 si n es par y (3n+1)/2 si es impar.
A=1 y B=110 son bloques realizados desde una sola semilla n. Para una
palabra no vacía W, L cuenta pasos T y S cuenta pasos impares. Escribir

```text
N=2^L, D=3^S, N*y=D*n+E,
C=D-N, g=gcd(C,E), q=C/g, r=E/g.
```

No hay ley aleatoria ni condicionamiento probabilístico. Cada bloque
expande, de modo que D>N; C,g,q son impares positivos. El encaje afín
da C<=E<=5C y, por tanto, q<=r<=5q. También se obtiene directamente
componiendo: A tiene punto fijo −1 y B punto fijo −5, y el punto fijo
de una composición expansiva permanece en ese intervalo.

El número racional −r/q es el punto fijo **negativo** de la extensión
afín de W. No es una órbita positiva ni una hipótesis de periodicidad
para la órbita que realiza W.

El criterio de cilindro D*n+E=0 mod N equivale exactamente a

```text
q*n+r=0 mod N.                                      (1)
```

En efecto D=N+gq y E=gr, y g es coprimo con N. La biyección entre
paridades y residuos muestra que (1) también es suficiente para realizar
W: no se han descartado las fronteras interiores. Cada palabra tiene
una única clase de semillas módulo N.

Como q*n+r>0, la condición necesaria de tamaño resultante es

```text
2^L <= q*n+r <= q*(n+5),
L <= ell(n)+log2(q),  ell(n)=ceil(log2(n+5)).         (2)
```

Una cota uniforme `q(W)<=K*2^(theta*L)`, K>=1 y 0<=theta<1,
**sería suficiente** para un reloj: `(1-theta)L<=ell+log2(K)`.
No es necesaria. (1) es exacta; pasar a (2) pierde información del residuo.

Para W=B^b, b>=1, se reduce a q=1,r=5. Para W=(AB)^b, q=11,r=19.
Recupera las barreras de repetición ya conocidas. Falta saber si conserva
una ventaja cuando se mezclan bloques de otra manera.

## 2. Una sola letra destruye esta cancelación

Tomar W=A B^b, b>=0. Componer las fórmulas de A y de B^b da

```text
N=2*8^b, D=3*9^b, E=11*9^b-10*8^b,
C=3*9^b-2*8^b,
3E+8*8^b=11C.                                      (3)
```

C es impar. Cualquier divisor común de C y E divide, por (3), la
potencia de dos `8*8^b`. Por tanto **g=1 para todo b**, y q=C.
Para b>=3, `3*9^b>4*8^b` (base b=3 e inducción multiplicando por 9 y 8),
de donde

```text
q>2*8^b=N.                                         (4)
```

Así (2) ya es trivial incluso antes de introducir n. Además

```text
q/2^L=(3/2)*(9/8)^b-1 -> infinito.
```

No existen K,theta con K fijo y theta<1 que satisfagan la condición
suficiente propuesta para todas las palabras. **No se refuta el reloj**:
A B^b tiene sólo dos rachas y lo acotan los resultados anteriores.
Tampoco se refuta usar simultáneamente varios subtramos: el sufijo B^b
conserva su barrera. Se descarta resumir el tamaño de toda la historia
únicamente mediante este denominador reducido y la estimación (2).

Ejemplo b=3: N=1024, C=q=1163 y E=r=2899. La menor semilla es n=679,
con L=10 y ell=10. La barrera global no explica esa altura.

## 3. Contraste independiente y alcance formal

[Cotejo](cotejar_denominador.py), con enteros y Fraction:

- Las 2046 palabras no vacías de hasta diez bloques, dos representantes
  por cilindro, dos constructores de semillas y recorrido literal de T.
- Familia A B^b para b=0..64; controles positivos B^b y (AB)^b para b=1..64.
- Los 34 testigos distintos del [censo histórico](../medicion_salida_ab.json),
  reconstruyendo sus paridades y comprobando el representante de cada palabra.
  En 33 no hay cancelación (g=1); sólo en dos se tiene q<N, requisito mínimo
  para que (2) aporte una restricción sobre n+5 mayor que uno.

[Resultado exacto](cotejo_denominador.json). No se rehizo el censo de
719 millones de nodos ni se infiere una frecuencia asintótica de estos datos.
La familia de §2, no el barrido, prueba la obstrucción universal.

[Lean](PerdicesDenominadorGlobal.lean) certifica el núcleo afín de (1),
la barrera entera (2), la coprimalidad de (3) y (4). La composición
orbital general, su equivalencia con las paridades, la identificación
de g como divisor impar, el encaje y los corolarios logarítmicos conservan
la prueba escrita; no se atribuye a este módulo una nueva formalización
del lenguaje entero. Revisión humana pendiente.

Reproducción del cotejo:

```powershell
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/cotejar_denominador.py --bloques-max 10 --familia-max 64 --salida depuracion/perdices20261007/congruencias_codex20261016/cotejo_denominador.json
```

El [verificador Lean](comprobar_denominador.py) recibe `--lean` con la ruta
del ejecutable 4.32.2 y `--salida` con la ruta del JSON de evidencia.
Comprueba versión, fuentes e imports directos de Mathlib fijado y
`#print axioms`; no usa `native_decide`. [Evidencia](evidencia_denominador.json)
y [salida](evidencia_denominador.txt).

## 4. Decisión de ruta y mensaje de Claude

El [mensaje del 19 de octubre](../../judas20261016/escalera/yah/PENDIENTES.md)
informa de búsquedas sin cierre al mezclar ramas, incluso debilitadas.
Es útil para evitar duplicar corridas y para recordar que un UNSAT sólo
descarta la forma buscada. No prueba que la mezcla sea intratable, ni
modifica ninguna hipótesis de Perdices. Las cifras y procesos se citan
como estado de esa nota; aquí no se inspeccionó ni se intervino su máquina.

El [artículo de YAH](https://arxiv.org/html/2105.14697v3) propone precisamente
buscar interpretaciones matriciales y obtiene debilitamientos, sin resolver
Collatz. Es una herramienta posible si aparece un sistema reducido concreto,
no evidencia de que prolongar una búsqueda vaya a cerrar nuestro reloj.

**Balance sincero:** hay matemáticas verificables y eliminación de intentos
falsos. Esta sesión no ha encontrado el mecanismo aritmético pendiente.
La abundancia de lemas, pruebas Lean y horas de CPU no mide la distancia a
Collatz. Resolver el reloj A/B tampoco resolvería por sí solo MuroB general
ni la ausencia de circuitos no triviales.

**Siguiente prueba de admisión:** una propuesta debe conservar el residuo
de (1), o relacionar varios subtramos desde la misma semilla, y obtener una
desigualdad cuyo coeficiente no crezca con los cambios. Debe explicar por
qué A B^b conserva una cota usando su sufijo pese al fracaso de q global,
y aportar información en los testigos no periódicos guardados. Un nuevo
porcentaje, un número fijo de cambios o un barrido mayor no cumplen eso.
Hasta disponer de tal propuesta, no se justifica otra corrida larga ni
anunciar un avance hacia el cierre universal.
