# Perdices: la carga terminal se convierte en reloj

18-10-2026. Continúa [Barrera](BARRERA.md). Se conserva el nombre Perdices,
sin reivindicar prioridad bibliográfica.

**Resultado:** toda carga terminal V permite añadir exactamente V pasos
reales a la palabra, conservando la semilla. Por tanto una cota uniforme
del reloj controla simultáneamente L+V. La existencia del presupuesto P
equivale a la existencia de un reloj logarítmico uniforme. **No se demuestra
ninguno de esos dos enunciados.**

**Continuación:** [Pendiente uno](PENDIENTE_UNO.md) construye una familia
real con L-ell(n) sin cota superior. Todo reloj uniforme necesita C>1;
la existencia de ese reloj con pendiente mayor sigue abierta.

## 1. Dominio y continuación exacta

T(x)=x/2 para x par, (3x+1)/2 para x impar, sobre naturales positivos.
A=1 y B=110 son bloques de paridades reales. Una palabra W, también vacía,
lleva n a x; L cuenta pasos de T. Para c=1 o c=5, sea V=v2(x+c).
No hay ley aleatoria ni condicionamiento probabilístico. No se cambia n.

Existe una palabra Q de A/B, realizada desde x, con exactamente V pasos:

```text
c=1:  Q=A^V.
c=5:  V=3q+r, 0<=r<3,  Q=B^q A^r.                    (1)
```

Prueba: un A satisface 2(y+1)=3(x+1); un B, 8(y+5)=9(x+5).
La divisibilidad por 2 o por 8 garantiza respectivamente las paridades
reales 1 o 110, y los cocientes son naturales positivos. Por inducción,
2^k|x+1 permite A^k; 2^(3q)|x+5 permite B^q. Después de estos B,
la frontera z satisface

```text
z+5=9^q*(x+5)/8^q,  por tanto 2^r | z+5.
```

Como r<=2, también 2^r|4 y por resta 2^r|z+1. Esto permite A^r.
No se pierde un resto de dos pasos: ese resto se convierte en A reales.
El sufijo no necesita ser maximal. El caso V=0 usa la palabra vacía.
La prueba vale incluso si c no corresponde al último bloque de W.

## 2. Cualquier cota del reloj absorbe la carga

Fijar n y un número real H. Son equivalentes:

```text
Para toda W real desde n:                  L <= H.
Para toda W real desde n y c en {1,5}:      L+v2(x+c) <= H.     (2)
```

La primera implica la segunda aplicándola a WQ, de longitud L+V por (1).
El recíproco descarta V>=0. La cuantificación incluye la palabra vacía,
de modo que también controla las cargas iniciales. No supone que ya se
conozca un H finito ni demuestra que exista.

## 3. Equivalencia con el presupuesto universal

Sea ell(n)=ceil(log2(n+5)). En una palabra no vacía, v_in usa la constante
del primer bloque, v_fin la del último. El [balance firmado](../RECARGAS.md#1-dominio-índices-y-presupuesto-elegido)
L=v_in+Eeta-v_fin transforma P exactamente en

```text
epsilon*L+v_fin <= v_in+alpha*ell(n)+beta,              (P')
epsilon>0, alpha,beta>=0, constantes uniformes.
```

El balance orbital general conserva su derivación escrita previa. El
nuevo módulo formaliza P' directamente, con constantes reales.

**De P' al reloj.** Siempre v_in<=ell(n) y v_fin>=0, luego

```text
L <= ((1+alpha)/epsilon)*ell(n)+beta/epsilon.           (3)
```

También vale para la palabra vacía. **Del reloj a P'.** Si existen C,D>=0
tales que L<=C*ell(n)+D para toda n>=1 y toda palabra real, (2) da
L+v_fin<=C*ell(n)+D. Por v_in>=0, esto implica P' con
epsilon=1, alpha=C, beta=D. En consecuencia,

```text
Existe P' uniforme
  <=> existe C,D>=0 con L<=C*ell(n)+D universalmente.  (4)

P'(epsilon,alpha,beta)
  => P'(1,(1+alpha)/epsilon,beta/epsilon).             (5)
```

(5) cambia las constantes: **no** mejora epsilon manteniendo K=2*ell.
La prueba necesita todas las palabras; el sufijo B^q A^r puede añadir un
cambio de tipo. No permite trasladar sin más los presupuestos restringidos
a dos o tres cambios.

La [conjetura de Salidas](../SALIDAS.md#1-convenciones-y-resultados-finitos),
lambda(n)<=3log2(n)+1, bastaría para P'(1,3,1). La medición de Salidas no
demuestra esa conjetura. Tampoco se deduce un reloj logarítmico de la mera
terminación individual, ni Collatz de esta equivalencia.

## 4. Evidencia y obligación pendiente

[PerdicesRelojTerminal.lean](PerdicesRelojTerminal.lean) certifica catorce
lemas: continuación desde divisibilidad, concatenación orbital, (1), (2),
carga inicial, (3), (4) y (5). Usa el Camino anterior, cuyos pasos se
identifican con T literal en `paso_a_real` y `paso_b_real`. No usa la
extracción de ventanas que permanece por escrito en Barrera.

[Compilación](evidencia_reloj.json) y [salida](evidencia_reloj.txt): transporte
y módulo nuevo recompilados desde fuente con Lean 4.32.2 y Mathlib fijado;
22 consultas de axiomas, catorce nuevas y ocho del transporte. Sólo
propext, Classical.choice y Quot.sound; sin sorryAx. Se cotejan los imports
directos, no toda la cadena transitiva de Mathlib.

[Cotejo independiente](cotejo_reloj.json): 2304 casos de semilla y palabra,
4608 continuaciones, ambos potenciales, palabra vacía, hasta cinco bloques,
cargas prescritas 0..16 y 65, dos representantes por cilindro. Dos
construcciones independientes de cilindros, T literal y fórmulas racionales
contrastan (1); los tres restos de V módulo 3 están presentes. Es una
verificación finita, no evidencia de un reloj uniforme.

**Siguiente obligación:** obtener una cota L<=C*ell(n)+D uniforme en las
palabras reales, o refutar su existencia. La carga terminal deja de ser
una obligación separada. La suma ponderada anterior aún no proporciona
esa cota; sus pesos pueden crecer geométricamente. P, MuroB y Collatz
siguen abiertos. La equivalencia se incorpora al registro versionado y
al catálogo mediante el generador, conservando las 352 afirmaciones previas.

```powershell
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/comprobar_reloj.py --salida depuracion/perdices20261007/congruencias_codex20261016/evidencia_reloj.json
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/cotejar_reloj.py --bloques-max 5 --carga-max 16 --carga-grande 65 --traslados 2 --salida depuracion/perdices20261007/congruencias_codex20261016/cotejo_reloj.json
```
