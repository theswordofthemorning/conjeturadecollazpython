# Ocelotas: 18 rachas, o 75 con Rozier–Terracol — 03-10-2026

**Continuación:** [RACHAS_UNILATERALES.md](RACHAS_UNILATERALES.md) formaliza
la criba y su aplicación a trayectorias, y reduce las cotas de semilla
mediante aproximaciones por arriba. Se conserva abajo la evidencia de
esta primera versión. El cierre posterior de
[18 rachas en Lean](DIECIOCHO_LEAN.md) está completo; el de 75 sigue pendiente.

Se afina la [prueba por convergentes](RACHAS_CONVERGENTES.md) sin ampliar
el censo de semillas. **Prueba escrita asistida por cálculo racional
exacto; esta primera versión no tenía cierre Lean completo.** La cola
usa Laurent–Mignotte–Nesterenko (1995), cuyo original ya se cotejó en las
[lecturas aportadas](LECTURAS_20261003.md).

## Enunciado y condiciones

Sea `T(n)=n/2` para n par y `(3n+1)/2` para n impar, en enteros positivos.
Para `n>=2`, sea `k=tau(n)` el primer índice positivo con
`3^S_k(n)<2^k`, donde `S_j(n)` cuenta las entradas impares entre los
primeros j pasos. Suponemos que k existe. Sea r el número de bloques
maximales de unos en esa palabra de paridad. Todos los logaritmos sin
subíndice son naturales; `log2` mide exponentes binarios.

**Bajo LMN, si r<=18, el primer descenso ocurre exactamente en k.**
Un fallo necesita al menos 19 rachas. Si se admite además el corolario
5.4 de Rozier–Terracol v5, lo mismo vale para r<=75 y un fallo necesita
al menos 76. No se afirma que todo primer cruce exista ni que toda órbita
llegue a 1. No interviene una ley probabilística.

## Dónde se recupera el margen

De los lemas de trayectoria ya certificados en Lean, un fallo satisface

\[
n<\frac r\Lambda,\qquad
2^{A_{i+1}}\le(n+1)3^{A_i},\qquad
\Lambda=k\log2-q\log3>0,
\]

con `q=S_k(n)`, `A_0=0`, `A_r=q`; `A_i` cuenta los pasos impares hasta
la racha i. El caso par desciende en un paso y se excluye del fallo.

Sean `q_j` los denominadores de los convergentes de `alpha=log2(3)`,
indexados desde `q_0=1`. Por mejor aproximación, en
`q_j<=q<q_(j+1)`, `j>=1`,

\[
\Lambda>\frac{\log2}{q_j+q_{j+1}},\quad
n<s_j:=\left\lceil\frac{1000R(q_j+q_{j+1})}{693}\right\rceil.
\]

Aquí se usa `log 2>693/1000` y `r<=R`. Como n y s son enteros,
**`n+1<=s_j`**, incluido el borde `n=s_j-1`.
Tomamos cotas racionales superiores `a>alpha`, `b_j>log2(s_j)` e iteramos

\[
C_0=0,\qquad C_{i+1}=\lfloor b_j+aC_i\rfloor.
\]

Aplicar `log2` a la congruencia da
`A_(i+1)<=log2(n+1)+alpha*A_i<b_j+a*C_i`, así que por inducción
`A_i<=C_i`. Además `C_i` es creciente: `b_j>=1`, `a>1`.
Por tanto `q=A_r<=C_r<=C_R`. Si `C_R<q_j`, se elimina todo ese intervalo;
en otro caso, sus semillas están acotadas por s_j.

La criba anterior redondeaba simultáneamente `alpha` a `8/5` y
`log2(s_j)` a la longitud entera en bits de s_j. Para R=18 y j=13:

- `q_j=190537`, `q_(j+1)=10590737`, `s_j=280033091`.
- La nueva cota da `q<=189768<190537`: el intervalo que impedía el cierre
  desaparece.
- El máximo restante ocurre en j=12 y obliga a `n<7837377<2^23`.

## Cálculo exacto y cola infinita

[rachas_afinadas.py](rachas_afinadas.py) encierra `alpha` con 256 bits y
`log2(s_j)` con 128 bits, por cuadrados sucesivos y redondeo dirigido
(64 bits de guarda). Si un bit es ambiguo, el programa se detiene.
Certifica 79 convergentes; los intervalos j=1,...,77 cubren

`1<=q<Q=51700032084971999781389768164307758537`.

Para `q>=Q` se conserva la cota anterior
`q<=G_R m(q)`, `G_R=5(8^R-5^R)/(3*5^R)`, derivada de los lemas Lean.
LMN da `n<R exp(30(log(4q)+21)^2)` porque `k<=2q`, luego sirve

`m(q) <= bits(R)+2+30(log(4q)+21)^2/log 2`.

El certificador comprueba la exclusión con la función de la séptima tanda.
El cotejo usa otro cierre: en `[2^t Q,2^(t+1) Q)`, la cota de q es menor que

`G_R [A+B(x+d*t)^2]`, con
`A=bits(R)+2`, `B=30000/693`, `d=6932/10000`,
`x=d*(bits(4Q)+1)+21`.

Se comprueba exactamente `x>=3d` y `G_R[A+B*x^2]<Q`. Como
`(y+d)^2<2y^2` para `y>=3d`, por inducción el lado derecho es menor que
`2^t Q<=q` en toda la cola. Así se evita depender de una medición o de
recorrer denominadores hasta un tamaño arbitrario.

## Resultados y evidencia

| R | Todo fallo obliga a n menor que | Intervalo decisivo | Cierre |
|---|---:|---:|---|
| 18 | 7 837 377 | 12 | Barrido propio existente, n<8 388 608 |
| 19 | 295 590 485 | 13 | No lo cierra ese barrido |
| 75 | 14 791 827 172 614 383 442 | 32 | Corolario externo, n<=28 000 000 000 000 000 000 |
| 76 | 43 599 691 994 443 572 162 | 33 | No lo cierra ese corolario |

Certificado: [rachas_afinadas.json](rachas_afinadas.json).
[Cotejador independiente](cotejar_rachas_afinadas.py) y
[salida](cotejo_rachas_afinadas.json): los 79 convergentes y los 308
intervalos de R=18,19,75,76 coinciden. Recalcula logaritmos mediante
`log x=2 atanh((x-1)/(x+1))`, suma y resto racionales; reconstruye los
convergentes por matrices; comprueba también la cola por duplicación.
No importa el certificador. Los casos vecinos impiden confundir el
alcance real del certificado con el número de rachas deseado.

El [censo conservado](verificar_r_rachas_23_salida.txt), revisado contra
su [implementación](verificar_r_rachas.py), cubre todas las semillas
`2<=n<2^23` y no detectó fallos. No se ha relanzado. El cotejo anterior
independiente sólo llegaba a 4 674 092: no se presenta como cobertura
independiente de las semillas hasta 7 837 376 que ahora bastan.

Se añadieron dos afirmaciones al [registro versionado](../coherencia20260913/registro.json)
y se regeneró `afirmaciones.db` con `guardarafirmaciones.py`: 253
afirmaciones, controles de vocabulario, referencias e integridad correctos
([salida](registro_afinadas.txt)). Los registros anteriores se conservan.

## Reproducir y continuar

```text
python -B -X utf8 depuracion/cst20260930/rachas_afinadas.py --bits-alfa 256 --bits-semilla 128 --guarda 64 --rmax 80 --salida depuracion/cst20260930/rachas_afinadas.json
python -B -X utf8 depuracion/cst20260930/cotejar_rachas_afinadas.py --certificado depuracion/cst20260930/rachas_afinadas.json --salida depuracion/cst20260930/cotejo_rachas_afinadas.json
```

Unos segundos; no hay barrido de órbitas. La mejora pertenece a Ocelotas;
se conservan los resultados anteriores como evidencia histórica. Lean
mantiene el cierre hasta diez rachas y ahora prueba además la traducción
del corolario publicado a `LMNDebil`. Pendiente: formalizar la criba
afinada y estudiar cotas de aproximación por un solo lado antes de
considerar un censo mayor. Novedad y revisión humana pendientes.
