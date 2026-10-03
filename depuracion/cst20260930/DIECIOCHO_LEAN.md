# Ocelotas: cierre de dieciocho rachas — 03-10-2026

**Extensión posterior:** [diecinueve rachas](DIECINUEVE_LEAN.md), mediante
criba reiniciada en prefijos reales. Se conserva la evidencia de esta tanda.

**Cierre verificado:** reconstrucción limpia de los 25 módulos con
Lean 4.32.2, código 0. Las 117 consultas de axiomas contienen 113 listas
con sólo `propext`, `Classical.choice`, `Quot.sound`, y cuatro declaraciones
libres de axiomas; ninguna depende de `sorryAx`.
Al cerrar esta tanda se cotejaron los hashes de las fuentes y del
comprobador con el [registro completo](lean_dieciocho.txt).

## Enunciado y alcance

Mapa atajo `T(n)=n/2` si n es par y `(3n+1)/2` si es impar, sobre enteros
`n>=2`. `S_j(n)` cuenta entradas impares en los primeros j pasos.
`PrimerCruce n k` exige `3^S_j(n)>=2^j` para `1<=j<k` y
`3^S_k(n)<2^k`. `rachas n k` cuenta bloques maximales de unos en esa
palabra de paridad. No hay ley probabilística ni condicionamiento aleatorio.

El enunciado de [OcelotasDieciocho.lean](OcelotasDieciocho.lean) es:

```lean
theorem cst_dieciocho_corolario (hL : LMN23) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 18) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n
```

La existencia del primer cruce sigue siendo una hipótesis. No se demuestra
que todos los n lo tengan ni que lleguen a 1. `LMN23`, el corolario 2 de
Laurent–Mignotte–Nesterenko especializado en 2 y 3, permanece como hipótesis
externa explícita; su paso a `LMNDebil` está formalizado y la fórmula
publicada fue [cotejada con el original](LECTURAS_20261003.md).
`fallo_exige_diecinueve` expresa el contrarrecíproco.

## 1. Tabla y cola

[OcelotasNumerica.lean](OcelotasNumerica.lean) parametriza las interfaces
de semilla pequeña y exclusión por criba. Reutiliza los lemas de logaritmos
y parejas unilaterales del cierre de [trece rachas](TRECE_LEAN.md).

La [tabla nueva](OcelotasDieciochoTabla.lean) cubre
`1<=q=S_k(n)<2213511501` con 42 parejas de determinante 1. Para un fallo
con r<=18 y `Lambda=k log 2-q log 3`, la cota racional `c<=Lambda`
y `18<=s*c` dan `n<s`. En 36 filas, `s<=4911698`; en las otras seis,
la criba certifica una contradicción. Se usan `alfa=1585/1000`,
`beta=B/256` y comparaciones enteras `s^256<=2^B`.

La [cola](OcelotasDieciochoCola.lean) prueba `cota(18,m)<=7869*m`.
Si `t=floor(log2 k)>=31`, LMN y un supuesto fallo implican

`n<32*2^(19(t+33)^2)` y `k<=15738*(19(t+33)^2+6)<2^t<=k`.

La desigualdad central se prueba por inducción para todo t>=31.
Para `q>=2213511501>2^31`, se tiene k>q; queda cubierta toda la cola.

## 2. Certificado finito por residuos

[OcelotasResiduos.lean](OcelotasResiduos.lean) prueba la corrección de un
verificador que comparte los prefijos de paridad. En el índice i, el
estado `(r,m,a,c)` representa

`n=r+m*u`, `T^[i](n)=a*u+c`, `m=2^i`, `a=3^S_i(n)`.

El estado inicial es `(2,1,1,2)`, con `u=n-2>=0`. La rama b separa
`u=2*v+b`, b en {0,1}, y pasa a residuo `r+m*b`, módulo `2*m` y valor
afín obtenido de `T(a*b+c)`. El prefijo certificado impide aceptar un
cruce posterior al primero.

- Si `a<m` y `c<r`, toda la clase desciende en ese primer cruce:
  `a*u+c<r+m*u` para u>=0.
- Si `r>limite`, la clase no contiene semillas del intervalo.
- Si `r+m>limite`, sólo queda n=r y se continúa con el verificador
  individual ya demostrado en `OcelotasFinito`.
- Agotar el combustible siempre rechaza.

La evaluación monolítica se detuvo tras observar unos 10,9 GB de memoria
de trabajo del proceso Lean. El certificado se dividió a profundidad diez:
64 bloques no resueltos y 27 hojas ya aceptadas; 181 nodos de ensamblaje
en [OcelotasResiduosBloques.lean](OcelotasResiduosBloques.lean).
Cada bloque se evalúa con `decide +kernel`; `acepta_rama` combina sus
resultados sin volver a evaluar los subárboles. Python sólo propone los
estados; Lean comprueba tanto los bloques como su unión.

[OcelotasResiduosFinito.lean](OcelotasResiduosFinito.lean) expresa el cierre
para **2<=n<=4912740**, con primer cruce k<=224. La unicidad lo aplica a
cualquier k que satisfaga `PrimerCruce`, sin límite adicional en el
teorema final. El rango contiene todas las semillas de la tabla y está
dentro del censo conservado hasta `2^23`.

## 3. Cotejos independientes

El [cotejo de la tabla](cotejar_dieciocho_lean.py), sin imports de los
generadores, encierra log 2 y log 3 mediante series racionales de `atanh`
y evalúa `C_(i+1)=(25*B+10144*C_i)//6400`. Confirma las 42 filas,
los seis descartes y la cota de semilla
([salida](cotejo_dieciocho_lean.json)). La nueva cota `4911698` es algo
menor que `4912741` del cálculo anterior porque utiliza directamente los
encierros más precisos de log 2 y log 3.

El [cotejo de residuos](cotejar_residuos.py) produce 121.613 clases.
Comprueba su disjunción mediante intervalos diádicos de bits invertidos y
que las cantidades suman **4.912.739 semillas**. Itera directamente dos
representantes de cada clase, incluidos representantes fuera del rango
cuando la clase sólo contiene una semilla. Confirma el primer cruce, las
potencias y el valor afín; también coteja los bordes 2, 31623, 31624,
4912739 y 4912740. El máximo cruce observado es 224
([salida](cotejo_residuos.json)).

El árbol emplea 243.225 nodos, 15.466 hojas compartidas y 106.147 hojas
individuales, con 1.549.108 pasos individuales adicionales. Es un cálculo
exacto finito independiente; la justificación de la inferencia universal
para cada clase está en el teorema de corrección de Lean.

El [registro versionado](../coherencia20260913/registro.json) incorpora
`ocelotas_cst_dieciocho_rachas_lmn_lean`. El generador de la base verificó
257 afirmaciones, vocabulario, referencias e integridad sin fallos
([salida](registro_dieciocho.txt)).

## 4. Preparación de las siguientes colas

Como lema auxiliar, [OcelotasGeometrica.lean](OcelotasGeometrica.lean)
certifica para todo r,m naturales

`3*5^r*cota(r,m) + 5^(r+1)*m <= 5*8^r*m`.

La derivación independiente usa `5*C_(r+1)<=5*m+8*C_r`: multiplicar por
`3*5^r` y sumar `5^(r+2)*m` deja ocho veces el miembro izquierdo del
paso anterior. La base r=0 es igualdad, también para m=0.
Así, una única comparación `5*8^r<=(3*A+5)*5^r` da `cota(r,m)<=A*m`.
Lean certifica como ejemplo `cota(75,m)<=3395059960557476*m`, sin desplegar
75 pisos. Este lema no cierra CST de 75 rachas; su
[compilación separada](lean_geometrica.txt) tiene tres consultas de axiomas
estándar y queda fuera de los 25 módulos del cierre principal.

## Reproducir

Desde la raíz, con Lean 4.32.2 y el Mathlib fijado:

```text
python -B -X utf8 depuracion/cst20260930/preparar_cierre_lean.py --rachas 18 --bits-cola 31 --salida depuracion/cst20260930/preparacion_dieciocho_lean.json
python -B -X utf8 depuracion/cst20260930/generar_dieciocho_lean.py --certificado depuracion/cst20260930/preparacion_dieciocho_lean.json --salida depuracion/cst20260930/OcelotasDieciochoTabla.lean
python -B -X utf8 depuracion/cst20260930/generar_residuos_lean.py --limite 4912740 --combustible 225 --profundidad 10 --salida depuracion/cst20260930/OcelotasResiduosBloques.lean
python -B -X utf8 depuracion/cst20260930/comprobar_rachas_lean.py --salida depuracion/cst20260930/lean_dieciocho.txt
python -B -X utf8 depuracion/cst20260930/cotejar_dieciocho_lean.py --certificado depuracion/cst20260930/preparacion_dieciocho_lean.json --salida depuracion/cst20260930/cotejo_dieciocho_lean.json
python -B -X utf8 depuracion/cst20260930/cotejar_residuos.py --limite 4912740 --combustible 225 --salida depuracion/cst20260930/cotejo_residuos.json
```

Revisión humana y novedad pendientes. El resultado de 75 rachas bajo
Rozier–Terracol conserva su prueba escrita y cálculo exacto; su cierre
Lean completo sigue pendiente.
