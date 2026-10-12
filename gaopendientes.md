# Gao: lo hecho y lo pendiente

25-09-2026, revisado el 26-09 (Alpacas). Qué está demostrado, qué falta y cómo cerrarlo. El estado breve
está en [ESTADO_INVESTIGACION.md](ESTADO_INVESTIGACION.md); las pruebas, en
las notas enlazadas. Esta hoja no las repite.

## El resultado

Mapa clásico `f(n)=n/2` si n es par y `3n+1` si es impar (A006370), sobre los
naturales. Conjunto

    G = { m : f^k(m) = f^k(m+1) para algún k <= floor(log2 m) }.

Teorema `GaoEnunciado.conjetura_gao`: `#(G ∩ [0,N))/N -> 1`, es decir, G
tiene **densidad natural 1**. Es la conjetura de Gao (1993) **en la forma
que resume Lagarias**. El artículo original, leído el 25-09, la enuncia de
otro modo, más exigente: `d̄_k -> 1`. **Esa forma literal está demostrada
desde el 26-09** (`GaoLiteral.conjetura_gao_literal`, [Hienas](depuracion/gao20260920/Hienas.md)),
junto con `d(x) -> 1`. No hay ley ni condicionamiento: el teorema es
determinista. La cadena con bits justos es sólo el vehículo, y Tejonas la
transporta de forma exacta a las clases módulo `2^t`. **No dice nada de
llegar a 1: no es la conjetura de Collatz.**

| Pieza | Qué da | Nota |
|---|---|---|
| Sesiones del 20-09 al 24-09 | EF, VH, Hormigas, H3, C1, protocolo guardado | [Guardias](depuracion/gao20260920/Guardias_finitas.md) |
| Lagartijas | pocas entradas; CF_F entera | [Lagartijas](depuracion/gao20260920/Lagartijas.md) |
| Martas | `P(sigma>h) -> 0` | [Martas](depuracion/gao20260920/Martas.md) |
| Tejonas | pares reales, mapa clásico, densidad | [Tejonas](depuracion/gao20260920/Tejonas.md) |
| GaoEnunciado | forma de límite, autocontenida | [GaoEnunciado.lean](depuracion/gao20260920/formal/GaoEnunciado.lean) |
| Hienas y GaoLiteral | forma literal de Gao: `d̄_k -> 1`, `d(x) -> 1` | [Hienas](depuracion/gao20260920/Hienas.md) |
| Alpacas y GarnerEnunciado | Garner (1985): rachas de todo largo con la misma altura | [Alpacas](depuracion/garner20260926/Alpacas.md) |

## Lo ya comprobado

- **Formalización.** Lean 4.32.2 y Mathlib `905b95818eb3`. `#print axioms`
  sólo muestra `propext`, `Classical.choice` y `Quot.sound`. No hay `sorry`,
  `admit`, `native_decide`, `axiom` propios ni `extern`.
- **Repaso desde cero, 26-09.**
  - Se apartó la compilación vieja y se recompiló todo: 1610 tareas,
    código 0 y 175 consultas de axiomas, todas estándar.
  - En algunas consultas `Classical.choice` sale como `choice` a secas. Los
    15 axiomas del entorno son del núcleo de Lean; el proyecto no declara
    ninguno.
  - En los fuentes no hay notaciones, macros ni instancias que cambien el
    sentido del enunciado.
  - `leanchecker` da código 0 en los 26 módulos propios.
  - `leanchecker --fresh`, que también revisa Mathlib desde cero, da código
    0 sobre la unión.
  - [La evidencia](depuracion/gao20260920/evidencia_gao_lean.json) toma ahora
    los hashes con LF. Los tres que no coincidían sólo diferían en CRLF.
- **Enunciado reescrito aparte.** [Hienas.lean](depuracion/gao20260920/formal/Hienas.lean)
  sólo importa Mathlib y escribe de nuevo la forma de Lagarias. Lean acepta
  que `conjetura_gao` la demuestra tal cual (`GaoLiteral.lagarias`).
- **Conteo exacto.** [Pares reales](depuracion/gao20260920/verificar_lagartijas_pares.py):
  262.144 pares `(n,n+1)` con n en `[2^18,2^19)`.
  - El estado real coincide con la cadena en cada paso.
  - Las fusiones coinciden hasta t=18.
  - Periodicidad módulo `2^18`.
  - Encuentro clásico con `k<=2t` en los 103.358 pares fusionados.
  - Cero fallos.

  La [cadena reimplementada](depuracion/gao20260920/verificar_lagartijas.py)
  comprueba las desigualdades de Lagartijas con parámetros pequeños.
- **Cotejo del enunciado.** `conjetura_gao` coincide literalmente con el
  resumen de Lagarias: entrada 68, releída el 26-09 en el PDF de `lecturas/`.
  La forma literal de Gao está en `GaoLiteral.conjetura_gao_literal`. Con
  sus mismas definiciones, un `#guard` recalcula la tabla 3 hasta k=12, y
  [verificar_hienas.py](depuracion/gao20260920/verificar_hienas.py) reproduce
  sus 21 valores.
- **Coherencia numérica.** Las fusiones balanceadas hasta t son A398792(t),
  y `A398792(32)/2^32 = 0,4356…`. La densidad observada de G es 0,364 en
  `2^20` y 0,374 en `2^22`. El 0,389 de Gao es otra cantidad: `d̄_24`, de su
  tabla 3. Son mediciones finitas: ni confirman ni refutan un límite.

## Lo que falta, en orden

La forma literal de Gao, que era el antiguo punto 2, quedó hecha el 26-09
([Hienas](depuracion/gao20260920/Hienas.md)).

1. **Lectura humana de los enunciados.** Lean certifica el enunciado, no su
   lectura.
   - Las líneas 11–20 de [GaoEnunciado.lean](depuracion/gao20260920/formal/GaoEnunciado.lean):
     - `f` es el mapa clásico, con `f(0)=0`.
     - `Nat.log 2 m` es `floor(log2 m)` si m>=1, y 0 si m=0. Para k entero,
       `k<=log2 m` equivale a `k<=floor(log2 m)`.
     - `f^[k]` es la k-ésima iteración.
     - El filtro de `Finset.range N` son los `m<N` de G; el cociente por N
       tiende a 1. En Lean `x/0=0`, lo que no afecta al límite.
     - `open Classical in` sólo da la decidibilidad del filtro.
     - El teorema no tiene hipótesis, y `f = TejonasGao.collatz` se prueba
       por `rfl`.
   - Las líneas 34–76 de [Hienas.lean](depuracion/gao20260920/formal/Hienas.lean):
     - `coalescen` pide la misma imagen, las mismas mitades y ningún 1 en
       `C^0..C^k`.
     - `dbarra k` cuenta los `n<2^k-1` que coalescen en algún `j<=k`, y
       divide por `2^k`.
   - Las líneas 11–27 de [GarnerEnunciado.lean](depuracion/gao20260920/formal/GarnerEnunciado.lean):
     - `altura n h` es `height(n)=h`: `C^h(n)=1` y ningún `C^k(n)=1` con `k<h`.
     - `mitades n h` cuenta los `k<h` con `C^k(n)` par. Con h la altura es
       `σ∞(n)`.
     - `FormaGarner`: para todo L y N hay `n>=N` con `n, …, n+L` de igual
       altura h e igual `σ∞`. Tres `#guard` reproducen ejemplos de Gao.
2. **Búsqueda bibliográfica a fondo.** El 26-09 se ampliaron las fuentes: las
   bibliografías de Lagarias, las 9 citas de Semantic Scholar y ccchallenge
   ([ficha](depuracion/gao20260920/ficha_gao_lagarias.md)). El 27-09 se leyó
   por su API la lista entera de ccchallenge (379 registros), y nadie en ella
   demuestra Gao, Garner ni Wu ([ruta transversal](depuracion/transversal20260927/LEEME.md)).
   Falta:
   - consultar MathSciNet y Google Scholar. zbMATH ya respondió por su API:
     por título el 27-09 y por citas el 11-10. Citan a Garner (1985)
     Elia–Tucker 2015, LaDue 2018 y Wu 1992; no hay citas indexadas a
     Gao (1993). Ninguno prueba rachas de todo largo ni la conjetura de Gao;
   - leer enteras las cuatro citas vistas sólo por título o resumen.
3. **Redacción en prosa autocontenida.** Las notas usan el vocabulario del
   laboratorio y dependen de las sesiones desde el 20-09. Un revisor necesita
   en un solo texto:
   - las definiciones, la cadena y el potencial de Lagartijas;
   - el transporte y la densidad;
   - el puente de Hienas con el enunciado original de Gao;
   - un mapa del código Lean.
4. **Revisión externa**, sólo con autorización del usuario. ccchallenge.org
   acepta formalizaciones en Lean y las audita. Exige declarar el uso de IA
   y el modelo, y que el auditor no sea el autor. El 27-09 su cola estaba
   parada: 6 esperando auditoría y ninguna en curso.
5. **OEIS.** La propuesta del 24-09 (borrador en zootheorem, que no se toca
   desde aquí) dice que Gao «proved that its density is at least 0.389 (as
   summarized by Lagarias)» y que «Gao's conjecture is thus the statement
   that…».
   - Según el original, 0,389 es `d̄_24` calculado, y lo probado es que
     existe `lim d̄_k`.
   - La conjetura literal es `d̄_k -> 1`.

   Conviene ajustar esas dos frases antes de enviarla. Lo decide y lo hace
   el usuario. No añadir que está demostrada mientras no haya revisión: el
   ARSENAL de zootheorem pide evitar «proved» como insignia. Las fichas de
   A398792 decían «They do not establish that lim A398792(n)/2^n = 1»
   ([nota del 24-09](depuracion/oeis20260924/LEEME.md)), y ese límite es justo
   lo que dan Tejonas y Martas. Cualquier edición, tras la revisión.
6. **Rutas que abre.**
   - **Rachas de Garner: hecho el 26-09** ([Alpacas](depuracion/garner20260926/Alpacas.md)).
     `GarnerEnunciado.conjetura_garner`: para cada L hay L+1 consecutivos,
     tan grandes como se quiera, con la misma altura y el mismo `σ∞`. Sale
     de Martas por cota de unión y de llevar el valor común a una potencia
     de 2. Pendiente de la misma revisión humana. Faltan MathSciNet y el
     texto de Garner (1985); zbMATH (11-10) no la registra resuelta.
   - Enunciar en Lean el corolario `A398792(t)/2^t -> 1`, que sale de
     `transporte` y `martas`.
   - Un ritmo útil. El de la prueba es pésimo: `J_F*p_m>1` sólo desde
     m=802923 ([Cigarras](depuracion/gao20260924/Cigarras.md)). El modelo
     sugiere que falta lo que tarda en volver un paseo al azar, del orden de
     `1/sqrt(t)`. Es una heurística, no está medida.
   - Garner (1): que la mayoría tenga la altura de un vecino. Sale con
     densidad 1 si la altura puede ser infinita. Con alturas finitas hace
     falta saber que esos n llegan a 1, y eso está abierto.
   - **Ruta transversal (27-09)**, para cruzar de los pares a la llegada a 1
     ([nota](depuracion/transversal20260927/LEEME.md)). Tiene tres cruces:
     Pandas con la pregunta de Gao, Condoras con Nashida (2026) y los
     predecesores de Wirsching.
   - Decidir si `phi_uno` se cierra en el registro: sigue pendiente por sus
     aristas históricas, aunque `gao_densidad` ya da su contenido.

## Reglas vigentes

El repositorio es público: lo que se sube es visible, pero no es un anuncio.
**No anunciar, no enviar a OEIS ni a revistas y no contactar a nadie sin
autorización del usuario.** Los cambios de afirmaciones van al registro
versionado. No se reconstruyen conversaciones. El PDF de Gao no se sube.

## Reproducir

```
cd depuracion/gao20260920/formal     # primera vez: lake exe cache get (README)
lake build GaoCore GaoFormal
lake env lean GaoEnunciado.lean      # axiomas del teorema final
lake env lean GaoLiteral.lean        # forma literal, con el #guard de la tabla 3
lake env leanchecker GaoLiteral
lake env lean GarnerEnunciado.lean   # Garner, con los #guard de Gao
cd ..
python -B -X utf8 evidencia_gao_lean.py            # todo, y reescribe la evidencia
python -B -X utf8 ../garner20260926/verificar_alpacas.py   # rachas construidas y tabla 1
python -B -X utf8 verificar_hienas.py              # tabla 3 de Gao y puente, n<2^24
python -B -X utf8 verificar_lagartijas_pares.py
python -B -X utf8 verificar_lagartijas.py
```

## Fuentes

- J. C. Lagarias, *The 3x+1 problem: An annotated bibliography (1963–1999)*,
  arXiv:math/0309224, pág. 28, entrada 68.
- G.-G. Gao, *On consecutive numbers of the same height in the Collatz
  problem*, Discrete Math. 112 (1993) 261–267, doi:10.1016/0012-365X(93)90240-T.
  Leído el 25-09, en el PDF que aportó el usuario.
- ccchallenge.org, que el 25-09 listaba Gao (1993) como «not formalized».
- arXiv:2603.11066 y arXiv:1511.09141: consultados el 25-09; no demuestran
  esta conjetura.
- 26-09:
  - la misma bibliografía, entrada 72 (Garner 1985, sus dos conjeturas) y
    entradas 189–190 (Wu); la bibliografía II (2000–2009);
  - Semantic Scholar, 9 citas de Gao (1993); LaDue, arXiv:1709.02979;
  - K. Frinkle et al., *Computing streaks of consecutive numbers with the
    same Collatz height*, J. Supercomputing (2025), sólo el resumen;
  - OEIS A078417, A078441 y A277109;
  - ccchallenge.org/contribute;
  - para Alpacas: M. Elia y A. Tucker, Integers 15 (2015), arXiv:1511.09141
    (refutan la caracterización de Garner por bloques y cadenas), y el
    volumen 112 de Discrete Math. que aportó el usuario, donde sólo Gao
    trata Collatz.
- 27-09: la lista de ccchallenge por su API, y los trabajos nuevos que cita
  la [ruta transversal](depuracion/transversal20260927/LEEME.md#fuentes).
