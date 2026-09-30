# Ocelotas: cierre aritmético de las diez rachas — 30-09-2026

**Resultado:** `OcelotasCertificado.ocelotas_diez` ya prueba el descenso
para las palabras reales de una a diez rachas, bajo `RhinEntera`.
La criba finita está demostrada en Lean y aplicada al ensamblaje:
**desaparece el argumento pendiente `hcriba`**. No se añade ningún axioma.

El enunciado usa la representación explícita `Palabra`, que exige las
paridades reales de cada paso. El caso par también está formalizado.
La [tanda siguiente](CONTADOR_LEAN.md) construye esa representación desde
un contador canónico de rachas y prueba la igualdad de los primeros tiempos.
Este documento conserva la evidencia del cierre aritmético anterior.

## Enunciado y alcance

```lean
theorem ocelotas_diez (hR : RhinEntera) {n r : ℕ} {a b : ℕ → ℕ}
    (hn : 2 ≤ n) (hw : Palabra n a b r) (hr : 0 < r) (hr10 : r ≤ 10)
    (hk : PrimerCruce n (tiempo a b r)) : T^[tiempo a b r] n < n
```

Mapa: `T(n)=n/2` para n par, `(3n+1)/2` para n impar. Dominio n>=2.
Los índices cuentan pasos de este atajo; `S k n` cuenta los impares
anteriores a k. `PrimerCruce` exige `3^(S k n)<2^k` y coeficiente al
menos uno en los prefijos anteriores. `Palabra n a b r` describe r bloques
consecutivos `1^(a_i) 0^(b_i)`, con ambas longitudes positivas; su tiempo
total es k. No se omiten pasos ni se imponen cotas a esas longitudes.
No hay condicionamiento probabilístico ni ley de distribución.

`RhinEntera` sigue siendo una **hipótesis externa explícita**. No queda
demostrada por este cierre ni desaparece por no figurar en `#print axioms`.
Tampoco se demuestra la existencia universal del primer cruce, CST para
cualquier número de rachas, ni Collatz.

[OcelotasCierre.lean](OcelotasCierre.lean) añade:

- `descenso_par`: el caso n par, sin Rhin; unicidad del primer cruce lo
  identifica con k=1.
- `fallo_exige_once`: bajo Rhin, cualquier fallo representado por una
  `Palabra` de r>0 exige r>=11.
- `descenso_hasta_diez`: reúne el caso par y la existencia de una palabra
  real de una a diez rachas cuyo tiempo total sea k.

## Criba exacta mediante intervalos

La [tanda anterior](FINITO_LEAN.md) redujo el trabajo a demostrar, para
1<=q<=82696, `CertificadoAritmetico q`. Con

```text
P = 3^q, k = Nat.log2(P)+1, Delta = 2^k-P, m = (q-1)/182,
```

esa condición es `10P<=11215 Delta` o `11P<=2^m Delta`.

[OcelotasCriba.lean](OcelotasCriba.lean) evita recalcular una potencia
enorme en cada paso del núcleo. Usa H=2^48 y un marco `(l,u,k)` con el
invariante **l*2^k <= H*3^q <= u*2^k**. No es aritmética flotante.

Al incrementar q se multiplica por 3 y se normaliza con d=2 o d=4:
si `3u<2H`, se elige d=2 e incrementa k en uno; en otro caso, d=4 y k
en dos. Los extremos nuevos son `floor(3l/d)` y `ceil(3u/d)`.
`paso_encierra` demuestra que estos redondeos conservan el invariante.
No presupone que la decisión de normalización haya acertado la ventana:
la aceptación exige además **H<2l y u<H**. Estas desigualdades implican
`3^q<2^k<2*3^q` y fijan el k que usa el certificado.

La aceptación comprueba una de las condiciones enteras:

```text
11225u <= 11215H,
(2^m+11)u <= 2^m H.
```

`acepta_correcto` demuestra que cada una implica la rama correspondiente
de `CertificadoAritmetico q`. `recorrer_correcto` prueba por inducción
que la aceptación de un bloque de c pasos cubre **todos** los exponentes
q+1,...,q+c.

## Cobertura y base de confianza

[OcelotasCertificado.lean](OcelotasCertificado.lean) contiene **81 bloques**:
80 de 1024 exponentes y el último de 776, hasta q=82696. Cada bloque
comprueba con `decide +kernel`:

1. Su marco inicial, comparándolo con las potencias exactas.
2. Todas sus transiciones y decisiones de aceptación.

Una división por casos en Lean une los intervalos y prueba
`criba_certificada`. Aplicarla a `diez_de_certificado` da `ocelotas_diez`.
La tabla no se acepta como un axioma ni como una salida externa fiable.
El [generador](generar_criba_lean.py) puede proponer los extremos, pero
cualquier extremo o recorrido incorrecto debe superar las comprobaciones
del núcleo para producir el teorema.

La cadena queda cerrada para el enunciado indicado: palabra real →
congruencias y control aditivo → Rhin → k<131072 → q<=82696 → criba
certificada → n<=11214 ante un fallo → descenso finito → contradicción.

## Cotejo y validación

El generador coteja **cada uno de los 82696 marcos** con `3^q` y `2^k`
exactos, y contrasta k mediante `bit_length`. Obtiene 82593 aceptaciones
por cota de semilla y 103 por criba lineal, coincidiendo con el
[cotejo independiente anterior](cotejo_finito_lean.json), que calcula
directamente las desigualdades sin estos intervalos. La anchura máxima
observada es 1010 unidades de la escala H; no se usa esa medición como
hipótesis de la prueba. El último k es 131071.
[Resultados y huellas](cotejo_criba_lean.json).
El campo `certificada_en_lean: false` del cotejo anterior se conserva
como evidencia histórica de aquella tanda; el estado actual lo acredita
la nueva compilación completa.

Los ejemplos de Lean comprueban el rechazo de la ventana de q=0,
el rechazo de un extremo falso y la aceptación exacta de q=1.
Los bordes de la cobertura, incluido el bloque final incompleto, forman
parte del teorema. Se conserva la certificación y el cotejo independiente
de las 11213 semillas de la [tanda finita](FINITO_LEAN.md); no se amplía
ni se vuelve a ejecutar su barrido Python.

Lean 4.32.2. Reconstrucción limpia de **siete módulos**, código 0;
todos los resultados auditados dependen únicamente de subconjuntos de
`propext`, `Classical.choice` y `Quot.sound`. Sin `sorryAx`, declaraciones
de axiomas propias ni evaluación nativa que sustituya al núcleo.
[Compilación completa y huellas](lean_cierre.txt).

Desde la raíz del repositorio:

```text
python -B -X utf8 depuracion/cst20260930/generar_criba_lean.py --hasta 82696 --bloque 1024 --lean depuracion/cst20260930/OcelotasCertificado.lean --salida depuracion/cst20260930/cotejo_criba_lean.json
python -B -X utf8 depuracion/cst20260930/comprobar_rachas_lean.py --salida depuracion/cst20260930/lean_cierre.txt
```

La primera orden reproduce la fuente generada y su cotejo; la segunda
recompila la cadena completa y audita los axiomas. Se actualizan la
entrada existente del registro y el estado breve: 246 afirmaciones,
sin alterar la captura literal de conversaciones ni los registros
anteriores ([controles del generador del registro](registro_cierre.txt)).
La interfaz del contador quedó cerrada en [CONTADOR_LEAN.md](CONTADOR_LEAN.md).
Siguen la auditoría de la hipótesis externa y la revisión humana.
No se certifica novedad.
