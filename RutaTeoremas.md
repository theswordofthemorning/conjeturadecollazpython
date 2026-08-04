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

**EL NORTE NUEVO — la pregunta única que queda, en coordenadas de la
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

## Dónde está cada cosa

| pieza | fichero |
|---|---|
| Perras, Gatas y las 16 comprobaciones | `nuevasfusion.py` |
| itinerarios (paso 1 de clasificación) | `itinerarios.py` |
| el mapa de dependencias y su regla | `guardarafirmaciones.py` → `afirmaciones.db` (tablas `nodos`, `dependencias`) |
| el registro por sesión | `bitacora.md` (03-08-2026, cinco bloques) |
| la palanca CST (rama aparte, congelada esta semana) | `atacacst.py/.lean`, `paradacoef.py` |
