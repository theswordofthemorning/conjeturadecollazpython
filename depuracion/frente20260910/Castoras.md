# Balance de las Castoras

10-09-2026. Balance de paridad, salida y mezcla para el exceso condicional.
Nombre del registro local; no se reclama novedad bibliografica para la
identidad clasica de varianza que se aplica aqui.

## Resultado y alcance

**Actualizacion posterior:** [Erizas](Erizas.md) excluye el margen
uniforme en todas las escalas incluso para las leyes alcanzables. El
balance y los testigos de esta nota siguen validos; se retira ese
objetivo global del apartado "Proximo ataque". Prueba escrita con
ingredientes Lean, aun sin formalizacion integral ni revision externa.

Para una distribucion finita arbitraria de conteos no negativos en
`(k,c)`, `k>=2`, con masa V>0, el paso de la excursion satisface

    (1-s) e_{t+1}(m) = e_t(m+1) - Q - R - s U - Delta.       (C)

La excursion termina al alcanzar k=1. No se identifica esa salida con
fusion del par. Todas las cantidades de (C) se definen abajo, y el lado
derecho usa las cuatro corrientes N0, N1, A, D, con sus pesos reales.

Es una IDENTIDAD, no una cota de contraccion. La demostracion general
esta escrita aqui. Lean formaliza sus identidades algebraicas escalares,
la equivalencia del umbral y dos contraejemplos concretos completos
(conteos, transicion y excesos). El enlace general de esas identidades
con todas las sumatorias de la cadena NO esta formalizado de extremo a
extremo: lo justifica esta demostracion y se cruza en Python.

## Definiciones

Fijar N=2^m. En cada altura k, sean n_k la masa, a_k la fraccion par,
b_k=1-a_k la impar, y P_k=n_k/V. Los grupos vacios aportan cero.
Sean E_{k,0}, E_{k,1} sus excesos internos:

    E_{k,b} = N sum_r p(r | k,b)^2 - 1.

Cada grupo ocupa N clases en el modulo padre 2N. No se usa 2N para
normalizar su exceso interno. Definir

    G = sum_k P_k [a_k E_{k,0} + b_k E_{k,1}],
    Q = sum_k P_k (a_k-b_k)^2,
    R = sum_k P_k (a_k-b_k)[a_k E_{k,0} - b_k E_{k,1}].

Sea O la masa impar de k=2. La fraccion de ramas que sale es
`s=O/(2V)`, por lo que `0<=s<=1/2` y la masa hija es `V'=2V-O`.
Sea `U=E_{2,1}`, o cero si ese grupo esta vacio.

En cada altura hija j hay hasta cuatro corrientes no vacias i, de masas
M_{j,i}, leyes p_{j,i} sobre N residuos, y masa total S_j. Definir

    D_{j,i,l} = N sum_r [p_{j,i}(r)-p_{j,l}(r)]^2,
    Delta = (1/(2V)) sum_j sum_{i<l}
              (M_{j,i} M_{j,l}/S_j) D_{j,i,l}.

Son no negativos Q, U y Delta. R puede ser negativo. Delta es cero
exactamente cuando, dentro de cada altura hija, todas las corrientes
no vacias tienen la misma ley. No se exige igualdad entre alturas.

## Demostracion

1. Separar pares e impares en el exceso padre da

       e_t(m+1) = sum_k P_k [2a_k^2(1+E_{k,0})
                             +2b_k^2(1+E_{k,1})-1]
                = G+Q+R.

   La segunda igualdad es `separar_paridad` en Lean, usando a_k+b_k=1.

2. Escribiendo c=2u o c=2u+1, cada corriente aplica una biyeccion
   afín de coeficiente 1 o 3 sobre los N residuos. Conserva, por tanto,
   el exceso interno de su grupo fuente. Si todas las ramas vivieran,
   la suma masa por exceso de las corrientes seria 2VG. La unica rama
   descartada aporta OU. La suma efectiva es `2VG-OU`.

3. Para cualquier mezcla de leyes, la identidad de varianza ponderada da

       S_j e_hija,j = sum_i M_{j,i} E_{j,i}
                     - sum_{i<l}(M_{j,i}M_{j,l}/S_j)D_{j,i,l}.

   Se obtiene multiplicando y sumando, residuo a residuo, la identidad
   escalar `varianza_cuatro` de Lean. Los pesos cero aportan cero.
   Sumando alturas: `V' e_{t+1}(m)=2VG-OU-2V Delta`.
   Dividir por 2V y sustituir G=e_t-Q-R entrega (C).

## El umbral, con todos los costos

Abreviar E=e_t(m+1), e'=e_{t+1}(m), B=Q+R+sU+Delta. Para cualquier rho,

    e' < rho E  <=>  B > [1-rho(1-s)]E.

Esta equivalencia esta en Lean (`contraccion_iff`), con la hipotesis
explicita s<1. Definir el margen respecto de 1/2:

    H = B - (1+s)E/2 = (1-s)(E/2-e').

Un margen uniforme `H >= epsilon(1-s)E`, epsilon>0 fijo, entregaria
`e' <= (1/2-epsilon)E`. NO se ha probado esa desigualdad sobre la orbita.
La identidad no garantiza H positivo; permite localizar y medir sus partes.

## Dos contraejemplos exactos

Primer testigo, todo en k=2, escala padre 8 y escala hija 4:

    c             0  1  2  3  4  5  6  7
    conteo padre  4  3  0  3  0  3  0  3
    hija k=2      8  0  0  0
    hija k=3      3  3  3  3

V=16; de las 32 ramas salen 12, quedan 20. E=5/8, e'=6/5,
`e'/E=48/25>1`. Q=1/4, R=-3/8, s=3/8, U=Delta=0.
El aumento es exacto, no ruido ni division por un exceso casi nulo.

Segundo testigo: solo `(2,0)` y `(2,1)`, ambos con peso 1. Paridad
exactamente equilibrada: Q=R=0. Las ramas vivas dan dos copias de
`(2,0 mod 4)` y una de `(3,2 mod 4)`. E=e'=3, Delta=0, s=1/4, U=3.
Por tanto, equilibrar la paridad tampoco implica contraccion estricta.

Ambos testigos se ejecutan por las leyes del nucleo dentro de Lean y
se verifican tambien en Python. NO se ha demostrado que estas leyes
sean alcanzables desde un arranque puntual de la excursion. Refutan
la extension a distribuciones arbitrarias, no el candidato sobre la orbita.

## Mediciones y reproducibilidad

`balance.py` compara cada identidad en Fraction, sin filtros numericos,
y reconstruye los conteos hijos contra `contraccion.py`. Reutiliza ese
DP: no es una implementacion ciega. Controles: 5.680 pasos contra pares
positivos, palabras hasta t=8, piso uniforme y grupos vacios, 20 leyes
sinteticas mas el testigo equilibrado.

- Barrido inicial: 200 celdas, c0=1,5,999983,999999937,1398101;
  t=8,12,16,20; m=1..10. Las identidades cierran y rho<1/2 en todas.
- Ventana original: 234 celdas, tres arranques grandes, t=12..24,
  m=5..10. Todas las identidades cierran y rho<1/2. H/E esta entre
  0,038917 y 0,266228 (decimales redondeados; testigos en la salida).
- En las 39 celdas a m=8 de esa segunda ventana, N0-N1 aporta entre
  aproximadamente 17,7% y 25,6% de Delta. El resto corresponde a pares
  de corrientes provenientes de alturas distintas. Esto NO es una
  fraccion de toda la contraccion: Delta es solo uno de sus terminos.

```powershell
python depuracion/frente20260910/balance.py
lean +v4.32.2 depuracion/frente20260910/balance.lean
python depuracion/frente20260910/balance.py --tiempos 12 13 14 15 16 17 18 19 20 21 22 23 24 --m-min 5 --m-max 10 --semillas 999983 999999937 1398101 --registro depuracion/frente20260910/balance_celdas.json
```

Los TXT conservan las salidas y `balance_celdas.json` los numeradores y
denominadores de cada termino en las 234 celdas. Lean 4.32.2, nucleo
sin Mathlib; `grind` para algebra y `decide` para conteos finitos,
sin `sorryAx` ni `native_decide`. Sin revision adversarial externa.

## Proximo ataque

Buscar una propiedad propagable de las leyes alcanzables que controle
H desde abajo. Ya no basta contar bits equilibrados ni eliminar un
invariante de dos operadores auxiliares. La pregunta concreta es cuanto
se separan las corrientes de distintas alturas con sus pesos reales,
y como se compensa R cuando es negativo. Cualquier propuesta debe
explicar por que no incluye los dos testigos sinteticos anteriores.

Para la revision posterior: atacar la normalizacion N frente a 2N,
la omision de grupos vacios, el factor 2V en Delta y s, el alcance de
la formalizacion general, y la distincion entre una ley arbitraria y
una ley alcanzable. No se cierra el conteo, P2 ni la densidad con este balance.
