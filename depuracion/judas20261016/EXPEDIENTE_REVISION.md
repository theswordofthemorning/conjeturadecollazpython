# Expediente para la revisión humana: Gao, Garner, Wu y Ocelotas

16-10-2026. Paso J3b de la [Ruta de Judas](../../RutaDeJudasIscariote.md#4-la-ruta-de-esta-rama),
tras la salida (b) de [J2](J2_MECANISMOS.md). Reúne en una página, al día,
cinco cosas de cada resultado:
- qué afirma;
- qué certifica Lean y con qué premisas;
- qué no dice;
- qué tiene que mirar quien lo revise;
- qué falta.

No sustituye a las notas enlazadas ni a la revisión humana, que sigue
pendiente en los cuatro. **No se envía nada ni se contacta a nadie** sin
autorización del usuario.

**Orden de lectura:** I → II → III → IV. II y III usan el teorema de I.

**Vigencia de la evidencia hoy.** [verificar_expediente.py](verificar_expediente.py)
recalcula, sin compilar, las huellas de los fuentes registrados y revisa las
auditorías guardadas ([vigencia_expediente.json](vigencia_expediente.json)):
- Gao, Garner y Wu: 10 módulos y 3 archivos del proyecto, iguales, y
  `leanchecker` en 0 en las 30 entradas;
- Ocelotas 83: 55 fuentes iguales y 146 consultas, todas con
  `propext`, `Classical.choice` y `Quot.sound`;
- récord de Roosendaal: 25 fuentes iguales y 9 consultas, una sin ningún
  axioma. 24 de esos fuentes son de la cadena de 83; el nuevo es
  `OcelotasRecordRoosendaal`.

En total son 69 archivos distintos. Ninguna diferencia. Una huella igual dice que el fuente no cambió desde su
auditoría; no repite la auditoría.

**Lemas de lectura.** [LecturaRevision.lean](LecturaRevision.lean) no añade
resultados. Reescribe en Lean, sin convenciones propias del sistema, las
piezas de I a III que más fácilmente se leen mal. Tiene 7 teoremas: cinco
usan sólo `propext`, `Classical.choice` y `Quot.sound`, y dos no usan ningún
axioma ([evidencia](evidencia_lectura.txt)). Se citan en las preguntas de
abajo.

## I. Gao (1993): consecutivos que coalescen, en densidad 1

**Afirma.** Para el mapa clásico `f(n)=n/2` o `3n+1`, el conjunto de los m
con `f^k(m)=f^k(m+1)` para algún `k<=floor(log2 m)` tiene densidad natural 1.
Es la forma de Lagarias, entrada 68. También vale la forma literal de Gao:
`d̄_k -> 1` y `d(x) -> 1`.

**Lean.**
- `GaoEnunciado.conjetura_gao` ([GaoEnunciado.lean](../gao20260920/formal/GaoEnunciado.lean),
  líneas 11–22).
- `GaoLiteral.conjetura_gao_literal`, con las definiciones de
  [Hienas.lean](../gao20260920/formal/Hienas.lean), líneas 34–76.
- `GaoLiteral.lagarias` reescribe aparte la forma de Lagarias.
- Premisas: ninguna. Axiomas estándar; `leanchecker`, también `--fresh`, en 0
  ([evidencia](../gao20260920/evidencia_gao_lean.json)).

**No dice** nada de llegar a 1.

**Ya comprobado.**
- Tablas 2 y 3 del original con código independiente.
- Cotejo con Lagarias y con el PDF de Gao, págs. 261–267.
- zbMATH: no hay citas indexadas a Gao (1993).
- Detalle en [revisión del 27-09](../../papers/revision20260927/REVISION.md) y
  [gaopendientes](../../gaopendientes.md).

**Para quien revise.**
1. ¿`encuentro` (línea 15) es exactamente la condición de Lagarias, con
   `Nat.log 2 m = floor(log2 m)` para m>=1? Ayuda Lean: según
   `LecturaRevision.gao_encuentro_iff`, para m>=1 equivale a
   `∃ k, 2^k <= m ∧ f^k(m) = f^k(m+1)`. Según `gao_cero`, m=0 no cuenta.
2. ¿`coalescen` y `dbarra` de Hienas son la coalescencia de Gao (pág. 264) y
   su `d̄_k` (pág. 265)? Tres condiciones: misma imagen, mismas mitades y
   ningún 1 antes.
3. ¿El cociente por N con `x/0=0` deja intacto el límite?

**Falta.**
- La lectura humana.
- MathSciNet y Google Scholar.
- Leer enteras las cuatro citas vistas sólo por título o resumen.
- El artículo I está en JAR desde el 01-10; el estado en SNAPP lo ve el
  usuario.
- Antes de cualquier edición OEIS, las dos frases de
  [gaopendientes §5](../../gaopendientes.md#lo-que-falta-en-orden).

## II. Garner (1985), conjetura (2): rachas con la misma altura

**Afirma.** Para cada L y N hay `n>=N` tal que `n, ..., n+L` tienen la misma
altura h y el mismo `σ∞`.

**Lean.** `GarnerEnunciado.conjetura_garner`
([GarnerEnunciado.lean](../gao20260920/formal/GarnerEnunciado.lean), líneas
11–29). Premisas: ninguna, aparte del teorema de I.

**No dice** la conjetura (1) de Garner, que la mayoría tenga la altura de un
vecino. Con alturas finitas necesita que esos n lleguen a 1, y eso está
abierto.

**Ya comprobado.**
- Rachas por otra ruta, para L=1..16, y la tabla 1 de Gao.
- Elia–Tucker (2015) refutan la caracterización de Garner, no la conjetura (2).
- La reseña de zbMATH mide la altura con T; el teorema cubre las dos alturas.
- Detalle en [Alpacas](../garner20260926/Alpacas.md).

**Para quien revise.** ¿`altura` y `mitades` (líneas 15 y 22) son la
altura y el `σ∞` de Gao, pág. 262? ¿`FormaGarner` cuantifica como Garner,
con n tan grande como se quiera? Ayuda Lean: `garner_altura_unica` prueba
que la altura, si existe, es única, así que «la misma altura h» no es ambigua.

**Falta.**
- El texto original de Garner (1985); sólo se leyó la reseña.
- MathSciNet.
- La lectura humana.
- El II está libre desde el rechazo de AFM del 28-09.

## III. Wu (1992): dos conjeturas

**Afirma.**
- **Conjetura 2:** `lim L(M)=∞`, con L la racha más larga de consecutivos de
  igual altura en `[1,M)`. Está demostrada.
- **Conjetura 1:** `lim d(M)=1` equivale a que los enteros que llegan a 1
  tengan densidad 1. Es una reducción, **no una prueba**: ese último
  enunciado está abierto.

**Lean.** `WuEnunciado.conjetura_wu_dos` y `conjetura_wu_uno`
([WuEnunciado.lean](../gao20260920/formal/WuEnunciado.lean); definiciones en
las líneas 15–44, teoremas en 46–52). Usan [Condoras](../gao20260920/formal/Condoras.lean).
Premisas: ninguna.

**Ya comprobado.** `K(2^N)` hasta N=26, con código independiente. Las dos
conjeturas y la racha de 176 se leyeron con la IA de CNKI
([nota](../../papers/revision20260927/cnki_wu_20260927.md)).

**Para quien revise.**
1. ¿`d(M)=K/(M-1)` y `enUpla` (líneas 25–31) son la `d` de Wu? En
   `enUpla 1`, la resta natural da `n-1=0`. Lean ya lo confirma:
   `wu_cero_sin_altura` prueba que el 0 no tiene altura, y `wu_enUpla_uno`
   que en n=1 sólo cuenta el vecino 2. Además, `altura_wu_garner` dice que la
   altura de Wu y la de Garner son la misma definición.
2. ¿`uplaEn` con `n+k<=M` describe k consecutivos dentro de `[1,M)`?

**Falta.**
- **El impreso de Wu (1992):** las conjeturas sólo se conocen por la lectura
  con IA, y el artículo III lo declara.
- Citar a Nashida (2026) en la conjetura 1.
- La lectura humana.
- El III tiene cambios locales sin commit que no son de esta rama.

## IV. Ocelotas: CST con hasta 83 rachas

**Afirma.**
- **Con las premisas (LMN23 o RhinHomogenea 2) y RecordRoosendaal:** si
  `n>=2`, k es el primer cruce `3^S_k<2^k` y hay a lo sumo 83 rachas
  impares, entonces la órbita no desciende antes de k y `T^k(n)<n`.
- **Sin cobertura externa:** 24 rachas bajo LMN
  ([VEINTICUATRO_LEAN](../cst20260930/VEINTICUATRO_LEAN.md)); 40, 41, 42 y 46
  con censos propios como hipótesis explícitas.
- **47:** el usuario lo aprobó como «no se hará» el 12-10, pero el cierre
  documental está sin hacer.

**Lean.** `OcelotasRozier.cst_83_lmn` y `cst_83_rhin`
([OcelotasRozier.lean](../cst20260930/OcelotasRozier.lean), líneas 15–48).
Definiciones:

| Pieza | Archivo | Líneas |
| --- | --- | --- |
| `PrimerCruce` | [Ocelotas.lean](../cst20260930/Ocelotas.lean) | 46–47 |
| `rachas` | [OcelotasContador.lean](../cst20260930/OcelotasContador.lean) | 15 |
| `LMN23` | [OcelotasLMNFuente.lean](../cst20260930/OcelotasLMNFuente.lean) | 20–24 |
| `RhinHomogenea` | [OcelotasRhin.lean](../cst20260930/OcelotasRhin.lean) | 33–36 |
| `DelayHasta` | [OcelotasRoosendaal.lean](../cst20260930/OcelotasRoosendaal.lean) | 18–19 |

`RecordRoosendaal` es `DelayHasta 46645791847966786687 2480`. Las tres
premisas son argumentos del teorema: `#print axioms` no las demuestra
([evidencia](../cst20260930/evidencia_rozier.json)).

**No dice** que el primer cruce exista para todo n, ni CST sin límite de
rachas, ni Collatz.

**Ya comprobado.**
- LMN, corolario 2, pág. 288, y Rhin (1987), pág. 160, ecuación (7), leídos
  en el original.
- Página y datos de Roosendaal guardados con huellas.
- Los 2480 pasos del récord, comprobados por el núcleo sin axiomas.
- Las constantes de Rozier–Terracol v5, reconstruidas.
- Terras (1976, pág. 252) ya da CST para tiempos cortos.
- Detalle en la [revisión del 16-10](../cst20260930/revision_rozier_20261016/REVISION.md).

**Para quien revise.**
1. ¿`LMN23` es el corolario 2 de LMN con `α1=3`, `α2=2` y `log A2=1`?
2. ¿`RhinHomogenea 2` es la ecuación (7) con `u0=0`?
3. ¿`DelayHasta N 2480` es lo que garantiza la tabla de récords de
   Roosendaal? Su completitud depende de verificaciones exhaustivas ajenas.
4. ¿`rachas n k` es la r del artículo IV? Ayuda Lean, sin código nuevo:
   - `OcelotasContador.rachas_eq_card` (OcelotasContador.lean, línea 19) la
     escribe como el número de `j<k` con `T^j(n)` impar y, si `j>0`,
     `T^(j-1)(n)` par;
   - `OcelotasFinito.primer_cruce_unico` (OcelotasFinito.lean, línea 68)
     prueba que el primer cruce es único: k es el τ(n) de Terras.
5. ¿Qué parte es nueva frente a Simons (2022) y sus m-nykels?

**Falta.**
- **Prioridad frente a Simons:** la búsqueda web no la certifica.
- Una reconstrucción limpia, porque la auditoría reutiliza por huellas una
  base local.
- La prueba de Rhin queda como teorema externo.
- El borrador del artículo IV está en 81 rachas con Rozier–Terracol; falta
  llevarlo a 83, con Roosendaal y Rhin.
- La respuesta a Rozier está aplazada por el
  [Plan B](../cst20260930/revision_rozier_20261016/PLAN_RESPUESTA.md).

## Resumen de pendientes y de quién los hace

| Pendiente | Quién |
| --- | --- |
| Lectura humana de los cuatro enunciados, con las preguntas de arriba | Una persona: el usuario o un revisor que él elija |
| Impresos de Wu (1992) y Garner (1985); MathSciNet y Scholar | El usuario, que tiene acceso o puede pedirlos |
| Estado de JAR en SNAPP; destino de II, III y IV; ORCID | El usuario |
| Llevar el IV a 83; integrar en el registro la cita de Dubickas (2009), ya validada en copia temporal ([J2 §5](J2_MECANISMOS.md#5-prioridad-la-cota-de-complejidad-ya-estaba-en-2009)); cerrar el 47 por escrito | Una próxima tanda, con permiso |
| Reconstrucción limpia de Ocelotas desde cero | Una tanda larga: horas de Lean y varios GB; sólo con permiso |

**Recomendación de esta rama.** Lo que más rinde por hora es la lectura
humana de los enunciados de I a IV: cada uno se lee en minutos con las
preguntas de arriba. Le siguen los impresos de Wu y de Garner. Como J2 salió
(b), un avance del piloto puede no llegar. Por eso esta rama mantiene su
consejo de no atar la respuesta a Rozier a ese avance. La decisión es del
usuario.

## Reproducir

```powershell
python -B -X utf8 depuracion/judas20261016/verificar_expediente.py --salida depuracion/judas20261016/vigencia_expediente.json
```

No compila: tarda segundos. Los lemas de lectura tardan unos dos minutos,
desde `depuracion/gao20260920/formal`:

```powershell
lake env lean ../../judas20261016/LecturaRevision.lean
```

Las reconstrucciones completas están en
[gaopendientes](../../gaopendientes.md#reproducir) y en la
[revisión del 16-10](../cst20260930/revision_rozier_20261016/REVISION.md#reproducir-y-responder).
