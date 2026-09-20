# Mangostas–Gacelas: reloj físico por bloques

## Enunciados y ley

Mapa atajo `T(x)=x/2` si x es par y `(3x+1)/2` si es impar.
La cadena usa el estado `{v,3^k*v+c}`, c entero firmado, y bits iid
justos que representan la paridad del ancla v. Parte de `(2,c0)` y se
detiene al llegar por primera vez a k=1. Ese instante es tau, no la
fusión del par. El tiempo cuenta pasos físicos desde cero.

Sea M_h el número de pasos mixtos ejecutados antes de h o de tau,
incluido el paso que sale del interior. Para n,a,s naturales con
`a>=2+floor(log2(n+2))`, p=2^-s y B=a+s+1:

    P(tau>nB y M_(nB)<n) <= n*p.                         (M6)

Si T_n es el mínimo entre tau y el tiempo del n-ésimo mixto, el
evento es `T_n>nB`. Para n=0 ambos lados son cero, tomando T_0=0.
Para L,n>=1 se obtiene además

    P(tau>nB) <= 1/L+(L-1)/n+n*2^-s.                    (H3)

Los dos enunciados están formalizados en
[Reloj.lean](formal/Reloj.lean), `reloj_original` y `cola_excursion`.
Se trata de promedios exactos sobre todas las palabras de longitud nB,
con multiplicidad, no de simulaciones ni de leyes condicionadas a sobrevivir.

## Derivación independiente

1. En un estado interior fijo k>=2, defínase A=v2(3^k-1). Para una
   racha compartida de longitud L, el evento `L>=h` exige que los h
   pasos se ejecuten compartidos; permite que el último deje c impar.
   La clasificación diádica de c da, con r=min(v2(c),A),
   `L=r` si r<A; si r=A, hay exactamente `2^min(h,A)` palabras
   de h bits que ejecutan h pasos compartidos. Para c=0 se toma r=A.
   Por tanto `P(L>=A+s)<=2^-s` para todo c firmado. Ampliar A a
   cualquier a>=A conserva la cota.
2. A=1 para k impar y A=2+v2(k) para k par. En ambos casos
   `A<=2+floor(log2(k))`. Los compartidos no cambian k y un mixto
   lo aumenta como máximo en uno: desde la raíz, `k<=M+2`.
3. Divídase el tiempo en bloques deterministas de B pasos. Sea
   F_j el evento «vivo en jB con menos de j mixtos». Condicionado
   sólo al prefijo hasta jB, si ya hubo al menos j+1 mixtos o la
   excursión salió, F_(j+1) es imposible. Si hubo menos de j,
   su probabilidad es como máximo 1 y el prefijo pertenece a F_j.
   En el caso restante, hay exactamente j mixtos y k<=j+2<=n+2.
   Para seguir vivo sin alcanzar j+1 mixtos deben ejecutarse B
   compartidos consecutivos. Los puntos 1–2 acotan ese caso por p.
   Así `P(F_(j+1))<=P(F_j)+p`. Como F_0 es vacío, la inducción
   entrega M6. La formalización usa el invariante de altura para
   todos los estados alcanzables y la composición de promedios.
4. A tiempo H=nB, el indicador de supervivencia es como máximo
   el de `tau>H y M_H<n` más el de `M_H>=n`. M6 controla el primero;
   [Banda.lean](formal/Banda.lean) controla el segundo por
   `1/L+(L-1)/n`. Su suma es H3.

No se escoge un bloque mirando el futuro ni se supone independencia
entre los eventos F_j. Sólo se promedian los bits futuros en cada
prefijo de longitud determinista.

## Certificados, contraste y límite

- [RachasEnteras.lean](formal/RachasEnteras.lean): clasificación de
  offsets, conteo exacto y enlace con la transición original.
- [UmbralRachas.lean](formal/UmbralRachas.lean): valoración de
  `3^k-1`, cota logarítmica y ampliación del umbral.
- [Reloj.lean](formal/Reloj.lean): contador, invariante de altura,
  bloques, M6 y H3.

La [evidencia Lean](evidencia_reloj_lean.json) registra versión,
dependencias, salida y hashes. Las consultas de axiomas no usan `sorryAx`.
El [contraste independiente](verificar_reloj.py) reconstruye dos enteros
positivos y aplica T, sin evaluar las definiciones Lean. Pasaron 832
conteos de rachas (k=2..12), con 189 igualdades en la cota; 280 casos
M6, 720 H3 y 2.312 descomposiciones del evento para h=0..16 y ocho
offsets, incluidos cero y signos opuestos. Estos son controles finitos
de interpretación; la universalidad procede de la prueba.
[Salida exacta](evidencia_reloj_exacto.json).

Esto cierra el enlace formal del reloj interior usado por CF_H.
La [ventana conjunta VH](Ventana_conjunta.md) se certificó después;
quedan el protocolo global de ensayos y el transporte a clases
residuales. No demuestra todavía CF_H, phi=1,
la conjetura de Gao ni la de Collatz. Tampoco resuelve la antigua
ventana de W de tamaño constante.
