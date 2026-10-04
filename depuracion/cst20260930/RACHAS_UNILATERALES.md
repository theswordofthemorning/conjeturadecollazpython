# Ocelotas: aproximación por arriba y criba en Lean — 03-10-2026

**Cierres posteriores:** [trece](TRECE_LEAN.md) y
[dieciocho rachas](DIECIOCHO_LEAN.md) en Lean bajo LMN. Se conservan
la preparación y los certificados de esta tanda. El posterior
[cierre condicional a 76](SETENTA_Y_SEIS_LEAN.md) ya está formalizado,
con LMN y el corolario finito de Rozier–Terracol como hipótesis explícitas.

Continuación de la [criba afinada](RACHAS_AFINADAS.md). Se formalizan sus
lemas universales y la conexión con las trayectorias, y se mejoran las
cotas de semilla mediante el signo del error logarítmico. Se mantienen
los cierres de **18 rachas bajo LMN**, o **75 bajo LMN y Rozier–Terracol**.
En esta tanda todavía faltaba el cierre Lean por encima de diez rachas.

## Mapa, índices y alcance

`T(n)=n/2` si n es par, `(3n+1)/2` si es impar; dominio `n>=2`.
`k=tau(n)` es el primer índice positivo con `3^S_k(n)<2^k`, que se supone
finito. `q=S_k(n)` cuenta los pasos impares; r cuenta sus rachas hasta k.
No hay ley probabilística. Los logaritmos son naturales y
`alpha=log(3)/log(2)` mide exponentes binarios.

Un fallo de CST satisface `Lambda*n<r` con
`Lambda=k log(2)-q log(3)>0`. Para pares n hay descenso inmediato; en el
resto, cada racha proporciona las congruencias empleadas abajo.
Nada prueba la existencia universal del primer cruce ni la llegada a 1.

## Lema unilateral

Escribamos `L(a,b)=a*x-b*y` para reales x,y. Sean U=(P,Q), V=(p,q), con

`Q,q>0`, `P*q-p*Q=1`, `L(P,Q)>0>L(p,q)`.

Entonces, para **todo** par de enteros (k,b) con
`0<b<Q+q` y `L(k,b)>0`, se cumple `L(k,b)>=L(P,Q)`.
No se exige que k y b sean coprimos ni que U,V sean convergentes.

Prueba: en la base unimodular,

`(k,b)=u(P,Q)+v(p,q)`, `u=k*q-p*b`, `v=P*b-k*Q`.

Si `u<=0`, la positividad de b obliga a `v>0`, y entonces `L(k,b)<0`:
contradicción. Por tanto `u>=1`. Si `v>=1`, entonces `b>=Q+q`, otra
contradicción. Queda `v<=0` y
`L(k,b)=u L(P,Q)+v L(p,q)>=L(P,Q)`.

El extremo derecho es **estricto**. El mediant `(P+p,Q+q)`, cuando su
error es positivo, tiene error menor que U porque `L(p,q)<0`.
Esta es precisamente la frontera que exige cambiar de cota.

En [OcelotasAfinada.lean](OcelotasAfinada.lean),
`aproximacion_superior` demuestra ese enunciado para reales x,y cualesquiera.
Aplicarlo a `x=log(2)`, `y=log(3)` aprovecha que el error en el primer
cruce siempre es positivo.

## Criba formalizada y conexión con la órbita

El mismo módulo define

`cota(alfa,beta,0)=0`,
`cota(alfa,beta,i+1)=floor(beta+alfa*cota(alfa,beta,i))`.

`paso_real` prueba que, si `n+1<=s`, `s>0`,
`2^a<=(n+1)3^p`, `log(3)<=alfa*log(2)` y
`log(s)<=beta*log(2)`, entonces `a<=beta+alfa*p`.
`criba_congruencias` itera el argumento, y `cota_monotona` permite
aumentar r a R cuando `alfa>=1`, `beta>=0`.

[OcelotasAfinadaTrayectorias.lean](OcelotasAfinadaTrayectorias.lean) enlaza:

- `criba_palabra`: usa `congruencias_acumuladas` de las rachas reales
  y concluye `S(tiempo a b r,n)<=cota(alfa,beta,R)`.
- `fallo_lambda`: demuestra `Lambda*n<r` desde `fallo_producto`, usando
  `exp(Lambda)=2^k/3^q` y `exp(Lambda)>=1+Lambda`.
- `semilla_de_cota`: si `0<c<=Lambda` y `R<=s*c`, un fallo con r<=R
  obliga a `n<s`, luego `n+1<=s`, sin perder el borde entero.
- `descenso_intervalo`: si además `qmin<=S_k(n)` y
  `cota(alfa,beta,R)<qmin`, el supuesto fallo es imposible. El teorema
  recibe el contador real `rachas n k`, no una palabra postulada.

Los **trece módulos** de la cadena compilaron en Lean 4.32.2, código 0;
77 consultas de axiomas, sólo `propext`, `Classical.choice`, `Quot.sound`,
sin `sorryAx` ([registro](lean_afinada.txt)).
**Pendientes en Lean:** las tablas numéricas completas, el cierre de la
cola para R>10 y las semillas adicionales. Estos lemas no se presentan
como CST hasta 18 rachas formalizada.

## Certificado exacto por mediantes

[rachas_unilaterales.py](rachas_unilaterales.py) parte de
`1/1<alpha<2/1`. En cada paso calcula el mediant de la pareja y decide
su signo con un encierro racional de alpha de 256 bits. Si el signo es
ambiguo, se detiene. Sumar uno de los vectores al otro conserva el
determinante 1. Los pasos que sólo cambian el extremo inferior se agrupan.

Para cada pareja, en el intervalo de denominadores correspondiente,

`Lambda >= L(P,Q) > c = (693/1000)*(P-Q*alpha_superior) > 0`.

Se toma `s=ceil(R/c)`, de modo que el fallo exige `n<s`; la criba afinada
usa `beta>log2(s)` calculada con 128 bits. La tabla contiene **158
intervalos contiguos** que cubren

`1<=q<Q0=11322003431549588082278945047`.

Para `q>=Q0` se usa la misma cota de LMN y la misma criba de la tanda
anterior. Su exclusión se comprueba también por duplicaciones en el
cotejador, con las desigualdades racionales de
[RACHAS_AFINADAS.md](RACHAS_AFINADAS.md#cálculo-exacto-y-cola-infinita).
La nueva tabla finita sólo necesita el lema unimodular ya certificado;
no toma un teorema de mejor aproximación como hipótesis externa.

| R | Todo fallo obliga a n menor que | Cierre disponible |
|---|---:|---|
| 10 | 10 699 | Semillas ya certificadas en Lean |
| 11 | 12 981 | Censo propio; la extensión Lean falta |
| 12 | 17 835 | Censo propio |
| 13 | 31 631 | Censo propio |
| 17 | 4 639 811 | Censo propio y cotejo orbital anterior |
| 18 | 4 912 741 | Censo propio hasta `2^23` |
| 19 | 294 601 937 | No cierra ese censo |
| 75 | 2 685 479 559 298 935 402 | Corolario 5.4 externo de Rozier–Terracol |
| 76 | 42 389 654 174 194 865 579 | No cierra ese corolario |

Datos: [certificado](rachas_unilaterales.json).
[Cotejador independiente](cotejar_rachas_unilaterales.py): no importa el
certificador; usa series racionales de `atanh`, comprueba signos y
determinantes de las 158 parejas, continuidad de los intervalos, 316
bordes, las 1 422 filas de la criba y la cola infinita. Todo coincide
([salida](cotejo_rachas_unilaterales.json)). No se volvió a recorrer ninguna
órbita. El cotejo orbital independiente antiguo llega a 4 674 092 y no
cubre por sí solo el nuevo límite para R=18; se conserva esa distinción.

## Próximo cierre Lean: preparación para trece rachas

Hay una [preparación exacta](preparacion_trece_lean.json) más pequeña,
reproducible mediante [preparar_trece_lean.py](preparar_trece_lean.py).
Usa las cotas de `log 2` y `log 3` ya probadas con 21 decimales en
`OcelotasLMN`, y por eso no necesita importar los 256 bits del certificado
anterior. Con `alfa=1585/1000` y `beta=B/256`:

- Bastan 40 intervalos, hasta `q=171928773`.
- Cada desigualdad `log(s)<=beta*log(2)` se sustituye por la comparación
  entera exacta `s^256<=2^B`, comprobada en las 40 filas.
- Los supervivientes exigen `n<31624`. El cambio frente a 31631 proviene
  de usar directamente los encierros de ambos logaritmos en c.
- La cola se prepara con `G_13<751` y la desigualdad base
  `1502*(19*(27+33)^2+5)<2^27`; falta su inducción y ensamblaje en Lean.

**Esto aún no es CST hasta trece rachas en Lean.** El siguiente bloque
debe certificar esas 40 filas, ampliar la prueba de cola a R=13 y
certificar el descenso hasta n=31623 en el núcleo. Ese rango ya está
dentro del censo empírico conservado; no requiere ampliar dicho censo.

## Reproducir

```text
python -B -X utf8 depuracion/cst20260930/rachas_unilaterales.py --salida depuracion/cst20260930/rachas_unilaterales.json
python -B -X utf8 depuracion/cst20260930/cotejar_rachas_unilaterales.py --certificado depuracion/cst20260930/rachas_unilaterales.json --salida depuracion/cst20260930/cotejo_rachas_unilaterales.json
python -B -X utf8 depuracion/cst20260930/preparar_trece_lean.py --salida depuracion/cst20260930/preparacion_trece_lean.json
python -B -X utf8 depuracion/cst20260930/comprobar_rachas_lean.py --salida depuracion/cst20260930/lean_afinada.txt
```

Los resultados conservan el nombre Ocelotas. No se formula una atribución
de novedad; la revisión humana continúa pendiente. El
[registro versionado](../coherencia20260913/registro.json) y su generador
quedaron sincronizados en 255 afirmaciones, con controles de referencias
e integridad correctos ([salida](registro_unilateral.txt)).
