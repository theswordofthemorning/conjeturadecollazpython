# Ocelotas: región finita para cualquier cantidad fija de rachas

03-10-2026. **Prueba escrita y formalización terminadas**, bajo LMN.
Este argumento es una continuación de las cotas del laboratorio; no se
ha establecido prioridad histórica. Revisión humana pendiente.

## Resultado y alcance

Se usa el atajo `T(n)=n/2` para n par y `(3n+1)/2` para n impar, con
`n>=2`. `S_j(n)` cuenta las entradas impares en los primeros j pasos.
El primer cruce finito k cumple `3^S_j>=2^j` para `1<=j<k` y
`3^S_k<2^k`. Una racha es un bloque maximal de entradas impares hasta k;
escribimos `r=rachas(n,k)`. No hay ley probabilística ni muestreo.

Bajo `LMNDebil`, si el primer cruce **no** produce descenso (`n<=T^k(n)`),
entonces:

```text
k < 2^(2r+32),
n < 2^(19(2r+65)^2+r).
```

[OcelotasCotaGeneral.lean](OcelotasCotaGeneral.lean),
`region_del_fallo`, lo prueba desde el contador real de la órbita.
`region_del_fallo_corolario` parte de `LMN23`, la especialización externa
del corolario publicado de Laurent–Mignotte–Nesterenko. La traducción
`LMN23 -> LMNDebil` está formalizada; el teorema trascendente sigue externo.

El argumento vale para **cualquier r**, sin elegir antes 21 o 22.
Como ambas cotas crecen con r, para cualquier R fijo todos los posibles
fallos con `r<=R` están en una región finita explícita. También se prueba
`descenso_de_tiempo_grande`: si `2^(2r+32)<=k`, ese primer cruce desciende.

En palabras: una trayectoria con pocas rachas no puede posponer
indefinidamente el primer cruce y luego fallar en descender allí.
Las cotas son muy holgadas. **No se demuestra que la región finita esté
vacía**, ni que todo n tenga primer cruce, ni Collatz.
El cierre hasta [21 rachas](VEINTIUNA_LEAN.md) usa cotas mucho mejores;
esta fórmula general no lo sustituye.

## Derivación independiente

Un fallo con n par es imposible por el descenso inmediato. Para n impar,
la palabra extraída tiene r>0 y k>=2. Pongamos
`q=S_k(n)`, `P=3^q`, `D=2^k-P>0`, `t=floor(log2 k)` y
`E=19(t+33)^2`.

Las identidades afines anteriores del laboratorio dan `Dn<rP`.
La forma entera de LMN da `P<=D*2^E`. Al cancelar D,

```text
n < r*2^E <= 2^(E+r).
```

Por integridad, `n+1<2^(E+r+1)`. Las congruencias de las rachas implican
`q<=cota(r,E+r+1)`, donde

```text
cota(0,m)=0,
cota(r+1,m)=floor((5m+8*cota(r,m)-1)/5).
```

La resta se interpreta como resta natural truncada. Se demuestra por
inducción `cota(r,m)+m<=2^r*m`; incluye m=0. Por otra vía, la suma
geométrica `m*sum((8/5)^i, i=0..r-1)` también domina la recurrencia.
La cota temporal elemental `5k<=8q+5` implica `k<=2q+1`.

Supongamos `t>=2r+32`. Entonces r<=t y
`E+r+1<=20(t+33)^2`, de modo que

```text
2^t <= k <= 40*2^r*(t+33)^2+1.
```

Esto contradice la siguiente desigualdad, probada por dos inducciones:

```text
40*2^r*(t+33)^2+1 < 2^t       para t>=2r+32.
```

En la base t=2r+32, el caso r=0 tiene margen entero 4294798295.
Al pasar de r a r+1, la derecha se multiplica por cuatro; basta
`(2r+67)^2<=2(2r+65)^2`. Su diferencia es
`4r^2+252r+3961>=0`.
Para aumentar t se usa `(t+34)^2<=2(t+33)^2`, cuya diferencia es
`t^2+64t+1022>=0`. Así queda `t<2r+32`, y por tanto la cota de k.
Sustituyéndola en la cota de n se obtiene la región anunciada.

La existencia de una cola finita para R fijo ya era parte del método
escrito en [REVISION_RACHAS.md](REVISION_RACHAS.md). Esta continuación
ofrece una fórmula uniforme y su formalización bajo LMN; no presenta
la idea de finitud como un descubrimiento sin antecedentes.

## Evidencia y reproducción

- [Auditoría](evidencia_cota_general.json) y [salida](evidencia_cota_general.txt):
  Lean 4.32.2, un módulo compilado, nueve consultas, sólo `propext`,
  `Classical.choice`, `Quot.sound`, sin `sorryAx`. Reutiliza un prefijo de
  38 módulos con fuentes, objetos y entorno comprobados por SHA256.
- [Contraste independiente](cotejo_cota_general.json): identidades
  polinómicas enteras y 606 casos de borde de la recurrencia, con otra
  cota en `Fraction`. La malla no prueba universalidad; no es un censo
  de órbitas ni verifica la hipótesis externa LMN.

```text
python -B -X utf8 depuracion/cst20260930/comprobar_extension_lean.py --modulo OcelotasCotaGeneral --compilados C:/Users/Home/AppData/Local/Temp/ocelotas_auditado_20261003 --salida depuracion/cst20260930/evidencia_cota_general.json
python -B -X utf8 depuracion/cst20260930/cotejar_cota_general.py --salida depuracion/cst20260930/cotejo_cota_general.json
```

El primer comando necesita el prefijo producido por
`comprobar_rachas_lean.py --compilados ...`; no modifica su manifiesto.
La [continuación geométrica](COLA_PARAMETRICA.md) ya afina estas cotas
mediante un certificado uniforme de tres desigualdades enteras.
Queda excluir la región restante mediante una reducción que no dependa
de aumentar R caso por caso. El cierre específico de
[22 rachas](VEINTIDOS_LEAN.md) quedó comprobado posteriormente.
