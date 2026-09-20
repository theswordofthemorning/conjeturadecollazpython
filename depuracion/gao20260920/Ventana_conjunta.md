# Gacelas: ventana armónica conjunta, certificada

20-09-2026. Se cierra VH para la primera excursión, incluyendo sus
parámetros y la uniformidad sobre offsets acotados. **CF_H continúa
conjeturada**: faltan los ensayos globales y el transporte formal a clases.

## Objeto, evento y parámetros

Mapa atajo `T(x)=x/2` si x es par y `(3x+1)/2` si es impar. La cadena
parte de `(2,c)`, c entero firmado; cada bit justo independiente indica
la paridad del ancla de `{v,3^k*v+c}`. Tau es la primera llegada a k=1,
no la fusión. El tiempo cuenta pasos físicos, comenzando en cero.

Para una cota C entera, escribir todos los logaritmos en base 2 y definir

    m=ceil(log2(2+|C|)),       T=32 max(32,m),
    Q=T+1,                    L=16Q,
    n=L^2,                    a=2+floor(log2(n+2)),
    s=3 ceil(log2(n+1)),       H=n(a+s+1),
    R=[128(H+1)Q]^2,           G=3(R+1).

Para todo c entero con |c|<=|C|:

    P_c(T<tau<=H y |c_tau|<=G) >= 1/(4Q).               (VH)

`ParametrosVentanaGao.ventana_uniforme` prueba este enunciado sobre
el árbol finito completo de H bits. `ventana_explicita` es el caso C=c.
La cota y el horizonte pueden fijarse antes del ensayo. No hace falta
deducir esta uniformidad a partir de una afirmación informal de monotonía.

El evento formal `salida_buena` contiene un prefijo y un sufijo cuya
concatenación es la palabra completa. Todas las entradas del prefijo
son interiores, su extremo es `(1,d)`, su longitud es mayor que T y
`|d|<=G`. Por ello ese prefijo termina exactamente en la primera salida;
su longitud no excede H. Se acota el offset **en la salida**, no después.

## Prueba conjunta y correspondencia con Lean

1. [Palabras.lean](formal/Palabras.lean) define un promedio recursivo
   con peso 1/2 por bit y lo identifica con los promedios de las cadenas.
   Promediar una función del prefijo de T bits entre todas las palabras
   de H bits conserva su media de longitud T. El evento de cruce del
   producto desde T se identifica con `ProductoGao.cruce_desde T (H-T)`.
   El cruce incluye ambos extremos temporales.
2. [SalidaPalabras.lean](formal/SalidaPalabras.lean) extrae la primera
   salida de una palabra que sobrevivió a T y salió antes de H. Evitar
   el cruce normalizado implica `Pi_tau<=rho^tau`, rho=31/32. La
   contracción inicial `rho^T |c|/9<=1` da `|Pi_tau*c/9|<=1`.
   Evitar el cruce de W entre 0 y H da `|W_tau|<=R`. La identidad
   afín hasta la salida, ya certificada, entrega `|d|<=3(R+1)`.
   W continúa multiplicativamente después de salir, como exige su cota
   de momentos; no se congela ni se evalúa una media en una parada aleatoria.
3. [Ventana.lean](formal/Ventana.lean) combina los indicadores sobre
   esa misma palabra: supervivencia a T es como máximo éxito, más
   supervivencia a H, más cruce de producto, más cruce de W. Al promediar:

       P(exito) >= 1/(T+1) - P(tau>H) - (61/62)^T - 1/(4Q).

   No se exige independencia entre esos cuatro eventos. H3 controla
   la supervivencia tardía bajo la ley original.
4. [ParametrosVentana.lean](formal/ParametrosVentana.lean) descarga
   todas las condiciones aritméticas. Prueba `T>=1024`, `T<=H`, la
   contracción inicial y el coste H3 `<=1/(4Q)`. La cota del producto
   procede de `4(T+1)61^T<=62^T`: base entera en 1024 e inducción
   usando `61(T+2)<=62(T+1)`. Los tres costes restados son como máximo
   `1/(4Q)` cada uno; queda el cuarto restante de `1/Q`.

La prueba usa enteros, potencias y logaritmos enteros exactos. No
supone convergencia de Collatz, absorción global ni una ley modificada
por supervivencia futura. El radio R crece con T; sigue sin resolver
el P2 antiguo de ventana constante para W bajo condicionamiento.

## Validación y siguiente obligación

Los cuatro módulos añaden 22 consultas de axiomas. La
[compilación y sus hashes](evidencia_ventana_lean.json) no contienen
`sorryAx`. Se fija Lean 4.32.2 y el commit de Mathlib del proyecto.
La universalidad de VH procede de ese certificado, no del barrido.

[verificar_ventana.py](verificar_ventana.py) reconstruye pares positivos
y utiliza `Fraction`. En h=0..8, siete offsets y cuatro radios pasó
3.577 palabras, 114.716 inclusiones de eventos y 315 cotas de producto.
Incluyó 81 palabras con salida exactamente en H y 10.312 cambios de W
posteriores a la salida. La aritmética de parámetros se contrastó
también para ocho offsets, hasta 2^1024, sin enumerar sus enormes H.
[Evidencia exacta](evidencia_ventana_exacta.json).

El [ensayo finito](Ensayo_finito.md) conecta después esta ventana con
Hormigas y certifica un piso de fusión antes de H+D. Siguiente:
formalizar las guardias, separación y número de ensayos de duración fija.
VH es un ingrediente local: no certifica CF_H, phi=1
ni la conjetura de Gao. Sigue pendiente cotejar el artículo primario.
