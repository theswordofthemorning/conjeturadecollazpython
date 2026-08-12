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

# ⇢ EL ESTADO Y LOS PRÓXIMOS PASOS (actualizado 12-08-2026, post-10ª)

**EMPEZAR POR AQUÍ.** Todo lo de abajo es historia; esto es el frente.

> **⇢ 12-08 (3) — EL COFRE ABIERTO: EL ENUNCIADO DEL PENDIENTE Nº 1,
> REFUTADO, Y EL COFRE MOVIDO DE SITIO** (`correlacionafin.py`, el
> 90º; nota autocontenida `notacorrelacionafin.txt`;
> `notaequidistribucion.txt` 3-bis.ix). El pendiente que dejó la
> sesión anterior era «un solo funcional concreto»:
> `Σ p(r)·p(τ(r)) ≤ γ·C2(p)` con `γ < 1` para τ afín impar.
> **Atacado por capa 1 —buscar el contraejemplo antes de demostrar—
> y el contraejemplo EXISTE:**
> 1. **El τ, identificado en enteros**: con el padre par `c = 2u`,
>    las corrientes compartidas son `N0: u ↦ u` y `N1: u ↦ 3u + s_k`
>    con `s_k = (1−3^k)/2` — y `s_k` es impar ⟺ `k` impar: **la
>    geografía del cofre ES la de TÓRTOLAS**.
> 2. **La identidad que lo parte en dos** (teorema, racionales):
>    `Σ p·p∘τ = C2(p) − ½Σ(p(r)−p(τr))²` para toda biyección ⟹
>    **`γ ≤ 1` es GRATIS** (no era el teorema) e igualdad ⟺ `p`
>    constante en cada ciclo de τ.
> 3. **EL CONTRAEJEMPLO** (teorema, racionales exactos): para `k`
>    impar τ tiene exactamente **dos ciclos de largo `2^{m−1}`**
>    (enumerado m = 4…10), así que `p = (1 + ε·χ)/2^m` con χ = ±1 por
>    ciclo es probabilidad legítima, tiene exceso `ε²` **tan chico
>    como se quiera** y da **`γ_centrado = 1` EXACTO**. El enunciado
>    universal es **FALSO — por igualdad, y en el régimen donde vive
>    la cadena** (`e ~ 0,04`). Y no hay gap que lo rescate: ortogonal
>    al obstructor, el siguiente autovalor es `1 − O(4^{−m})`.
> 4. **LA SORPRESA, MEDIDA CON CRUCE**: el γ que la órbita realiza es
>    **negativo en todo `k' ≥ 3`** (hasta −0,33) y sólo `+0,10…+0,19`
>    en `k' = 2`. **El par que la nota señalaba (N0-N1) es el par
>    BUENO**; lo que carga el exceso son los pares que **cruzan
>    fibra** (peor **A-N1 = 0,905**; el `D-N0 = 0,507` fue el «~0,5»
>    mal atribuido — número medido de un objeto, escrito de otro:
>    el modo de fallo del ANDAMIO). Cruce con `SystemExit`: Rayleigh
>    centrado del padre = `E_N0N1/E_N0N0` de `corrienteszocalo` a 12
>    cifras en las 12 celdas.
> 5. **EL MECANISMO**: como `w_N0 = w_N1` siempre, con sólo las dos
>    compartidas sería `e_hija(m) = (1+γ)/2 · e_padre(m+1)` exacto —
>    **el umbral 1/2 del telescopio equivale a `γ < 0`**, que es
>    justo lo que la cadena da en `k' ≥ 3`. El resto es `k' = 2`, la
>    fibra sin corriente A: la frontera de absorción otra vez.
> 6. **EL ENUNCIADO REPARADO**: no es sobre un τ, es sobre la
>    **mezcla** — `‖Σ_i w_i P_i‖ < 1` en media cero, cuya única
>    obstrucción es el **invariante COMÚN** de las corrientes,
>    **medido trivial** (una sola clase, m = 4, 6, 8). La forma del
>    teorema es de **EXPANSIÓN** (norma de un promedio de
>    permutaciones afines de `Z/2^m`), no de correlación de dos
>    mapas.
> 7. **LA ANATOMÍA DEL PAR MALO** (teorema, enteros):
>    `A(c) − N1(c−1) = (3+3^k)/2` **constante** — bajo la
>    identificación `c' = c−1`, A y N1 difieren por una **traslación
>    pura**, no por un afín con multiplicador 3. **El par bueno
>    MEZCLA; el par malo sólo DESPLAZA** — ésa es la razón mecánica de
>    quién carga el exceso.
> 8. **EL NEGATIVO**: el par malo **no decae, CRECE** (0,395 → 0,905
>    en `k'=3`, t = 12…24) mientras `ρ_ms` **baja** (0,42 → 0,33). La
>    contracción es un **balance con pesos**: la contabilidad exacta
>    (`ρ_ms = Σ_ij w_i w_j E_ij/E00`, cierre con `SystemExit`) reparte
>    **propias 0,23–0,30** (el branching hace casi todo), **N0-N1
>    negativo**, y el par malo sólo `+0,05…+0,09` porque pesa 0,04.
> 9. **⇢ LA RESTRICCIÓN QUE MÁS IMPORTA PARA LA PRÓXIMA SESIÓN**
>    (medida, no razonada): la cota **Cauchy-Schwarz cruda**
>    `(Σ_i w_i√E_ii)²/E00` vale **0,74 / 0,90 / 1,00 / 1,10** en
>    `k' = 2/3/4/5` — **supera 1**: ni siquiera demuestra contracción.
>    ⇒ **toda demostración del teorema de conteo que acote las
>    cruzadas en VALOR ABSOLUTO está condenada**, por buena que sea la
>    cota. El teorema tiene que usar los **signos**, y el enunciado
>    útil no es `|E_01| ≤ γE00` con `γ<1` —insuficiente aunque fuera
>    cierto— sino **`E_N0N1 ≤ 0` sobre la órbita**. *Ahí está el cofre
>    nuevo.* *Bautizo pendiente (user-gated).*
>
> **⇢ 12-08 (2) — LA 10ª REVISIÓN ADVERSARIAL, HECHA Y APLICADA**
> (acta `actarevision1208.txt`; informes `_adv1/2/3.txt`): **la
> estructura de la tanda del 12-08 AGUANTÓ ENTERA** (enteros
> idénticos en la reproducción independiente; Lean↔objeto 0 fallos
> en 40.034 casos; el doble conteo IMPOSIBLE — biyección verificada
> + obstrucción mod 8 nueva; el bump del escalón 10 no puede
> falsear; sin cruces de 1/2 en ~500 celdas × 5 arranques). Mordió
> la letra: el compuesto de recargas estaba ROTO desde siempre y su
> reemplazo es MEJOR (la **unión por palabras**: razón 2^{−1/2}
> exacta directa de L2), P2-b reescrito con FORZADO vs realizado,
> la razón media, el 1,042, el filtro declarado, el margen honesto
> **4%** (peor 0,480 en m=10). **EL PENDIENTE Nº 1 SIGUE SIENDO EL
> TEOREMA DE CONTEO** (ρ_ms < 1/2 sobre la órbita del DP), ahora
> con dos sub-lemas nombrados: (a) la unión por palabras — **YA
> FORMALIZADA la misma tarde** (`unionpalabras.lean`, el 21º:
> `corre_comparte` por inducción sobre la palabra +
> `una_clase_palabra_bit0/bit1`, con q libre por paso; 0 `sorryAx`;
> cruce `union_cruce.py`: 1.260 combinaciones, EXACTAMENTE una
> clase en todas — unicidad teorema, existencia medida; bautizo
> pendiente) — y (b) el wedge escala-tiempo — **TAMBIÉN ESCRITO la
> misma tarde** (`notaensamblajep2.txt` P2-a: el lema de racha
> honesto con sus dos regímenes, L2 en el bulk y quenched en el
> prefijo).
> Deuda de documentación **PAGADA**: las seis leyes en la subsección
> nueva de este documento; la serie de cajas en `pinzacw.py`
> (regalo: `C_s = 3·4^s` unifica los diez escalones).
>
> **⇢ Y EL FUNCIONAL DEFINITIVO DEL CONTEO, FIJADO Y MEDIDO**
> (`conteoconjunto.py`, la misma tarde): el exceso conjunto ABSOLUTO
> queda **descartado con negativo registrado** (no contrae bajo 1/2:
> carga la difusión de k), y el blanco definitivo es el **exceso
> CONDICIONAL** `e_cond = Σ_k P(k)·(C2_k − 1)` — domina a la
> marginal por Cauchy-Schwarz (el puente, demostrable en una línea),
> es inmune al contraejemplo naif de 3-bis.vi, y **contrae bajo 1/2
> en toda la ventana medida** (peor 0,460, margen 8%, ventana
> declarada). EL ENUNCIADO A DEMOSTRAR: `ρ_cond < 1/2` para la
> transición del DP sobre su órbita — `notaequidistribucion.txt`
> 3-bis.vii. Los siguientes pasos naturales: (1) el puente C-S a
> Lean (o declarar por qué no se puede sin Mathlib), (2) el zócalo
> k ≤ 4 (donde vive el ~80% del exceso: la contabilidad fina de los
> ocho mapas τ en alturas bajas), (3) la 11ª revisión cuando la
> tanda post-10ª tenga masa.

> **⇢ 11-08 (2) — LA SUB-TEORÍA DE LURRUS** *(bautizada por el
> usuario en sesión — «no basta con los números, tiene que tener
> estilo»; los nombres de animal para los teoremas individuales
> quedan para mañana, P7)*: el cuerpo nuevo de la sesión — la
> reversión temporal en la absorción, el h-transform explícito
> `h(k) = k−1`, la mediana universal como objeto, el teorema V2/L3,
> y el mapa honesto del trasvase a la cadena real (las dos
> equidistribuciones + δ + condicionada) — con sus tres
> verificaciones exactas y su acta (la 9ª). Es la hermana de LA
> SUB-TEORÍA DE LA MADRIGUERA (09-08): aquélla dio el criterio de
> recurrencia; LURRUS da el piso por excursión.
>
> **EL SALTO DE LA SESIÓN (bitácora manda, resumen
> aquí): L3 QUEDÓ TEOREMA módulo UN lema clásico citado.** AGKV
> 2005 leído entero (`fichaagkv.txt`); el mecanismo es la REVERSIÓN
> temporal en la absorción con `h(k) = k−1` explícita; las piezas
> (ii) [serie revertida], (i) [lema D de comparación, sup medido
> 2,823 vs 2^{3/2} = 2,8284 teórico] y (iii) [el trasvase] están
> escritas con todas las letras en `teoremav2.txt` — lo único
> citado es el LLT del paseo perezoso absorbido (clásico,
> Vatutin–Wachtel 2009). **⟹ el TEOREMA V2 (φ_V2 ≥ c/√log x, la
> forma de L-A en el modelo autónomo) está completo módulo ese
> lema y la revisión externa.** La mediana universal medida
> (`medianauniversal.py`): 17,50 (V2a) / 17,60 (V2b — casi
> invariante al reloj: la pata de P2). Récords del día: `φ ≥
> 0,462781` (renovación sin cap, `recordsincap.py`) y `λ ≥
> 1,989042` CERTIFICADO (escalón 10, `certificadocw.py`).
>
> **LA RUTA PARA MAÑANA, EN ORDEN (post-9ª REVISIÓN — el acta
> `actarevision1108c.txt` manda; la 9ª ya está HECHA y aplicada:
> V2/L3 y los récords AGUANTARON, lo escrito mordió y está
> reparado):**
> 1. ~~**LAS DOS EQUIDISTRIBUCIONES DE P2**~~ ⇢ **UNIFICADAS Y
>    MEDIDAS EXACTAS (12-08)**: la reducción es TEOREMA
>    (`lecturaracha.lean`, el 20º — racha ≥ j Y salto de recarga
>    ≥ s son cada uno UNA clase de c mod 2^m; unicidad por
>    `tres_inyectivo`), y la equidistribución está medida EXACTA
>    con conteos enteros + cruce independiente
>    (`equidistribucionmixto.py`: C_j ≤ 2,95 → ~1, adaptada al
>    k-camino ≤ 1,000, contraejemplos del adv 1 reproducidos y
>    muertos; `recargaexacta.py`: C_s ~ 1, la Geom(1/2) predicha).
>    **QUEDA UN SOLO TEOREMA DE CONTEO** — la ruta (inyección de
>    bits por Δ de Tórtolas: k impar inyecta un bit fresco exacto;
>    esquema telescópico autoconsistente) está en
>    `notaequidistribucion.txt` §3. Ése es ahora EL pendiente 1.
> 2. ~~**MEDIR la dominación condicionada a sobrevivir**~~ ⇢ **HECHO
>    (12-08, `dominacioncondicionada.py`)**: la dependencia del bit
>    de apertura era TRANSITORIA (el 7σ vivía en el tramo inicial
>    determinista de c₀; en rachas tardías z ≈ 0 y en el arranque B
>    el signo global se invierte) y la ley condicionada converge a
>    la geométrica NEUTRA: `C_j` condicionado ∈ [0,87, 1,06], C ~ 1.
>    La dominación condicionada AGUANTA — nota §5(iii) actualizada.
> 3. ~~**CARGAR los δ de Arañas en el ensamblaje P2**~~ ⇢ **ESCRITO
>    (12-08, `notaensamblajep2.txt` P2-c)**: dominados por 2^{−k_j}
>    en colas largas; el sufijo k = 2,3 corre W̃_∞ ≤ 5% y se absorbe
>    en la holgura M+1 de la ventana (cualificador declarado: la
>    densidad del límite cerca de M es medida, no demostrada).
> 4. ~~**El tramo inicial determinista quenched**~~ ⇢ **ESCRITO
>    (12-08, `notaensamblajep2.txt` P2-b)**: cota individual exacta
>    `racha ≤ 1 + log₂|c|` (v2 no supera el tamaño), presupuesto de
>    bits ≤ log₂|c_i| contra T = 20,8·log₂|c_i| — cabe con margen
>    ~20×; la contabilidad del gasto de bits es parte del MISMO
>    teorema de conteo del punto 1, no un hueco nuevo.
> 5. ~~**El paso Perron/SCC del puente espectral**~~ ⇢ **PAGADO PARA
>    LOS ESCALONES 1–9 (12-08, `pinzacw.py` — LANGOSTAS)**: en cada
>    caja hay UNA SCC no trivial y cero lazos sueltos ⟹ `ρ(M_T) =
>    ρ(S*)` con Perron aplicable, y la pinza CW min/max en enteros
>    da ancho ≤ 1e-5 hasta K = 17 — **y el ESCALÓN 10 CORRIDO la
>    misma tarde** (22,5M estados, |S*| = 20,2M, 892 s): `ρ(M_T) ∈
>    [1,989042, 1,989176]`, inferior = certificado. La letra chica
>    del récord, pagada ENTERA en el truncado.
> 6. ~~**L-B como teorema (P3)**~~ ⇢ **ESCRITO COMO TEOREMA
>    CONDICIONAL (12-08, `notalb.txt`)**: `τ_i ≤ i^{2+ε}` c.s.
>    condicional a la dominación (D) — reflexión (clásico) +
>    Chernoff adaptado sobre (D) + presupuesto quenched (`L_i =
>    log₂|c_i|`, β = 0 medido) + Borel–Cantelli. Supera el
>    `e^{o(i²)}` con margen infinito; coherente con η = 2,082
>    medido. Cualificadores declarados: (D) = el conteo pendiente,
>    constantes L2 por rehacer, β = 0 es medición.
> 7. **Bautizos** ⇢ la tanda del 12-08 BAUTIZADA por orden del
>    usuario (VÍBORAS, AVISPAS, EFÍMERAS, PIRAÑAS, TORTUGAS,
>    LANGOSTAS — ver el ZOOLÓGICO); **y la tanda restante BAUTIZADA
>    el 12-08 (2) por delegación del usuario** («tenemos un
>    diccionario... para que hagas los bautizos»; el diccionario de
>    22 del CLAUDE.md ya estaba agotado — nombres nuevos en el mismo
>    espíritu): **LORAS** (la unión por palabras, el 21º lean),
>    **BALLENAS** (el funcional condicional del conteo), **TRUCHAS**
>    (el teorema V2/L3 por reversión temporal), **GRULLAS** (la
>    mediana universal), **CIGARRAS** (la dominación del reloj
>    real). El certificado CW ya vive bajo PUMAS/LANGOSTAS. Sigue
>    user-gated P5 (ley del borde a Lean/trío). Y la **predicción falsable nueva** del adv 3 queda
>    registrada para vigilar: `a(k)/2^k` cruzaría 0,462781 hacia
>    k ≈ 45–50 (extrapolación declarada; sugiere φ ≈ 0,52).

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
exponencialmente — ésa sigue siendo la vía.

> **⇢ 10-08: el último paso ya tiene su instrumento —
> `monedacondicionada.py` (GARZAS, propuesto).** Forward-backward
> exacto: el sesgo condicionado al fondo vive en `k ≤ 3`, es
> `≤ ~0,03` por moneda y su TOTAL por trayectoria crece sólo
> ~0,003–0,004/paso (peor caso `a_D → ~0,004`: ×60 bajo el umbral);
> condicionado a `(1,1)` el balance es **negativo** (la obstrucción
> de CEBRAS no aparece); y el exponente local de `P(X_t=(1,1))` —
> la ventana de UN estado, la INDECIDIDA del acta — **cruzó 1 hacia
> abajo y baja monótono (0,76 a t=30): la dirección es la de la
> recurrencia.** Todo medido/orienta; validado contra `urracas.py`
> a 6 cifras y por fuerza bruta entera. El teorema que esto deja a
> tiro: el desbalance por moneda acotado a la vista es la mitad
> cuantitativa del `O(1/k)`; falta la cota a priori.
>
> **⇢ 10-08 (2): la cota a priori ya tiene su lema —
> `firmaacoplamiento.py` (TÓRTOLAS, propuesto).** Los dos hijos de
> toda moneda difieren en `Δ = c + (1−3^k)/2` y bajo la misma
> palabra `v₂(Δ)` baja exacto 1 por paso: divergen JUSTO en
> `j* = v₂(Δ)` (48.015 pruebas, 0 fallos; dos excepciones nombradas
> con masa 2·10⁻⁵). Corolario clavado al 99,85%: `j* ≥ horizonte ⟹
> sesgo EXACTAMENTE cero`. **El desbalance condicionado queda
> reducido a sensibilidad-al-timing de un paseo justo perezoso,
> desacoplado de `c`** — y la extensión de la serie del criterio a
> t=34 da `P_t·t` SUBIENDO (0,246→0,277): en la ventana medida
> `P(X_t=(1,1))` decae más lento que `1/t`, el lado de la
> divergencia de Green. Pendiente inmediato: el lema a Lean (el
> 19º) y la cota del timing. *(El 19º quedó cobrado la misma tarde:
> `tortolas.lean`, 20 teoremas, 0 `sorryAx` — queda la cota del
> timing como ÚNICO frente analítico.)*
>
> **⇢ 10-08 (4): GAVIOTAS — LA COTA MARTINGALA, y tras la
> corrección nº 50, LA SUMA ENTERA BAJO EL UMBRAL.** La cota
> (`gaviotas.py`): bits justos dado el pasado + Doob +
> Cauchy–Schwarz — **la endogeneidad del horario desaparece del
> argumento**. La corrección 50 (cazada por Opus 5): el umbral
> 0,2446 es de LA SUMA `a_V + a_D − a_K`, no de `a_D` solo; la
> reparación salió más fuerte: el vórtice es moneda centrada (a_V
> absorbido en la martingala) y la frontera impar resta, y la cota
> fina certifica **la SUMA entera bajo 0,2446 en todos los T
> computados** (0,198→0,192 en T = 16…28; valor real 0,019).
> Ortogonalidad verificada como igualdad de racionales. Asintótico
> `O(T^{−1/4}) → 0` módulo UN lema local: `P(fondo en T) ≥ c/√T`
> (medido: `P·√T` = 1,27→1,38 a t=34 — forma Lamperti clásica; la
> ruta v₂ del reloj, con sus lemas de racha ya en `tortolas.lean`).
> **El programa queda así: el balance de Lyapunov condicionado está
> DEMOSTRADO bajo el umbral a todo T computado, y el cierre
> asintótico depende de un único lema local con forma clásica.**
>
> **⇢ 10-08 (5): el esqueleto clásico del lema local, con nombres.**
> La vía que NO es circular (la del piso por constructor lo era:
> `P(F_T) ≥ 2^{−w}·P(ventana en T−w)` sólo TRANSFIERE el piso entre
> tiempos — queda como lema de suavizado): **(i) regeneración de
> Doeblin sobre el conjunto finito de LIEBRES** (ε ≥ 17887/131072,
> ya exacto) ⟹ ciclos de renovación i.i.d.; **(ii) cola del ciclo
> `P(τ > t) ≍ t^{−1/2}`** — el paseo crítico de `k` con el reloj de
> cola geométrica (los lemas de racha de `tortolas.lean`) — la única
> pieza por demostrar; **(iii) el teorema de renovación fuerte de
> Erickson** (renovaciones nulas-recurrentes con cola `t^{−1/2}`)
> ⟹ `P(X_t ∈ C) ≍ t^{−1/2}` — el lema local entero. Con eso,
> GAVIOTAS-B da `suma → 0` y **la hipótesis de Kesten de CEBRAS
> queda demostrada asintóticamente para las historias que vuelven**.
> ⇢ **Erickson FICHADO (10-08, `fichaerickson.txt`)**: α = 1/2
> exacto es el borde duro — Erickson sólo da `liminf`; el SRT en
> 1/2 pide la condición de Caravenna–Doney (T1.4 iff; T1.5 el
> atajo: basta `S(t)·√t → c` finito, y entonces `u(t) ~
> 1/(π·c·√t) ≈ 0,29/√t` con la `c ≈ 1,1` medida). El empalme:
> split de Athreya–Ney/Nummelin. Y la lectura que manda: **para
> φ=1 el SRT ni hace falta** — `Σ P(X_t ∈ C) = ∞ ⟺ recurrencia a
> secas; el SRT es el ritmo cuantitativo del paper. Todo cuelga de
> UNA pregunta: `P_{(2,2)}(τ_C < ∞) = 1`.
>
> **⇢ 10-08 (6) — EL CIERRE DE LA JORNADA: la pregunta única, con
> todas sus piezas medidas y su forma de lema.** (a) **La
> obstrucción Foster**: `V = k + f(u)` está estructuralmente
> obstruido (cuatro rejillas: el punto fijo `u* = −1`, la parada,
> el ratchet, el clamp suave — bitácora (9)); la vía es la
> transferencia de Arañas, no una Lyapunov monótona. (b) **La
> anatomía de la entrada**: todo ingreso al fondo pasa por `k=2`
> con selección expansiva ×1,5–2; la primera entrada NUNCA es el
> pre-vórtice (la absorción exige recircular — PALOMAS). (c) **La
> cuota de ventana en la entrada**: 0,94 → 0,54 (t ≤ 33, exacto)
> → 0,44 (t=55, poda acotada), con exponente local CAYENDO
> (0,50 → 0,40): el primer test dobla al lado recurrente. (d) **LA
> MEZCLA, verificada**: tres arranques con `u` distinta convergen
> a < 0,03 en t=29 — las excursiones olvidan su `u` inicial. **La
> cadena del argumento que queda por demostrar: mezcla (medida) +
> cuota de exponente < ½ (medida) + Golondrinas (demostrado) ⟹
> recurrencia de la ventana ⟹ φ=1 (LIEBRES) — con GAVIOTAS-B ya
> certificando el balance de Lyapunov bajo el umbral en todo T
> computable.** Pendientes user-gated: bautizos (GARZAS, TÓRTOLAS,
> GAVIOTAS, y QUELTEHUES — bautizado por el usuario post-7ª: el
> lema de la mezcla, roto en su pieza 3 y salvado por la vía
> annealed — el queltehue corta con los espolones), la adversarial
> YA HECHA (7ª, `actarevision1008.txt`), LaTourette/Frinkle/Rozier.
>
> **⇢ 10-08 (7) — LA SÍNTESIS FINAL (bitácora (12), EMPEZAR POR
> AHÍ): el círculo se cierra sobre el piso por visita, MEDIDO EN
> `p* ≈ 0,76` en las coordenadas correctas** (por excursión desde
> `(2,2)`, a la ventana de Doeblin — que contiene el atractor
> entero; horquilla certificada [0,763, 0,960]; el viejo
> `p_34 = 0,0457` medía otro objeto). Cuotas de la banda tardía
> (t ∈ [23,30], h = 3…8): 0,79/0,75/0,62/0,52/0,39/0,26 *(7ª
> revisión: esta lista NO es `q(h)` global, que empieza 1,00/0,95;
> y en h ≤ 5 la cuota aún baja banda a banda — decelera, no
> estable)*.
>
> **⇢ TRAS LA 7ª REVISIÓN (acta: `actarevision1008.txt`), la
> cadena queda ASÍ — más fuerte en el esqueleto, más honesta en
> los lemas**: por **MARKOV FUERTE** (regalo de la ronda),
> `P(ventana en la excursión i | todo el pasado) = φ(c_i)` EXACTO —
> la mezcla NO hace falta para ese salto y Lévy–Borel–Cantelli es
> teorema. Quedan DOS lemas: **(L-A)** el piso poly-log
> `φ(c₀) ≥ c/(log c₀)^A` — pero la forma `1/√log` exacta quedó
> **EXCLUIDA** con cotas certificadas en 200–2000 (ratio ≤ 0,744
> vs 0,836) y el rango limpio ajusta potencia `γ ≈ 0,4` estable:
> **decidir si `γ(c₀) → 0` por décadas ES el punto donde el
> programa se decide** (γ baja ⟹ la reducción vive; se estabiliza
> ⟹ φ < 1 con techo); **(L-B)** el ritmo de visitas
> `τ_i ≤ e^{o(i²)}` c.s. — la unión con Moscas es válida, falta el
> ritmo (saldría del SRW de `k` + el reloj de rachas de
> `tortolas.lean`, cuyo régimen k-par es DETERMINISTA — 7ª).
> **QUELTEHUES** (ex-FOCAS, rebautizado por el usuario) pieza (3)
> ROTA (los bits compartidos son funciones del camino — TÓRTOLAS
> los delata); la vía annealed de Arañas es el espolón: el lema se
> salva como herramienta para L-A.
>
> **⇢ 10-08 (3): y el timing ya tiene su núcleo medido** —
> `κ(m) ~ 0,45/m` (la sensibilidad de γ a un salto impar de `c`,
> firma del laplaciano discreto; C4 de `firmaacoplamiento.py`).
> Composición cerrada por las dos puntas: total `≈ 0,08·log T`
> reproduce nivel y tasa de la serie de GARZAS ⟹ **`a_D ~ log T/T
> → 0`: el desbalance condicionado SE DESVANECE** (con `a_K ≤ 1/T`
> y `a_V` sublineal, el sesgo entero de URRACAS apunta a 0). **La
> única pieza analítica del programa queda enunciada así: demostrar
> `κ ≤ C/m` a priori** — suavidad del núcleo de un paseo justo
> perezoso, sin `c` de por medio. **Regalo de la revisión,
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

### LAS SEIS LEYES EXACTAS (referencia rápida; la fuente es `cadenakc.lean`)

El estado es un par vivo `{v, 3^k·v + c}` (`k ≥ 1`, núcleo; `c ∈ Z`,
puede ser negativo) o `{v, v + g}` (`k = 0`, frontera; gap `g ≥ 1`).
El bit de Terras es **la paridad del ancla `v`** (bit 0 ⟺ `v` par —
corrección de la 6ª: el ancla, no «el menor»), y la ley de la moneda
(`ley_moneda`) dice que el gap `(3^k−1)·v + c` tiene la paridad de `c`:
**paso mixto ⟺ `c` impar**. Cotejado rama a rama contra `transicion()`
de `rachasreales.py` / `pinzacw.py` / `certificadocw.py` (idénticas).

**Núcleo `k ≥ 1`, `c` PAR (paso compartido — la torre quieta):**

1. **N1** (bit 0): `(k, c) → (k, c/2)` — `ley_N1`; vale para TODO
   coeficiente `p` (la paridad de `p` no hace falta).
2. **N2** (bit 1): `(k, c) → (k, (3c + 1 − 3^k)/2)` — `ley_N2`; `p`
   impar arbitrario.

**Núcleo `k ≥ 1`, `c` IMPAR (paso mixto — la torre se mueve):**

3. **N3** (bit 0): `(k, c) → (k+1, (3c+1)/2)` — ASCIENDE, deuda `+1`
   (`ley_N3`; el mayor gana el impar).
4. **N4** (bit 1, `k ≥ 2`): `(k, c) → (k−1, (c − 3^{k−1})/2)` —
   COMPENSA, deuda `−1` (`ley_N4`; el menor gana el impar).
5. **N4 EN EL PISO (`k = 1`, bit 1) — EL ABS que a la 10ª le faltó**:
   `g' = (c−1)/2`, y hay dos salidas:
   - `g' = 0` (⟺ `c = 1`): **FUSIÓN** — el vórtice `(1,1)`-bit 1, la
     única absorción de la cadena (`vortice_fusion`);
   - `g' ≠ 0`: `(1, c) → (0, |g'|)` — **el valor absoluto es
     obligatorio**: la frontera `{v, v+g}` es un par SIN orden y con
     `c < 1` el gap sale negativo; se guarda `|g'|`.
6. **F4 (frontera `k = 0`, `g` impar, bit 1) — EL VUELCO, el otro que
   faltaba**: `(0, g) → (1, (1−3g)/2)` — `ley_F4`: el que era menor
   pasa a ser el ancla y el par reentra al núcleo con
   `c' = (1−3g)/2 < 0` (torre negativa).

**El resto de la frontera NO son leyes nuevas**: son las leyes 1–3 con
coeficiente `p = 3^0 = 1` — **F1** (bit 0, `g` par): `(0,g) → (0, g/2)`
es N1; **F2** (bit 1, `g` par): `(0,g) → (0, 3g/2)` es N2 con `3^k = 1`;
**F3** (bit 0, `g` impar): `(0,g) → (1, (3g+1)/2)` es N3 (reentra al
núcleo). Por eso `cadenakc.lean` demuestra N1–N3 con `p` impar GENERAL
y sus seis teoremas de transición son exactamente los seis de arriba:
`ley_N1`, `ley_N2`, `ley_N3`, `ley_N4`, `vortice_fusion` y `ley_F4`
(0 `sorryAx`).

*(Subsección añadida el 12-08-2026 pagando la deuda de documentación de
la 10ª — `actarevision1208.txt` III.)*

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
  espacios finitos), SIN Collatz ni nuestra forma: ⇢ **LEÍDO Y FICHADO
  (10-08, `fichagrimmettholmes.txt`)** — cero solapamiento (no citan
  Collatz ni Garner/Gao/E–T); todo espacio finito, sin herramienta
  directa para el piso; importables: la cita canónica Doeblin 1938
  para Liebres, el test de bloques (T4.3/4.4) y la obstrucción del
  período (T3.13b) como plantilla para `c mod 3`; y **ccchallenge.org**
  (formalización Lean de la literatura Collatz, paper a paper) —
  referencia útil para la línea Lean del repo. *«No encontrado» sigue
  sin ser «no existe», pero ya se buscó.*
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
| **PUMAS** | cotas | el acorralado de λ: **`λ ≥ 1.989042` CERTIFICADO** por DIEZ truncados anidados con certificado Collatz–Wielandt en enteros exactos (el 10º: `K=19, \|c\| ≤ 3145728`, 22,5M estados, 11-08 (2)), gaps ×0.51→×0.846 por escalón subiendo hacia 1 — el gap se resiste cada vez más: consistente con λ = 2 | demostrado (cotas certificadas) | `matriztransferencia.py`, `retornoslambda.py`, `pumasescalera.py`, `certificadocw.py` |
| **ARDILLAS** | identidad | los flecos de R: `c(m) = Σ F(j)·a(m−j) + D(m)` exacta en 26 niveles — el término directo `D` era los flecos | verificado entero | `flecosr.py` |
| **NUTRIAS** | identidad | los canales: `e_s(N) = e_{s−2}(N−2) + e^h_s(N−2) + e^par_s(N−1)` — los subárboles de los dos primeros bits. **Refinada (09-08 (11))**: `e^h₈ = (4N²−76N+384−2·[N≡2 mod 3])/3` exacta; la escalera de formas termina en `e₆` (C4) y el ingrediente combinatorio de `e₈` entra TODO por el canal par (C5) | verificado entero (`s ≤ 12`, `N ≤ 29`); e₈/e₁₀/e₁₂ fuera de OEIS | `estratoscadena.py`, `sucesiones.txt` |
| **OVEJAS** | serie + cruce | los primeros retornos al corral: blocks/strings de LaTourette 2007 = retornos por orden/vuelco; su Tabla 4.2 tiene UN error; catálogo extendido a largo 30 | verificado (fe de erratas triple) | `retornoslambda.py` |
| **VACAS** | teorema verificado | la identidad entera `a(k+2) = a(k) + (2^k−1) + G(k) + H(k)` — la que alimenta todo | verificado `k = 3..14` + `k = 31, 32` | `identidadexacta.py`, `segundocamino.py` |
| **RATAS** | leyes + heurística | el paseo de la deuda por la torre: ±1 con monedas de Terras entre las torres gemelas; recurrente ⟺ Gao–Wu | leyes exactas (pisos 2–3 en Lean); recurrencia heurística | `torredeladeuda.lean` |
| **YEGUAS** | teorema | la unicidad alternante: exactamente una clase `\|M\|=2` por nivel, trotando `2^{k−1}−2 / 3·2^{k−1}−2`; y la ruta impar de `\|M\|=4` | demostrado | `nuevasfusion.py` C7/C9 |
| **CONEJAS** | teorema | la familia extremal del repunit: `(2^j−2, 2^j−1)` funde en `j+2` ⟹ `b(j+2) ≥ 1` — **las nuevas nunca se acaban** | demostrado; **formalizada en Lean (el 18º, 10-08 madrugada)** — la fusión en `j+2` exacto con el testigo `3^{j−1} = 4t+3` y `separados_antes`; la «primera vez» sigue en el barrido | `nuevasfusion.py` C5, `conejas.lean` |
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
| **VÍBORAS** | teorema | la lectura: racha ≥ j y salto de recarga ≥ s LEEN los bits bajos de c — cada evento es UNA clase mod 2^m (unicidad por `tres_inyectivo`, ×3 inyectivo mod 2^n); las «dos equidistribuciones» de la 9ª son UN objeto (bit 1: k ≥ 3 en la prosa; la cadena aplica desde k = 2 y el DP absorbe ahí — cuantificador precisado por la 10ª) | demostrado (Lean, el 20º, 0 sorry); instancia adversarial `3·1398101+1 = 2^22` por kernel | `lecturaracha.lean`, `equidistribucionmixto.py`, `recargaexacta.py` |
| **AVISPAS** | teorema | el aguijón: en el paso compartido con `k` IMPAR la mitad `m` de `3^k = 2m+1` es impar y los dos hijos difieren mod 2 — el bit de la palabra se INYECTA como bit fresco en la posición 0; `k` par no inyecta (`v2(Δ) = 1 + v2(a − m/2)`) | demostrado (Lean, misma pieza; `pot3_mod4` con testigo) | `lecturaracha.lean` |
| **EFÍMERAS** | hallazgo medido | viven un día: la dependencia del bit de apertura (el «7σ» del adv 1) es TRANSITORIA — en rachas tardías se anula (z ≈ 0, ambos arranques) y el signo global se invierte en B; la ley condicionada a sobrevivir converge a la geométrica NEUTRA (C ~ 1) | medido (dos arranques, ventana emparejada); cierra el §5(iii) de la nota de dominación | `dominacioncondicionada.py` |
| **PIRAÑAS** | medición + reformulación | se comen el exceso: `e_t = C²(t) − 1` se contrae con razón MEDIA ~0,7 (t = 8…26), uniforme en arranques (adversarial incluido); la serie a escala fija NO es monótona paso a paso (picos >1: A t=22→23 ×1,38) — contracción de TENDENCIA; el objeto monótono es la razón multi-escala (X4) — la ganancia estricta que el telescopio crítico (Σ2^{−i} = 1) necesita EXISTE; el conteo queda reducido a `ρ < 1` de UNA transición del DP (sobre la órbita del DP — 3-bis.vi) | medido exacto (t = 0…26, tres arranques); el teorema ABIERTO | `excesocolision.py`, `notaequidistribucion.txt` §3-bis |
| **TORTUGAS** | teorema condicional | el reloj polinomial: `τ_i ≤ i^{2+ε}` c.s. condicional a la dominación (D) — reflexión + Chernoff adaptado + presupuesto quenched + Borel–Cantelli; supera el `e^{o(i²)}` pedido con margen infinito. La hermana de fábula de LIEBRES: la tortuga llega a tiempo | condicional a (D); piezas clásicas escritas; η = 2,082 medido de respaldo | `notalb.txt`, `arranquesporvisita.py` |
| **LANGOSTAS** | teorema por escalón | la pinza de dos tenazas: en cada caja truncada hay UNA SCC no trivial y cero lazos sueltos ⟹ `ρ(M_T) = ρ(S*)` (Perron aplica), y CW min/max en enteros lo PINZA por ambos lados — ancho ≤ 1e-5 en los escalones 1–9 y `ρ(M_T) ∈ [1,989042, 1,989176]` en el 10 (22,5M estados): la letra chica del ritmo del récord, pagada ENTERA en el truncado | demostrado por cómputo exacto (los DIEZ escalones, K ≤ 19) | `pinzacw.py`, `certificadocw.py` |
| **URRACAS** | teorema | la contabilidad del sesgo: `exp − contr = 2V + (Ee−E0) + k0 − k_t` EXACTO por palabra (libro mayor de nueve tipos); corolario: `⟺` en la sombra IFS con umbral 0,26186, umbral EFECTIVO ~0,2446 en la cadena (error del modelo medido); sin condicionar `Σ(Ee−E0) = 0` — el h-transform aislado en UNA moneda condicionada | demostrado (Lean 0 sorry); **AGUANTÓ ENTERA la 5ª revisión** (tabla rederivada, 200.000 palabras, Lean cotejado a máquina, circularidad rota con 59.990 pares reales) | `urracas.py`, `urracas.lean`, `actarevision0908b.txt` |
| **LORAS** | teorema | leen la palabra entera: «racha ≥ j con palabra u tras el mixto» es A LO SUMO UNA clase mod 2^{j+1}, para TODA palabra (división lineal directa; recarga por `tres_inyectivo`; q libre por paso — más fuerte que lo que la cadena usa) — la unicidad que la unión por palabras necesita: `P(racha_total ≥ j) ≤ √C₂·2^{−(j+1)/2}`, el reemplazo del compuesto roto por la 10ª | demostrado (Lean, el 21º, 0 sorry); cruce 1.260 combinaciones: EXACTAMENTE una clase (existencia medida, unicidad teorema) | `unionpalabras.lean`, `union_cruce.py` |
| **BALLENAS** | medición + reformulación | filtran por fibra: el funcional definitivo del conteo es el exceso CONDICIONAL `e_cond = Σ_k P(k)·(C2_k − 1)` (el piso móvil de k DIVIDIDO, no restado — las barbas de la ballena); domina a la marginal por el puente C-S (una línea), inmune al contraejemplo naif, y `ρ_cond < 1/2` en toda la ventana (peor 0,460, margen 8%); el absoluto queda DESCARTADO con negativo registrado (ρ ~ 0,9: carga la difusión de k) | medido exacto (78 celdas × 3 arranques; cruce 2^14 en enteros); el teorema ABIERTO — es EL enunciado a demostrar | `conteoconjunto.py`, `notaequidistribucion.txt` §3-bis.vii |
| **TRUCHAS** | teorema (en V2) | nadan contra la corriente: el teorema V2/L3 por REVERSIÓN TEMPORAL en la absorción — el h-transform explícito `h(k) = k−1` (Bessel-3 discreto), la serie revertida convergente, el lema D de comparación (sup 2,823 vs 2^{3/2}) y el LLT autocontenido ⟹ `φ_V2(x) ≥ c/√log x` con ventana universal | teorema autocontenido en el modelo V2 (`teoremav2.txt`); **AGUANTÓ la 9ª revisión** (verificación exacta en racionales; 3 reparaciones de escritura) | `teoremav2.txt`, `trasvasel3.py`, `fichaagkv.txt` |
| **GRULLAS** | hallazgo medido | migran todas al mismo punto: la MEDIANA UNIVERSAL — la ley de `log\|u\|` a la entrada del fondo, condicionada a `τ ∈ [T, 2T]`, es independiente del arranque (mediana límite 17,50 en V2a / 17,60 en V2b, desvío 1,9%; en la CADENA REAL deriva 0,07 décadas sobre seis órdenes de c₀) y es la del h-transform de AGKV; la balota real 1,117–1,145 = la constante de V2 | medido por dos caminos sin código común (forward condicionado vs cadena revertida); es mecanismo, no cota | `medianauniversal.py`, `medianareal.py` |
| **CIGARRAS** | hallazgo medido | el reloj que canta a ritmo: la dominación del reloj real — `P(racha ≥ j)·2^j = 0,92–0,97` para todo j ≤ 12 con muestra (3,86M rachas de 150k excursiones reales), POR DEBAJO de 1: el reloj real dominado por la Geom(1/2) de V2b sin inflación, casi una igualdad medida | medido (la formulación con «offset O(log k)» de su salida fue RETIRADA por la 9ª — la dominación como hecho aguanta); el teorema es (D), el conteo pendiente | `rachasreales.py`, `dominacioncondicionada.py` |

## Dónde está cada cosa

| pieza | fichero |
|---|---|
| Perras, Gatas y las 16 comprobaciones | `nuevasfusion.py` |
| itinerarios (paso 1 de clasificación) | `itinerarios.py` |
| el mapa de dependencias y su regla | `guardarafirmaciones.py` → `afirmaciones.db` (tablas `nodos`, `dependencias`) |
| el registro por sesión | `bitacora.md` (03-08-2026, cinco bloques) |
| la palanca CST (rama aparte, congelada esta semana) | `atacacst.py/.lean`, `paradacoef.py` |
