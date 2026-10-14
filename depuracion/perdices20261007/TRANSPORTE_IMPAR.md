# Perdices: transporte de partes impares y presupuesto con un cambio

14-10-2026. Continúa la obligación de [Perfiles](PERFILES.md#5-obstrucción-al-rango-y-límites-exactos)
y el [piloto acordado](../coherencia20260913/RUTA_339_20261012.md#4-dónde-pondría-el-esfuerzo-principal).
Se conserva el nombre Perdices; no se reclama prioridad bibliográfica.

**Resultado positivo parcial:** todo prefijo real A/B que cambia de tipo
de bloque a lo sumo una vez satisface `Eeta <= 2*ell(n)`, donde
`ell(n)=ceil(log2(n+5))`. Por tanto cumple (P) con epsilon=1 y K=2*ell,
y también el candidato epsilon=1/2, K=2*ell. No hay restricción sobre
la semilla ni sobre las longitudes de esas dos rachas.

Para cualquier cantidad de cambios se demuestra y formaliza el transporte
global (3). El presupuesto con un cambio, el producto firmado (2) y la
familia de §5 tienen prueba escrita; su formalización completa queda
pendiente. **No se demuestra el presupuesto para varias alternancias ni
la salida universal del piloto.** Revisión humana pendiente.

## 1. Dominio, unidades y partes impares

Atajo T sobre enteros positivos: T(x)=x/2 para x par y (3x+1)/2 para
x impar. A=1 y B=110 son palabras de paridades reales desde una misma
semilla n. Para una palabra no vacía p_0,...,p_(s-1), sus fronteras son
x_0=n,...,x_s. Cada bloque aumenta estrictamente la frontera. No se
asigna distribución probabilística ni se cambia de semilla entre bloques.

Usar c_A=1, c_B=5, d_A=1, d_B=3 y e_A=1, e_B=2. Entonces

```text
2^d_p (y+c_p) = 3^e_p (x+c_p).
L = suma d_p,                 S = suma e_p.
v_in = v2(n+c_(p_0)),        q_in = (n+c_(p_0))/2^v_in.
v_fin = v2(x_s+c_(p_(s-1))), q_fin = (x_s+c_(p_(s-1)))/2^v_fin.
```

L cuenta pasos de T; S cuenta entradas impares, con 2L/3<=S<=L.
Las valuaciones se aplican a enteros positivos y las partes impares
son enteros positivos impares. Con las recargas **firmadas** de
[Recargas, §1](RECARGAS.md#1-dominio-índices-y-presupuesto-elegido),

```text
Eeta = suma [v2(x_(i+1)+c_(p_(i+1))) - v2(x_(i+1)+c_(p_i))],
L = v_in + Eeta - v_fin.                              (1)
```

## 2. El factor de los cambios queda acotado

Definir el producto racional positivo

```text
C = producto, 0<=i<s-1, de
    (x_(i+1)+c_(p_(i+1))) / (x_(i+1)+c_(p_i)).
```

Dentro de un bloque la parte impar se multiplica por 3^e_p. Al cambiar
de potencial, su cociente se multiplica por el factor correspondiente
de C y por 2^(-eta_i). Telescopar da, incluso si alguna recarga es negativa,

```text
2^Eeta * q_fin = 3^S * q_in * C.                      (2)
```

Los exponentes negativos se interpretan en los racionales. No se
sustituye Eeta por la suma de sus partes positivas.

Sea r(x)=(x+5)/(x+1), estrictamente decreciente para x>=1. Los cambios
A→B aportan r(x); los B→A, su inverso. Como las fronteras crecen y
los cambios alternan, los logaritmos forman una suma alternada de
términos positivos decrecientes. Agrupar parejas desde ambos extremos
da: si se empieza por A, 1<=C<=r(n); si por B, 1/r(n)<=C<=1.
Incluye cero cambios, cuando C=1. En forma única:

```text
(n+1)/(n+c_(p_0)) <= C <= (n+5)/(n+c_(p_0)).
```

El factor acumulado queda entre 1/3 y 3, con intervalo mucho menor
para semillas grandes. No puede aportar por sí solo una ganancia
proporcional a L en (P): log2(C) está acotado independientemente de L.

## 3. Contraste independiente y certificado universal

Sin usar valuaciones ni el producto de cambios, cada bloque satisface

```text
3^e_p (x+1) <= 2^d_p (y+1),
2^d_p (y+5) <= 3^e_p (x+5).
```

Para A hay igualdad en la primera y una diferencia 4 en la segunda;
para B hay igualdad en la segunda y una diferencia 4 en la primera.
Una inducción sobre la palabra, multiplicando siempre por factores
positivos, obtiene

```text
3^S(n+1) <= 2^L(x_s+1),
2^L(x_s+5) <= 3^S(n+5).
```

En consecuencia, para cualquier entero c entre 1 y 5, no solamente
para la constante del último bloque,

```text
3^S(n+1) <= 2^(L+v2(x_s+c))*impar(x_s+c) <= 3^S(n+5). (3)
```

Es la misma cota de §2 por (1) y (2). Esta segunda derivación es la
formalizada en [PerdicesTransporteImpar.lean](PerdicesTransporteImpar.lean).
`Paso A x y` es 2y=3x+1 y `Paso B x y` es 8y=9x+5 sobre naturales.
Los teoremas `paso_a_real` y `paso_b_real` prueban equivalencia con
las paridades y pasos de T; `Camino` enlaza esas relaciones sin cambiar
la frontera compartida. `transporte_impar` vale para cualquier lista
finita, incluida la vacía. La interpretación de (3) es universal,
no una extrapolación del cotejo finito.

## 4. Cierre cuando hay como máximo un cambio

Si no hay cambios, Eeta=0. Si hay exactamente uno, escribir la palabra
como p^a q^b, p!=q, a,b>=1. Sea u=a*d_p la longitud hasta el cambio y
y su frontera. Consumir el primer potencial da

```text
u <= v_in,   2^u <= 2^v_in <= n+c_p <= n+5.
```

Por el encaje superior de §3 aplicado a esa primera racha, y porque
S_1<=u y 3^S_1<=4^u,

```text
y+5 <= 2^u(n+5) <= (n+5)^2 <= 2^(2*ell(n)).
```

Así `v2(y+c_q)<=2*ell(n)`. Sólo hay una recarga posiblemente distinta
de cero y se resta una valuación no negativa; por tanto

```text
Eeta = v2(y+c_q)-v2(y+c_p) <= 2*ell(n),
L+v_fin <= v_in+2*ell(n) <= 3*ell(n).                  (4)
```

Esto prueba (P) con epsilon=1 para esta subclase. La cota de longitud
(4) sólo cubre prefijos con como máximo un cambio: no es una cota de
salida de la clase A/B completa. Las alternancias posteriores pueden
recargar desde fronteras mayores; aplicar (4) reiniciando n allí no
produce un presupuesto desde la semilla original.

## 5. Una sola alternancia ya permite colapso de la parte impar

Para cualquier a>=1, poner

```text
k=2*3^(a-1), q=(2^k-1)/3^a, n=2^(a+2)*q-1.
```

q es entero: 3^a divide 2^k-1 por inducción. El caso a=1 es 3|4-1;
al pasar de a a a+1 se eleva 2^k=1+3^a*t al cubo, cuyos tres términos
no constantes son divisibles por 3^(a+1). q es positivo e impar.

La misma semilla realiza A^a B: tras A^a se llega a
`2^(k+2)-5 = 3 mod 8`, y B lleva a `9*2^(k-1)-5`. Luego

```text
L=a+3, v_in=a+2, v_fin=k-1, Eeta=k, q_in=q, q_fin=9.   (5)
```

La parte impar terminal puede permanecer en nueve mientras la inicial
crece sin cota. Así, una supuesta monotonía de partes impares tampoco
cierra el argumento. Esto es compatible con (4): las semillas de (5)
crecen con a. No se obtiene una órbita infinita desde una semilla fija.
Tampoco se refuta por (5) el presupuesto doble.

## 6. Obligación que queda para varias alternancias

El candidato epsilon=1/2, K=2*ell equivale por (1) a

```text
L+2*v_fin <= 2*v_in+4*ell.                             (P2)
```

Para precisar el crecimiento requerido sin logaritmos numéricos, poner
`Q=2^(2*v_in+L+4*ell)*q_fin^2`. De (3) se deduce:

```text
Condición necesaria para P2: 3^(2S)*(n+1)^2 <= Q.
Condición suficiente para P2: 3^(2S)*(n+5)^2 <= Q.      (6)
```

En efecto, elevar (3) al cuadrado sitúa
`2^(2L+2*v_fin)*q_fin^2` entre los dos miembros izquierdos; comparar
potencias de dos y cancelar q_fin^2>0 prueba ambas implicaciones.
No se afirma equivalencia de P2 con cada desigualdad por separado.

El hueco entre las condiciones es sólo el factor ((n+5)/(n+1))^2.
Pero **ninguna de ellas queda probada para todas las alternancias**.
La identidad (2) y el encaje (3) no bastan para deducirlas: organizan
el transporte y acotan el cambio de potencial, sin dar la nueva
estimación aritmética de q_fin que necesita (6).

Siguiente acción: buscar esa estimación en cadenas de dos o más
alternancias, usando las ramas enlazadas de
[Cancelaciones, §3](CANCELACIONES.md#3-f-observar-solamente-los-cambios).
Hay que conservar n y la carga terminal; multiplicar presupuestos
locales evaluados en semillas nuevas dejaría abierto el mismo problema.

## 7. Evidencia y reproducción

- [Cotejo exacto](cotejo_transporte_impar.json): 396 palabras construidas,
  dos representantes por cilindro, 792 casos; 624 con hasta un cambio y
  35 con recargas negativas. Incluye las dos orientaciones, rachas hasta
  12 bloques, diez miembros de (5), igualdades extremas, n=59 con BA y
  recarga -1, y el contraejemplo histórico n=4591.
- Las 34 semillas ya guardadas aportan 1817 prefijos completos, sin
  ampliar el censo. Se cotejan T literal, composición afín, dos
  implementaciones de valuación, producto racional C y (6).
- [Lean](evidencia_transporte_impar.json) y [salida](evidencia_transporte_impar.txt):
  Lean 4.32.2, ocho consultas con sólo axiomas estándar. Fuente compilada
  de nuevo, imports directos cotejados con Mathlib fijado; sin auditoría
  transitiva completa. Formaliza §3 y un criterio algebraico suficiente;
  §§2, 4–6 conservan prueba escrita.
- [Conservación y controles](evidencia_sesion_transporte_impar.json):
  las 342 afirmaciones previas y respuestas.db permanecen intactas;
  una alta nueva, mapas regenerados y enlaces comprobados.

```powershell
python -B -X utf8 depuracion/perdices20261007/cotejar_transporte_impar.py --bloques-max 6 --racha-max 12 --traslados 2 --familia-a-max 10 --salida depuracion/perdices20261007/cotejo_transporte_impar.json
python -B -X utf8 depuracion/perdices20261007/comprobar_transporte_impar.py --salida depuracion/perdices20261007/evidencia_transporte_impar.json
```
