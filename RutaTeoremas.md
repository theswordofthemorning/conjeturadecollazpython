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

## LA RUTA TRAZADA para la próxima sesión

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
