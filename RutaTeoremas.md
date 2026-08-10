# RutaTeoremas.md — el camino a Perras y Gatas, y la ruta que sigue

Escrito el 03-08-2026 al cierre de la sesión que los produjo. **Este fichero es
el contexto de arranque de la próxima sesión**: qué se demostró, por qué rama
del mapa de dependencias se llegó, y cuál es el siguiente movimiento. El mapa
vive en `afirmaciones.db` (tablas `nodos` y `dependencias`, con la REGLA DEL
AVANCE en la COMPROBACIÓN 0 de `guardarafirmaciones.py`).

---

## Los dos teoremas, con sus etiquetas honestas

### TEOREMA DE PERRAS (la mitad exacta del estrato 2)

> Para `r` PAR, el par `(r, r+1)` se funde con `|M| = 2` **si y sólo si** en el
> vector de paridad de `s₁ = r/2` el primer 0 va seguido de un 1; y entre
> `s₁ ∈ [1, 2^m)` fusionan **exactamente `2^{m−1}`**, para todo `m ≥ 2`.

- Demostración y verificación: `nuevasfusion.py`, COMPROBACIÓN 15
  (equivalencia exhaustiva `s₁ < 2^16`, conteos `m = 2…16`).
- **Estado bibliográfico (verificado 03-08-2026):** el patrón ES el *stem*
  `s_i` de **Garner 1985**, que demostró la suficiencia (⟸) y conjeturó la
  necesidad para TODA fusión; **Elia–Tucker 2015** (arXiv:1511.09141, leído
  entero) refutaron esa necesidad (3067/3068). **Lo nuevo de Perras:** la
  necesidad restringida al estrato mínimo (`|M| = 2 ⟺ stems`) es VERDADERA,
  y el conteo exacto con el borde resuelto (de los dos residuos frontera
  funde exactamente uno para cada `m`, según `3^m mod 4`). *Perras = la
  conjetura de Garner, falsa en general, demostrada en el estrato mínimo con
  su densidad exacta. Los contraejemplos de Elia–Tucker viven en `|M| ≥ 4`.*

### TEOREMA DE GATAS (el reinicio uniforme y la ecuación de renovación)

> (a) La contracción manda `r = 4t+1` al par consecutivo **fresco**
> `(3t+1, 3t+2)`, y `t ↦ 3t+1` es biyección de `Z/2^m`: la autosimilitud del
> problema de fusión es **exacta** — `P(fusión | contracción) = f`, la misma
> incógnita. (b) El parámetro `w` del rebote es exactamente uniforme
> (Terras 1.2). **Corolario:** la ecuación de renovación
>
> ```
> f  =  1/4·1  +  1/4·f  +  1/4·g  +  1/4·h        (exacta)
> ```
>
> con `f ≥ 1/3` demostrado en tres líneas.

- Demostración y verificación: `nuevasfusion.py`, COMPROBACIÓN 16.
- `f` = P(fusión de par consecutivo uniforme); `g` = P(fusión | rebote,
  familia real `(w, 9w+2)`, objetivo `ΔS = −2`); `h` = P(fusión | `r ≡ 3
  mod 4`). Medido con topes declarados: `f ≈ 0,445`, `g ≈ 0,188`, `h ≈ 0,173`
  — y la ecuación **cierra** (0,4504 contra 0,4453).
- **Estado bibliográfico:** sin rastro de renovación para coalescencia de
  consecutivos; lo único cercano (arXiv:2005.09456, pares `(n, 3n+2)`) es
  empírico y está retirado. «No encontrado» no es «no existe».

---

## El camino por el mapa de dependencias (cómo se llegó)

```
definiciones (mapa del atajo, buenas(k), b(k) = nuevas)
    │
    ├── ecuacion_vortice ─ una clase se estrena ⟺ primer encuentro en un
    │        vórtice (a = 3b+1, S compensada). Convirtió b(k) en congruencia.
    │
    ├── lema_identidad (T(c·2^m − 1) = 3c·2^{m−1} − 1)
    │        └── lema_general (C ≡ 3^q mod 4) ── teo_repunit ── nuevas_no_acaban
    │
    ├── lema_v2 (mixto ⟺ d impar; compartido quita un factor 2; |M| par)
    │        ├── unicidad_M2 (2^{k−1}−2 / 3·2^{k−1}−2, alternando)
    │        └── coordenadas_DE
    │              ├── D = g − 2s − 1: vórtice ⟺ D = 0 con s impar;
    │              │     dos afines en compartidos; D < 0 absorbente
    │              ├── E = D − 3s: AUTÓNOMA (su paridad elige su mapa)
    │              ├── familias_E (censo: DIEZ ciclos, ninguna órbita escapa)
    │              └── no hay tercera coordenada (H = l − 1: el estado es 2D)
    │
    ├── estratos (|M| par; filas 2 y 4 únicas por nivel; entrada de estratos
    │        como mecanismo de la razón → 2)
    │
    ├── ⇒ TEOREMA DE PERRAS  (D = 1 → primer par de la trayectoria de s₁ →
    │        vórtice ⟺ bit siguiente = 1 → conteo por biyección de Terras)
    │
    └── ⇒ TEOREMA DE GATAS   (contracción literal + uniformidad del rebote →
             ecuación de renovación; su primer uso CAZÓ LA FAMILIA FANTASMA:
             el rebote real es (w, 9w+2), no (w, 6w+2) — corrección nº 34)
```

**Las lecciones del camino que hay que recordar:** (1) la ecuación de
renovación que no cierra es un detector de premisas falsas más fino que
cualquier barrido — así cayó el fantasma; (2) las familias canónicas se
verifican CONTRA EL OBJETO REAL antes de razonar sobre ellas; (3) la familia
asintótica de E es invariante ruidoso para contar (itinerarios.py) — etiquetar
por datos finitos.

---

## ⇢ ACTUALIZACIÓN AL CIERRE DEL 03-08-2026 (tres revisiones externas después)

**Estado tras las tres revisiones de Opus 5** (actas completas en las
secciones finales de los tres `.txt` y en `bitacora.md`):

- **Perras**: sólido. R1–R7 aplicadas. El conteo `2^k − 1` tiene ya
  demostración de dos líneas (del revisor) — falta subirlo de
  verificación a proposición en el `.txt`.
- **Gatas (a)** y la ecuación de partición: intactas. Gao 1993 citado
  (el levantamiento y la existencia de `f` son suyos).
- **Jirafas**: el teorema aguanta; **C1 retirado** (corrección nº 36);
  **C2 demostrado por coeficientes**. El revisor confirmó: Jirafas era
  un atajo, no un cimiento — nada de lo demás lo usaba.
- **LA IDENTIDAD ES TEOREMA, NO TAUTOLOGÍA** — la pregunta decisiva del
  revisor, contestada con enteros ANTES de que llegara su carta:

      a(k+2) = a(k) + (2^k − 1) + Σ_{i=0}^{k−1} b(i) + c(k)

  con `b(i)` = clases de `{w, 9w+2}` que funden de clase en ≤ i pasos y
  `c(k)` = ídem de `{w, 9w−1}` — **computadas desde sus propias
  definiciones, sin mirar el `r` original**, clavadas `k = 3…14`
  (`identidadexacta.py`, comprobación final). Los bits libres igualan el
  presupuesto en la rama g: «la estructura del problema asomando».
- **El 10,3% instrumentado**: las 13.137 fusiones desbalanceadas chocan
  TODAS en el valor 2; densidad ~0,39 decayendo lentísimo. Masa real,
  fuera del sistema legítimamente (no aporta a `g`).
- **Test espejo `3n−1`**: 12/12 con las etiquetas volteadas (`r` par ↔
  `v` impar), tras cazar un off-by-one propio en el mapeo del espejo.

## ⇢ ACTUALIZACIÓN 04-08 (LA JORNADA DE JORNADAS + LA CADENA)

**Esta sección deja obsoleta la ruta de abajo** (que era la del cierre
del 03-08). Lo que pasó después, en orden (detalle en `bitacora.md`):

1. **El sistema de φ quedó cerrado en fórmula**:
   `φ = (1+β+γ)/3` (demostrada), `β = γ/2 + (φ+γ)/8 + ε_torre`,
   `γ = ρφ` con `ρ = Σ R(j)·2⁻ʲ` ⟹ **`φ = 8(1+ε)/(23−13ρ)`**, y
   **`φ = 1 ⟺ ε_torre = 1/4 ⟺ el paseo de la deuda es recurrente`**
   (= Gao–Wu en densidad). Afirmaciones #86–93.
2. **Komodo 3** (mod 3) demostrado y en Lean; **auditoría rigor mortis**
   35/35 (`auditoria_rigor.py`); 10 `.lean`, todos núcleo puro.
3. **LA CADENA (k, c)** (`paseodeladeuda.py`, 04-08 tarde): el programa
   entero es un sistema simbólico de SEIS leyes con moneda de Terras;
   reproduce `a(k)` exacto (k ≤ 32) y **extiende a(33), a(34)**
   (razones de b: 1,9412 → 1,9432); la torre no retiene masa — la
   obstrucción a φ = 1 es la dispersión de `c`, no el paseo en `k`.

**LA RUTA VIGENTE (actualizada al cierre del 04-08 (3)):**

1. ~~el paseo de la deuda~~ **HECHO** (`paseodeladeuda.py` + `cadenakc.lean`).
2. ~~retaguardia~~ **HECHA**: seis leyes en Lean con `k` general
   (`cadenakc.lean`), flecos de `R` resueltos (`flecosr.py`), conteo de
   Perras en Lean (`perrasconteo.lean`), y de regalo `zoologico.lean`
   (los núcleos de los .txt portados, orden del usuario).
3. ~~contabilidad de canales de e₈~~ **HECHA y estructural**
   (`estratoscadena.py`); ~~segundo camino a(33)/a(34)~~ **HECHO**
   (`segundocamino.py`). El cruce LaTourette sigue **bloqueado**
   (falta el PDF: yumpu págs. 28–31 o correo a Fraboni/Moravian).

---

# ⇢ EL ESTADO Y LOS PRÓXIMOS PASOS (actualizado 09-08-2026)

**EMPEZAR POR AQUÍ.** Todo lo de abajo es historia; esto es el frente.

## ⇢ LA SUB-TEORÍA DE LA MADRIGUERA (09-08 (6)–(7), manda sobre lo de abajo)

Tres piezas encajadas y **YA PASADAS por la 5ª revisión externa
adversarial** (tres revisores independientes, acta íntegra en
`actarevision0908b.txt`; quinta revisión, quinta vez que rompió algo —
correcciones aplicadas el mismo cierre):

1. **LIEBRES** (AGUANTÓ): `φ = 1 ⟺ Σ_t P(X_t ∈ C) = ∞` para TODA
   ventana finita — Green + clase cerrada + Doeblin exacto
   (`17887/131072` reproducido dígito a dígito por el revisor);
   aperiódica (gcd de retornos = 1); para `C` arbitrario la
   accesibilidad se apoya en HORMIGAS cualitativo (cita añadida — era
   cuantificador escondido). **Ojo con la medición**: a PROF = 30 la
   ventana `C_625` contiene el 99,99% del fondo y su serie diverge
   bajo LAS DOS hipótesis (Golondrinas) — el alfa ~0,40 es el retorno
   al fondo, no evidencia sobre φ. Lo informativo: `r_5`, `r_25`
   bajando sin estabilizar — **INDECIDIDO**.
2. **CEBRAS** (PARTIDA EN DOS): la clasificación afín y el umbral
   `log 2/log 3` **como exponente de Lyapunov de los multiplicadores**
   aguantan (100.398 transiciones independientes) — es la hipótesis de
   Kesten de la perpetuidad de Arañas. La lectura «deriva de `log|u|`
   de la cadena» está **ROTA y RETIRADA**: la deriva real del fondo es
   +0,02 (allí `|u| ≥ 1/3` siempre), el desplazamiento afín −1/2 es el
   IFS y no la perturbación, y el margen «13 puntos» (son 12,1) era
   menor que el error de modelado en nats. Las tres `q1` van
   separadas: global 0,4585 (foto, sube a 1/2), histórica del fondo
   0,5095 (pico y baja), instantánea del fondo 0,420 bajando.
3. **URRACAS** (AGUANTÓ ENTERA): `exp − contr = 2V + (Ee−E0) + k₀ −
   k_t` exacto — tabla rederivada por el revisor, 200.000 palabras
   propias, t = 20 reconstruido desde cero, Lean cotejado a máquina
   (2.709 estados), y la circularidad C0/Lean/modificada **rota por
   fuera** con 59.990 pares enteros reales. El corolario queda con
   etiqueta fina: `⟺` exacto en la sombra IFS; en la cadena, umbral
   **efectivo ~0,2446** (error del modelo ~+0,009 nats/paso, rebote
   2/3). Sesgo medido ~0,019: margen ×13.

**EL ÚLTIMO PASO, con la etiqueta del acta:** acotar la esperanza
condicionada del desbalance de la moneda justa (más la ocupación del
vórtice, que decae) por debajo del umbral efectivo ~0,2446 por paso.
El h-transform del paseo crítico de `k` sesga `O(1/k)`, no
exponencialmente — ésa sigue siendo la vía. **Regalo de la revisión,
YA COBRADO (09-08 (8)):** el invariante mod 3 resultó ser la puerta de
CABRAS por la cadena entera y está formalizado en **`cabras.lean` (el
16º)** con el corolario `torre_sin_ceros` — los saltos de `c = 0` son
teorema, no convención.

## ⇢ EL PUENTE — lo que hay DESPUÉS de φ (esbozado por el usuario con Opus 5, 09-08 noche)

La ruta si el programa de la densidad cierra, escrita para que no se
pierda:

1. **Si `φ = 1` cae** (Gao–Wu en densidad): casi todo `n` funde con su
   vecino, y fundirse es compartir destino — encadenando vecinos salen
   **bloques enormes de números con el mismo final** (las rachas de
   Frinkle et al. 2025, medidas en decenas de miles de consecutivos).
   Eso convierte «todo número llega al 1» en «**los representantes de
   cada bloque llegan al 1**»: no es Collatz demostrada, es **Collatz
   REDUCIDA a un conjunto flaco** — y esa frase sí se puede escribir
   en un paper. *(Cuantificador honesto: el conjunto excepcional de
   densidad 0 es exactamente donde viviría el contraejemplo — el
   mismo muro de Tao 2019, y se declara como tal.)*
2. **El techo de la maquinaria, con su porqué**: el teorema del espejo
   (`a₊ = a₋`) limita los TEOREMAS de esta cadena, no las
   herramientas — todo enunciado que salga de aquí vale igual para
   `3n−1`, así que no puede decidir lo que los separa. **El
   ingrediente que falta para tocar Collatz misma tiene nombre: seguir
   el VALOR, no la diferencia.** La cadena `(k,c)` sigue la diferencia
   de dos órbitas (ciega al signo); una extensión que arrastre
   información del valor (la altura, el tamaño de `v`) rompería la
   simetría del espejo. Ésa es la puerta del zoológico que queda por
   abrir cuando la densidad esté cerrada.

## ⇢ LA REFORMULACIÓN DEL 09-08 (manda sobre lo de abajo)

**`φ = 1 ⟺ (1,1) es RECURRENTE en la cadena MODIFICADA`** (la de
Leonas con el vórtice rebotado a `(2,2)`): cada visita al vórtice
sobrevive con moneda 1/2, luego `P(no fundir) = E[2^{−N}]` con `N` =
visitas — positivo sii `N` puede ser finito. **Sin condicionamiento a
vivo: el problema de Bessel desaparece.** Equivale a `Σ retornos(L)·2^{−L}
= 1` (la serie de Ovejas): la razón 2 en su disfraz final.

**El camino demostrado y el que falta** (`lamperti.py`, 09-08):

1. **EXACTO (C1)**: `k` es martingala en todo el núcleo (deriva 0,
   28.436 estados enumerados), con empuje `+1` sólo en frontera impar
   y vórtice rebotado. Oscilación de martingalas: si hay infinitos
   mixtos, `A → ∞` = **infinitas visitas al fondo**.
2. **(L2) infinitos mixtos — DEMOSTRADO** (`oscilacion.py` C1/C2, la
   misma tarde): con `k` congelado entre mixtos y `A = v₂(3^k−1)`,
   ambos bits bajan `v₂(c)` salvo bit 1 exactamente en `v₂ = A`; bajo
   `A` el descenso es determinista, y en la frontera los dos bits
   restan 1 a `v₂(g)` — toda ventana de `A+1` ceros fuerza un mixto.
   **⟹ TEOREMA DE GOLONDRINAS: la cadena modificada visita el fondo
   (k ≤ 1) infinitas veces c.s.** (L2 + tabla de derivas + oscilación
   de martingalas: `k = M + A`, `M` no converge, `A → ∞`).
3. **(B) EL MURO FINAL — el empalme por visita**, en la formulación
   que la 4ª revisión validó como LA buena (`retorno11.py`):
   **`φ = 1 ⟺ p = P₍₁,₁₎(retorno) = 1 ⟺ Σ_t P(X_t = (1,1)) = ∞`**
   (dicotomía de Markov + comunicación `(0,1)↔(1,1)` verificada).
   Medido: las dos supervivencias bajan con exponente local SUBIENDO
   (`S(35) = 0,437`, α 0,22→0,24; `1−p₃₄ = 0,685`, α 0,17→0,20) —
   la transitoriedad exigiría lo contrario. El exponente del piso por
   visita debe remedirse (la constante 2,5 de Hormigas era muestra;
   sup exhaustivo ~2,73, demostrable candidata ~4,8).

**⇢ ACTA DE LA 4ª REVISIÓN EXTERNA (09-08, `actarevision0908.txt`),
APLICADA**: Abejas es INCONDICIONAL (Kraft) y su contrapositivo era
VACUO — el «programa en una desigualdad `M_G ≥ c/t`» apuntaba a una
diana demostrablemente inalcanzable; el blanco no-vacuo es `M_G/L` o
la cadena modificada (retorno11, que AGUANTÓ). Hormigas: teorema
intacto, constante 2,5 falsa (muestra). L2 y Golondrinas: conclusiones
en pie con las pruebas remendadas (palabra dependiente del estado;
caso partido núcleo/borde). Águilas: la lectura «la fusión se apaga»
refutada por su propia tabla. Lechuzas: exige el calificador «con S
igualada». Palomas y el criterio: aguantaron todos los ataques.
Retaguardia: ⇢ SALDADA la misma noche — `pisoremedido.py` (el piso
sobrevive a `e = 5`: α = 0,675 < 1 bajando) y **`hormigas.lean`, el
14º `.lean`** (descenso del gap en los dos regímenes + descenso de
frontera exacto, núcleo puro, a la primera). ⇢ El aterrizaje de N2
en `v₂ = A−1` (2-ádica con signo) quedó COBRADO el 09-08 (12):
**`aterrizajen2.lean`, el 17º** (tres teoremas con testigos sin
división, cotejados en 42.196 instancias). El paso teórico abierto
de siempre sigue siendo la estacionaria condicionada.

## Dónde está el programa, en cinco líneas

La cadena `(k, c)` (**Leonas**) es el programa entero. Sobre ella:
**Tigresas** (moneda justa `×1/2 / ×3/2`, `E[m] = 1` exacto: perpetuidad
crítica κ=1) → **Arañas** (en `u = c/3^k` la torre desaparece: IFS
`{u/2, (3u−1)/2}` + perturbación sumable) → **Moscas** (la tensión
transferida: masa viva con `|u| > x` ≤ `B_θ/x^θ`, **uniforme en t**,
autocontenido). **Queda UNA pieza: el piso de absorción por visita.**

## LA ÚLTIMA PIEZA, enunciada con precisión

> Sea `p_t` = (masa de palabras vivas en el pre-vórtice `(1, c=1)` al
> nivel `t`) / (masa viva en `k = 1` al nivel `t`). Medido: `p_34 =
> 0,0457`. **¿`liminf p_t > 0` o `p_t → 0`?**
>
> - Si **no se desvanece** (más uniformidad sobre las visitas): la
>   absorción es casi segura ⟹ **`φ = 1` — la conjetura de Gao–Wu en
>   densidad, CIERTA**.
> - Si **se desvanece**: `φ < 1` con techo calculable ⟹ **el techo
>   exacto de la densidad de fusión**, igualmente publicable.

## Los tres ataques, en orden de valor (con su porqué)

1. **MEDIR `p_t` COMO SERIE, no como foto** (barato, decide el rumbo).
   `p_t` para `t = 10…34` ya se puede extraer de `aranas.py` T4: falta
   la serie completa y su ajuste (¿constante, `t^{−a}`, `1/log t`?).
   **Cuidado con la lección de la casa**: una serie que baja despacio no
   distingue «tiende a constante positiva» de «tiende a 0» — hay que
   mirar el MECANISMO, no extrapolar (el muro de `b(k)`, tres veces).
2. **EL PISO POR ESTRUCTURA, que es donde está el teorema.** La vía:
   Moscas da masa acotada lejos del origen, así que hay masa que vuelve
   a `|u|` chico; en `u` chico el estado `(1,1)` es un punto de una
   rejilla FINITA (`c` acotado ⟹ pocos estados con `k = 1`). Si se
   demuestra que la cadena visita esa rejilla con frecuencia acotada
   abajo y que desde ella `(1,1)` se alcanza con probabilidad acotada
   abajo (bloque de bits explícito), el piso es teorema. **Es el
   argumento de Doeblin/minorización sobre un conjunto pequeño** — el
   nombre técnico a buscar en la literatura.
3. **LA COSTURA DE LA FRONTERA** (~6% de la masa; `k = 0`, donde la
   sombra de Arañas no es exacta: F2 lleva `δ = 1/2` y F4 voltea el
   signo). Si la tensión o el piso fallan, fallan ahí. Vale medir
   aparte la contribución de la frontera al piso.

## La retaguardia (barata, cierra flancos)

- **Formalizar Moscas en Lean**: la dominación `|u'| ≤ m_b|u| + 1/2` es
  aritmética pura — sería el 14º `.lean` y blindaría la única cadena de
  teoremas nuevos del cierre.
- **`e₁₀` y `e₁₂` — RESUELTO EN NEGATIVO (09-08 (10)):** no hay forma
  cerrada que esperar. La C4 nueva de `estratoscadena.py` demuestra por
  exclusión exacta que `e₈`, `e₁₀` y `e₁₂` **no son cuasi-polinomiales**
  (grado ≤ 8, período ≤ 8, arranque ≤ 16, validación entera con control
  `e₆` positivo): **la escalera de formas cerradas termina en `e₆`** —
  del estrato 8 en adelante manda la combinatoria tipo `b(k)`. Y las
  tres series **no están en OEIS** («No results», 09-08) — añadidas a
  `sucesiones.txt` con su ficha.
- **La revisión bibliográfica de la cadena — HECHA (09-08 (9), cuatro
  barridas web con ángulos distintos):** la forma `{v, 3^k v + c}` como
  sistema simbólico con leyes exactas y moneda de Terras **no aparece
  publicada**. Vecinos encontrados y fichados: la coalescencia clásica
  (`8n+4/8n+5`, Garner, Gao, Elia–Tucker — ya en el libro de la casa);
  Frinkle et al. 2025 (streaks, ya en la ruta); **Grimmett & Holmes,
  «Coalescence in Markov chains», arXiv:2510.13572, J. Theor. Probab.
  2026** — el marco general (clases de coalescencia por acoplamiento,
  espacios finitos), SIN Collatz ni nuestra forma: leerlo es pendiente
  nuevo; y **ccchallenge.org** (formalización Lean de la literatura
  Collatz, paper a paper) — referencia útil para la línea Lean del
  repo. *«No encontrado» sigue sin ser «no existe», pero ya se buscó.*
- **Cortesía a Moravian**: el error de la Tabla 4.2 de LaTourette 2007
  es publicable como nota a Michael Fraboni (decisión del usuario).
- **Revisión externa adversarial** de la terna Tigresas/Arañas/Moscas:
  las tres anteriores rompieron algo cada vez.

## Los peligros anotados de esta línea (leer antes de seguir)

1. **La lectura «κ = 1 ⟹ tensa ⟹ φ = 1» es HEURÍSTICA**, y en la base
   está etiquetada así. Moscas demostró la tensión *incondicional*; el
   salto que falta es el condicional a vivo — y si `φ = 1`, la masa viva
   tiende a 0 y el cociente pierde la cota. **No escribir «φ = 1» sin
   ese paso.**
2. **El paso 1 (`dispersionc.py`) leyó «dispersión ⟹ φ < 1» y el paso 2
   lo revirtió.** La medición sola cambió de signo la conclusión en una
   hora. Es el precedente: aquí manda el mecanismo.
3. Lo que NO está: la cola lejana de `u` sigue en tránsito a `t = 34`;
   la distancia CDF cadena–IFS (0,222) es una comparación cruda con
   condicionamientos distintos, no una medida de error.

---

**EL NORTE ANTERIOR — la pregunta única que queda, en coordenadas de la
cadena:** el paseo en `k` vuelve (medido: 93% de la masa viva en
`k ≤ 8`, decae geométrico), así que `φ = 1` ⟺ **la órbita de `c` en
las visitas al núcleo bajo se concentra lo bastante para que la cadena
toque `(1,1)` con probabilidad plena**. Candidatos de ataque:
(a) medir la dispersión de `c` condicionada a `k = 1` por profundidad
(¿masa de `|c|` acotado → constante o → 0?); (b) la sub-renovación de
los estados `(1, c)` con `c` chico (el grafo de los chanchitos
generalizado); (c) formalizar «paseo recurrente ⟹ masa no se pierde
en la torre» como teorema sobre la cadena (el análogo del argumento
de moneda de Terras). Y la retaguardia menor: los estratos `e₁₀`/`e₁₂`
recién medidos esperan sus formas; los conteos del `CLAUDE.md`
esperan su pasada.

**⇢ EL GOAL DE LAMBDA (04-08 (4)) LO AFINÓ:** el autovalor NO separa —
`λ < 2 ⟹ φ = 1` (teorema de inversión, `retornoslambda.py`) y los
truncados demuestran `λ ≥ 1.9754` subiendo. La vía del autovalor
desemboca en el paseo; el norte de arriba (la dispersión de `c`) sigue
siendo el único frente. Regalo del goal: el catálogo de LaTourette
2007 = los primeros retornos de la cadena (con UN error en su Tabla
4.2, cazado y documentado), extendido de largo 11 a largo 30 — la
serie de retornos es ahora un instrumento con precedente bibliográfico
y fe de erratas propia.

**⇢ Y LOS PASOS 1–3 (04-08 (5)) LE PUSIERON NOMBRE AL MECANISMO:**
la dinámica de `c` es una **perpetuidad de Kesten crítica** (cada paso
del núcleo es moneda justa entre `×1/2` y `×3/2`: `E[m] = 1` exacto,
κ = 1), con dos puertas mod 3 (directa → clase 2, vuelco → clase 1) y
la absorción en la clase del vuelco. La serie `b` llegó a `b(35)`
(razones 1.9469 subiendo). **EL BLANCO FINAL con forma de teorema:**
(i) la perpetuidad sobre la medida de las palabras (shifts de torre
sumables: `2^{−k}·log 3^k`); (ii) tensión de la estacionaria — decide
φ = 1 contra φ < 1; (iii) el piso de absorción uniforme por visita.
Ficheros: `dispersionc.py`, `subrenovacionc.py`, `empujarb.py`.

## LA RUTA PARA LA PRÓXIMA SESIÓN (la orden del revisor, puntos 3–6)

1. **Subir `2^k − 1` a proposición** en `teoremadeperras.txt` — la
   demostración ya está escrita (bits libres del prefijo `1^j 0 1`);
   revisar los dos residuos de borde por si dejan corrección en `G`.
2. **Cerrar R6 como teorema de familia**: medir `t` de fusión de
   `(3067, 3068)`; si `t ≤ 19`, por Terras TODA la familia
   `2^19·m + 3067` tiene `|M| = 8` — teorema, no muestra.
3. **EL PROBLEMA NUEVO DE GATAS §5** (el más importante): «fusión al
   mismo índice» ⟹ igual altura, pero el recíproco NO está demostrado —
   dos trayectorias pueden encontrarse en índices distintos `k₁ ≠ k₂`
   con `k₁ + S_{k₁} = k₂ + S_{k₂}` e igual altura sin fundir. Luego
   `f ≤ d(igual altura)` y podría ser estricta. **Contar bajo 10⁶
   cuántos pares de igual altura funden al mismo índice y cuántos no.**
   Si todos: lema y equivalencia real. Si no: hay una TERCERA cantidad
   y el §5 de Gatas se reescribe. (Contexto: Gao midió `d → 0,512` a
   `10⁸`; nuestro `a(12)/2^12 = 0,36` — separar cuánto es truncamiento
   y cuánto es esta brecha.)
4. **Pedir LaTourette 2007** (acción del usuario: correo a la
   biblioteca de Moravian College) — sigue condicionando la novedad de
   Perras. Y leer: Rozier (paridad 2-ádica), Frinkle et al. 2025,
   OEIS A277109.
5. Después de eso: las sub-renovaciones de `b(i)` y `c(i)` (con el
   chequeo de rango anti-tautología ANTES de invertir), que es el
   camino a decidir `f`.

**Nota de empaque**: los nombres (Perras, Gatas, Jirafas) son internos,
estilo versiones de macOS; para cualquier texto que salga del repo se
cambian por nombres serios (p. ej. «lema de la mitad exacta», «teorema
del reinicio uniforme», «lema del balance de clase»).

## LA RUTA TRAZADA para la próxima sesión (la original, superada por lo de arriba)

**El pez gordo tiene nombre y ecuación: decidir `f`.** Si `f = 1`, la razón de
`b(k)` llega a 2 y *casi todo par consecutivo tiene la misma altura* — *la
conjetura de Wu en versión densidad*. Si `f < 1`, también es teorema (y
explica el techo de la fracción de fusión). El camino, en orden:

1. **Calcular `g` exacto** (la incógnita del rebote). Estado inicial
   `(w, 9w+2)` con `w` uniforme, `D = 6w+1`, `E = 3w+1`, objetivo `ΔS = −2`.
   El método que ya funcionó dos veces: descomponer por los primeros bits de
   `w` (como Perras: cada decisión es un bit de Terras) y buscar el reinicio
   (¿alguna rama de `(w, 9w+2)` se contrae a par consecutivo fresco o a la
   propia familia? — ésa sería la sub-renovación que cierra `g`).
2. **Calcular `h` exacto** (la ruta `r ≡ 3 mod 4`). Tras 3 pasos el par es
   `{(3r+7)/8, +(3r−1)/4}` con `D = −3` (r ≡ 3 mod 8) o encadena 4 mixtos
   (r ≡ 7 mod 8). Misma táctica de bits.
3. **Cerrar el sistema** — si `g` y `h` generan sub-familias nuevas, el
   sistema puede necesitar N incógnitas: mientras N sea finito, es un sistema
   lineal y `f` sale EXACTA. Si N no cierra, medir el residuo de masa y
   acotar `f` por arriba y por abajo (ya hay `f ≥ 1/3` estructural).
4. **Pendientes que no son de esta línea** (siguen en bitácora): las 2
   excepciones reales de `M = 27` en `franjaeverett.py`; cobrar el
   `X₀ = 10⁹` de `atacacst2` con la `B(k)` de `paradacoef.py`; formalizar
   Perras/Gatas en Lean (serían el 6º `.lean`).

**Regla vigente:** no avanzar una rama sin la anterior comprobada — el mapa
corta solo (`COMPROBACION 0`). `unicidad_M4` sigue CONGELADA (problema abierto
interno, rama B-β sobre la familia real). `clasificacion_rutas` tiene su paso
1 hecho (`itinerarios.py`) y espera el etiquetado por datos finitos.

---

## EL ZOOLÓGICO — la tabla de teoremas, lemas y hallazgos con nombre
*(bautizo completado el 04-08-2026: los 20 nombres de la manada asignados;
Pandas, los 3 Chanchitos y Komodo 3 quedan como nombres históricos.
Regla vigente: para textos que salgan del repo, numeración seria con el
descriptivo entre paréntesis.)*

| nombre | tipo | qué dice, en una línea | estatus | fichero |
|---|---|---|---|---|
| **PERRAS** | teorema | `\|M\|=2 ⟺ stems de Garner`, y el conteo exacto `2^{m−1}` con el borde resuelto | teorema; novedad verificada (Garner/E–T/LaTourette) | `teoremadeperras.txt`, `nuevasfusion.py` C15, `perrasconteo.lean` |
| **GATAS** | teorema | contracción literal + reinicio uniforme + ecuación de renovación `f = 1/4 + f/4 + g/4 + h/4` | teorema; (a) en Lean | `teoremadegatas.txt`, `contracciondegatas.lean` |
| **JIRAFAS** | lema-caracterización | fusión S-balanceada ⟺ evento de clase (ida + recíproco) | demostrado; C1 retirado | `teoremadejirafas.txt`, `zoologico.lean` |
| **PANDAS** | lema condicional | igual altura ⟹ fusión al mismo índice (`Res < 3`); corolario `φ = d` (el puente a Gao) | condicional; incond. `< 2^71` | `lemadepandas.txt`, `zoologico.lean` |
| **3 CHANCHITOS** | teoremas | `b₄ = 7·2^{m−7}−m+4`, `c₄ = 6·2^{m−7}−m+4` (grafo `{−3,−5}` + puertas + torre + gasto) | teoremas ∀m | `teoremadelos3chanchitos.txt` |
| **KOMODO 3** | teorema en Lean | tras el paso 0 el mayor es `≡ 2 (mod 3)` y «no múltiplo de 3» es invariante para siempre | demostrado, 0 sorry | `teoremadekomodo3.lean` |
| **LEONAS** | teorema-marco | LA CADENA `(k,c)`: seis leyes exactas con moneda de Terras (la paridad DEL ANCLA — 6ª revisión); el zoológico entero son sus estados. **Cualificador de la 6ª**: es la dinámica DE CLASES (ahí `a(k)` exacto y la única absorción es el vórtice); a nivel de instancias existen además las coalescencias del ciclo terminal (`{1,4}→2`, 28% del censo) que NO son fusiones de clase ni tocan φ | demostrado (leyes en Lean, `p` impar arbitrario); **pasó la 6ª revisión: cálculo intacto (12,5 M de pasos contra pares reales, 0 fallos), dos frases corregidas** | `paseodeladeuda.py`, `cadenakc.lean`, `rondadeltronco.py` |
| **TIGRESAS** | teorema | el multiplicador: cada paso del núcleo es moneda justa `×1/2 / ×3/2` — `E[m]=1` exacto: perpetuidad de Kesten CRÍTICA (κ=1) | demostrado (lectura φ=1: heurística declarada) | `subrenovacionc.py` |
| **CABRAS** | teorema | las puertas mod 3: directa → clase 2, vuelco → clase 1, nunca 0; **la puerta que funde es la del vuelco**. Y por la cadena entera: todo alcanzado con `k ≥ 1` tiene `c % 3 ≠ 0` — la torre no fabrica múltiplos de 3; corolario `torre_sin_ceros` (`(k,0)` inalcanzable) | demostrado; **formalizada en Lean (el 16º)** — el regalo de la 5ª revisión resultó ser esta puerta | `subrenovacionc.py`, `cabras.lean` |
| **ZORRAS** | teorema condicional | la inversión: `λ < 2 ⟹ φ = 1` — el autovalor no puede separar (`b(t+2) ≥ N_t(1,2)` exacto; piso `s_t` medido) | mecanismo exacto + piso medido | `retornoslambda.py` |
| **LOBAS** | lema | la libertad de la torre: única absorción `(1,1)`-bit1; ningún truncado finito demuestra `λ < 2` | demostrado (test exacto) | `matriztransferencia.py` |
| **PUMAS** | cotas | el acorralado de λ: **`λ ≥ 1.9844`** por OCHO truncados anidados (conteo entero; el 8º: `K=15, \|c\| ≤ 196608`, 1,3M estados, 09-08 (13)), gaps ×0.51→×0.81 por escalón subiendo hacia 1 — el gap se resiste cada vez más: consistente con λ = 2 | demostrado (cotas) | `matriztransferencia.py`, `retornoslambda.py`, `pumasescalera.py` |
| **ARDILLAS** | identidad | los flecos de R: `c(m) = Σ F(j)·a(m−j) + D(m)` exacta en 26 niveles — el término directo `D` era los flecos | verificado entero | `flecosr.py` |
| **NUTRIAS** | identidad | los canales: `e_s(N) = e_{s−2}(N−2) + e^h_s(N−2) + e^par_s(N−1)` — los subárboles de los dos primeros bits. **Refinada (09-08 (11))**: `e^h₈ = (4N²−76N+384−2·[N≡2 mod 3])/3` exacta; la escalera de formas termina en `e₆` (C4) y el ingrediente combinatorio de `e₈` entra TODO por el canal par (C5) | verificado entero (`s ≤ 12`, `N ≤ 29`); e₈/e₁₀/e₁₂ fuera de OEIS | `estratoscadena.py`, `sucesiones.txt` |
| **OVEJAS** | serie + cruce | los primeros retornos al corral: blocks/strings de LaTourette 2007 = retornos por orden/vuelco; su Tabla 4.2 tiene UN error; catálogo extendido a largo 30 | verificado (fe de erratas triple) | `retornoslambda.py` |
| **VACAS** | teorema verificado | la identidad entera `a(k+2) = a(k) + (2^k−1) + G(k) + H(k)` — la que alimenta todo | verificado `k = 3..14` + `k = 31, 32` | `identidadexacta.py`, `segundocamino.py` |
| **RATAS** | leyes + heurística | el paseo de la deuda por la torre: ±1 con monedas de Terras entre las torres gemelas; recurrente ⟺ Gao–Wu | leyes exactas (pisos 2–3 en Lean); recurrencia heurística | `torredeladeuda.lean` |
| **YEGUAS** | teorema | la unicidad alternante: exactamente una clase `\|M\|=2` por nivel, trotando `2^{k−1}−2 / 3·2^{k−1}−2`; y la ruta impar de `\|M\|=4` | demostrado | `nuevasfusion.py` C7/C9 |
| **CONEJAS** | teorema | la familia extremal del repunit: `(2^j−2, 2^j−1)` funde en `j+2` ⟹ `b(j+2) ≥ 1` — **las nuevas nunca se acaban** | demostrado | `nuevasfusion.py` C5 |
| **COMADREJAS** | herramienta | las coordenadas `D = g−2s−1` (vórtice ⟺ `D=0`, `s` impar; `D<0` absorbente) y `E = D−3s` (autónoma) | demostrado | `nuevasfusion.py` C10/C11 |
| **PANTERAS** | recursión | la diagonal vertical del triángulo: `e_s(N)\|_{r≡1} = e_{s−2}(N−2)` — la contracción trepando estratos | demostrado (motor en Lean) | `recursionvertical.lean` |
| **CIERVAS** | ecuación | una clase se estrena ⟺ primer encuentro en un vórtice (`a = 3b+1`, `S` compensada) — la ecuación fundacional de las nuevas | caracterización medida (`k ≤ 15`, 0 fallos) | `nuevasfusion.py` C2/C3 |
| **OSAS** | sistema | el sistema cerrado de φ: `φ = 8(1+ε)/(23−13ρ)`; `φ = 1 ⟺ ε_torre = 1/4 ⟺` el paseo recurrente | medido (ecuación 1 demostrada; 2 y 3 verificadas) | `auditoria_rigor.py` #86–88 |
| **ARAÑAS** | teorema | la sombra: en `u = c/3^k` las leyes colapsan al IFS `{u/2, (3u−1)/2}` con perturbación exacta `≤ 3^{−k}/2 ≤ 1/6` — Goldie–Kesten aplica al IFS puro. **Etiquetas de la 6ª**: la perturbación es ACOTADA con esperanza por paso < 1/10, **NO sumable en trayectoria** (Golondrinas ⟹ `δ = 1/6` i.o.), y en el fondo llega a la mitad del piso de `\|u\|` — la transferencia IFS→cadena sigue PENDIENTE, como el propio fichero declara | demostrado (354.293 identidades exactas, intactas); dos adjetivos corregidos por la 6ª | `aranas.py`, `actarevision0908c.txt` |
| **MOSCAS** | teorema | la tensión transferida: `S_t(θ) ≤ B_θ` uniforme en `t` (Lyapunov con `r_θ < 1` para todo `θ < 1`) — la masa viva con `\|u\| > x` es `≤ B_θ/x^θ` siempre; las moscas no escapan de la telaraña. **Extensión de la 6ª: vale VERBATIM en la cadena MODIFICADA** (el rebote 2/3 cumple la dominación y `(2/3)^θ ≤ r_θ` — la ventana de Lyapunov lo absorbe) | demostrado (dominación exacta + subaditividad, autocontenido); **salió REFORZADA de la 6ª** | `moscas.py`, `notamoscas.txt`, `rondadeltronco.py` |
| **HORMIGAS** | teorema | la accesibilidad: desde TODO estado `(k, c)` hay una palabra finita que fusiona — política explícita, terminación demostrada (redemostrada por la 4ª revisión), largo `O(k + log₂\|c\|)` — siempre hay camino a casa. *(4ª revisión: la constante 2,5 era muestra; sup exhaustivo ~2,73, demostrable candidata ~4,8 — constante fina ABIERTA)* | demostrado + exhaustivo rejilla + aleatorios a 10^30 | `accesibilidad.py` |
| **ABEJAS** | lema | el lema de bloques: la ocupación de toda rejilla finita sumada por bloques es `≤ 2^{T_G}` — **INCONDICIONAL (es Kraft)**. *(4ª revisión: el contrapositivo «`M_G` no sumable ⟹ φ=1» era VACUO — `M_G` es sumable siempre; el blanco no-vacuo es `M_G/L` o la cadena modificada = el criterio de retorno)* | demostrado (más fuerte de lo anunciado; lectura corregida) | `minorizacion.py`, `actarevision0908.txt` |
| **PALOMAS** | identidad | `b(t) = N_t(1,1)` EXACTO: las clases nuevas del nivel `t+1` SON las palabras en el pre-vórtice al nivel `t` — las nuevas vuelven del pre-vórtice, mensajeras; afila a Zorras y da `p_t = b(t)/m_{k1}` | exacto (t = 3..15 vs publicada) | `minorizacion.py` C0, `pisoporvisita.py` |
| **ÁGUILAS** | teorema (rapaz) | `E[m] = (1+q)/4` para la familia `(qx+r)/2`: la criticidad κ=1 de Tigresas CARACTERIZA a `q = 3`; para `q ≥ 5`, `E[log m] > 0` y Jensen cierra la ventana de Moscas — corta la familia entera en el 3 | exacto, una línea; densidades de `5x+1`/`7x+1` medidas por primera vez | `cadenaqnr.py` |
| **LECHUZAS** | teorema (rapaz) | si `3 \| r`, los consecutivos NO funden JAMÁS bajo `(qx+r)/2`: la fusión exige `c ≡ 0 (mod 3)` y las seis leyes sólo multiplican `c` por unidades mod 3 — ve en la oscuridad que no hay nada | demostrado (una línea) + barrido `a(k) = 0` clavado k ≤ 22 | `cadenaqnr.py` C4 |
| **HALCONAS** | corolario (rapaz) | la masa viva ABSOLUTA de toda banda finita `k ≤ K` tiende a 0 — **incondicional** *(4ª revisión: no discrimina φ; la versión que discriminaría es sobre masa condicionada a vivo)* | demostrado (lectura corregida) | `minorizacion.py`, `actarevision0908.txt` |
| **GOLONDRINAS** | teorema | en la CADENA MODIFICADA (vórtice rebotado; `φ = 1 ⟺ (1,1)` recurrente), la masa visita el fondo `k ≤ 1` INFINITAS veces c.s.: `k` es martingala exacta con empuje sólo en el borde (tabla de derivas, 28.436 estados), L2 (infinitos mixtos) sale del descenso determinista de `v₂` con `A = v₂(3^k−1)`, y la oscilación de martingalas fuerza `A → ∞` — siempre vuelven | demostrado (L2 con 60.010 instancias exactas + frontera determinista); queda el empalme por visita | `lamperti.py`, `oscilacion.py` |
| **LIEBRES** | teorema | basta con volver a la madriguera: `φ = 1 ⟺ Σ_t P(X_t ∈ C) = ∞` para TODA ventana finita `C` con `(1,1)` dentro — Green + clase recurrente cerrada + Doeblin EXACTO sobre conjunto finito (`ε ≥ 17887/131072`; para `C` arbitrario, accesibilidad = HORMIGAS cualitativo) | demostrado; **AGUANTÓ la 5ª revisión externa** (Doeblin reproducido, aperiodicidad gcd = 1; correcciones: cita de Hormigas, lectura del alfa degradada — la ventana grande no muerde a PROF 30) | `liebres.py`, `actarevision0908b.txt` |
| **CEBRAS** | lema | el sesgo se lee en las rayas: clasificación afín exacta (`u' = rama + δ`, `\|δ\| ≤ 3^{−k}/2`, rama expansiva clasificada, frontera incluida) y el umbral `q1 < log 2/log 3` como EXPONENTE DE LYAPUNOV de los multiplicadores (hipótesis de Kesten de Arañas) | **PARTIDA por la 5ª revisión**: la clasificación y el umbral-Lyapunov aguantan (100.398 transiciones independientes); la lectura «deriva de `log\|u\|` de la cadena» ROTA y RETIRADA (deriva real del fondo +0,02; `\|u\| ≥ 1/3` allí) | `liebres.py`, `actarevision0908b.txt` |
| **URRACAS** | teorema | la contabilidad del sesgo: `exp − contr = 2V + (Ee−E0) + k0 − k_t` EXACTO por palabra (libro mayor de nueve tipos); corolario: `⟺` en la sombra IFS con umbral 0,26186, umbral EFECTIVO ~0,2446 en la cadena (error del modelo medido); sin condicionar `Σ(Ee−E0) = 0` — el h-transform aislado en UNA moneda condicionada | demostrado (Lean 0 sorry); **AGUANTÓ ENTERA la 5ª revisión** (tabla rederivada, 200.000 palabras, Lean cotejado a máquina, circularidad rota con 59.990 pares reales) | `urracas.py`, `urracas.lean`, `actarevision0908b.txt` |

## Dónde está cada cosa

| pieza | fichero |
|---|---|
| Perras, Gatas y las 16 comprobaciones | `nuevasfusion.py` |
| itinerarios (paso 1 de clasificación) | `itinerarios.py` |
| el mapa de dependencias y su regla | `guardarafirmaciones.py` → `afirmaciones.db` (tablas `nodos`, `dependencias`) |
| el registro por sesión | `bitacora.md` (03-08-2026, cinco bloques) |
| la palanca CST (rama aparte, congelada esta semana) | `atacacst.py/.lean`, `paradacoef.py` |
