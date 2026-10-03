# Ocelotas: CST hasta trece rachas en Lean, bajo LMN — 03-10-2026

**Extensión posterior:** [dieciocho rachas](DIECIOCHO_LEAN.md), también en
Lean bajo LMN. Se conserva aquí el cierre de trece y su evidencia original.

Se cierra la [preparación de trece rachas](RACHAS_UNILATERALES.md#próximo-cierre-lean-preparación-para-trece-rachas).
La tabla numérica, la cola infinita y el descenso de las semillas están
formalizados. La cota trascendente de Laurent–Mignotte–Nesterenko sigue
siendo una hipótesis externa explícita; su original fue cotejado en las
[lecturas aportadas](LECTURAS_20261003.md).

## Enunciado

Para enteros `n>=2`, se usa el atajo `T(n)=n/2` si n es par y
`(3n+1)/2` si es impar. `S_j(n)` cuenta las entradas impares entre los j
primeros pasos. `PrimerCruce n k` expresa que `3^S_j(n)>=2^j` para
`1<=j<k`, y `3^S_k(n)<2^k`. El contador `rachas n k` cuenta los bloques
maximales de unos de esa palabra de paridad. No hay ley probabilística.

[OcelotasTrece.lean](OcelotasTrece.lean) prueba:

```lean
theorem cst_trece_corolario (hL : LMN23) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 13) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n
```

`cst_trece_lmn` recibe directamente `LMNDebil` y
`fallo_exige_catorce` prueba el contrarrecíproco: un fallo necesita al
menos catorce rachas. El caso par está incluido.
La existencia del primer cruce es una hipótesis; no se afirma que todos
los n lo tengan ni que lleguen a 1.

`LMN23` conserva las constantes y el máximo del corolario 2 de LMN,
especializado en 2 y 3. El paso a `LMNDebil` ya estaba formalizado. Sólo
se usa LMN en la cola; la tabla y las semillas son incondicionales.

## Prueba y módulos nuevos

Sea un fallo impar con r<=13, `k=tau(n)`, `q=S_k(n)` y
`Lambda=k log(2)-q log(3)>0`. Los lemas anteriores dan
`Lambda*n<r` y las congruencias de rachas reales.

**1. Interfaces numéricas.**
[OcelotasTreceBase.lean](OcelotasTreceBase.lean) demuestra que
`alfa=1585/1000` satisface `log 3<=alfa*log 2` y que una comparación
entera `s^256<=2^B` implica `log s<=(B/256)log 2`.
Transporta la cota unilateral de una pareja de determinante 1 a la forma
logarítmica de la órbita y reúne las dos salidas: semilla pequeña o
contradicción por la criba.

**2. Tabla completa.**
[OcelotasTreceTabla.lean](OcelotasTreceTabla.lean) certifica los 40
intervalos que cubren `1<=q<171928773`. Para cada pareja U=(P,Q), V=(p,v),
comprueba el determinante y los signos con los encierros de `log 2` y
`log 3` ya demostrados en Lean. La aproximación unilateral da una cota
racional `c<=Lambda`; `13<=s*c` obliga a `n<s`.

En 25 filas se tiene `s<=31624`. En las otras 15, el núcleo comprueba
`s^256<=2^B`, y `norm_num` certifica los trece pisos de
`C_0=0`, `C_(i+1)=floor(B/256+(1585/1000)C_i)`: resulta `C_13<q_inicio`.
`pequeno_de_tabla` verifica la cobertura de todos los intervalos, incluidos
sus bordes, y concluye `n<31624`.

El [generador](generar_trece_lean.py) usa el
[JSON preparado](preparacion_trece_lean.json) para proponer constantes.
Lean vuelve a comprobar cada obligación; ni el JSON ni Python se aceptan
como una premisa. Ese JSON conserva su etiqueta histórica de preparación.

**3. Descenso de semillas.**
[OcelotasTreceFinito.lean](OcelotasTreceFinito.lean) reutiliza la prueba
para `2<=n<=11214` y certifica las **20 409 semillas adicionales**
`11215<=n<=31623` mediante `decide +kernel`.
El verificador mantiene el valor de la órbita y las potencias del
coeficiente; agotar sus 225 unidades de combustible es un rechazo.
Su corrección produce un primer cruce y descenso en un índice <=224.
La unicidad del primer cruce permite aplicarlo al k original, sin imponerle
un límite en el enunciado final.

**4. Cola universal.**
[OcelotasTreceCola.lean](OcelotasTreceCola.lean) prueba
`cota(13,m)<=751*m`, donde `cota` es la criba entera anterior.
Con `t=floor(log2(k))`, LMN y el fallo dan

`n<16*2^(19(t+33)^2)` y `k<=1502*(19(t+33)^2+5)`.

Para todo entero `t>=27`, la última expresión es menor que `2^t`,
por una inducción certificada; contradice `2^t<=k`.
Si `q>=171928773`, entonces `k>q>2^27`, de modo que este caso queda
cubierto sin una enumeración adicional.

**5. Ensamblaje.** `descenso_palabra` une tabla, semillas y cola.
`descenso_contador` extrae las rachas desde la órbita real y trata los n
pares. `no_desciende_antes`, ya certificado, completa la igualdad entre
primer descenso y primer cruce.

## Validación y límites

La reconstrucción limpia de los **18 módulos** terminó con código 0 en
Lean 4.32.2. Las **94 consultas de axiomas** sólo contienen
`propext`, `Classical.choice`, `Quot.sound`; ninguna depende de `sorryAx`
([registro y hashes de fuentes](lean_trece.txt)). La tabla se regeneró
en un directorio temporal y coincidió byte por byte.

El [cotejo independiente](cotejar_trece_lean.py), sin importar generadores
ni verificadores anteriores, usa series racionales de `atanh` para los
logaritmos y la recurrencia entera equivalente
`C_(i+1)=(25*B+10144*C_i)//6400`.
Confirma las 40 filas, los 15 descartes, la cota 31624 y la base de la
cola. También itera directamente las **31 622 semillas** del rango
completo: no hay fallos ni descensos anteriores al cruce. El mayor cruce
observado es 105; hay 17 semillas con exactamente trece rachas.
Se cotejaron explícitamente n=2, 11214, 11215 y 31623
([salida](cotejo_trece_lean.json)). Es un contraste de la interpretación,
separado de la certificación universal de Lean.

El rango empírico anterior, hasta `2^23`, no se amplía. Los resultados de
18 rachas, o 75 con Rozier–Terracol, estaban en esta tanda con prueba escrita
y cálculo exacto. La frontera formal de esta tanda fue trece; la extensión
posterior a 18 está enlazada arriba. El cierre de 75 sigue pendiente en Lean.
Revisión humana y novedad pendientes.

El [registro versionado](../coherencia20260913/registro.json) incorpora
`ocelotas_cst_trece_rachas_lmn_lean`, con la hipótesis LMN explícita.
`guardarafirmaciones.py` regeneró la base con **256 afirmaciones** y
comprobó vocabulario, referencias e integridad, sin fallos
([salida](registro_trece.txt)).

## Reproducir

Desde la raíz del repositorio:

```text
python -B -X utf8 depuracion/cst20260930/generar_trece_lean.py --certificado depuracion/cst20260930/preparacion_trece_lean.json --salida depuracion/cst20260930/OcelotasTreceTabla.lean
python -B -X utf8 depuracion/cst20260930/comprobar_rachas_lean.py --salida depuracion/cst20260930/lean_trece.txt
python -B -X utf8 depuracion/cst20260930/cotejar_trece_lean.py --certificado depuracion/cst20260930/preparacion_trece_lean.json --salida depuracion/cst20260930/cotejo_trece_lean.json
```

Se necesita también `Mathlib.Algebra.Order.Floor.Semifield`, descargado el
03-10 desde la caché del mismo Mathlib fijado. El comprobador recompila
toda la cadena; `--compilados RUTA` conserva los `.olean` y no omite
compilaciones por sí solo. Por defecto usa un directorio temporal limpio.
La tanda de [veinte rachas](VEINTE_LEAN.md#compilación-conservada) añade
la opción explícita `--reutilizar`, con manifiesto y cotejo de huellas.
