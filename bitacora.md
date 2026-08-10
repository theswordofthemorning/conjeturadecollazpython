# Bitácora

Resumen corto por sesión. Lo detallado va en `CLAUDE.md`; esto es para saber en
diez líneas qué pasó y por dónde se iba. La entrada más reciente arriba.

---

# ⇢ 10-08-2026 (11) — EL LEMA DE LA MEZCLA, REDUCIDO A CUATRO PIEZAS EXACTAS (el esqueleto demostrable)

El cierre teórico de la jornada: la mezcla medida en (10.6) no es
sólo empírica — **su demostración se arma con piezas que el repo ya
tiene**, condicionando al camino de `k` de la excursión:

1. **El balance exacto**: una excursión que sale de `k=2` y vuelve
   tiene subidas = bajadas (`d` y `d`).
2. **Los mapas forzados se compensan**: dado el camino de `k`, los
   pasos mixtos fuerzan el mapa de `u` — subida N3 aplica `f₀`
   (`u → u/2 + δ`, `K = 1/2`), bajada N4 aplica `f₁`
   (`u → (3u−1)/2`, `K = 3/2`) — y el producto de las constantes
   de Lipschitz forzadas es `(1/2)^d (3/2)^d = (3/4)^d < 1`
   **EXACTO: la parte forzada contrae siempre**, en toda excursión.
3. **Las monedas libres contraen en promedio**: los pasos
   compartidos quedan como monedas justas LIBRES dado el camino de
   `k` (Terras), aplicando `f₀/f₁` con `E[log K] = ½·log(3/4) =
   −0,144 < 0` — el marco clásico es **Diaconis–Freedman 1999
   («Iterated random functions», SIAM Review): E[log K] < 0 +
   momento ⟹ ley estacionaria única atractora, convergencia
   geométrica** (ancla bibliográfica nueva, hipótesis verificadas:
   mapas afines, probabilidades constantes ½/½ — el caso más
   limpio del teorema).
4. **La perturbación es la de Arañas**: `|δ| ≤ 3^{−k}/2` por paso,
   exacta y chica arriba de la torre.

**⟹ el exponente de Lyapunov condicional de la diferencia es
negativo en TODA excursión** — el olvido exponencial: la tasa
predicha `e^{−0,144·ℓ}` CLAVA la medición de (10.6) (a ℓ=29:
`e^{−4,2} ≈ 0,015` contra el < 0,03 medido). La mezcla pasa de
hipótesis a **lema con esqueleto**; el trabajo que queda es la
redacción cuidadosa (la ley de entrada = mezcla + el paso de
selección expansiva de (10.3)) y su verificación de trío. Con eso,
la cadena de la ruta queda: **mezcla (lema con esqueleto) + cuota
de exponente < ½ (medida, el hueco de verdad) + Golondrinas
(demostrado) ⟹ recurrencia de la ventana ⟹ φ=1.** El único
eslabón sin forma de teorema es la cuota — y ahora está aislado.

# ⇢ 10-08-2026 (10) — LA SERIE DEL PISO EN SU FORMA RENOVACIÓN-CORRECTA, Y «LA ENTRADA NUNCA ES EL PRE-VÓRTICE»

Las dos últimas mediciones de la jornada, sobre la excursión real
desde el rebote `(2,2)` con absorción exacta al entrar al fondo:

1. **`P(|c| ≤ 25 | primera entrada al fondo en t)`** — la serie del
   piso por visita en el objeto condicional CORRECTO (el de la
   renovación; `pisoporvisita.py` medía la ocupación a t fijo, no la
   entrada): **0,94 (t=11) → 0,54 (t=33), con tasa DECRECIENTE**
   (−0,016 → −0,010 por paso). La ventana chica `|c| ≤ 8` da
   0,43 → 0,15. La serie corta no distingue `→ p₀ > 0` de `→ 0`
   lento (la lección, siempre); es LA serie a extender y el insumo
   directo de la transferencia de Arañas.
2. **La primera entrada NUNCA aterriza en `(1,1)`**: 0 exacto en
   los 33 niveles. Estructura: el único acceso externo al
   pre-vórtice es `(2,5) →bit1→ (1,1)`, y `(2,5)` no aparece en un
   BFS de 44 M de estados desde `(2,2)` sin tocar fondo (acotado a
   `|c| ≤ 10⁷, k ≤ 40` — hecho finito, NO teorema; sin obstrucción
   simple mod 9: el residuo 5 sí vive en k=2). Consistente con
   PALOMAS: el pre-vórtice se puebla desde ADENTRO de la
   circulación del fondo — la absorción exige recircular.
3. **La anatomía de la entrada**: TODO ingreso viene de `k=2` (la
   única puerta, estructural) y el paso de entrada ES la rama
   expansiva (`bit1` en impar: `u → (3u−1)/2`) — la entrada
   selecciona ×1,5-2 de `u`, por eso aterriza en el borde de la
   ventana y no en el atractor. Mediana de `|c|` al entrar: 8 → 23
   (t = 9…33), crecimiento sublineal; q90: 19 → 95.
4. **LA LECTURA DE TRABAJO (etiqueta: ajuste de exponentes en dos
   décadas — punto 5 de la capa 1, NO resultado)**: la cuota de
   ventana en la entrada cae `~t^{−0,50}` (log(0,94/0,54) /
   log(33/11) ≈ 0,50); con densidad de visitas `~t^{−1/2}`, la
   serie de Green iría como `Σ 1/t`: **divergente POR UN
   LOGARITMO** — φ=1 en el filo exacto. Explicaría de una vez por
   qué TODAS las series del programa (la razón de b, r_25, S(t),
   p_t) convergen con lentitud agónica: κ=1 crítico en todas
   partes, marginalidad máxima en todas las coordenadas. Es la
   hipótesis de trabajo a testear — no una conclusión.
5. **Y EL PRIMER TEST DE LA HIPÓTESIS, mismo cierre** (barrido con
   poda acotada: exacto hasta t=32; de ahí a t=55 con poda al tope
   de 2 M de estados y la masa podada contabilizada EXACTA — las
   cotas rigurosas se vacían en t≈37 y el instrumento lo declara;
   los puntos t>32 son estimadores del barrido superviviente, sesgo
   de dirección desconocida): la cuota sigue suave 0,538 → 0,439
   (t = 33 → 55) y **el exponente local CAE: 0,50 en [11, 33] →
   0,40 en [33, 55]** — la caída se frena más que una potencia
   fija. Si `δ < ½` persiste, `Σ visitas × cuota ~ Σ t^{−1/2−δ}`
   diverge POLINOMIALMENTE, no por un logaritmo: el primer test
   dobla hacia el lado recurrente, sin decidir (la lección de
   siempre). La serie y el instrumento quedan listos para la
   próxima extensión.
6. **Y LA MEZCLA DE LA TRANSFERENCIA, VERIFICADA**: tres barridos
   de excursión desde arranques con `u` distinta (`(2,2)`,
   `(2,−4)`, `(2,20)`) — a t=9 las leyes de entrada difieren
   fuerte (cuotas 0,91 / 0,77 / 1,00); **a t=29 están a < 0,03
   (0,574 / 0,583 / 0,600), medianas 20/20/19: las excursiones
   largas OLVIDAN su `u` inicial.** La ley de entrada es
   asintóticamente independiente del arranque — el insumo exacto
   de mezcla que la transferencia de Arañas y la renovación
   (ciclos i.i.d.) necesitan. La cadena del argumento futuro:
   mezcla (medida) + cuota con exponente < ½ (medida, punto 5) +
   Golondrinas (demostrado) ⟹ recurrencia de la ventana — cada
   pieza medida tiene ya su forma de lema.

# ⇢ 10-08-2026 (9) — LA LÍNEA FOSTER: TRES INTENTOS, TRES DIAGNÓSTICOS, Y LA OBSERVACIÓN QUE REORDENA EL PROBLEMA

Se atacó la recurrencia de la ventana con **Foster de m pasos**
(`V = k + β·log₃₊(|u|/u₁)`, β = 2 — las piezas: martingala exacta de
`k` (Lamperti C1), contracción −0,131/paso de la moneda (Tigresas),
compensación de la frontera con β ≥ 1,585). **Tres verificadores,
tres fallos instructivos** (rejillas de ~37.000, ~11.600 y ~6.200
estados, 2^8 y 2^12 palabras exactas por estado):

1. `u₁ = 1, m = 8`: positivos en el rayo `u = −1` para TODO k —
   **el clamp estaba sentado sobre el punto fijo `u* = −1 de la
   rama expansiva del IFS** (`(3u−1)/2 = u`), donde el atractor
   bombea el borde sin parar. Lección de diseño: el clamp va FUERA
   del atractor `[−1, ½]`.
2. `u₁ = 4, m = 12`: los peores positivos eran **estados
   inalcanzables** (`(0, c<0)`: el gap de frontera es ≥ 1) y
   contaminación post-visita (la deriva de m pasos debe usar el
   **proceso PARADO** en `C₀`, `E[V(X_{m∧τ})] ≤ V`).
3. Parado + filtros (alcanzabilidad, CABRAS): el positivo
   persistente vive EXACTAMENTE en el borde del clamp (`u ≈ ±4`,
   +0,80 en k=4): **el clamp duro es un RATCHET** — los cruces
   hacia arriba pagan `+β·log₃(13/8) ≈ 0,44β` y los de bajada no
   reembolsan (el `max(·,0)` no baja de 0). Candidatos siguientes,
   anotados: clamp suave `f = ½·log₃(1+(u/4)²)` (reinyección casi
   gratis: +0,007β) o pendiente `−δ` bajo el clamp (reembolso).

**Lo estructural que quedó demostrado por el camino**: (a) en el
interior (`k ≥ 3, |u| ≤ 7/3`) la deriva es **CERO EXACTO** — el
clamp es incruzable en un paso (`|u'| ≤ 3|u|/2 + ½ < 4`) y `k` es
martingala: la cadena es genuinamente crítica-nula ahí, y el Foster
de recurrencia lo tolera (pide ≤ 0, no < 0); (b) la reinyección
(`u ~ 0 → u' ≈ −½` vía N4) aterriza DENTRO del atractor: con el
clamp en 4 es gratis; (c) **LA OBSERVACIÓN QUE REORDENA: la ventana
de Doeblin `|c| ≤ 25` en `k = 1` es `|u| ≤ 25/3 = 8,33` — contiene
el atractor ENTERO del IFS con margen ×8**. La recurrencia de la
ventana equivale a «`u` cerca del atractor cuando `k` toca fondo» —
exactamente lo que el diagnóstico del mecanismo midió (la masa
superviviente lleva `u = O(1)` pegado a la torre) y lo que la
transferencia IFS→cadena de Arañas (pendiente declarada) debería
dar. La línea Foster queda ABIERTA con sus candidatos; el interior
crítico-nulo y el ratchet están mapeados para no repetirlos.

**⇢ EL CUARTO INTENTO (clamp suave) Y LA OBSTRUCCIÓN ESTRUCTURAL,
nombrada**: el clamp suave también filtra (+0,52 en `k=5,
u ∈ [−2,−1]` — la zona del atractor, otra vez) y el patrón de los
cuatro fallos es UNO: hay una tensión de fondo entre las tres
exigencias del Foster de una función — (1) conjuntos de nivel
finitos exigen que `V` crezca en `|c|` a TODO `k`; (2) el interior
crítico tiene `E[Δk] = 0` EXACTO: no hay presupuesto con qué pagar;
(3) cerca del atractor la dinámica de `u` bombea cualquier
funcional monótono de `|u|` (el punto fijo expansivo, la
reinyección y el ratchet son tres caras de lo mismo), y un `f(u)`
exactamente armónico no existe salvo constantes (ergodicidad del
IFS). **El Foster «V = k + f(u)» está estructuralmente obstruido
para esta cadena crítica-nula** — como el paseo 2D, que exige
funciones log-afinadas casi-armónicas. El análogo fino aquí ES la
transferencia IFS→cadena de Arañas (la pendiente que el propio
fichero declara): la vía que queda para la recurrencia de la
ventana es esa transferencia (mezcla del `u` sobre el atractor en
los tiempos de fondo — y la ventana CONTIENE el atractor con
margen ×8), no una función de Lyapunov monótona. Cinco rejillas
corridas, cero desperdicio: cada fallo dejó su pieza.

# ⇢ 10-08-2026 (8) — T=30 EN LA TABLA CERTIFICADA, Y EL ESQUELETO DEL LEMA LOCAL CON NOMBRES: DOEBLIN + LAMPERTI + ERICKSON

Cierre de la jornada: la tabla de GAVIOTAS-B extendida a **T=30**
(cota fina 0,1906 — quinta fila bajo el umbral, bajando). Y el lema
local inferior (`P(fondo en T) ≥ c/√T`, lo único asintótico que
queda) recibió su **esqueleto clásico con nombres**, tras descartar
por circular la vía del piso-por-constructor (sólo transfiere el
piso entre tiempos vecinos — queda como lema de suavizado):

1. **Regeneración de Doeblin** sobre el conjunto finito de LIEBRES
   (ε ≥ 17887/131072, ya exacto) ⟹ ciclos de renovación.
2. **La cola del ciclo `P(τ > t) ≍ t^{−1/2}`** — el paseo crítico
   de `k` con reloj de cola geométrica (medida exacta
   `P(racha ≥ j)·2^j → 0,9265`; los lemas de racha ya en
   `tortolas.lean`). **La única pieza por demostrar.**
3. **Erickson 1970** (strong renewal theorem) ⟹ `P(X_t ∈ C) ≍
   t^{−1/2}` — el lema local entero, y con GAVIOTAS-B, `suma → 0`:
   la hipótesis de Kesten de CEBRAS demostrada asintóticamente para
   las historias que vuelven. Pendiente bibliográfico nuevo:
   Erickson, Trans. AMS 1970.

**⇢ Y LA PIEZA (ii) YA TIENE SU MEDICIÓN DIRECTA** (misma tarde):
la cola del ciclo de regeneración REAL — masa sin volver a
`C = {(0,g): g ≤ 25} ∪ {(1,c): |c| ≤ 25}` partiendo del rebote
`(2,2)`, absorción exacta al entrar — da **`S(t)·√t = 1,03 → 1,16`
en t = 6…33** (tope de estados en t=34), deriva suave hacia arriba:
la firma `t^{−1/2}` del ciclo crítico con corrección lentamente
variable. OJO del oficio: en α = 1/2 exacto el SRT clásico puede
exigir condiciones extra (Caravenna–Doney) — la ficha de Erickson
está encargada y dirá qué hay que verificar sobre esta cola.

**⇢ LA PRECISIÓN DE CAPA 1 SOBRE EL PROPIO ESQUELETO (antes de que
envejezca)**: la mitad «`S(t) → 0`» de la pieza (ii) **ES la
recurrencia misma** — el ciclo termina c.s. ⟺ la ventana finita es
recurrente ⟺ φ = 1 (LIEBRES + dicotomía) — así que el esqueleto NO
reduce el problema: le da la FORMA cuantitativa que tendrá la
prueba (una vez esté la recurrencia, Erickson convierte la cola en
el local `≍ t^{−1/2}` y todo lo demás encaja), y deja la pregunta
abierta en su enunciado más limpio conocido:

> **`φ = 1 ⟺ P_{(2,2)}(τ_C < ∞) = 1`** — ¿el rebote del vórtice
> vuelve casi seguro a la ventana `{k ≤ 1, |c| ≤ 25}`?

con `S(33) = 0,2016` medido y la firma crítica en la cola. La
medición NO distingue `S → 0` de `S → s∞ > 0` (la lección de la
casa, una vez más): el veredicto es del mecanismo.

**⇢ Y EL MECANISMO, DIAGNOSTICADO** (dónde vive la masa que no
vuelve): el 98% de la superviviente está ARRIBA en la torre
(`k` medio 3,8 → 6,2 entre t = 9 y 33: crecimiento DIFUSIVO ~√t),
con `log₂|c|` del núcleo clavado en `1,585·k` — **`u = c/3^k` se
queda O(1): el escape es pura difusión crítica de `k`, NO
dispersión de `c`**. La rebanada que pisa el fondo sin entrar a la
ventana es ~2%, con `log₂|c| ≈ 5–7` estable (pegada al borde
`log₂25 ≈ 4,6`, sin fuga). Con Golondrinas (el paseo vuelve c.s.)
y Moscas (u tenso, verbatim en la modificada), el mecanismo
favorece `S → 0` al paso `t^{−1/2}`; lo que decide sigue siendo la
cuota de ventana dentro del fondo (la `r_25` de LIEBRES,
INDECIDIDA). El intento de armar «Golondrinas + Moscas ⟹ visitas a
la ventana i.o.» tropieza con el salto condicional-en-visita (la
tensión de Moscas es incondicional en t, no en tiempos de parada) —
el mismo salto que la base ya tenía etiquetado en la heurística
κ=1: anotado para que nadie lo recorra dos veces.

# ⇢ 10-08-2026 (7) — LA CORRECCIÓN 50 (cazada por Opus 5, vía el usuario) Y EL TEOREMA B: LA SUMA ENTERA, BAJO EL UMBRAL

**La crítica, y es correcta**: el umbral efectivo 0,2446 del
corolario de URRACAS es sobre **LA SUMA `a_V + a_D − a_K`**, no
sobre `a_D` solo — y la entrada (6) escribía «a_D ≤ 0,0739 < 0,2446
— CERTIFICADO», comparando una parte contra el umbral del todo,
con el término MAYOR (`a_V`) sin cota. Tenía la forma exacta de los
errores históricos y es la **corrección nº 50** (en la base).

**La respuesta de fondo (teorema B de GAVIOTAS, mismo día): el
mismo argumento martingala acota LA SUMA ENTERA.** En el libro de
URRACAS el paso del vórtice también es moneda centrada (bit 0 =
tipo 6 contractivo, bit 1 = tipo 9 expansivo), igual que mixtos y
monedas; el ÚNICO paso no centrado es el tipo 3 (frontera impar,
contractiva segura), que RESTA. Así `exp − contr = Σ ε'_s − #tipo3`
con todos los `ε'` justos dado el pasado, y

> `E[a_V + a_D − a_K | F] ≤ (√(N'·V') − E[#tipo3·1_F]) / (P(F)·T)`

con la ayuda tipo-3 computada EXACTA. **La cota fina: 0,198 /
0,196 / 0,194 / 0,192 en T = 16…28 — LA SUMA ENTERA certificada
POR DEBAJO de 0,2446 en todos los T computados, bajando** (valor
real 0,019; `a_V` absorbido en la martingala, sin cota aparte).
C4 ahora EXIGE la cota fina bajo el umbral con `SystemExit`. El
asintótico queda igual: `O(T^{−1/4}) → 0` módulo el lema local
`P(F) ≥ c/√T`. Y de esta ronda: los cuatro lemas de la muerte de
la racha (`racha_sigue`, `racha_muere_*`, `pot3_mod4`) entraron a
`tortolas.lean` (0 `sorryAx`) — la cola geométrica del reloj de los
mixtos, medida exacta (`P(racha ≥ j)·2^j → 0,9265`), tiene ya su
aritmética demostrada. **La lección de la 50**: una cota nueva se
compara contra el umbral DE SU PROPIA CANTIDAD — parte contra
umbral de suma es el cuantificador escondido de las cotas.

# ⇢ 10-08-2026 (6) — GAVIOTAS (propuesto): LA COTA MARTINGALA — EL «ÚLTIMO PASO», CERTIFICADO BAJO EL UMBRAL A T FIJO

**El resultado más fuerte de la jornada, y esquiva el hueco de la
endogeneidad por completo.** `gaviotas.py` (el 69º `.py`):

> **TEOREMA (propuesto: GAVIOTAS).** Con `M_s = E[1_F | F_s]` la
> martingala de Doob del evento fondo y `ε_s` el bit ±1 de los pasos
> moneda: `|E[(Ee−E0)·1_F]| ≤ √(N_c·V_c)`, con `N_c` = monedas
> esperadas y `V_c` = energía de martingala de los pasos moneda,
> `V_c ≤ Var(1_F) = P(1−P)`. Demostración de OCHO líneas: los bits
> son justos dado el pasado (exacto en la medida de clases de
> Leonas) ⟹ `E[ε_s·1_F] = E[ε_s·ΔM_{s+1}]`, y Cauchy–Schwarz dos
> veces + ortogonalidad de incrementos. **Sin horario producto, sin
> Efron–Stein, sin CLT local: la endogeneidad desaparece.**

Los números (tabla de `gaviotas.py`, exactos): a T=24 la cota da
**`a_D ≤ 0,0739 < 0,2446` — el «último paso» del acta de la 5ª
queda CERTIFICADO bajo el umbral efectivo a T fijo, con desigualdad
demostrada + aritmética exacta y CERO lemas pendientes** *(⇢
CORREGIDO en la entrada (7): el umbral 0,2446 es de LA SUMA
`a_V + a_D − a_K`, no de `a_D` solo — corrección nº 50; la
reparación, el teorema B, salió MÁS FUERTE)*; la cota
baja con T (0,0851 → 0,0705 en T = 16→28) y la holgura contra el
valor real es ×8. Asintótico: con `P(F) ~ 1,37/√T` (medido),
`a_D = O(T^{−1/4}) → 0` — el único pendiente asintótico es el lema
local inferior `P(fondo en T) ≥ c/√T` (forma Lamperti clásica).
Las monedas cargan sólo ~11% de la varianza de información del
fondo. Comprobaciones: **la ortogonalidad `Σ_s E[ΔM²] = P(1−P)`
verificada como IGUALDAD EXACTA DE RACIONALES (`Fraction`) en los
cuatro T** — el descuadre más mínimo delataría un error de γ —,
cruce con GARZAS a 6 cifras, cota cumplida con holgura, y la capa 1
cazó en vivo números escritos a mano en el veredicto antes de
correr (ahora se imprimen desde los datos). De paso: la distorsión
del horario bajo condicionamiento quedó medida (−0,014 media al
fondo) — ya no hace falta para la cota, queda como dato. Conteos:
**69 `.py` · 19 `.lean` · 3 `.db`**. Bautizo y adversarial externa:
en cola, del usuario.

**⇢ Addendum: la base del lema local, extendida a t=34** (forward de
un nivel): `P(fondo)·√t` = 1,271 → 1,383 entre t = 16 y 34,
subiendo suave con incrementos decrecientes — consistente con
`c/√t` por corrección lentamente variable, `c ≥ 1,27` en toda la
ventana. **La ruta de demostración del lema, esbozada**: lejos del
borde `k` es paseo justo con reloj (los mixtos); los huecos del
reloj tienen cola exponencial POR EL ARGUMENTO v₂ DE L2 (una racha
todo-compartido agota `v₂(c)`) ⟹ el cambio de tiempo es a lo sumo
geométrico ⟹ las cotas locales del paseo justo transfieren salvo
constante. Escribirlo riguroso es el único trabajo asintótico que
queda.

# ⇢ 10-08-2026 (5) — LA COSECHA VOLCADA (182·49) Y EFRON–STEIN CIERRA EL ESLABÓN EXÓGENO

1. **El pendiente doble del volcado, COBRADO** (agente en segundo
   plano según la regla de prioridad; diff revisado por la sesión
   principal antes del sello): `afirmaciones.db` pasa de
   **170·46·20 a 182·49·20** — las 12 filas de la madriguera y la
   ronda del tronco (Liebres, Cebras partida, Urracas, la 6ª/Leonas
   cualificada, Moscas extendida, Conejas/Cabras/N2 formalizadas,
   Pumas 7-8, Garzas, Tórtolas, el núcleo) y las 3 correcciones (la
   deriva de Cebras rota, las dos frases de Leonas, y la
   **degeneración de la identidad de URRACAS en la convención del
   vórtice** con su lección: una identidad que cierra certifica la
   suma, no la convención de cada sumando — sólo el cruce sin código
   común las distingue). Los conteos del D-06 en `CLAUDE.md`,
   actualizados.
2. **El eslabón (ii) de la cota del timing quedó con nombre clásico:
   EFRON–STEIN.** El efecto persistente es la desviación típica de
   `γ` sobre horarios, y para horario producto
   `Var ≤ Σ(sensibilidad por slot)² ≤ m·C²/m³ ⟹ std ≤ C/m` —
   riguroso. Verificado en el modelo puro (DP del par con horario
   compartido y bits independientes): `std·m → ~1,1` en m = 32…512,
   arranques 1/2/4. La cadena exógena entera es ahora clásica (CLT
   local + Efron–Stein); lo único no clásico es la ENDOGENEIDAD del
   horario. `maquinaria.txt` objetivo 6, actualizado.

# ⇢ 10-08-2026 (4) — GRIMMETT–HOLMES FICHADO (cero solapamiento) Y EL MODELO PURO CORRIGE EL EXPONENTE: UN SLOT ES `m^{−3/2}`, EL PERSISTENTE ES `1/m`

Dos cierres de retaguardia, uno con mordida de capa 1:

1. **La ficha de Grimmett & Holmes** (arXiv:2510.13572, el pendiente
   de la ruta) — leída por agente, archivada en
   `fichagrimmettholmes.txt`. Lo esencial: **cero Collatz** (no citan
   a nadie de la coalescencia 3x+1 — la novedad de la cadena sigue en
   pie); su marco («grand coupling») es exactamente nuestro objeto y
   el nuestro es el caso degenerado del acoplamiento determinista de
   Terras; pero TODO es espacio finito — sin Lyapunov, sin
   recurrencia numerable, sin tasas. Importables: Doeblin 1938 como
   cita canónica de Liebres, el test de bloques (T4.3/4.4: clases
   c.s. constantes ⟺ cociente doblemente estocástico) y la
   obstrucción del período (T3.13b) como plantilla para `c mod 3`.
2. **El DP exacto del modelo puro** (paseo justo reflejado, K=4000,
   m ≤ 1000) **corrigió el objetivo 6 de `maquinaria.txt` antes de
   que envejeciera**: la sensibilidad a UN slot de horario decae
   `~C(k₀)/m^{3/2}` (constantes clavadas: `δ·m^{3/2} →` 1,59 / 4,76 /
   7,87 para k₀ = 1/2/4), NO `1/m` — el `κ ~ 0,45/m` de la cadena es
   el efecto PERSISTENTE (la divergencia cambia el horario para
   siempre) = suma de ~√m slots efectivos × m^{−3/2}. La cadena de
   cotas queda: un slot ≤ C/m^{3/2} (CLT local, el ejercicio) ⟹
   persistente ≤ C/m ⟹ composición con `P(j*=j) ~ 2^{−j}` ⟹ total
   ≤ C·log T ⟹ `a_D → 0`. Los dos niveles medidos, consistentes
   entre sí y con la serie de GARZAS.

# ⇢ 10-08-2026 (3) — EL NÚCLEO DE SENSIBILIDAD: `κ ~ 0,45/m` — EL DESBALANCE CONDICIONADO SE DESVANECE COMO `log T / T`

La segunda mitad de TÓRTOLAS, integrada a `firmaacoplamiento.py`
(sección nueva + C4): tras la divergencia el par queda a la MISMA
altura con paridades opuestas, así que la cota necesita
`κ(m) = |γ(k,c+δ) − γ(k,c)|/(suma)` con `δ` impar, contra el
horizonte `m`. **Medido (proxy: pares alcanzables al mismo nivel,
ponderado por masa): `κ·m ≈ 0,42 / 0,46 / 0,45 / 0,37` en
m = 4, 8, 16, 24** — decaimiento `~0,45/m`, casi independiente de
`δ` (1, 3, 9) y de `k`: la firma del laplaciano discreto (el efecto
es de SEGUNDO orden en el paseo justo). C4 nueva: decrecimiento
estricto exigido con `SystemExit`.

**La composición cierra por las dos puntas**: sesgo por moneda
`≈ Σ_j 2^{−j}·κ(m−j)` ⟹ total por trayectoria `≈ c·log T` con
`c ≈ 0,08` — que reproduce simultáneamente el NIVEL (0,239 en T=30)
y la TASA (~0,003/paso = c/T) de la serie de GARZAS. La lectura
mecánica completa del «último paso»: **`a_D ~ log T/T → 0` — el
desbalance de la moneda condicionada no sólo queda bajo el umbral
efectivo 0,2446: SE DESVANECE.** Con `a_K ≤ 1/T` y `a_V` sublineal
(E[2V] crece con tasa decreciente), el sesgo total de URRACAS
apunta a 0: el exponente de Lyapunov de las historias que vuelven
tiende al incondicionado (−0,144 nats < 0). **Queda UNA pieza
analítica: `κ ≤ C/m` a priori** — un enunciado de suavidad del
núcleo de un paseo justo perezoso, desacoplado de `c`. (Todo mide y
orienta; el veredicto sigue siendo del mecanismo.)

# ⇢ 10-08-2026 (2) — TÓRTOLAS (propuesto): EL LEMA DEL ACOPLAMIENTO — EL SESGO DE LA MONEDA ES TIMING PURO

La continuación estructural de GARZAS, la misma tarde: el sesgo de la
moneda condicionada NO es un misterio — **es un efecto de timing
controlado por un acoplamiento exacto**. `firmaacoplamiento.py`
(el 68º `.py`):

- **EL LEMA**: los dos hijos de una moneda en `(k, c par)` son
  `(k, c/2)` y `(k, (3c+1−3^k)/2)` — mismo `k`, diferencia
  `Δ = c + (1−3^k)/2`. Bajo la MISMA palabra, comparten trayectoria
  de `k` y paridad; las seis leyes son afines con parte lineal
  `±1/2 / ±3/2` y las partes afines se cancelan: `v₂(Δ)` baja
  EXACTAMENTE 1 por paso y las paridades divergen JUSTO en
  `j* = v₂(Δ)`. `Δ = 0` (`c = (3^k−1)/2`) ⟹ los dos hijos son EL
  MISMO estado. Excepciones, exactamente DOS y nombradas: (E1) el
  vórtice asimétrico (una sola copia pisa `(1,1)`); (E2) el signo
  mixto — la salida `k=1 impar bit 1` lleva el ÚNICO `abs` de la
  cadena, y con `g` de signos opuestos la diferencia salta (hasta
  coalescer). En la frontera no puede pasar: el gap es positivo.
  **Verificado: 48.015 pruebas, 0 fallos, y las únicas
  interrupciones fueron 1×E1 + 1×E2.**
- **EL COROLARIO** (la mitad del «último paso» del acta):
  `j* ≥ horizonte ⟹ las trayectorias de k coinciden hasta T ⟹ el
  sesgo de esa moneda respecto del fondo es EXACTAMENTE CERO`.
  Medido: 1.315 de 1.317 monedas-estado clavadas (99,85%); las 2
  violaciones son E1/E2 con masa 2,2·10⁻⁵ de F.
- **LA FIRMA**: el sesgo por moneda CAE con la vida del acoplamiento
  en las cubetas con masa: 0,0216 (j*=0) / 0,0171 (1) / 0,0075 (2) /
  ~0 (3+).

**Lo que esto cambia**: la pieza analítica que queda (acotar a
priori el desbalance condicionado bajo ~0,2446) se REDUCE a la
sensibilidad-al-timing del paseo crítico de `k` — un enunciado sobre
paseos justos perezosos, DESACOPLADO de la dinámica de `c`. El lema
es aritmética por ley (testigos sin división, estilo
`aterrizajen2.lean`): candidato natural al 19º `.lean`.

**⇢ Y EL 19º QUEDÓ COBRADO LA MISMA TARDE: `tortolas.lean`**,
compilado A LA PRIMERA (la segunda pasada sólo afinó la salida:
los lemas del `abs` ahora hablan de `natAbs` — el warning de
hipótesis sin usar delató que la primera forma era N1 disfrazado,
capa 1 en vivo). Veinte teoremas, 0 `sorryAx`: `delta_hijos` (la
diferencia de los hijos ES `Δ`), `moneda_sin_efecto`, las siete
leyes par a par con testigos sin división, `pot2_mitad` (el
enganche del descenso), la imparidad conservada, las dos
imposibilidades de paridad, **`salida_signo_mixto`** (el porqué de
E2 como teorema: con signos opuestos los abs restan la SUMA — el
salto exacto que el lema exceptúa), y la instancia `(2,8)`
(`Δ=4, j*=2`) cotejada con `decide` sobre las 4 palabras contra la
transición real. Cruce sin código común: `firmaacoplamiento.py` C0.
Conteos: **68 `.py` · 19 `.lean` · 3 `.db`**.

# ⇢ 10-08-2026 — GARZAS (propuesto): LA MONEDA CONDICIONADA, LEÍDA POR ALTURA — Y EL EXPONENTE DEL CRITERIO CRUZA 1 HACIA ABAJO

El «último paso» del acta de la 5ª (acotar el desbalance de la moneda
condicionada bajo el umbral efectivo ~0,2446), atacado con el
instrumento que faltaba: **`monedacondicionada.py` (el 67º `.py`)** —
forward-backward EXACTO en enteros sobre la cadena modificada
(`alfa_s` × `gama_s`, el h-transform medido estado a estado), que
descompone el sesgo POR ALTURA `k` y POR MITAD de trayectoria, cosa
que la acumulación forward de `urracas.py` no puede.

**Los tres hallazgos (miden, ORIENTAN):**

1. **El sesgo condicionado al fondo vive en `k ≤ 3`** (más del 99% de
   las monedas), es `≤ ~0,03` por moneda, DECAE de k=1 a k=3
   (0,025 / 0,009 / 0,005) y está en LAS DOS mitades — no es efecto
   de borde final. El TOTAL por trayectoria `E[Ee−E0 | fondo]` crece
   ~0,003–0,004/paso (0,187 en T=16 → 0,239 en T=30): aun el peor
   caso lineal da `a_D → ~0,004`, sesenta veces bajo el umbral.
2. **Condicionado a estar EN `(1,1)`** — el evento cuya serie ES el
   criterio de `retorno11.py` — el balance `a_V + a_D − a_K` es
   **NEGATIVO** (~−0,05 y subiendo lento): la obstrucción de CEBRAS
   (multiplicadores supercríticos en las historias que vuelven) NO
   aparece en ninguna de las dos condicionadas.
3. **La ventana de UN estado de LIEBRES, la que el acta dejó
   INDECIDIDA**: el exponente local de `P(X_t = (1,1))` cruzó 1
   HACIA ABAJO en t≈22 y baja monótono (1,14 → 0,76 entre t=18 y 30).
   La serie de Green diverge (= φ=1) sii el decaimiento es más lento
   que 1/t: **la dirección medida es la de la recurrencia.** Etiqueta
   honesta: `1/(t·log²t)` también daría α→1⁻ y converge — orienta,
   no decide.

**La revisión propia, ANTES de entrar (C1–C5):** conservación 2^s;
identidad de URRACAS entera; objetivo trivial ⟹ sesgo CERO entero;
**el cruce contra `urracas.py`** (fila t=28 reproducida a 6 cifras
por algoritmo independiente) — que **cazó un bug real**: contar V en
los dos bits del vórtice duplica `a_V` y **la identidad del libro
mayor cierra igual** (exp↔contr y V se compensan, +2−2=0): la
identidad es DEGENERADA en la convención del vórtice y ningún C2 la
distingue — lección nueva del oficio; y **la fuerza bruta** (2^12
palabras una a una, igualdad de enteros en todos los acumuladores y
el perfil, para los dos objetivos). Pendientes que deja: la
adversarial externa cuando el usuario la pida (regla del ritmo; se
suma a la cola de la terna de la madriguera), el volcado a
`afirmaciones.db` (sigue pendiente de la noche anterior), y el
bautizo — GARZAS es propuesta. Conteos: **67 `.py` · 18 `.lean` ·
3 `.db`**. *(De paso, operativo: `lean --version` se colgaba —
elan en «stable» intentando bajar v4.33; default fijado a v4.32.2,
lock huérfano borrado.)*

# ⇢ 09-08-2026 (15, madrugada) — CONEJAS EN LEAN: EL 18º, COBRADO CON SU REVISIÓN POR DELANTE

El pendiente que la regla del ritmo dejó esperando, cobrado como
manda: **primero la revisión, después el registro.**
**`conejas.lean`, el 18º `.lean`, 0 `sorryAx`**: para todo `j` par,
el par `(2^j−2, 2^j−1)` llega al MISMO `x = 3t+2` en EXACTAMENTE
`j+2` pasos (con `3^{j−1} = 4t+3` — el testigo de por qué `j` debe
ser par), con el vórtice en el repunit ternario `w = 2t+1`. La
arquitectura: el atajo como relación `PasoT` con testigos sin
división, `CaminoN` con largo exacto, **el peldaño**
`3^p·2^{q+1}−1 → 3^{p+1}·2^q−1` (el lema de identidad del repo) y
**la escalera** por inducción; más `separados_antes` (en `j+1` los
valores son `w` y `3w+1`, impar contra par: el encuentro es de
verdad) y el caso `j=2` (el par `(2,3)` a `x=2` en 4 pasos)
instanciando el teorema.

**La revisión adversarial propia, ANTES de entrar al repo** (A1–A5,
cero fallos): los constructores SON el atajo; las dos trayectorias
reales coinciden PASO A PASO con las fórmulas del fichero para
`j = 2…20` y llegan juntas en `j+2` exacto; el paso `j+1` es
`(w, 3w+1)`; `w` es el repunit impar; y ninguna fusión real ocurre
antes de `j+2` (lo que afirma `nuevasfusion` C5, comprobado igual —
este fichero sólo formaliza «a más tardar en `j+2`», la «primera
vez» sigue siendo del barrido). Corolario del repo ahora con núcleo:
**`b(j+2) ≥ 1` para todo `j` par — las nuevas nunca se acaban,
máquina-verificado.** Conteos: **66 `.py` · 18 `.lean` · 3 `.db`**.

# ⇢ 09-08-2026 (14) — LA 6ª REVISIÓN: LA RONDA DEL TRONCO. SEXTA VEZ QUE ROMPE ALGO — Y ESTA VEZ MORDIÓ A LEONAS

**Orden del usuario: revisar el mapa de dependencias DE LAS RAMAS AL
TRONCO** — las ramas acababan de pasar por tres adversarios; el tronco
(Leonas) y la terna (Tigresas/Arañas/Moscas) no los había mirado
nadie. Método: releer cada ENUNCIADO y preguntar si el cálculo lo
respalda — recomputando desde las definiciones del papel, sin agentes.
**Acta íntegra: `actarevision0908c.txt`. Verificación permanente:
`rondadeltronco.py` (el 66º `.py`).**

- **LEONAS [EXAGERADO, el central]**: «la única absorción es el
  vórtice» es verdad A NIVEL DE CLASES (donde `a(k)` sale exacto) y
  falso a nivel de instancias: **el par (7,8) funde en el paso 10 sin
  pasar por el vórtice** (estado `(2,−5)`, instancia `{1,4}`,
  `T(1)=T(4)=2`). Censo `n ≤ 50.000`: 22.027 fusiones de clase (todas
  en el vórtice), **14.009 coalescencias de instancia fuera (28%) —
  TODAS el mismo evento `{1,4}→2` del ciclo terminal** (`v = 1`,
  `c = 4−3^k`, verificado una a una). La φ del programa es FUSIÓN DE
  CLASE (el puente a igual altura es Pandas); la coalescencia eventual
  sería trivialmente 1. Cualificador aplicado al encabezado.
- **LEONAS [EXAGERADO]**: «la paridad del menor» → es la paridad DEL
  ANCLA (el ancla no es el menor en 4,6 M de pasos-instancia rumbo al
  ciclo). Con el ancla: **0 fallos en 12.516.313 pasos** contra pares
  reales (V1 perfecto). Las seis fórmulas: intactas.
- **TIGRESAS [OK, intacta]** — etiquetas ejemplares. Matiz nuevo
  escrito: las monedas de Tigresas (en `c`) y Cebras (en `u`) tienen
  bit OPUESTO en los pasos impares (la torre absorbe el 3) — la nota
  de reconciliación no existía y casi produce confusión en la 5ª.
- **ARAÑAS [EXAGERADO ×2]**: «perturbación SUMABLE» no es sumable en
  trayectoria (Golondrinas ⟹ `δ_t = 1/6` infinitas veces c.s.; lo que
  vale: `|δ| ≤ 1/6` y esperanza por paso < 1/10); «diminuta» llega a
  la MITAD del piso de `|u|` en el fondo. Las identidades: intactas.
- **MOSCAS [OK + EXTENSIÓN]**: la dominación vale VERBATIM en la
  cadena MODIFICADA (84.020 transiciones con el rebote, 0 fallos;
  `(2/3)^θ ≤ r_θ` en todo θ — la ventana de Lyapunov absorbe el
  rebote). La brecha «demostrado para la real, razonado sobre la
  modificada» — cerrada con cálculo.

**El veredicto: el tronco aguanta COMO CÁLCULO; lo que cayó es lo de
siempre — tres frases que decían más que su cálculo.** Conteos:
**66 `.py` · 17 `.lean` · 3 `.db`**.

**⇢ EL FILTRO CLASE/INSTANCIA (pedido del usuario, addendum del
acta):** ¿el cualificador estaba sólo en Leonas? Pasado por toda la
terna y los criterios: **sí — sólo en Leonas.** φ está definida en su
fuente como «probabilidad de absorción de esta cadena» (clase por
definición); Tigresas/Arañas/Moscas hablan de la cadena; los
criterios, de la modificada (palabras/masa); Pandas es instancia POR
DISEÑO (el puente a Gao); la cota 43,56% transfiere a instancias en
la dirección segura. El error no estaba replicado.

**⇢ Pendientes que deja la noche para la próxima sesión:**
`conejas.lean` **compilado limpio (0 sorryAx) en el scratchpad** —
la fusión en `j+2` de la familia extremal formalizada (escalera de
peldaños impares + testigo `3^{j−1} = 4t+3`) — entra al repo CON su
revisión propia (regla del ritmo: tres piezas nuevas ya esperan
revisión externa); y la terna nueva de la noche (Liebres/Cebras
post-acta, Urracas, los teoremas de la ronda) espera la próxima
adversarial cuando el usuario la pida.

# ⇢ 09-08-2026 (13) — LOS ESCALONES 7 Y 8 DE PUMAS: `λ ≥ 1,9844`

**`pumasescalera.py`** (el 65º `.py`): la escalera de truncados
re-computada ENTERA con tabla de sucesores precomputada (conteo
entero, ni un float en la cadena que decide) — **los seis escalones
publicados reproducidos dígito a dígito** con monotonía y convergencia
exigidas por `SystemExit` — y **dos escalones nuevos, nunca corridos**:

    escalón 7: K = 13, |c| ≤  49152 (  313.672 estados)  λ_T = 1,980748
    escalón 8: K = 15, |c| ≤ 196608 (1.312.342 estados)  λ_T = 1,984415

    ⟹  λ ≥ 1,9844      (antes 1,9754)

con las razones planas en la cola (t = 250…420). Los gaps
consecutivos: 0,513 / 0,498 / 0,669 / 0,733 / 0,755 / 0,784 /
**0,810** — subiendo hacia 1 sin señal de piso: el gap se resiste cada
vez más, exactamente como corresponde si `λ = 2` (resto polinomial), que
es lo que LOBAS dice que ningún truncado puede refutar. El escalón 8
queda tras la bandera `ESCALON_8` (son ~10 min de CPU; con `False` la
pasada rápida verifica los siete primeros en ~2 min). En el camino, la
capa 1 atrapó un susto de convergencia: a 400 pasos el escalón (9)
parecía dar MENOS que el «(7) publicado» — era que el 1,9754 publicado
venía del escalón (11) de `retornoslambda.py`, no del (7); la réplica
independiente restauró la monotonía y validó los seis.

# ⇢ 09-08-2026 (12) — EL ATERRIZAJE DE N2, EN LEAN: EL 17º `.lean`, Y EL PENDIENTE DECLARADO DE GOLONDRINAS, COBRADO

**`aterrizajen2.lean`** — la pieza 2-ádica CON SIGNO del lema del
descenso de Golondrinas, la que la bitácora 09-08 (5) declaró
candidata al siguiente `.lean`. Tres teoremas, estilo testigos sin
división (la valuación viaja en los testigos, `A = B+1` y `w`
parametrizado para esquivar la resta en `Nat`):

- **`aterrizaje_N2`**: si `v₂(c) > A = v₂(3^k−1)`, el paso bit 1
  entrega `2·(2^{A−1}·impar explícito)` — aterriza EXACTO en
  `v₂ = A−1`;
- **`aterrizaje_c0`**: `c = 0` igual (el impar es `−(2b+1)`);
- **`descenso_bajo_A`**: si `v₂(c) < A`, baja EXACTO en 1 (el
  descenso determinista de L2).

El mecanismo formalizado es la línea de `oscilacion.py`: `3c+1−3^k =
3c − 2^A·impar` y el mínimo de valuaciones cuando difieren. Táctica:
`pot2_add` propio + distribución y normalización AC con `simp only` +
`omega` sobre los átomos — compiló con esa receta a la tercera
iteración. `#print axioms` limpio en los cinco, casos conocidos por
`decide` e instanciación de los teoremas generales con los mismos
números. **El caso `v₂ = A` queda fuera A PROPÓSITO** (es la única
subida posible — C1c de `oscilacion.py`).

**Revisión adversarial propia:** los tres enunciados instanciados con
sus testigos exactos contra el numerador real del paso bit 1 —
**42.196 instancias** (`k = 1…10`, `|c| ≤ 6000` par), 0 fallos, impar
del testigo verificado en todas. Conteos: **64 `.py` · 17 `.lean` ·
3 `.db`**. El pendiente que queda de esta línea es el de siempre: la
estacionaria condicionada.

**Y la C6 de `urracas.py`** (el cabo de «los tres q1» del acta,
cerrado): la q1 INSTANTÁNEA tiene techo exacto 1/2 — la rama expansiva
exige bit 1 siempre, así que `q1_inst(fondo) = (1 − masa(k=0 impar |
fondo))/2`, identidad de enteros verificada en `t = 1…20`; a `t = 20`
da 0,4212 — **el «0,42 bajando» del revisor 2, ahora con fórmula**. El
sesgo del corolario vive entero en la q1 histórica: la brecha entre
las dos ES el h-transform, ya ledgerizado por URRACAS.

# ⇢ 09-08-2026 (11) — LA LOCALIZACIÓN: EL INGREDIENTE COMBINATORIO DE `e₈` ENTRA TODO POR EL CANAL PAR, Y `e^h₈` TIENE FORMA CERRADA

La continuación inmediata del (10), por los canales de NUTRIAS
(`e₈(N) = e₆(N−2) + e^h₈(N−2) + e^par₈(N−1)`). **Hallazgo positivo: el
piso h del estrato 8 SÍ tiene forma cerrada**, cuasi-cuadrática exacta
con período 3:

    e^h₈(N) = (4N² − 76N + 384 − 2·[N ≡ 2 mod 3]) / 3      (N ≥ 13)

clavada como igualdad de enteros en `N = 13…27` (COMPROBACIÓN 5 nueva
de `estratoscadena.py`; descubierta con el buscador de la C4 y diez
puntos retenidos en la validación). Como `e₆` es cuadrática y `e^h₈`
cuasi-cuadrática, **todo el ingrediente no cuasi-polinomial de `e₈`
entra por el CANAL PAR** — el subárbol de `r` par es la puerta
combinatoria. Y dentro del canal h la frontera está entre sus estratos
8 y 10 (`e^h₁₀`, `e^h₁₂` sin forma, verificado).

**La trampa que la capa 1 atrapó en vivo:** la primera réplica de los
canales usó `m_inicial = 0` (el fichero usa 2 para el piso h y 1 para
el par) y dio `e^par ≡ 0` — la identidad de Nutrias lo delataba
(`e^par₈(13)` tenía que ser 22). Se rehízo con las convenciones
exactas y con la C2 reproducida entera como control ANTES de leer
ninguna serie. El mapa fino queda: estrato 6 geometría pura; estrato
8 geometría en dos canales (vertical + h) y combinatoria en uno (par);
estratos ≥ 10 combinatoria en todos.

# ⇢ 09-08-2026 (10) — LA ESCALERA DE FORMAS CERRADAS TERMINA EN `e₆`: EL PENDIENTE DE `e₁₀`/`e₁₂`, RESUELTO EN NEGATIVO

El peldaño que la retaguardia esperaba («`e₁₀` y `e₁₂` esperan su forma
cerrada») no existe. **COMPROBACIÓN 4 nueva en `estratoscadena.py`**:
búsqueda exhaustiva de forma cuasi-polinomial `P(N) + corrección(N mod
p)` con grado ≤ 8, período ≤ 8 y arranque `N₁ = 10…16`, ajuste EXACTO
(`Fraction`, eliminación gaussiana) validado como igualdad de enteros
sobre toda la cola con ≥ 6 puntos retenidos — y con `e₆` de CONTROL
(su cuadrática SÍ se encuentra, grado 2, como debe). Resultado: **`e₈`,
`e₁₀` y `e₁₂` no admiten ninguna** — las diferencias altas oscilan con
amplitud creciente, la firma de un ingrediente combinatorio tipo
`b(k)`. La lectura estructural: los estratos ≥ 8 heredan la
combinatoria de las nuevas, no la geometría de la rejilla — la
frontera exacta entre «geometría» (e₂ = e₄ = 1, `e₆` cuadrática) y
«combinatoria» está entre los estratos 6 y 8.

**Y las tres series NO ESTÁN EN OEIS** (consultas API del 09-08, «No
results» las tres; el control Fibonacci del método sigue valiendo) —
añadidas a `sucesiones.txt` con su ficha completa. La autocrítica
adversarial aplicada al negativo antes de escribirlo: el ajuste se
ancló también en arranques tardíos (una forma legítima puede valer
sólo desde un `N₁`, como la propia `e₆`) y el buscador se valida a sí
mismo con el control positivo — sin eso, «no encontré» no habría
distinguido «no existe» de «mi buscador está roto».

# ⇢ 09-08-2026 (9) — LA REVISIÓN BIBLIOGRÁFICA DE LA CADENA, HECHA: LA FORMA `{v, 3^k·v + c}` NO ESTÁ PUBLICADA

El pendiente de la retaguardia que «ni siquiera se había buscado»,
cerrado con cuatro barridas web de ángulos distintos (coalescencia de
consecutivos, diferencia de dos órbitas como cadena, la forma `3^k·v +
c` literal, coalescencia + Markov). **Resultado: la cadena `(k, c)` de
Leonas — el par como `{v, 3^k·v + c}` con seis leyes exactas y moneda
de Terras — no aparece en la literatura.** Vecinos fichados: la
coalescencia clásica y los consecutivos (Garner, Gao, Elia–Tucker,
Frinkle 2025 — todos ya en el libro); **Grimmett & Holmes,
«Coalescence in Markov chains» (arXiv:2510.13572, J. Theor. Probab.
2026)** — marco general de clases de coalescencia por acoplamiento en
espacios finitos, sin Collatz ni nuestra forma: **pendiente de
lectura** (es el pariente abstracto más cercano de la pregunta φ); y
**ccchallenge.org**, el proyecto comunitario de formalización Lean de
la literatura Collatz — referencia nueva para la línea Lean del repo.
La novedad de Leonas queda con su búsqueda hecha y documentada; el
único cruce bibliográfico que sigue bloqueado es LaTourette (el PDF).

**Y el paper, LEÍDO la misma noche** (bajado a `lecturas/` — la
convención nueva del usuario: los textos se dejan ahí, fuera de git,
con respaldo zip en el escritorio). Veredicto de lectura: espacio de
estados FINITO en todo el paper, cero Collatz, cero espacios
numerables. Lo que sí da: **el lenguaje abstracto correcto** — dos
trayectorias de Collatz son exactamente el *grand coupling
determinista* (`F_t = T` para todo `t`) de su marco, y nuestra φ es la
densidad de coalescencia de ese acoplamiento sobre ℕ; su lema de
«densidad estacionaria `π_s > 1/m` fuerza el encuentro» es el pariente
finito de nuestro criterio de recurrencia. Nada transferible
directamente (todo depende de estacionariedad en espacio finito); la
pista que deja: su companion previo «Non-coupling from the past»
(Springer 2021). Los cuatro problemas abiertos que listan (3.3, 3.8,
3.11, 7.4) no tocan nuestro régimen.

# ⇢ 09-08-2026 (8) — EL PENDIENTE DEL ACTA, COBRADO: `cabras.lean` (EL 16º), EL INVARIANTE MOD 3 DE LA TORRE

El «regalo» del informe 1 de la 5ª revisión resultó ser **la puerta
mod 3 de CABRAS** (`subrenovacionc.py`) viajando por la cadena entera —
no un animal nuevo: por la regla de la casa, se formaliza bajo su
nombre. **`cabras.lean`, el 16º `.lean`, núcleo puro, 0 `sorryAx`:**
desde cualquier arranque en la frontera, todo estado alcanzado con
`k ≥ 1` cumple `c % 3 ≠ 0` (`paso_puerta` en los once constructores +
inducción sobre caminos), con el corolario **`torre_sin_ceros`**
(`(k, 0)` inalcanzable) — lo que justifica como teorema los saltos de
`c = 0` en las C0 de `liebres.py`/`urracas.py` y los 17 fantasmas del
conjunto de Doeblin. Mecánica: el esqueleto de `urracas.lean` sin
contadores; la llave es `3^{k+1} = 2m+1 ⟹ m ≡ 1 (mod 3)`: la rama
par-bit1 «resetea» a clase 2 y el descenso manda `{1,2}` en `{2,1}`.

**Revisión adversarial propia (régimen del usuario: avanzar y
revisarse una misma, sin agentes):** (A1) los once constructores
transcritos DESDE el `.lean` y cotejados contra `modificada()` —
25.521 estados con `c = 0` y rejilla fea: **0 desajustes**; (A2)
intento de falsificación por BFS a **7.709.949 estados** (profundidad
34): **cero** estados de torre con `3 | c`, clases vistas `{1, 2}`;
(A3) el paso del descenso `(d − m)` enumerado bajo las hipótesis del
lema: 0 violaciones. Conteos: **64 `.py` · 16 `.lean` · 3 `.db`**.

# ⇢ 09-08-2026 (7) — LA 5ª REVISIÓN EXTERNA: TRES ADVERSARIOS CONTRA LA TERNA. QUINTA REVISIÓN, QUINTA VEZ QUE ROMPE ALGO

**Acta íntegra (los tres informes verbatim): `actarevision0908b.txt`.
Correcciones aplicadas el mismo cierre.** Tres revisores adversariales
independientes, uno por pieza, cada uno con cálculo propio:

- **LIEBRES AGUANTÓ**: Green, clase cerrada, acoplamiento `E[2^{−N}]`,
  aperiodicidad (gcd de retornos = 1) y Doeblin (`17887/131072`
  reproducido dígito a dígito, y EXACTO para C — la ventana contiene
  la bola de L pasos). Correcciones: (a) el enunciado general «C
  finito arbitrario» tenía **cuantificador escondido** — la
  accesibilidad para C arbitrario es HORMIGAS cualitativo, cita
  añadida; (b) el titular «alfa 0,40 contra umbral 1» sobrevendía: a
  PROF 30 `C_625` contiene el 99,99% del fondo y esa serie **diverge
  bajo las dos hipótesis** (Golondrinas) — lo informativo es `r_5`,
  `r_25` bajando sin estabilizar: INDECIDIDO. Regalo del revisor: **el
  invariante mod 3** (entrada a la torre ⟹ `c ≡ 2 mod 3`; `c ≡ 0 mod
  3` no se fabrica desde `(0,1)`) — justifica los saltos de `c = 0` y
  deja 17 estados fantasma en C.
- **CEBRAS PARTIDA EN DOS**: la clasificación afín y el umbral
  aguantan una verificación independiente de 100.398 transiciones
  exactas — pero como **exponente de Lyapunov de los multiplicadores**
  (la hipótesis de Kesten de Arañas), NO como deriva de la cadena. La
  lectura dinámica está **ROTA y RETIRADA**: deriva real del fondo
  +0,023 nats/paso (la fórmula daba −0,133), `|u| ≥ 1/3` en el fondo
  la prohibía aritméticamente, el desplazamiento afín −1/2 es el IFS y
  no la perturbación (14–17 puntos de q1 contra un margen de 12,1),
  «ESTABLE» era pico en t≈25 y baja, el control `r_625 < 0,5` era un
  **control muerto** (cuantil 99,9% de `|c|` en el fondo: 238), y «el
  rebote conservador» es falso en agregado. Reenunciada; el guardián
  del barrido pasó a `r_25`.
- **URRACAS AGUANTÓ ENTERA**: tabla de los nueve tipos rederivada sin
  mirar la nuestra, identidad clavada en 200.000 palabras propias
  (largo ≤ 60), nivel t = 20 reconstruido desde cero dígito a dígito,
  Lean cotejado A MÁQUINA constructor a constructor (2.709 estados,
  `c = 0` y `|c| ~ 2^120`), y **la circularidad C0/Lean/modificada
  rota por fuera**: 59.990 pares enteros reales `{v, 3^k v + c}` bajo
  el atajo, 0 fallos. Correcciones: el `⟺` del corolario es exacto
  sólo en la sombra IFS (rebote 2/3 viola la cota de Arañas en ese
  estado; error medido ~+0,009 nats/paso ⟹ **umbral efectivo
  ~0,2446**, la dirección sobrevive ×13); C0 ampliada con la rejilla
  fea (c = 0, ±3^k±3, primos, k = 10..14 — pasa); «q1 global 0,455»
  es foto, no régimen (sube hacia 1/2).

**El estado de la sub-teoría tras el acta:** los dos pilares (LIEBRES,
URRACAS) en pie con etiquetas finas; CEBRAS reducida a su mitad
verdadera; el «último paso» pierde el puente heurístico de la deriva y
queda SOLO la reducción exacta de URRACAS: el sesgo condicionado
contra ~0,2446, margen medido ×13. Todo reejecutado tras las
correcciones (los dos `.py` limpios, `urracas.lean` recompilado, cp1252
a 0). Pendiente que dejó el acta: el lema del invariante mod 3 como
fichero propio, y la estacionaria condicionada de siempre.

# ⇢ 09-08-2026 (6) — LA SUB-TEORÍA DE LA MADRIGUERA: LIEBRES Y CEBRAS REVISADAS Y ADOPTADAS, Y URRACAS (TEOREMA + EL 15º .LEAN)

**Procedencia y revisión.** `liebres.py` apareció sin trackear, escrito a las
19:02 por una sesión de Opus 5 que el usuario frenó a tiempo (no tocó nada
más: cero diffs, cero commits). En vez de borrarlo, **revisión adversarial
completa** (guion en el scratchpad de la sesión): (A1) su `transicion`
validada contra **pares reales** `{v, 3^k·v + c}` del mapa del atajo —
30.600 transiciones, semillas de 60 bits, la fusión real `T(v) = T(3v+1)`
sólo en `(1,1)`-bit1; (A2) la constante de Doeblin **recomputada por camino
independiente** (probabilidades exactas con `Fraction`, no conteo de
palabras): `eps = 17887/131072` clavado; (A3) el caso `k = 0` de CEBRAS que
su C3 no cubría, verificado exacto; (A4, hallazgo anotado: el rebote
`(1,1)→(2,2)` tiene multiplicador `|u'|/|u| = 2/3` — ni 1/2 ni 3/2 — y C4 lo
cuenta como expansivo: dirección CONSERVADORA). **No se pudo romper:
adoptado, con bautizo confirmado LIEBRES y CEBRAS.**

**Y la pieza nueva de la casa — TEOREMA DE URRACAS** (`urracas.py` +
`urracas.lean`, el 15º, núcleo puro, 0 `sorryAx`, compilado en dos
iteraciones): en la cadena modificada, para TODA palabra,

    exp − contr = 2·V + (Ee − E0) + k0 − k_t     (igualdad de ENTEROS)

(`V` = rebotes en el vórtice, `Ee − E0` = desbalance de bits en pasos con
`c` par). Demostración por libro mayor (los NUEVE tipos de paso conservan
`exp − contr − 2V − (Ee−E0) + k`), formalizada en Lean (once constructores
con testigos sin división, invariancia + inducción sobre caminos);
exhaustividad de los nueve tipos contra la cadena verificada en la C0 del
`.py` (76.000 transiciones — el hueco Lean↔Python cerrado); la identidad
clavada palabra a palabra (2^15 exhaustivo + cuatro arranques con `k0 ≠ 0`)
y estado a estado (todos los estados de los 30 niveles, 1,2 M en el último).

**El corolario que reduce el último paso de CEBRAS:** la deriva del fondo es
negativa ⟺ `a_V + a_D − a_K < 2(log₂/log₃ − 1/2) = 0,26186`, y SIN
condicionar `Σ(Ee−E0) = 0` EXACTO en cada nivel (la moneda justa) — el
sesgo del h-transform queda aislado en UNA esperanza condicionada de
incrementos centrados. Medido (orienta, no decide): sesgo total ~0,019
plano, margen ×13,8; el término mayor es `a_V` (bajando), compensado por
`a_K`; la moneda `a_D ≈ 0,008` y baja. Regalo de Lean: los dos bits del
vórtice aterrizan en `(2,2)` (`vortice_bit0/1`, sin calculadora).

**LA SUB-TEORÍA DE LA MADRIGUERA, en una línea por pieza:** LIEBRES — basta
mirar cualquier ventana finita (`φ = 1 ⟺ Σ P(X_t ∈ C) = ∞`, Doeblin exacto
sobre conjunto finito, sin la constante fina de Hormigas); CEBRAS — el
mecanismo es la deriva de `log|u|` con umbral `log 2/log 3` (la constante
clásica, otra vez); URRACAS — el sesgo de esa deriva es una identidad
entera con tres términos medibles, y el último paso queda con nombre:
acotar la moneda condicionada bajo 0,26186 por paso (el h-transform del
paseo crítico sesga `O(1/k)`, no exponencialmente).

Conteos nuevos: **64 `.py` · 15 `.lean` · 3 `.db`**.

# ⇢ 09-08-2026 (5) — LA RETAGUARDIA SALDADA: EL PISO SOBREVIVE AL EXPONENTE HONESTO Y EL 14º .LEAN COMPILA A LA PRIMERA

Los tres frentes de la lista, ejecutados tras aplicar el acta:

1. **`pisoremedido.py` — el piso REMEDIDO** con tres exponentes (el
   viejo 2,5; el sup exhaustivo 2,75; el demostrable-con-margen 5):
   **con `e = 5`, α local = 0,675 < 1 y BAJANDO** (0,845 → 0,675) —
   «E[toques a (1,1)] diverge» SOBREVIVE al exponente honesto, con
   margen. La corrección #44 queda cobrada, no sólo anotada.
2. **La estacionaria condicionada, sondada por RENOVACIÓN** (Medida
   2): la ley de `|c|` del flujo de entrada al fondo (`k=2 → k=1`) se
   desliza con decrementos geométricos decrecientes (mismo patrón que
   la u-CDF de `empalme.py`) — extrapola a límite positivo. El paso
   teórico que decidiría (perturbed IFS condicionado) sigue ABIERTO y
   así queda dicho: esto lo sondea, no lo demuestra.
3. **`hormigas.lean` — EL 14º `.lean`, compilado A LA PRIMERA**: el
   esqueleto aritmético de Hormigas y del descenso de frontera de
   Golondrinas — `hormigas_viaje_j0` y `_j_ge1` (el descenso estricto
   del gap, los dos regímenes), `frontera_desciende_F1/_F2` (los dos
   bits quitan exactamente un factor 2: la pieza determinista de L2),
   `impar_por_tres` (v₂ baja EXACTO 1), estilo testigos sin división,
   núcleo puro, `#print axioms` limpio en los cinco, y los dos casos
   conocidos (g = 5 y g = 3) cerrados por `decide`. **Pendiente
   declarado: el aterrizaje de N2 en `v₂ = A−1` (2-ádica con signo)
   es el candidato al 15º.**

# ⇢ 09-08-2026 (4) — LA CUARTA REVISIÓN EXTERNA DICTÓ Y ROMPIÓ; APLICADA ENTERA. Y EL CORREO A FRABONI, ENVIADO

**El acta completa está en `actarevision0908.txt`; las correcciones
43–46 en la base.** En una línea por pieza: **el criterio de retorno
(`retorno11.py`) y Palomas AGUANTARON todos los ataques** — el
revisor validó el criterio como «la formulación buena del programa»;
**Abejas es cierta pero INCONDICIONAL (es Kraft)** — su contrapositivo
era VACUO y el «programa reducido a una desigualdad» apuntaba a una
diana demostrablemente inalcanzable (la salvación: la misma jornada
produjo retorno11); **Hormigas aguanta como teorema** con la constante
2,5 FALSA (muestra tomada por constante — el error nº 5 de la casa,
otra vez; sup exhaustivo ~2,73, demostrable candidata ~4,8; el −5/2
del piso hereda y hay que remedir); **L2 y Golondrinas aguantan** con
dos frases impresas falsas remendadas (palabra dependiente del estado;
caso partido núcleo/borde); **Águilas**: la línea exacta bien, la
lectura «la fusión se apaga» refutada por su propia tabla (φ₇ ≥ 0,107
subiendo — lo defendible es razón de b < 2 ⟹ φ_q < 1 plausible);
**Lechuzas**: correcta con el calificador «con S igualada». Cuarta
revisión externa, cuarta vez que rompe algo — la doctrina no falla.

**Y EL CORREO A FRABONI, ENVIADO** (orden del usuario, desde su
Gmail): la errata de la Tabla 4.2 de LaTourette 2007, con el email
verificado en el directorio oficial de Moravian
(`frabonim@moravian.edu`), el hallazgo exacto (L11 viola su
Definición 4; el conteo bueno es 19), la triple verificación, el tono
humilde de la casa y el link al repo. «Mensaje enviado» confirmado.
*Nota: se mantuvo la cita de Wu–Huang en OEIS contra una sugerencia de
quitarla — la corrección #8 la respalda (MR 1885838, entrada 125 de
Lagarias byte a byte); la «Elongate iteration» que Lagarias no vio es
OTRO paper de Wu.*

# ⇢ 09-08-2026 (3) — LA REFORMULACIÓN, LAMPERTI Y GOLONDRINAS: EL FONDO SE VISITA SIEMPRE

Mientras esperamos a los editores de OEIS, el ataque de Lamperti — y
salió mejor que Lamperti:

1. **EL CRITERIO**: `φ = 1 ⟺ (1,1) es RECURRENTE en la CADENA
   MODIFICADA` (vórtice rebotado a `(2,2)`): cada visita sobrevive con
   moneda 1/2, `P(no fundir) = E[2^{−N}]` — positivo sii `N` finito
   posible. **Sin condicionamiento a vivo: el Bessel desaparece.**
   Equivale a `Σ retornos·2^{−L} = 1` (Ovejas): la razón 2, disfraz final.
2. **`lamperti.py`**: la tabla de derivas de `k` EXACTA por enumeración
   (28.436 estados): martingala pura en el núcleo, `+1` sólo en
   frontera impar y vórtice rebotado; masa muy-par `≤ 0,57·2^{−j}`
   uniforme; fracción mixta → 0,513 estable.
3. **`oscilacion.py` — EL TEOREMA DE GOLONDRINAS** (bautizo de la
   lista: siempre vuelven): **la cadena modificada visita el fondo
   `k ≤ 1` infinitas veces c.s.** Demostración: (L2) con `k` congelado
   y `A = v₂(3^k−1)`, ambos bits bajan `v₂(c)` salvo bit 1 en
   `v₂ = A` exacto — bajo `A` el descenso es DETERMINISTA (60.010
   instancias, 0 fallos; frontera: determinista puro) ⟹ toda ventana
   de `A+1` ceros fuerza un mixto ⟹ infinitos mixtos c.s.; luego
   `k = M + A` con `M` martingala que no puede converger ⟹
   `liminf M = −∞` ⟹ `A → ∞` = infinitas visitas al borde. QED.
4. **LO QUE QUEDA — una pieza, la última de verdad**: el EMPALME POR
   VISITA: de las infinitas visitas al fondo a tocar `(1,1)` i.o.
   Hormigas da `P ≥ ~|c|^{−2,5}` por visita; medido a t=34: el piso
   `E[(1+|c|)^{−5/2}|fondo] ≈ 0,0496` con exponente local **0,52 →
   0,26 desacelerando** — camino a constante positiva. El mecanismo
   que lo decidiría: la estacionaria del IFS de Arañas condicionada al
   fondo (perturbed IFS — el blanco técnico ya nombrado).

**⇢ EL CRITERIO EN SU FORMA FINAL** (`retorno11.py`, la noche): el
segundo momento resultó INNECESARIO — la dicotomía de Markov lo hace
todo: **`φ = 1 ⟺ p = P_{(1,1)}(retorno) = 1 ⟺ Σ_t P(X_t = (1,1)) =
∞`**, porque `(0,1)` y `(1,1)` SE COMUNICAN (vuelta explícita:
`(1,1)→(2,2)→(2,−1)→(1,−2)→(1,−1)→(0,1)`, verificada) y la
recurrencia es de clase. La conjetura ES la divergencia de una serie
computable / el retorno con probabilidad 1. Medido: primeros retornos
a `(0,1)` con la serie prima de Ovejas (el vórtice rebotado cambia los
conteos, como debe); `S(35) = 0,437` y `1 − p_34 = 0,685`, **ambas
bajando con exponente local SUBIENDO** (0,22→0,24 y 0,17→0,20) — la
transitoriedad exigiría α → 0 con S estancada, y pasa lo contrario.
Orienta fuerte a recurrente; no decide.

**⇢ Y EL EMPALME, ACORRALADO** (`empalme.py`, la misma tarde): (1) la
u-CDF condicionada al fondo se desliza con DECREMENTOS GEOMÉTRICOS
(−0,023 → −0,016 → −0,012 por cuatrienio: extrapola a límite positivo
≈ 0,31 — no decide, orienta); (2) el sesgo de visita existe y es
acotado (fondo: `P(|u|≤1) = 0,34` contra torre 0,48 — llegar abajo
exige bits 1 = rama expansiva); (3) **la tasa de Hormigas
`E[2^{−2,5(k+log₂(1+|c|))}]` tiene α local ≈ 0,65 estable y bajando:
`E[# toques a (1,1)]` DIVERGE como `t^{0,35}` — el empalme vale EN
MEDIA.** Lo que decidiría: convergencia de la estacionaria
condicionada (perturbed IFS) o un segundo momento para pasar de
media divergente a i.o. casi seguro.

**Y EL SEGUNDO ROUND DE OEIS, la misma tarde**: Michel Marcus pidió en
A398792 alfabetizar referencias y aclaró que «Jia-Bang» no es
apellido. Aplicado (Gao antes de Garner; «J.-B. Wu and G.-L. Huang»
bajo la W) y respondido con el ancla MR 1885838 + entrada 125 de
Lagarias. **La sugerencia de QUITAR la cita de Wu se rechazó con la
corrección #8 en la mano** — es la Mathematica Applicata verificada
byte a byte, no la «Elongate iteration» que Lagarias no vio: quitarla
habría repetido el error que esa corrección documenta, en espejo.
Las tres re-propuestas.

**Capa 1 de la tanda**: el primer borrador afirmaba la versión
uniforme de la tensión en `k` (falsa: frente difusivo), un testigo
inventado en OEIS (`r = 690` → real `r = 909`), y un print roto en
`empalme.py`; los tres cazados antes de publicar/correr.
`respuestas.db` capturada a mitad de sesión (1.161 mensajes) y
transcripciones re-zipeadas, como manda la regla.

# ⇢ 09-08-2026 (2) — LA SALIDA AL MUNDO: zootheorem + OEIS A398792–A398795

**Orden del usuario**: repo público `zootheorem` sólo con hallazgos (sin
la ruta ni el método) y las sucesiones a OEIS desde su cuenta.

- **`github.com/theswordofthemorning/zootheorem` PUBLICADO**: 3 papers
  en inglés (merging classes con procedencia de los 36 términos;
  familia `(qx+r)/2` con Águilas y Lechuzas como Theorems 1 y 2 —
  incluida la generalización de Lechuzas a todo primo `p | r, p ∤ 2q`,
  con predicción confirmada en `(3x+5)/2`; y Moscas standalone),
  4 b-files, 2 verificadores por fuerza bruta (corren limpios, sin
  código compartido con el laboratorio), `mirror_theorem.lean`
  (= espejoak), y los drafts OEIS. **La cadena, la reducción y el
  programa de φ NO están ahí** — eso queda en este repo.
- **OEIS**: A-numbers reservados A398792–A398795. **Tres PROPUESTAS**:
  A398792 (a(n), 36 términos), A398793 (b(n), 35), A398794 (`5x+1`,
  22). A398795 (`7x+1`) reservada: el límite de 3 drafts activos por
  cuenta nueva la deja en cola (el texto está listo en
  `zootheorem/drafts/`). **Primera interacción editorial en minutos**:
  Michel Marcus pidió «more terms» en A398793 y devolvió el draft a
  editing; respondido en la discusión (los 35 términos son todos los
  alcanzables: el último exige 2^36 exacto por dos vías) y re-propuesto.
- **Capa 1 en vivo**: un testigo inventado (`r = 690`) en el ejemplo de
  A398794 se cazó ANTES de guardar; el real es `r = 909` (calculado).
- **Pendiente que NO pude hacer**: la página wiki de usuario de OEIS
  (que enlaza `conjeturadecollazpython`) está **protegida** — los user
  pages los edita el staff. Para completar el redireccionamiento:
  pedir el cambio a los editores de OEIS, o decisión del usuario sobre
  el repo viejo. **Ninguna de las 4 submissions enlaza el repo viejo.**
  > ⇢ **RESUELTO por decisión del usuario, la misma tarde**: puso
  > `conjeturadecollazpython` en PÚBLICO en GitHub — *«aunque nos roben
  > el alma, la humanidad está primero»*. El pendiente de la wiki queda
  > sin urgencia: el enlace apunta a un repo abierto a propósito. La
  > separación se mantiene igual: a OEIS sólo se envía lo de
  > `zootheorem`; A398795 quedó documentada entera para el envío
  > (`zootheorem/drafts/PENDING_A398795.md`, con testigo verificado
  > `a(4) = 1` en `r = 8`).

# ⇢ 09-08-2026 — EL LEMA DE BLOQUES: EL PISO QUEDA EN UNA SOLA DESIGUALDAD. Y LA FAMILIA q

Sesión de goal («avanzar hasta donde puedas», todo local, sin agentes).
Cuatro `.py` nuevos y un `.txt`; **sin commit — el usuario decide**.

| # | resultado | estatus |
|---|---|---|
| 1 | **`b(t) = N_t(1,1)` EXACTO** — las nuevas SON el pre-vórtice; afila a Zorras (`p_t = b(t)/m_k1`) | exacto (`minorizacion.py` C0, t=3..15 vs publicada) |
| 2 | **La serie `p_t` completa** (t=1..34): cociente bianual ↑ 0,981, exponente local 0,32 y bajando | medido, no decide (`pisoporvisita.py`) |
| 3 | **EL LEMA DE BLOQUES**: si `φ<1`, la ocupación viva de TODA rejilla finita, sumada por bloques de largo `T_G`, es `≤ 2^{T_G}` (continuaciones disjuntas). **Contrapositivo: `M_G(t)` no sumable ⟹ `φ = 1`** | elemental, dado (A); argumento entero en `minorizacion.py` |
| 4 | **Accesibilidad (A), TEOREMA constructivo**: política explícita de bits fusiona desde TODO estado; terminación demostrada (torre ↓, gap `g → ~3g/4` estricto por viaje, ventana de Perras cierra); largo `≤ 2,5·(k+log₂|c|+1)` | demostrado + exhaustivo rejilla + 2000 aleatorios a 10^30 (`accesibilidad.py`) |
| 5 | BFS hacia atrás: la rejilla `k≤8, |c|≤2000, g≤2000` fusiona ENTERA con `T = 23` óptimo | exacto (`minorizacion.py` C1/C2) |
| 6 | **El frente difusivo**: `sup_t m(k,t)·2^k` se alcanza en el último nivel para `k ≥ 6` — la versión UNIFORME de la tensión en k es dudosa; el lema de bloques la esquiva | medido; etiqueta honesta |
| 7 | **La serie decisiva `M_G(t)`**: 0,497 a t=30, exponente local α ≈ 0,35 subiendo despacio; RATAS predice `~1/√t` (no sumable) | medido, no decide — **α tendría que cruzar 1 para salvar `φ<1`** |
| 8 | **La cadena para `(qx+r)/2`**: las seis leyes con `3→q` (53.400 instancias × 4 mapas), simbólico=directo k≤14, espejo `3x−1` clava `a(k)` idéntica k≤22 | exacto (`cadenaqnr.py`) |
| 9 | **`E[m] = (1+q)/4`: κ=1 (Tigresas) CARACTERIZA a q=3** en la familia; `q≥5` supercrítica en log (Jensen cierra la ventana de Moscas) | exacto, una línea |
| 10 | **Densidades de fusión medidas POR PRIMERA VEZ**: `3x+1`: 0,409 ↑; `7x+1`: 0,107 casi parada (razón b ~1,6 — huele a límite `<1`); `5x+1`: 0,0044 (primera fusión en k=13) | medido k=22; OEIS/literatura SIN consultar |
| 11 | Los 5 objetivos de la maquinaria sin Collatz, con etiquetas (Moscas standalone = teorema listo para nota; cripto y relacional = diccionarios; método = 6 casos) | `maquinaria.txt` |

**EL ESTADO DEL PROGRAMA**: `φ = 1` queda reducido a **UNA desigualdad
sobre UNA serie** — que `M_G(t)` no sea sumable (p. ej. `≥ c/t`). La
pieza (A) del lema ya es teorema (arriba); el muro que queda es (B):
la ocupación de la rejilla contra la recurrencia del paseo.

**⇢ LA SEGUNDA PASADA DE LA MISMA JORNADA (bautizos del usuario
aplicados):** cinco habitantes nuevos del zoológico — **HORMIGAS**
(accesibilidad, teorema), **ABEJAS** (lema de bloques), **PALOMAS**
(`b(t) = N_t(1,1)`), **ÁGUILAS** (`E[m] = (1+q)/4`: κ=1 caracteriza a
`q = 3`) y **LECHUZAS** (`3 | r ⟹` los consecutivos no funden jamás:
`c ≡ 0 mod 3` inalcanzable — `a(k) = 0` clavado k ≤ 22 en `5x+3` y
`7x+3`). Y tres entregas más: **`diferenciales.py`** — el perfil
diferencial exacto `a_Δ(k)` para `Δ ≤ 16` (la «DDT 2-ádica»: Δ = 1 es
la diferencia más fusible, 0,402; con la identidad par→impar
`a_{2m}(k) = a_m(k−1) + a_{3m}(k−1)` exacta) — el instrumento de los
objetivos 3 (cripto) y 4 (relacional); **`notamoscas.txt`** — Moscas
sin Collatz, nota autocontenida completa (la ventana `(0,1)` abierta
POR la criticidad, vía convexidad; contraste supercrítico por Jensen);
y los flujos de la rejilla en `minorizacion.py` (`entra/sale` sube
0,11 → 0,66: el intercambio se hace recurrente, no fuga seca). La
tabla del zoológico en `RutaTeoremas.md` está al día.

**⇢ Y LA TERCERA PASADA cerró los flancos que quedaban:**

- **EL COROLARIO DE HALCONAS** (demostrado desde Abejas + Hormigas +
  Moscas, en el encabezado de `minorizacion.py`): **`φ < 1` ⟹ la masa
  viva de TODA banda finita `k ≤ K` tiende a 0** — Abejas da
  sumabilidad (⟹ `M_G → 0`) en la rejilla `{k ≤ K, |u| ≤ x}`, y como
  Moscas es uniforme en `t` para TODO `x`, el limsup queda `≤ B/x^θ`
  con `x` arbitrario: cero. Contrapositivo: **una banda de torre que
  conserve masa viva da `φ = 1`** — y el 93% medido vive en `k ≤ 8`.
  El escenario `φ < 1` exige que toda la masa suba y no vuelva,
  contra la recurrencia de RATAS.
- **OEIS consultada con control** (curl, 09-08): `a_5(k)` y `a_7(k)`
  dan «No results» las dos; el control Fibonacci devuelve `A000045`.
  **Las dos series de la familia NO están catalogadas.**
- **Literatura de los secundarios LOCALIZADA** (búsqueda web; el
  matiz de la casa: *localizado no es leído*): #2 → el caso crítico
  de `X = MX + Q` es Babillot–Bougerol–Elie 1997 + arXiv:2105.04994,
  y los momentos fraccionarios de ecuaciones de recurrencia
  estocásticas tienen paper propio — la vecindad existe, la
  comparación fina pendiente; #3 → Lipmaa–Moriai FSE 2001 (xdp+) y
  «The Additive Differential Probability of ARX» (FSE 2011) es el
  hermano exacto del perfil de `diferenciales.py`; #4 →
  self-composition (Barthe et al.), product programs / ct-verif,
  CtChecker (ECOOP 2024). Punteros escritos en `maquinaria.txt` y
  `notamoscas.txt`.

*Capa 1 del día: un cursor de sqlite reutilizado me hizo «desaparecer»
cuatro tablas de `afirmaciones.db` en el primer listado — verificado
contra `sqlite_master` antes de creerlo. Y el primer borrador de la
tensión en k afirmaba la versión uniforme; la C4 la degradó a dudosa
ANTES de publicarla.*

---

# ⇢ CIERRE DEL 04-08-2026 — EMPEZAR POR `RutaTeoremas.md`, SECCIÓN «EL ESTADO Y LOS PRÓXIMOS PASOS»

**La jornada más larga del repo.** Lo que entró, en una línea cada cosa:

| # | resultado | estatus |
|---|---|---|
| 1 | **Leonas** — la cadena `(k,c)`: seis leyes exactas, el programa entero como sistema simbólico | teorema (leyes en Lean, `p` impar arbitrario) |
| 2 | `a(33)`…`a(36)`, `b(34)`, `b(35)` — la serie más vieja del repo, cinco niveles nuevos | verificado (identidad-teorema, dos caminos) |
| 3 | **Zorras / Lobas / Pumas** — el goal de λ: `λ ≥ 1.9754` y `λ < 2 ⟹ φ = 1` | el autovalor NO separa |
| 4 | **Ovejas** — LaTourette 2007 = nuestros retornos; **un error en su Tabla 4.2** | fe de erratas triple; catálogo a largo 30 |
| 5 | **Ardillas / Nutrias** — los flecos de R muertos; los canales, estructurales | igualdades de enteros |
| 6 | **Tigresas** — la moneda `×1/2 / ×3/2`: perpetuidad crítica κ=1 | demostrado |
| 7 | **Arañas** — la sombra `u = c/3^k`: la torre desaparece | demostrado (354.293 identidades) |
| 8 | **Moscas** — la tensión transferida, uniforme en `t`, autocontenida | demostrado |
| 9 | El **bautizo del zoológico**: 20 nombres asignados, tabla en `RutaTeoremas.md` | convención registrada |

**6 `.lean` nuevos** (cadenakc, perrasconteo, zoologico + los tres de la
madrugada) → **13 en total**, todos núcleo puro, 0 `sorryAx`.
**9 `.py` nuevos** → 52, con 49 cortando con `SystemExit`.
**`afirmaciones.db`: 161 afirmaciones, 42 correcciones** (dos propias de
hoy, las dos cazadas por `SystemExit` en su primera corrida).

**EL PROGRAMA DE LA DENSIDAD QUEDA REDUCIDO A UNA PIEZA: el piso de
absorción por visita** (`p_34 = 0,0457`). Si no se desvanece, `φ = 1`
(Gao–Wu en densidad); si se desvanece, `φ < 1` con techo. **Los tres
ataques, la retaguardia y los peligros anotados están en
`RutaTeoremas.md` — sección «EL ESTADO Y LOS PRÓXIMOS PASOS».**

*Y la lección de método del día, que es una vieja con ropa nueva: el
paso 1 midió «dispersión ⟹ φ < 1» y el paso 2 lo revirtió en una hora
al encontrar el mecanismo. **La medición orienta; el mecanismo decide.**
Por eso ninguna de las tres lecturas heurísticas de hoy entró a la base
sin su etiqueta.*

# ⇢ 04-08 (7): EL TEOREMA DE MOSCAS — LA TENSIÓN, TRANSFERIDA: LAS MOSCAS NO ESCAPAN DE LA TELARAÑA

El paso (ii) del norte, ejecutado (`moscas.py`) — y salió mejor de lo
pedido: **no hizo falta ni citar a Kesten**. Autocontenido:

- **(a) exacto**: en TODO estado vivo (frontera y F4 incluidos),
  `|u'| ≤ m_b·|u| + 1/2` con `(m₀, m₁) = (1/2, 3/2)` — 354.299
  transiciones con `Fraction`, 0 fallos. El vuelco F4, que rompía el
  acople de Arañas, aquí es INOFENSIVO (pendiente 1/2 ≤ 3/2).
- **(b) subaditividad**: para `0 < θ < 1`,
  `S_{t+1} ≤ r_θ·S_t + (1/2)^θ` con `r_θ = ((1/2)^θ+(3/2)^θ)/2 < 1` —
  la ventana entera de momentos fraccionarios está abierta EXACTAMENTE
  porque `E[m] = 1` es la criticidad κ=1 de Tigresas.
- **(c) LA TENSIÓN**: `S_t ≤ B_θ` **uniforme en t** (θ=1/2: 21,8;
  θ=0,9: 46,2) ⟹ la masa viva con `|u| > x` es `≤ B_θ/x^θ` para TODO
  t. Comprobado sobre la cadena real nivel a nivel (t = 1..34), con
  `S_t` medida en [0,38, 1,44] — veinte veces bajo la cota: el teorema
  es holgado; el contenido es la uniformidad.

**Lo que queda, dicho con todas las letras:** (1) si φ = 1 el
condicional a vivo pierde la cota (la masa viva se va a 0); (2) **el
PISO de absorción por visita — la última pieza abierta del programa de
la densidad**. El pre-vórtice `(1, c=1)` pesa 4,6% de la masa de k=1
(Arañas T4): demostrar que ese piso no se desvanece cerraría φ = 1;
demostrar que se desvanece daría φ < 1 con techo. `afirmaciones.db`:
**161**.

# ⇢ 04-08 (6): EL TEOREMA DE ARAÑAS — LA SOMBRA: LA TORRE DESAPARECE DEL OFFSET

El paso (i)+(ii) del norte, ejecutado (`aranas.py`): en la coordenada
re-escalada **`u = c/3^k`**, las cuatro leyes del núcleo colapsan a UNA
pareja — **bit 0: `u' = u/2 + δ`, bit 1: `u' = (3u−1)/2 + δ`** — con
`δ` EXACTA de la tabla `{0, 3^{−k}/2, 3^{−(k+1)}/2, 0}` y la salida a
frontera con `δ = 0`. **354.293 identidades con `Fraction`, 0 fallos.**
El nivel de la torre desaparece de la dinámica del offset: la cadena
es el **IFS de moneda justa `{u/2, (3u−1)/2}` más una perturbación
dominada** (`|δ| ≤ 3^{−k}/2`, masa `2^{−k}` por piso: total sumable,
`Σ 2^{−k}3^{−k}/2 = 1/10`).

**Lo que compra:** el IFS puro cumple TODAS las hipótesis de
Goldie–Kesten i.i.d. (`E[log m] < 0`, `E[m] = 1 → κ = 1`, shifts
`{0, −1/2}`, no-lattice) — **estacionaria única TENSA con cola `1/x`
es teorema estándar citable**. El «no es Kesten» de Tigresas queda
reducido a «Kesten más perturbación sumable»: el blanco técnico de la
próxima sesión es *perturbed random iterated function systems* —
transferir la tensión del IFS a la cadena perturbada, más el piso por
visita (medido en coordenada limpia: el pre-vórtice `(1, c=1)` pesa
4,6% de la masa de `k=1`). Mediciones con etiqueta: distancia CDF
cadena–IFS 0,222 a t=34 (comparación cruda — la cadena condiciona a
no-absorción), cola en `u` con meseta κ=1 en `x = 1..8` y la lejana
en tránsito. Excepción declarada: la frontera (F2 `δ=1/2`, F4 voltea
signo) es la costura, ~6% de la masa. `afirmaciones.db`: **160**.

# ⇢ 04-08 (5): LA PERPETUIDAD CRÍTICA — EL MECANISMO DE LA DENSIDAD, CON NOMBRE — Y b HASTA 35

Los pasos 1–3 del norte, ejecutados en orden (`dispersionc.py`,
`subrenovacionc.py`, `empujarb.py`):

- **Paso 1 — la dispersión de c, medida** (`dispersionc.py`): en las
  visitas a `k = 1`, `E[log₂|c|]` crece DIFUSIVO (incrementos ~0.02 y
  decayendo — tipo `t^0.65`, no deriva lineal), las cubetas relativas
  caen DESACELERANDO, `s_t = masa(1,2)/viva` con exponente local
  `β_t ~ 0.78` a la baja, y — exacto — **c ≡ 0 (mod 3) tiene masa CERO
  en el núcleo**: Komodo 3 en coordenadas de la cadena.
- **Paso 2 — LA ESTRUCTURA DEBAJO** (`subrenovacionc.py`), el hallazgo
  de la jornada: **el TEOREMA DEL MULTIPLICADOR** — en el núcleo y la
  frontera par, cada paso de la cadena es MONEDA JUSTA entre `c → c/2 + s`
  y `c → 3c/2 + s'`: `E[m] = 1` EXACTO, `E[log₂ m] = −0.2075 < 0`.
  **La dinámica de c es una perpetuidad de Kesten CRÍTICA (κ = 1)** —
  el mismo balance 3/2–1/2 que hace `B/A → 2`: la criticidad ES la
  constante del problema. Única excepción: la frontera impar (ambas
  ramas |m| = 3/2, una con vuelco de signo) — la bomba de reentrada.
  Y **las leyes mod 3**: cada puerta de entrada al núcleo trae su clase
  (directa → `c ≡ 2`, vuelco → `c ≡ 1`; nunca 0), y la absorción
  `(1,1)` vive en la clase del vuelco — **la puerta que funde es la del
  vuelco**. El reparto 1:2 medido en `k = 1` es la huella de las dos
  puertas. LECTURA (etiquetada, no teorema): κ = 1 ⟹ estacionaria
  tensa de cola `1/x` ⟹ piso de absorción por visita ⟹ con el paseo
  recurrente, φ = 1 (Gao–Wu) — el «escape» del paso 1 sería
  convergencia crítica lenta. Por qué no es teorema: los `(m, s)` no
  son i.i.d. (el shift crece `3^k` con la torre) y el piso exige
  uniformidad. La cola medida (bandas diádicas) aún está en formación
  a t = 34: bandas medias ~0.5, cola lejana llenándose.
- **Paso 3 — b empujada dos niveles** (`empujarb.py`): por la
  identidad-teorema con los pisos (control: G/H de 31 y 32 clavan
  `segundocamino.py`): **`a(35) = 15.188.796.435`,
  `a(36) = 30.516.174.184`, `b(34) = 71.181.933`,
  `b(35) = 138.581.314`** — razones 1.9432 → 1.9452 → 1.9469, subiendo
  como exige la cota demostrada λ ≥ 1.9754. Densidad:
  `a(36)/2^36 = 0.4441`.

**El estado del programa tras la jornada completa: la pregunta de la
densidad tiene MECANISMO CON NOMBRE** — una perpetuidad de Kesten
crítica con dos puertas mod 3 — y el blanco con forma de teorema que
queda: (i) formalizar la perpetuidad sobre la medida de las palabras
(los shifts de torre pesan `2^{−k}·log 3^k`, sumable); (ii) demostrar
la tensión (o refutarla) — eso decide φ = 1 contra φ < 1; (iii) el
piso de absorción por visita, uniforme. Todo lo demás — λ, ρ, ε_torre,
la razón 2 — quedó reducido a esto.

# ⇢ 04-08 (4): EL GOAL DE LAMBDA — RESPONDIDO CON INVERSIÓN — Y EL ERROR EN LA TABLA DE 2007

El /goal («termina cuando sepas si λ < 2») cerró en dos ficheros
(`matriztransferencia.py`, `retornoslambda.py`), y la respuesta tiene
más filo que la pregunta:

- **VEREDICTO: λ NO es estrictamente menor que 2.** Tres piezas:
  (1) **cotas inferiores demostradas por truncados** (los caminos del
  truncado son caminos reales): λ ≥ 1.7400 → 1.8667 → 1.9336 → 1.9556
  → 1.9675 → **1.9754** (K=11), gap hacia 2 achicándose ×0.5–0.75 por
  escalón; la b-razón medida (1.9432 en t=33) está DEBAJO de la cota
  demostrada — las razones deben seguir subiendo al menos hasta 1.9754;
  (2) **el lema de la libertad** (test exacto): la única absorción de
  la cadena es (1,1)-bit1 — ningún truncado finito puede demostrar
  λ < 2; (3) **EL TEOREMA DE INVERSIÓN**, que es el hallazgo:
  `b(t+2) >= N_t(1,2)` (enteros, verificado: el estado (1,2) fusiona
  en 2 pasos exactos) y la fracción viva en (1,2) está acotada
  (s_t ≥ 0.015 medido) ⟹ **si φ < 1 entonces λ = 2**. Contrapositivo:
  **λ < 2 ⟹ φ = 1 (Gao–Wu CIERTA)**. El atajo del goal se INVIERTE:
  demostrar λ < 2 no daría f < 1 — daría f = 1. En ambos mundos λ no
  separa; el autovalor no rodea el paseo, desemboca en él.
- **EL CRUCE LaTOURETTE, CERRADO — y con hallazgo bibliográfico.** La
  tesis entera bajada a `lecturas/latourette2007/` (51 págs. del visor
  de Yumpu). Sus «blocks» (Tabla 4.1) son los PRIMEROS RETORNOS del
  par a gap 1 con orden conservado, y sus «strings» (4.2) los retornos
  con vuelco: 21/21 y 26/27 clavados contra la cadena, largo a largo.
  **La entrada que falla es un ERROR EN SU TABLA de 2007**: la L11
  (00011100101, 10110100010) — marcada * «newly found» — toca gap 1 en
  t = 9 (su prefijo ES su propia entrada L9) y viola su Definición 4.
  Verificado triple: formal, realizable, fuerza bruta mod 2^11. El
  conteo bueno de L11 es 19, no 20. La cadena extiende su catálogo a
  largo 30 (eran 48 entradas a mano; ahora la serie completa:
  1,0,0,1,1,3,5,6,11,19,31,55,98,176,313,578,1099,2047,3847,...).
- Los `.lean` VIEJOS compilados (regla del goal): `cotatramos` (el 221
  por el núcleo, sin axiomas), `cotatramos3n1`, `espejoak`,
  `pruebaresta`, `atacacst` — todos limpios, 0 `sorryAx`.
- Los PDF del usuario, identificados: `LaTourretteMiWasho.pdf` es
  **Elia–Tucker 2015** (ya leído por el programa); `SinAsunto.pdf` es
  IJNRD 2023 (Bhat) que afirma «la conjetura se demostró en 2021» —
  falso, no es fuente. La tesis real vino del visor.
- **γ en forma cerrada / ε_torre por álgebra**: NO alcanzables por esta
  vía — eran el premio condicional a λ < 2, y λ = 2 (salvo Gao–Wu
  cierta, que responde el programa entero). La cota honesta que queda:
  bajo la cola de balota del paseo (α = 3/2), φ ≤ ~0.585 (impresa en
  `matriztransferencia.py` C4, heurística declarada).

# ⇢ 04-08 (3): LA RETAGUARDIA Y LOS CANALES — TRES .LEAN NUEVOS, LOS FLECOS MUERTOS, e6 A 29 NIVELES

La continuación de la sesión de la cadena ejecutó los puntos 2 y 3 del
norte, todo local (Python + Lean, sin agentes):

- **`cadenakc.lean` (11º)**: LAS SEIS LEYES DE LA CADENA con
  coeficiente impar ARBITRARIO `p` (más general que `3^k`) — N1–N4,
  la ley de la moneda, el vórtice `(1,1)`, el vuelco F4 y la escalera
  `p → 3p` con `piso_impar` por inducción. Núcleo puro, 0 `sorryAx`.
  **Cierra «el k general del Lean de torre» en su forma fuerte.**
- **`flecosr.py`**: los flecos ±1 de la serie `R`, RESUELTOS. `F(j)` =
  primeras visitas de la cadena a `(0,1)` desde la forma h `(2,−1)`
  clava el R publicado en `j = 3…9`, y la identidad
  `c(m) = Σ F(j)·a(m−j) + D(m)` cierra como igualdad de enteros en 26
  niveles — el R publicado deconvolvía SIN el término directo `D`
  (fusiones al vórtice sin pasar por consecutivo; despierta en j = 13):
  eso eran los flecos. La contabilidad de orientación bajo vuelcos ya
  no hace falta. Y `c(m)` extendida a `m = 26` (era 16).
- **`perrasconteo.lean` (12º)**: el esqueleto aritmético del conteo de
  Perras — suma de ventanas `= 2^m − 1`, el borde alternante
  `3^m mod 4`, y `exactamente_uno` (los dos residuos frontera deciden
  en sentidos opuestos para todo m). 0 `sorryAx`.
- **`zoologico.lean` (13º, orden del usuario: portar lo que vivía solo
  en .txt)**: el núcleo de JIRAFAS entero (`jirafas_coeficientes` —
  igualar afines en dos puntos — más `pow3_inyectiva`, compuestos en
  `jirafas_nucleo`), las potencias de 6 de PANDAS, el grafo `{−3,−5}`
  de los CHANCHITOS completo con `D1 = −3` y P3, y la rama h de GATAS
  (`(4t+3,4t+4) → {t+1, 9(t+1)−1}`). 0 `sorryAx`. Los `.txt` quedan
  como documentos; esto es su esqueleto de máquina.
- **`estratoscadena.py`**: LA CONTABILIDAD DE CANALES, ESTRUCTURAL —
  los canales de `e₈` (afirmación 84) son los subárboles de los dos
  primeros bits de la cadena, y la identidad
  `e_s(N) = e_{s−2}(N−2) + e^h_s(N−2) + e^par_s(N−1)` cierra como
  igualdad de enteros en TODOS los niveles y estratos (`s ≤ 12`,
  `N ≤ 29`). No hizo falta Lipmaa–Moriai. Además: **`e₆` cuadrática
  confirmada hasta N = 29** (once niveles más allá de lo medido),
  `e₈` extendida a N = 29 (terceras diferencias oscilando: NO cúbica,
  definitivo), y `e₁₀`/`e₁₂` medidas por primera vez.
- **`segundocamino.py`**: `a(33)` y `a(34)` SOSTENIDOS — cumplen la
  identidad-teorema `a(k+2) = a(k) + (2^k−1) + G(k) + H(k)` en
  `k = 31, 32` con `G` y `H` de barridos separados de los pisos g y h
  (`G(32) = 691.256.829`, `H(32) = 701.445.504`).

**Bloqueado en local**: el cruce LaTourette (21+27 pares) — sus tablas
4.1/4.2 nunca se descargaron; hace falta el PDF (yumpu pags. 28–31 o
el correo a Fraboni/Moravian).

**Deuda de conteos**: +4 `.py` (paseodeladeuda, flecosr,
estratoscadena, segundocamino) y +3 `.lean` (cadenakc, perrasconteo,
zoologico → 13 en total). El `CLAUDE.md` ya venía desfasado de la
jornada anterior (dice «cinco .lean»); pendiente una pasada de
conteos completa.

# ⇢ 04-08 (2): LA CADENA (k, c) — EL PROGRAMA ENTERO ES UN SISTEMA SIMBÓLICO, Y a(k) SE EXTIENDE A 34

El ataque al punto 1 del norte («¿el paseo de la deuda es recurrente
sobre las clases?») produjo algo más grande que la pregunta:
**`paseodeladeuda.py` — LA CADENA (k, c)**. Todo estado de par vivo es
una forma `{v, 3^k·v + c}` (núcleo `k >= 1`) o `{v, v+g}` (frontera
`k = 0`), y la dinámica entera son SEIS LEYES exactas de una línea,
decididas por un solo bit fresco (la paridad del menor — la moneda de
Terras). Verificadas en 181.400 instancias, 0 fallos. El zoológico
COMPLETO son estados de esta cadena: la contracción de Gatas es el lazo
`(0,1) -1-> (1,-1) -1-> (0,1)`, la ventana de Perras es
`(0,1)->(1,2)->lazo->(1,1)`, el vórtice es `(1,1)` (D = 0 es c = 1), el
rebote `{w,9w+2}` es `(2,2)`, la forma h es `(2,-1)`, las puertas P1-P3
y la torre T1/T2 son transiciones, y el grafo `{-3,-5}` de los
chanchitos es el par de estados `(1,-2)/(1,-4)` (D = c-1).

**La consecuencia dura: el barrido SIMBÓLICO de la cadena reproduce
a(k) EXACTO sin tocar un solo par** — contra la sucesión publicada y el
recomputo directo (k = 3..14), y contra b(k) entera (k = 3..31,
incluida la cola del barrido a 2^32: b(31) = 9.701.007, clavada). Y
como la renovación coalesce estados (7,7 millones de estados donde el
barrido de restos necesitaba 2^34 = 17 mil millones), **la serie se
extiende DOS NIVELES nunca calculados:**

```
a(33) = 3.761.106.610    b(32) = 18.831.364    razon 1,9412
a(34) = 7.558.807.251    b(33) = 36.594.031    razon 1,9432
```

*(estado: el cruce k <= 32 es exacto, y los dos niveles nuevos quedaron
SOSTENIDOS la misma sesión por `segundocamino.py` — la identidad-teorema
con G y H de barridos separados; ver la entrada 04-08 (3).)*

**Y la respuesta a la pregunta del norte, hasta donde la medición
llega (comprobación 5):** a profundidad 34, la masa viva por nivel de
torre decae geométricamente — 93% en `k <= 8`, menos de 0,07% en
`k >= 15`. **La torre NO retiene masa: el paseo en k vuelve, también
sobre las clases.** La obstrucción a `phi = 1` queda localizada en la
DISPERSIÓN DE c sobre la frontera y el núcleo bajo — la pregunta del
programa cambia de forma: ya no es «¿vuelve el paseo?» (vuelve), sino
«¿la órbita de c en las visitas a k = 1 se concentra o se dispersa?».

# ⇢ EL CIERRE DEL 04-08: EL TEOREMA MOD 3 — DEMOSTRADO, FORMALIZADO, Y EL 6º .LEAN

La jornada post-rigor-mortis cerró con la pieza redonda: **el TEOREMA DE KOMODO 3** (el mod 3) — tras el paso 0 el lado mayor es siempre `≡ 2 (mod 3)` (base
en ambas paridades) y «mayor no múltiplo de 3» es invariante para
siempre. Con él, **el fenómeno de los aterrizajes queda CERRADO** (el
módulo `|D| = 2^j` era definicional — corrección 39 —, el signo es este
teorema), y las dos mitades del laboratorio (los rayos mudos del árbol
inverso y la dinámica de pares) se tocan en un teorema común.
**Y está FORMALIZADO: `teoremadekomodo3.lean`**, el sexto `.lean`, núcleo
puro, 0 `sorryAx` — el primer teorema del programa de fusión con
verificación de máquina (sugerencia de la revisión externa, ejecutada
la misma noche). Test R34 en `auditoria_rigor.py` (34/34).

La foto honesta del día, en palabras del revisor: *«cuatro teoremas
nuevos, seis conjeturas muertas, 39 correcciones y una frontera
dibujada donde se sabe qué está demostrado y qué está solo medido»* —
más `e₆` cuadrática confirmada en tres niveles vírgenes, la escalera
fallada en `e₈` y registrada, LaTourette verificada (Perras ES nuevo),
y Komodo 3 rematado en Lean.

**Pendientes con método, para sesión fresca**: (1) la contabilidad de
canales de `e₈` (Lipmaa–Moriai 2001 como herramienta sugerida);
(2) formalizar el conteo `2^{m−1}` de Perras (el 7º `.lean`);
(3) el cruce LaTourette (21+27 pares) ↔ nuestros gérmenes.

# ⇢ LA AUDITORÍA RIGOR MORTIS (04-08): 30/30, TODA AFIRMACIÓN CON SU TEST

Orden del usuario: auditar HACIA ATRÁS — ninguna afirmación del día sin
test exacto de enteros en fichero del repo. Hecho, local, sin agentes:
**`auditoria_rigor.py`** — 30 tests numerados (R01–R30) con `SystemExit`,
**30 de 30 PASS**, más la re-certificación de `nuevasfusion.py`,
`identidadexacta.py` y `masasdeclase.py` (exit 0 los tres). Las
afirmaciones que solo tenían mediciones ad-hoc (fórmulas `b₄`/`c₄`,
germen único, preludios y huecos, aterrizajes, grafo `h`, puerta `g`,
torre, gasto, ley mod 3, la doble corrección) tienen ahora test
permanente y reproducible, con rangos declarados. La R30 reproduce la
doble corrección con números frescos (`f₀` del 33: 10.372; `+16`→consec:
7 en `r < 2^16`). **El día queda auditado entero.**

Sobre la supresión del `j = 3`, el estado FINAL tras las correcciones:
la ley mod 3 (cruda, R29) mata `D = 11`; el `+16` SÍ ocurre en crudo y
la supresión real es de contabilidad de `S` bajo el filtro de fusión de
clase — conjetura puntual: «un aterrizaje `+16` no puede saldar
`ΔS = +2`». Corrección nº 37 con su lección: medir sin el filtro antes
de conjeturar inalcanzabilidad.

# ⇢ LA TABLA FINAL DE LA JORNADA 03/04-08 (para empezar mañana por aquí)

| # | resultado | estatus |
|---|---|---|
| 1 | **Perras** — `\|M\|=2 ⟺ stems de Garner` + conteo `2^{m−1}` con borde | teorema; novedad verificada (Garner/E-T/LaTourette) |
| 2 | **Gatas** — contracción literal + reinicio uniforme + ecuación de renovación | teorema; (a) en Lean |
| 3 | **Jirafas** — fusión balanceada ⟺ evento de clase (ida + recíproco) | lema-caracterización; C1 retirado, C2 demostrado |
| 4 | **Pandas** — igual altura ⟹ mismo índice; `φ = d` (puente a Gao) | lema condicional (`Res < 3`; incond. < 2^71) |
| 5 | **3 Chanchitos** — `b₄ = 7·2^{m−7}−m+4`, `c₄ = 6·2^{m−7}−m+4` | teoremas ∀m (grafo + puertas + torre + gasto) |
| 6 | **Komodo 3** — mod 3: base + invariancia + inducción `komodo` | teorema EN LEAN (núcleo, 0 sorry) |
| 7 | `e₆ = 3 + T(N−8)` | confirmada por predicción (N=16–18) |
| 8 | Identidad entera `a(k+2) = a(k)+(2^k−1)+G+H`; `G=Σb`, `H=c` | teorema verificado (anti-tautología) |
| 9 | Recursión vertical `e_s\|_{r≡1} = e_{s−2}(N−2)` | 4/4 + motor en Lean + espejo 4/4 |
| 10 | Contabilidad de `e₈` = vertical + par (acum.) + r≡3 (directo) | exacta 4 niveles |
| 11 | Sistema de φ: `φ=(1+β+γ)/3`, `β=γ/2+(φ+γ)/8+ε`, `γ=ρφ` | 1ª demostrada; 2ª 11/11 dos implementaciones; 3ª deconv. exacta |
| 12 | **`φ = 8(1+ε)/(23−13ρ)`; `φ=1 ⟺ ε_torre=1/4 ⟺ paseo recurrente`** | la reducción final del programa |
| 13 | Serie `R` = gérmenes de reentrada (1,0,1,3,2,4,9,14,25,47,89) | deconv. exacta; razones → 2 |
| 14 | Paseo de la deuda: 3 leyes de torre; torres gemelas ±; monedas de Terras | leyes exactas; recurrencia = heurística |
| 15 | Lemas menores: vórtice-iff, arranque D₁=1, C≡3^q, repunit, unicidades, huecos, gasto, P1–P3, T1/T2, aterrizajes | demostrados (varios en Lean) |

**Lean nuevos hoy (5)**: `teoremadekomodo3`, `lemasdeperras`, `contracciondegatas`, `recursionvertical`, `torredeladeuda` — 10 en total, todos núcleo puro.
**Muertas por los instrumentos (~12)**: familia fantasma, C1 de Jirafas, cierre 0.4504, supresión j=3 (×3), ley (−2)^j independiente, escalera e₈ cúbica, `Res<6`, `c(m−6)`, ε omitido, preludio doble, orden del +16.
**Infra**: `auditoria_rigor.py` (35 tests R01–R35), 6 docs de revisión externa, 147 afirmaciones, 41 correcciones.
**MAÑANA**: el paseo de la deuda — ¿recurrente sobre las clases? (= Gao–Wu). Y la retaguardia: k general del Lean de torre, flecos de R, Perras-conteo en Lean.

# ⇢ EL GRAN CIERRE DE LA MADRUGADA DEL 04-08: LOS TRES ÁTOMOS Y LAS DOS FÓRMULAS

La ráfaga de investigación abierta terminó con la estructura completa:

- **Los tres átomos del programa, los tres universales y demostrados**:
  el grafo `{−3, −5}` (todo `w` impar), la ventana de Perras (todo `k`),
  y el lema general de la torre 3-ádica (todo `k`, `T1`/`T2`).
- **Las dos fórmulas cerradas, TEOREMAS COMPLETOS**:
  `c₄(m) = 3·2^{m−6} − m + 4` (vía el grafo, `D₁ = −3` constante) y
  `b₄(m) = 7·2^{m−7} − m + 4` (vía la puerta: `g` entra a `h` en un
  paso, el hueco en 5 es la imagen del hueco en 4, la torre gasta
  mixtos y no toca el estrato 4, y la suma de ventanas cierra el
  álgebra). **Las masas exactas del estrato mínimo de las
  sub-renovaciones están completas.**
- **Los dos pisos son EL MISMO piso con puertas distintas** — toda la
  asimetría `g`/`h` es la aritmética de la puerta.
- Leyes con masa: aterrizajes en potencias de `(−2)` (~66.000 casos,
  cero prohibidos), supresión del `j = 3` (conjetura aplastante),
  reentrada total (107/107).
- Y ~10 correcciones propias cazadas por los instrumentos en la misma
  ráfaga, todas registradas.

**`afirmaciones.db`: 122 afirmaciones.** Los hilos que siguen: la
formalización fina (palabra ↔ clase vía Terras) de los dos teoremas; la
demostración de la supresión del `j = 3`; los estratos superiores con
la gramática de tres átomos; y las masas al sistema de `φ`.

---

# ⇢ 03-08-2026 — LA ECUACIÓN DE LAS NUEVAS, y dos agujeros cerrados

Sesión de lectura completa del repo + visita a OEIS, y después tres entregas
**todo local** (Lean + Python, sin agentes — orden del usuario por presupuesto):

1. **`nuevasfusion.py` (fichero nuevo): las clases nuevas de `b(k)` tienen
   ECUACIÓN.** Una clase se estrena en el nivel `k+1` exactamente cuando
   `T^k(r)` y `T^k(r+1)` se encuentran **por primera vez en un vórtice**
   (`a = 3b+1`, paridades opuestas, `S` compensada en 1 — la regla del
   segundo padre del 221). Caracterización **con recíproco**, `k = 3…15`,
   0 fallos y 0 falsos positivos; reproduce `b(k)` término a término.
   **La pregunta de la razón 2 deja de ser un conteo ciego.** Precedente
   encontrado en OEIS: `A076227`/`A100982` tienen recursión exacta
   (Zarubin 2019, Winkler) vía los saltos de `Smin` — la continuación es
   derivar la recursión de `b(k)` contra esos saltos, que son las
   semiconvergentes de `log₂3` ya certificadas en `verificar_ciclos.py`.

2. **`franjaeverett.py` NO COMPILABA** (dos strings sin cerrar en las líneas
   542 y 589: texto adversarial del 01-08 pegado dentro de un `print`). **El
   fichero nunca había corrido en su forma actual.** Reparado y corrido
   entero, exit 0: la afirmación enterrada **se confirma contra su propia
   tabla** — `M = 5, 9, 101, 1001, 10001` empatan a 0 excepciones reales
   (hasta `10⁶`; los «sin certificar» son exactamente los impares `< M`), y
   con `M = 10001` el umbral baja a **1,585011**, a `4,8e-05` de `log₂3`.
   Detalle nuevo que la tabla regala: **`M = 27` tiene 2 excepciones
   reales** (14 sin certificar contra 12 impares `< 27`) — el único de la
   lista que no empata, y nadie sabe cuáles son ni por qué. Salida completa
   en `franjaeverett_salida.txt`.

3. **El hueco Lean↔Python de `atacacst` está cerrado.** `tramo_finito` sólo
   cubría `m > T^k(r)` y el `.py` decide con `m > T^k(r) − r`: la franja
   intermedia no tenía teorema. Nuevo **`tramo_finito_fino`** en
   `atacacst.lean` (tres líneas desde `palanca`, hipótesis sin resta
   truncada: `T^k(r) < r + m`), compilado, `#print axioms` limpio.

De OEIS: **`a(k)` y `b(k)` siguen sin estar** (consultadas hoy con los
términos correctos — la primera consulta usó colas mal recordadas y la cazó
la capa 1 — y control Fibonacci que devuelve `A000045`). El rincón está
vivo: comentario de jul-2026 en `A076227` (Hikawa: palabras binarias con
`2^m < 3^(suma parcial)`) y tres preprints 2026 sobre vectores de paridad.

## ⇢ Y EL PASO SIGUIENTE SE DIO LA MISMA SESIÓN: los vórtices, tabulados

Midiendo QUÉ vórtices producen las nuevas (`k = 3…15`) salieron dos cosas,
y la capa 1 las separó en el acto:

- **DEMOSTRADO — la familia extremal.** El `b` máximo de cada nivel es un
  **repunit ternario** (`13, 121, 1093, 9841, 88573, 797161 = (3^m−1)/2`,
  `m` impar) y el resto extremal es el par «casi todo unos»: **para todo
  `j` par, `(2^j−2, 2^j−1)` se funde por primera vez en el paso `j+2` con
  vórtice en `b = (3^{j−1}−1)/2`**. Demostración de cuatro líneas (está en
  la COMPROBACIÓN 5 de `nuevasfusion.py`), comprobada `j = 4…60`.
  **Corolario: `b(j+2) ≥ 1` para todo `j` par — las nuevas nunca se
  acaban.** Que ese `b` sea el máximo del nivel queda medido, no demostrado.
- **REFUTADO ANTES DE PUBLICARSE — «todo `b` es `1 mod 3`».** Vale hasta
  `k+1 = 14` y se rompe en `k+1 = 15` con `b = 2255 ≡ 2 (mod 3)`
  (`r = 16891`). Era muestra chica. Quedó anotado en el fichero para no
  rederivarlo.

`afirmaciones.db` regenerada: **84 afirmaciones** (las 4 de hoy: ecuación
de las nuevas, familia extremal, `tramo_finito_fino`, franja `M = 10001`)
y **33 correcciones** (la del fichero que no compilaba).

## ⇢ Y LA SEGUNDA VUELTA ENCONTRÓ LA FORMA DE LA RECURSIÓN: los estratos

Estratificando las nuevas por el número `|M|` de **pasos mixtos** (paridades
del par distintas ⟺ diferencia impar), comprobación 6 de `nuevasfusion.py`:

- **`|M|` es PAR siempre** (779 de 779; demostrable en tres líneas — `ΔS`
  cambia ±1 sólo en mixtos y vuelve a 0).
- **El estrato `|M| = 2` tiene EXACTAMENTE UNA clase por nivel, y es la
  familia del repunit** (verificado a mano en `(14,15)` y `(22,23)`).
  `|M| = 4` también exactamente una. Las dos unicidades: medidas, no
  demostradas.
- **Los estratos altos crecen como polinomios de grado creciente** (`|M|=6`
  termina con diferencias 5,6,7,8: cuadrático) y **entra un estrato nuevo
  cada dos niveles**. O sea: la razón `b(k+1)/b(k) → 2` vendría de la
  ENTRADA de estratos, no de que ninguno acelere — **el triángulo tipo
  Pascal que Zarubin encontró para `A076227`, ahora con candidato propio.**

## ⇢ Y LA PRIMERA FILA DEL TRIÁNGULO QUEDÓ DEMOSTRADA la misma noche

**TEOREMA (comprobación 7 de `nuevasfusion.py`): en cada nivel `k+1 ≥ 4`
hay EXACTAMENTE UNA clase nueva con `|M| = 2`** — `r = 2^{k−1}−2` si `k`
impar, `r = 3·2^{k−1}−2` si `k` par, alternando. Demostración en cuatro
piezas (está entera en el comentario): `|M| = 2` fuerza `r` par; la
diferencia pierde exactamente un factor 2 por paso compartido, luego
`v₂(r+2) = k−1` deja **solo dos candidatos**; el ganador cumple el
encuentro con la identidad `T(c·2^m − 1) = 3c·2^{m−1} − 1`; y el perdedor
falla siempre (su vórtice pediría `3^q − 1 = 3^{q+2} − 1`). Comprobado
hasta `k = 60`, más la unicidad completa por fuerza bruta en `k ≤ 15`.
**La primera fila del triángulo de estratos es `1, 1, 1, …` para siempre —
la primera pieza demostrada del mecanismo «la razón 2 viene de la entrada
de estratos».** `afirmaciones.db`: **86 afirmaciones, 47 demostradas.**

## ⇢ Y LA REDUCCIÓN ENTRE ESTRATOS, DEMOSTRADA: |M|=4 es un |M|=2 con preludio

La hipótesis «el estrato `|M| = 4` es el perdedor prolongado» **falló**
(capa 1, 12 de 12 en contra) — y lo que salió es mejor. El ganador de
`|M| = 4` es **el vecino izquierdo del perdedor** (`2^{k−1}−3` / 
`3·2^{k−1}−3`, con `r` IMPAR — justo el caso que `|M| = 2` excluía), con
mixtos siempre en `[0, 1, 2, k]`. Y al derivarlo salieron dos teoremas
(comprobación 8 de `nuevasfusion.py`, exit 0):

- **LEMA GENERAL**: para `C` impar con `C ≡ 3^q (mod 4)`, el par
  `(C·2^q−2, C·2^q−1)` se funde exactamente en el paso `q+2`, `S = q`,
  vórtice en `(3^{q−1}C−1)/2`. Los casos `C = 1, 3` son la alternancia
  del teorema de `|M| = 2`. Comprobado en ~2.000 pares (`C ≤ 201`,
  `q ≤ 40`).
- **FAMILIA `|M| = 4`**: los dos primeros pasos **contraen el par a
  consecutivo otra vez** (`d₂ = 1`), dejándolo en el lema con `C = 3c`,
  `q = k−3`. **Los estratos se reducen unos a otros** — `|M| = 4` es dos
  mixtos de preludio más un `|M| = 2` desplazado. *Esa reducción es la
  forma de la recursión del triángulo.* Comprobada `k = 4…60`. La
  unicidad de `|M| = 4` sigue **medida** (1 por nivel, `k ≤ 15`).

`afirmaciones.db`: **88 afirmaciones, 49 demostradas.**

## ⇢ EL MAPA DE DEPENDENCIAS ENTRA A LA BASE, con su regla (orden del usuario)

`afirmaciones.db` tiene ahora **dos tablas nuevas: `nodos` (14) y
`dependencias` (20 aristas)** — el árbol del programa de las nuevas, de
`definiciones` hasta `recursion_bk`. Y la **REGLA DEL AVANCE**, en código
(`COMPROBACION 0` del generador, corta con `SystemExit`): un nodo
`demostrado` no puede depender de un nodo no demostrado; nada trabajado
puede depender de un `pendiente`; y los pendientes se listan `AVANZABLE`
sólo con todos los padres demostrados. Hoy: `cuadratica_M6` y
`recursion_bk` están **BLOQUEADOS** — porque `unicidad_M4` sigue en
`medido`. La regla se aplicó a sí misma en el acto: el nodo
`M4_ruta_impar` no se registró como demostrado hasta que la comprobación 9
compiló y pasó.

## ⇢ Y LA RUTA IMPAR DE |M| = 4, DEMOSTRADA (comprobación 9)

- **`r` impar ⟹ pasos 0, 1, 2 mixtos** (`|M| ≥ 4` siempre) — el reverso
  exacto del teorema de `|M| = 2`. Exhaustivo `r < 2^14`.
- **La contracción es exacta**: con `r ≡ 1 (mod 4)`, el par vuelve a ser
  consecutivo en el paso 2, con menor `(3r+1)/4`.
- **Unicidad dentro de la ruta**: tras la contracción se aplica entero el
  argumento de `|M| = 2` — `v₂(s₂+2) = k−3`, rango `C ≤ 11`, necesidad
  `C ≡ 3^{k−3} (mod 4)`, y `r` entero exige `3 | C`: quedan `C ∈ {3, 9}`
  y el mod 4 elige **uno**. `k = 5…60`.
- *Capa 1 se cobró dos descuidos míos en el chequeo (no en la matemática):
  comparaba la contracción tras 3 pasos en vez de 2, y medía el exit del
  `grep` en vez del de python.*

`afirmaciones.db`: **89 afirmaciones, 50 demostradas, 14 nodos, 20
aristas.**

## ⇢ LA COORDENADA D — la herramienta nueva — y la ruta `r ≡ 3 (mod 4)` excluida

Al atacar la exclusión salió **la coordenada del programa entero**:
`D = g − 2s − 1` (gap menos dos veces el menor, menos uno). Tres hechos,
demostrados en el comentario de la comprobación 10:

- **el vórtice es exactamente `D = 0` con `s` impar** (con `s` par el
  mixto es β, que agranda el gap y no fusiona nunca);
- **en compartidos `D` es impar y evoluciona afín**: `(D−1)/2` o
  `(3D−1)/2`; el tramo termina cuando `D` se hace par, y el mixto que
  sigue es vórtice si y sólo si ese `D` es 0;
- **`D < 0` es invariante** — quien entra en negativo no vuelve.

Con eso: `r ≡ 3 (mod 8)` cae en `D₃ = −3` (par tras tres mixtos:
`{(3r+7)/8, +(3r−1)/4}`) y su cuarto mixto **nunca** es vórtice;
`r ≡ 7 (mod 8)` encadena cuatro mixtos seguidos. **EXCLUIDAS de
`|M| = 4`** (exhaustivo `r < 2^15` + seguimiento del tramo completo).
Junto con la comprobación 9: **la unicidad de `|M| = 4` está demostrada
para TODO `r` impar.** Falta sólo la ruta `r` par (medida, `k ≤ 15`) —
`unicidad_M4` sigue en `medido` y el mapa mantiene `cuadratica_M6`
BLOQUEADO. *La D convierte «se funden» en «D llega a 0», y los estratos
en la contabilidad de sus rebotes — ésa es la reformulación con la que
seguir.*

`afirmaciones.db`: **90 afirmaciones, 51 demostradas.**

## ⇢ LA COORDENADA E — autónoma de verdad — y la ruta par acorralada

Mejorando la D salió **`E = D − 3s`, que dentro de un tramo compartido
es un mapa 1-dimensional determinista**: su propia paridad elige su
regla (`E` impar → `(E−1)/2`, `E` par → `(3E−4)/2`), sin mirar los
valores. Con eso (comprobación 11, exit 0):

- **La órbita del rebote es forzada**: un par con `r` par arranca en
  `D = 1`, su primer mixto llega exactamente en `D = 0`, y si rebota
  (`s` par) entra en `E = 1` → `1, 0, −2, −5, −3` y el ciclo
  `(−2, −5, −3)` para siempre.
- **El vórtice directo del rebote es IMPOSIBLE**: exigiría
  `(E, s) = (−3, 1)` — el par `{1, 4}` — y la cadena hacia atrás,
  forzada por las paridades de la órbita, pide `(2·4−1)/3 = 7/3`. No es
  entero. *(Consistente con `|M|` par; la E lo re-demuestra por vía
  independiente.)*
- **El límite honesto, que es el `+1` reapareciendo**: en los pasos
  MIXTOS ni `D` ni `E` son autónomas — ahí entra el valor. Por eso el
  patrón `[0, rebote, m₃, vórtice]` de `r` par queda ABIERTO en general.
- **Acorralado con barrido dirigido** (pares sueltos, sin construir
  `buenas(k)`): entre las más de 300.000 fusiones con `S` igualada de
  pares `r` par `< 2^20`, **el estrato `|M| = 4` está VACÍO** — el
  diccionario salta de `|M|=2` a `|M|=6`. Y una perla medida: los
  `|M|=2` son exactamente `2^18` — la mitad exacta — huele a biyección
  de Terras, anotado sin demostrar.

`afirmaciones.db`: **91 afirmaciones, 52 demostradas.** `unicidad_M4`
sigue `medido` (solo falta el patrón de 4 mixtos con `r` par);
`cuadratica_M6` sigue BLOQUEADO.

## ⇢ EL TERCER MIXTO CLASIFICADO, Y EL CENSO DE LAS DIEZ FAMILIAS DE E

**Comprobación 12** — el tercer mixto de `r` par, clasificado entero con
`(D, E)` (dentro de un tramo el par es determinista y `s = (D−E)/3` se
recupera): **caso A** (`w` impar: mixto inmediato) cae en
`D' = −(3w+1)/2 − 1 < 0 → excluido, DEMOSTRADO`; **caso B-α** (tramo
rebotado terminando en `E ∈ {1, −5, −3}`) cae en `D' = D/2 − 3s − 2 < 0
→ excluido, DEMOSTRADO`. **La única puerta que le queda a un `|M| = 4`
con `r` par es la rama B-β** (`E ∈ {0, −2}`), abierta en general (árbol
2-ádico) y acorralada doble: ningún `(w, 6w+2)` con `w < 2^16` funde en
su segundo mixto, más el barrido real a `2^20`.

**Comprobación 13 — el censo, de la idea del usuario** (*«toda órbita
relevante de E pertenece a una de N familias»*): el mapa de `E` como
sistema propio sobre `Z` (`impar → (E−1)/2`, `par → (3E−4)/2`) **es de
tipo Collatz**, y su censo en `[−10⁵, 10⁵]` da **DIEZ familias** — fijos
`−1` y `4`, 2-ciclo `(−11)`, 3-ciclos `(−5)` (el del rebote, 47% de la
cuenca) y `(24)`, 5-ciclos `(−77)` y `(−59)`, 11-ciclo `(84)`, 27-ciclos
`(−4163)` y `(−5099)`. **Ninguna órbita escapa.** Aviso de alcance: censo
medido, no teorema — la completitud para todo `Z` es exactamente la
pregunta que en Collatz lleva 90 años abierta. El nodo nuevo
`clasificacion_rutas` (el salto propuesto) queda en el mapa, BLOQUEADO
hasta cerrar `unicidad_M4`.

`afirmaciones.db`: **93 afirmaciones, 53 demostradas, 17 nodos, 26
aristas.**

## ⇢ Y LA RAMA B-β, ITERADA EN EL MAPA (D, E) PURO HASTA u = 10⁷

El cuarto tramo es determinista en `(D, E)`, así que no hace falta
simular pares: comprobación 14 itera el mapa desde las dos familias de
arranque (`(15u+1, 12u+1)` y `(15u−2, 12u−2)`) para `u ≤ 10⁷` — **ninguna
de las 2·10⁷ órbitas termina en `D = 0`**. El acorralado pasa de `2^16`
estados a ~300× más lejos. En papel además: `E < 0` también es
absorbente (mismos mapas que `D`), y el vórtice exigiría pasar por
`(D, E) = (1, 1−3s)` con `s` par — el pre-vórtice tiene forma fija.
La rama sigue **abierta en general** (el árbol 2-ádico de paridades);
`unicidad_M4` continúa en `medido`.

## ⇢ EL VIRAJE (03-08-2026, decisión del usuario, con criterio propio validado)

El usuario preguntó: *«¿qué propiedad nueva tiene `H` que `D` y `E` no
tenían?»* — y la respuesta cerró la vía: **NINGUNA. `H = 2D − E = l − 1`,
el valor MAYOR del par menos 1** (dos líneas de álgebra; por eso sus
mapas eran «otro Collatz»: SON la trayectoria del grande). Corolario:
`D = l − 3s − 1`, `E = l − 6s − 1` — **el estado es 2-dimensional,
`(D, E)` lo genera, no existe tercera coordenada.** Registrado como
afirmación demostrada.

**Decisión:** B-β queda **CONGELADA como problema abierto interno** (era
otro Collatz dentro de Collatz; triple acorralado la respalda). El
programa vira a `clasificacion_rutas`. Dos arreglos honestos al mapa:
la arista `clasificacion_rutas ← unicidad_M4` sobraba (la clasificación
no la necesita), y la regla del avance decía «padres demostrados» donde
el usuario dictó «comprobada» — un censo nunca va a ser teorema y no por
eso bloquea lo que se apoya en él. Ahora: **`clasificacion_rutas` →
AVANZABLE**; `cuadratica_M6` y `recursion_bk` siguen en cola.

## ⇢ EL PASO 1 DE LA CLASIFICACIÓN, HECHO EN AUTONOMÍA (`itinerarios.py`)

*(Sesión con el usuario ausente — «elige las rutas tú misma». Ruta
elegida: el único nodo AVANZABLE del mapa.)* Fichero nuevo con tres
comprobaciones (cruce contra `b(k)` en los 13 niveles incluido), y el
resultado es una de cal y una de arena:

- **POSITIVO — la contracción, visible en las etiquetas**: el último
  tramo de todo `|M| = 4` vive en `{−5, −77, −4163}`, exactamente las
  familias que aparecen en `|M| = 2`. El teorema de la reducción entre
  estratos dejó huella medible.
- **NEGATIVO, y vale tanto como el positivo**: la familia ASINTÓTICA es
  un invariante ruidoso para contar — el tramo solo usa un prefijo
  finito de la órbita de `E`, y la familia mezcla información que el
  tramo nunca ve (conteos por itinerario erráticos, no polinómicos).
  Itinerarios distintos por estrato: 3, 9, 90, 243, 224, 76, 7.
- *Dos conjeturas de un minuto de vida, muertas por la capa 1: «solo
  aparecen familias negativas» (las positivas sí aparecen en estratos
  altos; solo falta el punto fijo `−1`, por cuenca trivial) — y el
  primer tanteo contaba TODAS las fundidas por un `ant = B1` que
  faltaba; lo cazó el cruce contra `b(k)`.*

`afirmaciones.db`: **95 afirmaciones.** Conteos del `CLAUDE.md`: **38**.

## ⇢ EL REINICIO UNIFORME, LA ECUACIÓN DE RENOVACIÓN — Y EL FANTASMA QUE CAZÓ

**TEOREMA DEL REINICIO UNIFORME (comprobación 16):** la contracción manda
`r = 4t+1` al par consecutivo **fresco** `(3t+1, 3t+2)`, y `t ↦ 3t+1` es
biyección de `Z/2^m` — **la autosimilitud del problema de fusión es
exacta**, `P(fusión | contracción) = f`. Y el `w` del rebote es uniforme
(Terras 1.2). Corolario: la **ecuación de renovación exacta**
`f = 1/4 + f/4 + g/4 + h/4`, con `f ≥ 1/3` demostrado en tres líneas.
Si `g` y `h` se calculan exactos al estilo Perras, **`f` queda decidida —
y `f = 1` sería la conjetura de Wu en densidad**: el pez gordo tiene
nombre y ecuación.

**Y LA ECUACIÓN TRABAJÓ DE DETECTOR EN SU PRIMER USO.** No cerraba
(`0,4039` contra `0,4453` medido), y perseguir la discrepancia destapó
**una familia fantasma**: el estado con `D = 0` es el par `{s, 3s+1}` y
su rebote real es **`(w, 9w+2)`** con `E = 3w+1` — no el `(w, 6w+2)` con
órbita `E = 1` de las comprobaciones 11 (corolario), 12 y 14. El error
nació de confundir el gap con el valor mayor, pasó tres comprobaciones
*porque solo miraban al fantasma*, y cayó cuando la ecuación no cerró
(con la familia real cierra: `0,4504`, y 8.191 rebotes de pares reales
caen todos en `(w, 9w+2)`). **Corregido todo**: comprobaciones 12 y 14
reescritas sobre la familia real (con el **teorema de paridad del
rebote**: `|M| = 3` no balancea `ΔS` ⟹ `r` par exige `|M| ≥ 4`), filas
de la base enmendadas, corrección nº 34 registrada con su lección:
*una ecuación de conservación que no cierra es un detector de premisas
falsas más fino que cualquier barrido — el barrido del fantasma pasaba
limpio porque medía al fantasma.*

`afirmaciones.db`: **97 afirmaciones, 56 demostradas, 34 correcciones.**
Medido con topes declarados: `f ≈ 0,445`, `g ≈ 0,188`, `h ≈ 0,173`.

## ⇢ EL CENSO DEL REBOTE Y EL LEMA DEL BALANCE: el sistema CIERRA en dos incógnitas

Paso 1 de la ruta de `RutaTeoremas.md`, ejecutado. **El censo de
reentradas del rebote real `(w, 9w+2)`** (`w < 2^15`, tope 600):
**cobertura 100%** — consec 45,4% (el **96% con `δ = 0`**), rebote 43,8%,
fusión desbalanceada 10,3%, fusión limpia 0,6%. Cero sin clasificar.

Y del análisis salió el **LEMA DEL BALANCE FORZADO** (comprobación 17,
demostrado en tres líneas desde Terras 1.2): toda fusión válida para una
clase residual ENTERA está S-balanceada — la igualdad de las dos formas
afines fuerza `3^{S_x} = 3^{S_y}`. **Corolarios:** (1) la fusión
desbalanceada tiene **medida 2-ádica CERO** (una solución esporádica por
clase — el fenómeno de cerca del atractor, otra vez); (2) las reentradas
consecutivas con `δ ≠ 0` tampoco pesan; (3) **el sistema de renovación
colapsa a DOS incógnitas** (`f` y `g`) más masas de clase calculables.
Cruce gratis: las clases fundidas mod `2^12` del verificador son
**1.476 = `a(12)` exacto**.

**El siguiente paso quedó afilado**: calcular las masas de clase del
censo de forma EXACTA (nivel a nivel, estilo Perras — cada salida del
censo es una unión de clases residuales decidida en pasos acotados) y con
la orientación canónica de las reentradas rebote (ojo: el signo de `δ` al
reentrar depende de qué lado quedó menor — el censo actual mide `δ` en
lados originales, hay que reorientarlo). Con esas masas, el sistema
lineal se resuelve y **`f` queda decidida**.

## ⇢ LA RÁFAGA DE LA MADRUGADA (goal: investigación abierta) — CINCO REGISTROS MÁS

1. **Pandas afinado**: la condición `Res < 6` era insuficiente para
   `d* = −1`; la limpia es **`Res < 3`** — corrección en vivo registrada
   dentro de `lemadepandas.txt` (ataque P1 señalado al revisor). Letras
   corregidas: `φ` (2-ádica) vs `d` (Gao).
2. **El recíproco de Jirafas**: fusión balanceada ⟺ evento de clase —
   LA CARACTERIZACIÓN; Jirafas baja a lema en numeración externa y sube
   de contenido. Cierra el puente `φ = d` con rigor.
3. **Los lemas de germen**: `b(6) = 1` con `w ≡ 46` (vórtice `(40,13)`)
   y `c(6) = 1` con `w ≡ 25` (vórtice `(22,7)`), únicos, decididos por
   clase. Las series `b` y `c` **no están en OEIS** (ni las nuevas de
   `c`).
4. **El doblado reducido**: `b(m+1) ≥ 2b(m)`, `c(m+1) ≥ 2c(m)` (Gao en
   los pares reducidos) ⟹ **los límites `β` y `γ` existen** — el
   sistema asintótico de los tres pisos es objeto bien definido.
5. **El lema general del vórtice**: toda primera coincidencia de dos
   trayectorias cualesquiera es un vórtice (`a = 3b+1`) — la base
   implícita de todo, ahora explícita.

`afirmaciones.db`: **106 afirmaciones.**

## ⇢ Y EL PERRAS DE LOS PISOS REDUCIDOS, MEDIDO CON FORMA CERRADA

La veta se abrió y dio de inmediato: **el estrato mínimo de los dos
pisos reducidos es `|M| = 4`**, con formas cerradas

> `b₄(m) = 7·2^{m−7} − m + 4`  y  `c₄(m) = 6·2^{m−7} − m + 4`

clavadas en `m = 7…14`, **y confirmadas por PREDICCIÓN en `m = 15, 16`
(los cuatro valores exactos: 1781, 1525, 3572, 3060)**. Además: `c₄` ES
`A079583` (`3·2^n − n − 2`) — confirmación independiente de la forma —
y `b₄` no está catalogada. **La ley del germen único** rige en los tres
pisos: cada estrato nuevo entra cada dos niveles con exactamente una
clase. El término `−m` (una clase excluida por nivel) es el candidato a
«indeciso de Perras» del piso reducido. **Pendiente: la demostración de
las dos fórmulas** — el análogo del argumento de la ventana sobre el
estado rebote — que cerraría el primer término de las sub-renovaciones
y daría al sistema de `φ` dos masas exactas más. `afirmaciones.db`:
**108 afirmaciones.**

**Y los dos últimos registros de la ráfaga:** (1) **la autosimilitud
germen a germen** — el germen `|M|=6` del piso `h` (`w ≡ 33`) reentra
literalmente en la cola del germen `|M|=4` (`w ≡ 25`), y el del piso
`g` pasa por dos pares consecutivos en ruta; (2) **LA LEY DE LA
REENTRADA TOTAL**: las 107 clases de estrato 6 de ambos pisos
(`m = 10, 11`) reentran TODAS antes de fundir — 64 por consecutivo, 43
por la forma `{v, 9v−1}` — **y la forma `{v, 9v+2}` no aparece NUNCA
como reentrada (0/107)**: la torre recursa por DOS formas canónicas, no
tres; la asimetría `g`/`h` es estructural y el sistema de `φ` podría
ser más chico de lo que parecía. `afirmaciones.db`: **110
afirmaciones.** La demostración de `b₄`/`c₄` por preludios sobre
gérmenes inferiores es la primera tarea de la continuación.

**Y LA RÁFAGA CERRÓ CON LA DERIVACIÓN**: (1) la anatomía universal del
estrato 4 reducido — 686/686 clases son «preludio + ventana de Perras»;
(2) los conteos por largo de preludio son potencias de 2 menos 1 PURAS
(una clase de preludio por largo × su ventana), y la suma geométrica
sobre los largos permitidos ({3,4,6,7,…} en `g` sin el 5; {3,5,6,…} en
`h` sin el 4) **reproduce algebraicamente las dos formas cerradas** —
el 7 y el 6 derivados. Para el ascenso a teorema faltan DOS lemas de
preludio único (género de la unicidad de `|M|=2`) y los dos huecos.
**Es la CUARTA aparición del patrón «germen único + ventana de
Perras»: el triángulo entero parece generado por esa sola estructura.**
`afirmaciones.db`: **112 afirmaciones.**

**Y EL REMATE**: los dos lemas de hueco (decide: sin largo 5 en `g`,
sin largo 4 en `h`) y **la unicidad del preludio 2-mixto**
(decide-verificada al módulo natural, `L = 3…12`, gérmenes explícitos)
⟹ **`b₄` y `c₄` son TEOREMAS en el rango `m ≤ 14`** — la cadena
preludio único + huecos + ventana de Perras + suma geométrica. El caso
general pende de UN lema (unicidad del preludio para todo `L`, método
`v₂`). En una noche: conjetura → predicción confirmada → derivación →
teorema en rango. `afirmaciones.db`: **114 afirmaciones.**

**Y LOS DOS CIERRES DE LA MADRUGADA**: (1) el mecanismo de los
preludios — aterrizan en `D ∈ {−2, −8}` (18/18, con la corrección en
vivo: no era solo `−2`); (2) **LA LEY DEL ATERRIZAJE EN POTENCIAS DE
`−2`**: en el estrato 6 aparece además `+4 = (−2)²` — los aterrizajes
son exactamente `(−2)^j`, y los valores hermanos que no lo son (`−4`,
`+8`, `−16`) no aparecen jamás (278 casos, cero excepciones). El signo
alterna con las divisiones por el saldo de `S`. **Predicción falsable
registrada: el próximo aterrizaje será `+16 = (−2)⁴`.** El lema general
del preludio queda enunciado como: la dinámica de `D` con dianas en las
potencias de `(−2)` — el método de la unicidad de `|M|=2`, con diana
móvil. `afirmaciones.db`: **116 afirmaciones.**

## ⇢ EL ÚLTIMO REGALO DE LA NOCHE: EL LEMA DE LA EQUIVALENCIA — `f = d`

Los puntos 3–5 de la orden del revisor, ejecutados la misma noche:

- **LEMA DE LA EQUIVALENCIA** (demostrado, condicional a `Res < 6` —
  forma ultra-débil de Roosendaal, incondicional bajo `2^71`): si
  `H(n) = H(n+1)`, las trayectorias del atajo se encuentran **al mismo
  índice** con `S` igualada. La demostración es el argumento `6^d`:
  `6^d = n·Res(n)/((n+1)·Res(n+1)) ∈ (1/6, 6)` ⟹ `d = 0`. **Corolario:
  `f = d` — nuestra densidad de fusión ES la densidad de pares de igual
  altura que Gao midió subiendo a 0,512 en 10⁸.** La brecha con
  `a(32)/2^32 = 0,4357` es truncamiento puro. Verificado: los 477.245
  pares de igual altura bajo 10⁶ funden todos al mismo índice, cero
  excepciones. Gatas §10.
- **La proposición del `2^k − 1`** subida con su demostración de dos
  líneas (Perras §10), con los bordes revisados (quedan fuera de toda
  ventana finita: sin corrección).
- **R6 cerrado como teorema de familia**: `(3067, 3068)` funde en
  `t = 18 ≤ 19` ⟹ por Terras TODA la familia `2^19·m + 3067` funde en
  el paso 18 con `|M| = 8`. Los contraejemplos a Garner viven en el
  estrato 8 **por teorema**.

Queda para la próxima sesión solo lo que no era de hoy: LaTourette por
correo, lecturas (Rozier, Frinkle, A277109), y las sub-renovaciones de
`b(i)` y `c(k)` con el chequeo de rango. `afirmaciones.db`: **103
afirmaciones.**

## ⇢ CIERRE DEL 03-08-2026 — LA RUTA QUEDA EN `RutaTeoremas.md`. EMPEZAR POR AHÍ

**La tercera carta de Opus 5 llegó cruzada con nuestro último commit: su
pregunta decisiva («¿tu `G(k)` es acumulativa?») YA ESTABA CONTESTADA** —
la reconstrucción desde estados reducidos es exactamente la forma
`G(k) = Σ b(i)`, `H(k) = c(k)` que él exige como firma de teorema, y
está clavada hasta `k = 14`. Su identidad
`a(k+2) = a(k) + (2^k−1) + Σ_{i<k} b(i) + c(k)` es la nuestra. Confirmó
además: **Jirafas era atajo, no cimiento — el zoológico no se cae** (sus
palabras: Perras intacto, Gatas (a) intacto, partición intacta,
identidad intacta).

**Para la próxima sesión** (todo en `RutaTeoremas.md`, sección «LA RUTA
PARA LA PRÓXIMA SESIÓN»): (1) subir `2^k − 1` a proposición (la
demostración de dos líneas ya está); (2) cerrar R6 como teorema de
familia midiendo `t` de `(3067, 3068)`; (3) **el problema nuevo de Gatas
§5** — separar «igual altura» de «fusión al mismo índice» (`f ≤ d`,
recíproco sin demostrar: contar bajo 10⁶); (4) LaTourette por correo +
lecturas (Rozier, Frinkle, A277109); (5) recién después, las
sub-renovaciones de `b` y `c` con chequeo de rango. El `CLAUDE.md` lleva
ahora un puntero de arranque a `RutaTeoremas.md` al principio.

## ⇢ LA SEGUNDA REVISIÓN ROMPIÓ EL COROLARIO 1 DE JIRAFAS — Y EL SISTEMA SOBREVIVIÓ SIN ÉL

**Opus 5 rompió C1 y tenía razón** («numerable ⟹ medida cero» es vacuo
en Haar y no acota densidad natural). Acta completa en la sección 8 de
`teoremadejirafas.txt`, corrección nº 36. Los tests que pidió,
ejecutados y decisivos: **las 13.137 fusiones desbalanceadas chocan
TODAS en el valor 2** (la entrada del ciclo — la historia del atractor
en su forma extrema) **pero su densidad es ~0,39 y decae lentísimo**:
masa real, no artefacto. Las dos cosas a la vez. **Y el hallazgo
propio**: el colapso del sistema **nunca necesitó C1** — la
descomposición por primer evento DE CLASE es exacta y la masa sin evento
aporta 0 legítimamente — y **el Corolario 2 quedó DEMOSTRADO por
coeficientes** (reentrada consecutiva de clase ⟹ `3^{Sx} = 9·3^{Sy}` ⟹
llega con `δ = 0` exacto; el C3 desplegado que pedía la primera
revisión).

**Y LA PREGUNTA ANTI-TAUTOLOGÍA, CONTESTADA CON ENTEROS**: `G(k)` y
`H(k)` se reconstruyen **desde los estados reducidos, sin mirar el `r`
original** — `G(k) = Σ_{m<k} B(m)` (suma sobre ventanas de Perras) y
`H(k) = B_h(k)` (directa) — clavadas hasta `k = 14`. **La identidad es
teorema verificado.** Además el test espejo pasó tras cazar un off-by-one
en mi propio mapeo (`v = −(r+1)`, no `−r−2`): en `3n−1` la partición da
los MISMOS `G` y `H` con las etiquetas volteadas (`r` par ↔ `v` impar),
12/12 exacto — el pipeline es invariante al espejo.

## ⇢ LA PRIMERA REVISIÓN EXTERNA DICTÓ (Opus 5) — Y LA IDENTIDAD EXACTA CIERRA

**Perras: no lo rompió** (A1–A5 aguantan). Tres agujeros de redacción,
cerrados en la sección 9 del `.txt`: el lema que faltaba (`r` impar ⟹
`|M| ≥ 3`, con demostración del revisor), la indexación paso/estado, y la
costura `N`/`Z₂` declarada. **Gatas: (a) aguanta; dos golpes que se
aplicaron**: (1) **Gao Guo-Gang 1993** (Discrete Math. 112) tiene el
levantamiento (su Lema 2) y la existencia de `f` (su Corolario 2, misma
letra `d_k`) — corrección nº 35, la base «elemental del repo» era de
1993; (2) **la sección 4 se retira como validación** — el «cierre»
0,4504/0,4453 comparaba dos estimaciones con el mismo sesgo de
truncamiento (Gao midió la densidad subiendo 0,310→0,512 entre 10² y
10⁸). *La lección del fantasma, un nivel más arriba.*

**Y LA VALIDACIÓN BUENA, PROPUESTA POR EL REVISOR, PASÓ ENTERA**
(`identidadexacta.py`): la partición vale como **igualdad de enteros**
en cada nivel —

> `a(k+2) = a(k) + (2^k − 1) + G(k) + H(k)` — EXACTA, `k = 3…14`,
> con la rama de la contracción dando `a(k)` clavado (12/12) y la
> ventana de Perras dando `2^k − 1` clavado (12/12).

Sin topes, sin Monte Carlo, sin sesgo. **`G` y `H` nacen como sucesiones
exactas** (`G: 0,0,0,0,1,5,16,44,110,259,588,1302`;
`H: 0,0,0,1,3,9,24,58,134,300,659,1426`) — las «`g` y `h` exactas» que
pedía la pregunta del día. Regalos verificados: la rama `h` se reduce a
`{w, 9w−1}` (casi espejo del rebote), y los contraejemplos de
Elia–Tucker viven **todos en `|M| = 8`** (la aserción ahora es tabla).
Pendientes del revisor que quedan: **conseguir LaTourette 2007** (riesgo
real para la novedad de Perras), leer Rozier y Frinkle et al. 2025 /
A277109, el test espejo `3n−1` del pipeline completo, y el chequeo de
rango (anti-tautología) antes de las sub-renovaciones. Conteos: **40**.

## ⇢ LAS MASAS DE CLASE, Y EL MURO CON NOMBRE (`masasdeclase.py`)

El paso siguiente ejecutado: la descomposición exacta de `g` y `h` en
masas de clase (enumeración mod `2^p`, `p = 8…16`, eventos de clase
F/C/B con dos testigos). **El sistema es exacto y las horquillas
rigurosas** — `f ∈ [0,4263, 1]` en `p = 16`, cota inferior subiendo,
horquilla conteniendo siempre el `f` medido (0,4453). **Y el muro,
honesto**: la masa indecisa decae ~2% por nivel — **el mismo muro de
convergencia lenta que la razón de `b(k)`, porque es la misma pregunta
escrita como sistema.** `a(32)/2^32 = 0,4357` sigue siendo la mejor cota
inferior. La vía que queda (anotada en el fichero): NO subir `p` — la
cola indecisa son «tramos largos antes de reentrar» y debería tener su
propia renovación; ésa es la conjetura de trabajo para la próxima
sesión. Jirafas quedó bautizado y con su `.txt` de revisión
(`teoremadejirafas.txt`). Conteos del `CLAUDE.md`: **39**.

## ⇢ LA VERIFICACIÓN BIBLIOGRÁFICA DE LOS DOS TEOREMAS (orden del usuario)

Leído entero **Elia–Tucker 2015** (arXiv:1511.09141, el PDF completo) y
barrida la web. Veredicto:

- **Perras cambia de etiqueta y GANA valor**: el patrón «primer 0
  seguido de 1» **es el stem `s_i` de Garner 1985**, que demostró la
  suficiencia (la mitad ⟸) y conjeturó la necesidad para TODA fusión —
  y Elia–Tucker la refutaron (3067/3068, el par que el repo ya conocía).
  **Lo que Perras añade y no está en ninguno de los dos**: la necesidad
  restringida al estrato mínimo (`|M| = 2 ⟺ stems`) es VERDADERA, y el
  conteo exacto `2^{m−1}` con el borde resuelto (Elia–Tucker solo
  midieron: «0,214% de contraejemplos bajo 5·10⁹»). **Perras = la
  conjetura de Garner, falsa en general, demostrada en el estrato mínimo
  con su densidad exacta.** Los contraejemplos de Elia–Tucker viven en
  estratos ≥ 4 — la estratificación es exactamente lo que reconcilia a
  Garner con sus contraejemplos.
- **El Reinicio Uniforme queda bautizado TEOREMA DE GATAS** (orden del
  usuario): no se encontró ecuación de renovación para coalescencia de
  consecutivos en la literatura; el único paper de distribución de
  coalescencia (arXiv:2005.09456) estudia pares `(n, 3n+2)`, es
  empírico y **está retirado por su autor**. Aviso de la casa: «no
  encontrado» no es «no existe».

## ⇢ EL TEOREMA DE LA MITAD EXACTA (comprobación 15) — el objetivo del /goal

La perla del `2^18` exacto **dejó de ser perla**:

> **TEOREMA.** Para `r` PAR, `(r, r+1)` se funde con `|M| = 2` si y sólo
> si en el vector de paridad de `s₁ = r/2` **el primer 0 va seguido de un
> 1**; y entre `s₁ ∈ [1, 2^m)` fusionan **exactamente `2^{m−1}`**, para
> todo `m ≥ 2`, sin casos.

Demostración entera en el comentario: con `D = 1`, el primer valor par
de la trayectoria de `s₁` baja `D` a 0; el vórtice pide `T^{j+1}(s₁)`
impar (el bit siguiente al primer 0); `ΔS = 0` es automático; y el
conteo cierra **incluido el borde** — de los dos residuos frontera funde
exactamente uno para cada `m`, según `3^m mod 4`. Equivalencia
exhaustiva `s₁ < 2^16`, conteos clavados `m = 2…16`. **Es la primera
MEDIDA exacta de una fila del triángulo** (el estrato 2 pesa 1/2 entre
los `r` pares — Terras 1.4, la moneda, actuando sobre dos bits), y el
caso `j = 0` es Garner 1985. `afirmaciones.db`: **96 afirmaciones, 55
demostradas.**

**Pendiente, en orden (el mapa manda):** (0) **el refinamiento del paso
1**: etiquetar los tramos por datos FINITOS (el `E` de arranque módulo
algo, el largo del tramo), no por el destino al infinito — ahí se decide
si el conteo por etiqueta es polinómico;
(2) `clasificacion_rutas`: qué familia de E toca cada ruta y dónde el
vórtice (`D = 0`) interrumpe la órbita — ahí los estratos dejan de
analizarse uno a uno; (3) `cuadratica_M6` vía esa clasificación; (4) las
2 excepciones de `M = 27`; (5) cobrar el `X₀ = 10⁹` con la `B(k)`.
Conteos del `CLAUDE.md` en 37. **Sin commit aún — todo junto cuando el
usuario diga.**

---

# ⇢ 02-08-2026 — LA DEPURACIÓN TOTAL DICTÓ: 100 de 100. EMPEZAR POR AQUÍ

**Encargo del usuario: verificar TODO `afirmaciones.db` (80 afirmaciones + 20
constantes) antes de publicar nada.** Los cuatro adversarios pendientes de la
entrada de abajo quedaron recogidos por el camino: la sesión de la mañana
(`429f4e04`) murió por límite de uso con la mega-tanda A en vuelo, y esta sesión
rescató todo de los journals — **el trabajo pagado no se pagó dos veces**.

## El marcador final

> **100/100 — 75 CONFIRMADAS · 13 CORREGIDAS · 12 NO_DECIDIBLES · 0 REFUTADAS.**
> Todo en `depuracion/veredictos.jsonl`, una fila por ítem con su evidencia.

## Cómo se pagó, porque el método cambió a mitad por orden del usuario

1. **Lotes 1–3 + mega-A: tríos completos** (Lean + Python a ciegas + comparador).
   ~9M tokens. El andamio de Terras, fusión, pinza, pisos, Garner/Wu, espejos,
   negativos — la parte donde la independencia importaba.
2. **El resto: pasada LOCAL a coste ~cero** — los `verificar_*.py` del repo
   (11 scripts, exit 0 todos), los 4 `.lean` recompilados (0 `sorryAx`), y un
   consolidado propio escrito de cero (`depuracion/pasada_local/`). *«El código
   tiene oráculo»: para mediciones, ejecutar ES verificar.*

## Lo que encontró que no se sabía

- **`A65`, y es un off-by-one publicado: el espejo base 10 tiene 44.451
  dos-ciclos bajo 100.000, no 44.450.** Cerrado con combinatoria, no medido:
  (90.000 reversibles − 1.098 palíndromos)/2 = 44.451.
- **`A71`**: la tupla de 176 en `722.067.240` se confirma entera; su
  **maximalidad** bajo `2^30` nadie la re-verificó — es de Wu, y así queda dicho.
- **`A29`**: «sube k veces seguidas» es del ATAJO (el clásico lo rompe en `k=2`),
  y `2^4000 − 1` da **4.000** impares seguidos, no 3.999.
- **`A51` re-verificado EXACTO**: desviación **0,0** prediciendo el bit siguiente
  sobre los 2^13 residuos completos — la biyección lo fuerza. *(El primer intento
  propio contaminaba con la cola post-convergencia; lo cazó la capa 1.)*
- Y las 11 corregidas de los tríos (A2/A3/A5 bordes `n=1`, A27 `k=0`, A28
  biyección a teorema, A34 asintótico vs régimen, A11/A13/A16/A63…).

## Los 12 NO_DECIDIBLES, por clase

- **bibliográficas** (Tao A37, 5x+1 A39, Barina `2^71` A66, Wang A64): se citan,
  no se re-demuestran aquí.
- **coral** (A44, A72, A73, A74 y C20): barrido caro prohibido — pendiente de
  una pasada CPU dedicada.
- **irreproducibles** (A52 sin nulo registrado, A54 la esfera borrada, A43 sin
  tendencia limpia): del pasivo «números sin código», y así quedan marcados.

## LO QUE QUEDA, en orden

1. ⇢ **HECHO la misma noche: las 13 correcciones aplicadas** al generador, la
   base regenerada y el `CLAUDE.md` (commit `96ee1fc`).
2. La pasada CPU del coral (barata en tokens, cara en horas de máquina).
3. `guardarrespuestas.py` + zip de transcripciones al cerrar esta sesión.

## ⇢ Y EL ATAQUE A CST ARRANCÓ, la misma noche, todo local

**`atacacst.py` + `atacacst.lean`** (encargo del usuario: atacar con Lean y
Python, sin agentes). La palanca: en cada clase `r mod 2^k` donde el
coeficiente cae, el fallo de CST sólo puede vivir en `m ≤ T^k(r) − r` — **un
tramo finito por clase, y eso está DEMOSTRADO en Lean para todo `k, r, m`**
(`palanca`, `tramo_finito`; núcleo, sin Mathlib, sin `sorryAx`, compiló a la
primera).

**Resultado:** CST decidida **para todo `n ≥ 2` con `σ* ≤ 27`** — incluido el
jump value `k = 27` — autocontenido, sin `X₀` importado. Complementa el corte
`σ* ≤ 16.294` de `paradacoef.py`, que sí depende del barrido a `2·10⁷`.

**Y el hallazgo que deja una pregunta afilada: el tramo estuvo VACÍO las 27
veces** (`T^k(r) ≤ r` en toda clase caída, con las únicas igualdades en
`r ∈ {0, 1}`). Si eso fuera teorema para todo `k`, **CST entera caería**.

> **⇢ CORRECCIÓN DE PUNTERÍA, la misma noche (capa 1 sobre esta bitácora).**
> Aquí decía que la continuación era el jump value `k = 46` por enumeración
> dirigida. **Mal apuntado, por dos motivos.** (1) «Tramo vacío en la clase de
> `r`» es EQUIVALENTE a «CST se cumple en el representante `r`» — no es un
> milagro aparte, es CST en los números chicos, reformulada. (2) La propia
> palanca implica que una clase con tramo abierto exige `r ≤ B(k)`, y
> `paradacoef.py` ya demostró `B(k) ≤ 2·10⁷` para **todo `k ≤ 16.294`** con su
> barrido propio — así que `k = 46` (y el 65, y el 149…) **ya estaban
> decididos**. La frontera real es **`k = 16.295`**, donde `B(k)` rebasa por
> primera vez el barrido de `2·10⁷`.
>
> **La continuación buena: subir `X₀` (el barrido directo `σ = σ*`), que es
> CPU pura y cero tokens, y dejar que el corte se corra solo por la curva
> `B(k)`.** La misma noche: **`10⁸` en 2 minutos y `10⁹` en ~18 — 0
> diferencias en los dos** (`atacacst2.py`, resultados en
> `atacacst2_progreso*.txt`). `X₀` queda **50×** por encima del `2·10⁷` de
> `paradacoef.py`. La conversión `X₀ → K nuevo` con la maquinaria `B(k)`
> queda para la sesión siguiente; a este ritmo, `10¹⁰` sería una noche de
> CPU si hiciera falta.

---

# ⇢ CIERRE DEL 01-08-2026 (noche) — LOS DOS TRÍOS DICTARON. EMPEZAR POR AQUÍ

> ## ⚠ LO PRIMERO AL VOLVER: HAY CUATRO ADVERSARIOS SIN RECOGER
>
> Se lanzaron al final de la sesión, sobre el repo **ya commiteado y pusheado en
> `5f4db09`**, y la sesión se cerró antes de que dictaran. **Sus veredictos no
> están aplicados.** Es el mismo caso del comparador que se perdió el 01-08 por
> la tarde, así que esta vez queda escrito qué se les pidió:
>
> | lente | encargo |
> |---|---|
> | **contradicciones internas** | buscar qué de lo escrito hoy contradice algo viejo que no se tocó. El fallo tiene historial: *«cuando se corrija algo, hay que buscar dónde más se afirmaba»* |
> | **prosa contra código** | coger afirmaciones con número del `CLAUDE.md`, ejecutar el fichero del que dicen venir, y ver si cuadran. Y listar las que **ya no son reproducibles** porque su fichero murió en la purga |
> | **romper lo de hoy** | atacar los tres bloques nuevos: el vuelco sobre OEIS, el veredicto del tipo `ℕ`, y lo que se dio por cerrado. En particular si *«ningún invariante mod `2^k` distingue los dos mapas»* está demasiado fuerte |
> | **ficheros sin auditar** | `espejoak.*`, `pruebaresta.lean`, `cotatramos3n1.*`, `paradacoef.py`, `franjaeverett.py`, `medidamonotona.py`, `auditarrefutaciones.py` y otra pasada a `verificar_terras.py`, que ya tuvo un bug |
>
> **Si no dejaron nada, hay que relanzarlos.** Y el aviso de método, que ya va
> por la segunda vez hoy: **un veredicto que no se aplica antes de cerrar, se
> pierde.**
>
> ### ⇢ EL PRIMERO SÍ DICTÓ, y trajo 25 hallazgos
>
> **El de contradicciones internas entregó: 7 graves, 10 medianos, 8 erratas.**
> Aplicados los 7 graves y 9 más. **Su hallazgo estructural explica casi todos:
> la sección «Lo que queda pendiente» de este fichero era un FÓSIL anterior al
> 30-07** — sin fecha, así que se leía como viva, y sobrevivió a la purga, a las
> dos auditorías y a los dos tríos sin que nadie la tocara. Siete de sus puntos
> mandaban trabajo ya hecho, ya refutado, o sobre ficheros borrados.
>
> **Lo que dejó sin aplicar, para mañana** (nada de esto cambia una decisión):
>
> | # | qué |
> |---|---|
> | 13 | `CLAUDE.md` cita *«la tabla de ángulos de arriba»* y sus cifras `0,003% vs 97%`: **esa tabla se borró con `coralcollaz.py`** |
> | 18 | esta bitácora dice *«80 · 22 · 20»* en la entrada de la tarde — era cierto entonces, hoy son **32** correcciones; conviene marcarlo, no reescribirlo |
> | 24 | en la tabla del 30-07, *«la causa es `45 = 3²·5`»* sigue sin marca de que `coralprimos.py` la refutó |
> | 25 | el `0,5186` de la densidad viene de `densidadfusion.py`, **retirado por ser un promedio muestreado** |
>
> ### ⇢ LOS CUATRO DICTARON. Y lo que hay que leer es el veredicto del cuarto
>
> **Los cuatro encontraron algo. Pero el que auditó prosa contra código, que era
> el que podía tumbar el repo, dijo esto:**
>
> > *«**El núcleo duro aguanta.** Las cinco cosas que sostienen decisiones —la
> > cota de ciclo con `X₀ = 2^71`, la sucesión `a(k)`, el criterio de fusión, el
> > piso de la altitud y la cota `B(k)` de CST— las derivé desde cero y **salen
> > clavadas**, incluida la coincidencia fina de que **16.294 es exactamente** el
> > corte que permite `X₀ = 2·10⁷`.»*
>
> **Verificó 24 afirmaciones con implementación propia y 24 cuadraron.** Lo que
> falla es de un solo tipo, y el repo ya le puso nombre: **un número publicado
> sin su rango.**
>
> **Aplicado:** la razón de la fila `k=23` era la del escalón de abajo
> (**1,9069**, no 1,8973); los vórtices del 221 son **51** aritméticos y el 50
> venía de una decisión de dibujo de un fichero borrado; CST está verificada a
> **2·10⁷**, no a `2·10⁶` —y de ese rango sale el corte `σ* ≤ 16.294`—; tres
> etiquetas decían **10⁷** y eran **10⁶**; el `0,5837` del piso es el valor a
> 200.000 y las *«once veces»* son **nueve**; el `0,5186` estaba declarado
> retirado en un párrafo y usado como dato vivo en el siguiente. Y en código:
> `franjaeverett.py` publicaba *«el óptimo está en M = 9»* **contra su propia
> tabla** (contando excepciones reales, `M = 5, 9, 101, 1001, 10001` empatan a
> cero, y el umbral baja a **1,585011**, no a 1,63763); y `verificar_terras.py`
> titulaba *«comprobado y no supuesto»* una sección **cuya mitad es un
> supuesto** — el fichero que ya tuvo un bug ahí.
>
> **PENDIENTE REAL, y es el pasivo de fondo: ONCE NÚMEROS siguen presentados
> como medidos sin código detrás**, y sólo uno (`3,49031`) lleva la marca. Están
> listados en el informe del adversario. *El peor no es el más grande: es
> «correlación latitud / `log₂(valor)` = 0,12», que **no es reproducible ni en
> principio** porque «latitud» era una coordenada de un dibujo que ya no existe.*
>
> Y lo que dejaron los otros dos, sin aplicar: `medidamonotona.py` cuenta 5
> codominios bien ordenados y son 7, etiqueta como «acotadas» tres candidatas
> que no lo están, y dice que «el precio crece con `k`» cuando su tabla baja en
> 4 de 7 escalones; `paradacoef.py` tiene un `if` que es la misma desigualdad que
> su `while` (dos verificaciones donde hay una) y una fila del A/B con **cero
> instancias medidas**; `auditarrefutaciones.py` arrastra un `243` heredado
> cuando él mismo calcula `240`, y su tabla del #54 muestra que **todo `N` primo
> adelanta 0** sin que el veredicto lo use — que es el resto vivo de la
> predicción del número primo de rumbos.
>
> ### Lo que SÍ quedó comprobado antes de cerrar
>
> - **Batería mecánica sobre el repo entero: 0 fallos.** 34 `.py` parsean, 0
>   hallazgos cp1252, los conteos cuadran, las tres bases con
>   `integrity_check = ok`, 0 filas apuntando a ficheros inexistentes, los 4 zips
>   abren, y los números que viven en varios sitios coinciden.
> - **EL REPO SOBREVIVE A UN CLON LIMPIO**, y es la primera vez que se comprueba.
>   Clonado desde GitHub a un directorio nuevo: **54 ficheros, ninguna diferencia
>   con el local**, y **11 de 11 scripts baratos corren** más la CLI
>   (`main.py camino 27` → 111 pasos, techo 9.232). *Es justo lo que le faltó a
>   `lecturas/*.pdf` y al toolchain de Lean.*
> - **La única excepción, y es por diseño:** `guardarrespuestas.py` **no puede
>   correr desde un clon en otra ruta**. Deduce el slug del directorio actual, y
>   las transcripciones viven donde Claude Code las escribió, indexadas por la
>   ruta original. Falla con un mensaje claro que dice qué cambiar. **No es un
>   bug, es una atadura a la máquina** — y por eso existe `transcripciones/`.

Sesión de **corregir**, no de medir. Salió una cosa que no se buscaba: **dos de
las correcciones eran el error**, y las dos enterraban algo bueno.

## Lo que cambia decisiones

1. **LEAN NO ESTABA INSTALADO.** El `CLAUDE.md` decía *«instalado el
   01-08-2026»* y `~/.elan` **no existía**. Reinstalado (4.32.2). Los **cuatro**
   `.lean` compilan a **0 errores / 0 `sorryAx`**. *Se perdió el verificador del
   único fichero con categoría de «demostrado»: los `.lean` están en git, el
   toolchain no.* **Regla nueva: `lean --version` al abrir.**

2. **El trío del `3n−1`: la frase del `CLAUDE.md` era FALSA.** *«Para `3n−1` la
   `C` es negativa **y el tipo `ℕ` ya no sirve**»*. Las dos mitades no se
   contradecían — **el error era el «luego»**, un *non sequitur*. Y los dos
   agentes **nunca discreparon**: sus `C` son opuestas (`C_lean = −C_python`).
   El comparador refutó también al **agente de Lean**, compilando él mismo la
   forma con resta. Queda en `pruebaresta.lean`.

3. **El trío de `a(k)`: es TEOREMA, y el motivo de retirar el envío a OEIS se
   cae.** `a₊(k) = a₋(k)` para **todo `k`**, demostrado en Lean sin Mathlib. La
   biyección es `2^k − 1 − r`. **La bitácora la tenía archivada como fallida por
   un `±1`** (decía `2^k−2−r`). Y el resultado es más ancho: `n ↦ −n` es un
   automorfismo de `Z/2^k`, luego **ningún invariante mod `2^k` distingue los dos
   mapas** — control que lo remata: **`A076227`, que SÍ está en OEIS, también
   sale idéntica**. El A/B contra `3n−1` no era un control para esto.

## Lo que se cerró sin gastar máquina

- **El pendiente «llegar a `k ≥ 20` y decidir si es teorema o se rompe»: cerrado
  a favor de teorema.** Iba a costar horas de CPU y costó una demostración.
- **Los conteos, por tercera vez.** 28 → **34** `.py`, 26 → **32** con
  `SystemExit`, cinco → **seis** `sqlite3`, siete → **ocho** `secuencia_de`, y
  **seis ficheros** que no tenían fila en la tabla. Barrido cp1252: 0 hallazgos.
- **`afirmaciones.db` iba una auditoría por detrás**: siete afirmaciones que el
  documento ya había refutado, y **20 filas** apuntando a ficheros borrados (yo
  había contado 9). Base regenerada: **80 · 32 · 20**.
- **`respuestas.db`**: 701 mensajes, 7 sesiones. **355 mensajes ya sólo viven
  ahí** — tres transcripciones desaparecieron del disco en menos de tres días.
  Nuevo: **`transcripciones/`**, un `.zip` por sesión, dentro del repo.

## La lección, y es la misma tres veces

> **Auditar una refutación encuentra tanto como auditar una afirmación.**

Pasó con la biyección `2^k−2−r` (un `±1` enterró un teorema), con el motivo de
la retirada de OEIS (un control que no controlaba), y con la explicación del
agente de Lean (conclusión correcta, razón falsa). **Y las tres se cazaron
compilando o ejecutando, no opinando.**

## Lo que queda abierto

- **`espejoak.lean` dice «para todo `k`» y tiene un tramo decidido sólo hasta
  `k = 7`**: Terras y el borde están demostrados para `T₊`, no para `T₋`. Es
  cierto y sale en tres líneas, pero **hoy no está demostrado**.
- La pregunta grande de siempre: la razón `b(k)/b(k−1)`, ¿converge por debajo de
  2 o llega a 2? Sigue sin decidirse; `k = 34` no la decidiría tampoco.
- **La independencia de los agentes hay que protegerla al lanzar.** El
  `CLAUDE.md` se les inyecta entero y ya contiene medio argumento. Dos tríos, dos
  contaminaciones — una declarada y otra no.

---

# ⇢ ESTADO AL CIERRE DEL 01-08-2026 (tarde) — lo anterior

*(Escrito con dos workflows todavía corriendo, por si la sesión se cierra antes
de que terminen. Si estás leyendo esto en una sesión nueva: lo primero es
comprobar si dejaron sus ficheros.)*

## ⇢ LO MÁS NUEVO: LEAN 4 ENTRA AL REPO, Y CON ÉL LA REGLA DE LOS TRES

**`cotatramos.lean`** (commit `3b3c6c2`) **demuestra** lo que `cotatramos.py`
mide: la identidad de Terras, la cota `3^A·n₀ ≤ 2^B·n_k` y el corolario, **para
todo `n₀` y todo `k`**, sin Mathlib, comprobado en 1,8 s. `#print axioms` sale
limpio (**no hay `sorryAx`**), y el 221 está verificado por el **núcleo** —
`A = 41, B = 73`, cruzado además contra Python sin compartir una línea.
*Fue el primero; al cerrar el día ya son cuatro.*

**Y el procedimiento que manda desde ahora, dictado por el usuario:**

> **Toda comprobación aritmética o matemática va por TRES agentes:** uno la
> demuestra en **Lean**, otro la calcula **por su cuenta sin ver el primero**, y
> un tercero **compara los dos**. Detalle completo en `CLAUDE.md` →
> *LA REGLA DE LOS TRES*.

**El matiz que hay que conservar, porque es fácil inflarlo:** Lean caza **unas
13 de las 32** correcciones que este repo tiene registradas — **menos de la
mitad**. No caza muestras tomadas por constante, estimadores ni citas. Lo que sí
caza es **la clase que este repo repite**: hipótesis que faltan (cuatro veces) y
confusión de mapas (tres). *Y salió un extra: al formalizar, la hipótesis
`0 < n₀` del corolario resultó **sobrar**. Primera vez que se quita una en vez
de descubrir que faltaba.*

### ⇢ EL PRIMER TRÍO YA ESTÁ LANZADO: el control A/B del `3n−1`

**Estrena la regla con algo cuyo resultado ya sospechamos**, que es la manera
barata de saber si el trío funciona antes de gastarlo en algo caro.

| agente | crea | estado |
|---|---|---|
| **1 · LEAN** | `cotatramos3n1.lean` | **ENTREGADO.** Compila sin Mathlib, sin `sorry`, 4 invocaciones y 0 fallidas |
| **2 · INDEPENDIENTE** | `cotatramos3n1.py` | **ENTREGADO.** 307.807 pares, 0 fallos, 0,63 s |
| **3 · COMPARADOR** | — | **CORRIENDO AL CERRAR LA SESIÓN.** Su veredicto es lo primero que hay que recuperar |

**A los dos se les dio el MISMO enunciado y NO se les dio la identidad** — cada
uno tuvo que derivar la forma de `C` por su lado, o la comparación no mediría
nada. Los dos ficheros están **commiteados pero sin veredicto**: no los cites
como verificados hasta que el comparador dicte.

### ⚠ LO QUE HAY QUE MIRAR PRIMERO AL VOLVER: una frase mía puede estar mal

**Los dos coinciden en (II), (III) y en la discriminación.** Pero sobre la
pregunta del tipo dicen cosas distintas, y **una de ellas contradice lo que yo
escribí en `CLAUDE.md` unas horas antes**:

| | qué dice |
|---|---|
| **yo, en `CLAUDE.md`** | *«para `3n−1` la `C` es negativa y **el tipo `ℕ` ya no sirve**»* |
| **agente 1 (Lean)** | **NO hizo falta `ℤ`.** El problema no es el tipo sino **dónde se pone la `C`**: con `2^B·n_k + C = 3^A·n₀` no hay resta y la inducción cierra sola |
| **agente 2 (Python)** | lo que cambia es **el signo de `C`** (`C ≤ 0`), y la desigualdad lo arrastra |

> ⇢ **RESUELTO (01-08-2026, noche). La frase era FALSA: `ℕ` basta.** Pero
> **ninguno de los dos agentes tenía razón del todo.** El comparador compiló él
> mismo la forma con resta, sobre estado arbitrario y **sin invariante
> reforzado**, y con eso refutó también la explicación del agente de Lean: poner
> la `C` al otro lado es **más cómodo, no necesario**. *Su conclusión quedó
> reforzada; su razón, corregida.* La compilación que lo decidió está en
> **`pruebaresta.lean`**, y el párrafo del `CLAUDE.md` está reescrito.

**Dos cosas más que dejaron los agentes y que el comparador tiene encargadas:**

- El corolario **no se traduce cambiando una palabra**: en `3n−1`, *«baja ⟹
  `2^B > 3^A`»* es **falso** (`n₀ = 2 → 1`, `A=2, B=3`, o sea `8 ≤ 9`; 2.023
  casos). El que vale es *«**sube** ⟹ `2^B < 3^A`»*.
- El agente 2 **confesó un riesgo de contaminación**: leyó `cotatramos.py` como
  plantilla, y ese fichero trae un cruce parcial sobre `3n−1`. *Que lo declarara
  él solo es exactamente lo que la regla busca.*

### LO QUE SE SACÓ EN LIMPIO, y es poco pero es duro

1. **`cotatramos.lean` — lo único DEMOSTRADO del repo.** La identidad de Terras,
   la cota y el corolario, para todo `n₀` y todo `k`. `#print axioms` sin
   `sorryAx`. **No es «0 fallos en 329.400 pares»: es todos.**
2. **Lean instalado y con su regla de uso escrita**, incluida la parte incómoda:
   caza **unas 13 de 32** correcciones, menos de la mitad. Lo que caza es la
   clase que este repo repite.
3. **LA REGLA DE LOS TRES**, y con ella la REGLA CERO pasa a tres capas.
4. **La auditoría de las diez refutaciones** (`eea5a8d`): 8 confirmada, 2
   exagerada, **0 refutada**. Y el adversarial encontró cuatro defectos **en la
   auditoría**, mejores que los que la auditoría encontró.
5. **Las tres vías cerradas** (`wzu334m64`, 7 agentes): CST sigue viva y es la
   mejor; franja y monótona se cierran **con su razón escrita**; y las tres
   midieron **`A076227` sin darse cuenta**, cruzada por accidente con 0
   discrepancias entre tres implementaciones.

### PUNTOS A FAVOR, al día

| pieza | categoría | estado |
|---|---|---|
| **la cota por tramo** `3^A·n₀ ≤ 2^B·n_k` | **teorema** | **demostrado en Lean**, todo `n₀`, todo `k` |
| el corolario «baja ⟹ `2^B > 3^A`» | **teorema** | **demostrado en Lean** |
| el piso de la altitud | cota | 0 fallos; enunciado afinado dos veces |
| el criterio de fusión (43,57%) | cota | exacto hasta `k = 32`, sin muestreo |
| la pinza de ciclos | rederivación | verificada; **vía cerrada a propósito** |
| **CST: «no hay contraejemplo con `σ* ≤ 16.294`, para todo `x`»** | **cota** | del workflow, **sin aplicar aún** |
| `A076227` | dato | **cruzada por tres implementaciones independientes** |

### PENDIENTES, en orden

1. ⇢ **HECHO (01-08-2026, noche). El comparador dictó: la frase era FALSA.**
   `ℕ` basta, y no por lo que decía el agente de Lean — el comparador compiló él
   mismo la forma con resta (`pruebaresta.lean`) y refutó también su
   explicación. Los dos agentes nunca se contradijeron: sus `C` son opuestas.
2. **Aplicar la auditoría de las diez** al `CLAUDE.md`: las dos EXAGERADAS, los
   cuatro defectos del adversarial (re-tecleo presentado como reimplementación,
   dos tautologías con recuento, una sensibilidad mal medida, y el `5,86x` que es
   una **elección de unidad** blindada con un `SystemExit` — verificación
   circular cometida por el auditor).
3. **Aplicar las tres vías** al `CLAUDE.md`: las dos correcciones obligatorias de
   CST, y las razones por las que franja y monótona se cierran.
4. **Commitear `medidamonotona.py`** si el workflow no lo dejó.
5. ⇢ **CERRADO (01-08-2026, noche): ES TEOREMA, y no hizo falta llegar a
   `k ≥ 20`.** `a₊(k) = a₋(k)` para todo `k`, demostrado en Lean; la biyección es
   `2^k − 1 − r` (la que aquí figuraba como *«no se pudo confirmar»* estaba
   corrida por uno). **Y con eso se cae el motivo que mató el borrador de OEIS**:
   `n ↦ −n` es un automorfismo de `Z/2^k`, así que ningún invariante mod `2^k`
   separa los dos mapas — **`A076227`, que está en OEIS, tampoco los separa**.
6. **El control A/B en Lean para el resto de piezas** — ahora que hay trío, es
   barato.
7. **Nueve de los diez bloques de la búsqueda web siguen sin código propio.**

### LA LECCIÓN DEL DÍA, que se repitió tres veces

**Auditar una refutación encuentra tanto como auditar una afirmación.** Pasó con
las diez del bloque E (dos exageradas), pasó con el adversarial que auditó a esa
auditoría (cuatro defectos más), y pasó **conmigo**: la frase del tipo `ℕ` la
escribí el mismo día en que documentaba que no se escriben frases así.

> *Una corrección suena a rigor, y por eso nadie la revisa.*

## 1. LA PURGA, hecha (commit `4f8efdc`)

El repo pasó de **43 a 28 `.py`**, de 16 programas que dibujan a **4**, y el
`CLAUDE.md` perdió **616 líneas (18,5%)**. Total: **−7.106 líneas.**

Lo borrado no estaba mal calculado: **medía la esfera, el ángulo o el módulo
elegidos a mano, no Collatz.** Fuera `collazcirculo`, `collazcruce`,
`mallabasica`, `mallacollaz`, `maquinitacollaz`, `collazejecucion`, `viz3d`,
`coralcollaz`, `cruzarestos`, `collazarbol`, `mallaespejo`, `mallaespejo2`,
`espejobases`, `densidadfusion`, `guardarmallas`, `collazlamina`, las 12 mallas
`.json`, `oeis_borrador.txt`, las notas a mano, y los `.html`/`.png`.

**Dos cosas se rescataron, y las dos importan:**

- **`cotatramos.py`** — el cálculo que `collazlamina.py` hacía antes de dibujar.
  De `C ≥ 0` en la identidad de Terras salen dos desigualdades:
  `2^B·seq[j] ≥ 3^A·seq[i]` para todo par, y **si un tramo baja entonces
  `2^B > 3^A`**. Verificadas sobre **prefijos que nunca tocan el 1** (329.400
  pares, 252.014 tramos descendentes, 0 fallos), o sea que **no asumen
  convergencia**. Y el control A/B discrimina: sobre `3n−1` la `C` es negativa y
  la desigualdad se invierte. *Convierte «el balance decide todo» de promedio
  sobre trayectorias en **cota por tramo**.*
- **`mallascerradas.py` se salvó.** El auditor lo acusaba de no discriminar. Se
  corrió el A/B que nunca se había corrido —los seis restos mod 6— y **sólo el
  resto 4 sale con 0 fallos en las dos ruedas**. La refutación era falsa.

`matplotlib` **se queda** en `requirements.txt` aunque ahora no lo importe nadie:
decisión del usuario, tarde o temprano hará falta.

## 2. LO QUE ESTABA CORRIENDO AL CERRAR

Los dos tienen **conjuntos de ficheros disjuntos** y **prohibido tocar
`CLAUDE.md` y `bitacora.md`** — la documentación se aplica después, a mano.

| workflow | crea | qué busca | estado |
|---|---|---|---|
| **`wzu334m64`** — las tres vías | `paradacoef.py`, `franjaeverett.py`, `medidamonotona.py` | CST, la franja `log₂(10/9)`, y una cantidad monótona | **corriendo**; ya dejó `2884b3d` (franja) y `c9b0bca` (CST) |
| **`wyefzghui`** — auditar refutaciones | `auditarrefutaciones.py` | las diez correcciones del bloque E, con adversario | **TERMINADO**, commit `eea5a8d` |

**Si esos ficheros existen, los workflows llegaron a commitear. Si no, se
perdieron y hay que relanzarlos** — los guiones quedan en el directorio de
workflows de la sesión.

**Resultado del que terminó (`wyefzghui`), en una línea: 8 CONFIRMADA, 2
EXAGERADA, 0 REFUTADA** — no hay nada que rescatar, las diez apuntaban al sitio
correcto, pero dos se sostenían con un número que no pasa el filtro que ellas
mismas exigen. *La regla que sale: **una refutación se publica con el mismo rigor
que una afirmación** — con su rango y sus cifras significativas.* El adversarial
además encontró fallos en la propia auditoría. **Está sin leer entera.**

### Las tres vías, en una línea cada una

- **CST** (`σ*(x) = min{k : 2^k > 3^{m_k}}` contra `σ(x)`). Es la **única** de las
  tres que da un criterio evaluable **antes** de terminar la trayectoria, porque
  `σ*` se calcula sólo del vector de paridad, o sea sólo de `n mod 2^k`. Si
  `σ* = σ`, **no hay ciclos** y el tiempo de parada queda descrito por clases.
  **El control que decide si sirve: medirla sobre `3n−1`.**
- **La franja `log₂(10/9) = 0,152`.** Everett certifica descenso desde
  `B/A > 1,73697`; el equilibrio está en `1,58496`. Los 24 números de 3 a 20.000
  que no certifica caen los 24 dentro, y el más chico es el **27**. La idea a
  probar: afinando la cota `5/3` a `(3M+1)/(2M)` el umbral **baja hacia
  `log₂3`** — pero condicionar a `m ≥ M` sólo vale en el prefijo. **Si queda un
  núcleo que resiste a todo `M`, ese núcleo es el resultado.**
- **La cantidad monótona.** No se espera encontrarla —el `+1` rompe toda medida
  que se porte bien con `n/2` y con `3n`—; **el objetivo es medir CÓMO fallan**.
  Una `Q` que decrece salvo en un conjunto describible es una demostración con un
  agujero localizado. Variante con más posibilidades: que decrezca **en todo
  tramo de `k` pasos** para algún `k` fijo, que basta igual.

## 3. LO QUE HAY QUE HACER CUANDO CIERREN

1. Aplicar al `CLAUDE.md` lo que salga de las dos pasadas.
2. **La cola de la purga**: ~50 menciones sueltas a ficheros borrados y una
   docena de conteos viejos en secciones que no se tocaron. Mecánico, a un agente.

## 4. LOS PENDIENTES DE FONDO, por orden

1. **`a(k)` es idéntica para `3n+1` y `3n−1`** (verificado `k = 3…13`). Falta
   llegar a `k ≥ 20` y decidir si es **teorema** o se rompe. Es lo único que
   puede tumbar o salvar lo que el repo tenía por mejor resultado, y es barato.
2. **Nueve de los diez bloques de la búsqueda web siguen sin código propio**:
   Böhm–Sontacchi, Bernstein–Lagarias, Monks 2006, Krasikov–Lagarias `x^0,84`,
   Applegate–Lagarias, Steiner 1977, la reducción mod 4, y el paper de Fibonacci
   de 2026. *(El bloque 1, CST, es la vía que está corriendo.)*
3. **El hueco de densidad.** `afirmaciones.db` tiene **5 filas `casi_todo_n` y
   las 5 sin fichero**. Cero instrumentos propios sobre densidad, y ahí vive el
   salto «casi todos → todos».
4. **La pasada cruzada**: las 80 afirmaciones contra los dos pools
   (`hilos.db` + `records.json`), respetando el filtro de cuantificador —
   `promedio` y `casi_todo_n` **no se evalúan**, se rechazan.
5. **La Fase 3 del plan de la pinza hay que recalibrarla**: apareció el
   corrigendum de Hercher (14-06-2026) que **acredita el hallazgo a Xinjun
   Wang**, el mismo cuyo preprint el repo descartaba por «cero citas».

## 5. LAS DOS REGLAS NUEVAS DE HOY

- **`git fetch` antes de tocar nada.** `git status` a secas compara contra la
  última copia local del remoto y puede mentir.
- **Lo secundario va a un agente, siempre.** La prueba: ¿esto responde una
  pregunta sobre Collatz, o deja el repo más prolijo? Lo segundo se delega.
- Y una tercera, del usuario: **no se re-ejecutan los barridos caros** en pasadas
  de rigor.

---

## 2026-08-01 (noche) — LAS DOS AUDITORÍAS APLICADAS. 6 de 6 adversarios rompieron algo

Se aplicaron al repo las correcciones de dos auditorías con revisores
adversariales. **La matemática venía verificada; esta pasada era de escritura** —
que el repo *diga* lo correcto. Nueve commits temáticos.

### La regla nueva, primero, porque cambia cómo se trabaja

> **NO SE RE-EJECUTAN LOS BARRIDOS CAROS EN PASADAS DE RIGOR.** Decisión del
> usuario, 01-08-2026. Los que quedan excluidos: `clasesfusion.py` (`K_MAX=32`,
> más de una hora), `pinzaciclos.py` (`K_MAX=30`, 12,5 min), `densidadfusion.py`
> (`POTENCIA=28`), el experimento 3 de `redhilos.py`, y `coralprimos.py`.
>
> **Sus resultados están en `sucesiones.txt`, en `resultado_paralelo_k32.txt` y
> en este documento, y no se vuelven a calcular para corregir un comentario.**
> Si una pasada toca uno de esos ficheros, se comprueba la sintaxis y el barrido
> cp1252 y se deja constancia de que no se corrió. *Correr una hora de CPU para
> validar un cambio de prosa es gastar la máquina en el sitio equivocado.*

### El saldo

**Seis adversarios, seis rompieron algo.** Ninguno salió con las manos vacías, y
eso es un dato sobre el repo, no sobre los adversarios.

### Las sorpresas, ordenadas por lo que cambian

1. **La cota de ciclos estaba mal, Y A NUESTRO FAVOR.** El
   `217.976.794.617 / 355.504.839.929` que se había escrito esa misma mañana
   exige `X₀ ≥ 2^71,884`, y Barina está en `2^71,019`. La buena es
   **`114.208.327.604` (atajo) / `186.265.759.595` (clásico)**, certificada por
   tres caminos. **Y el número lo publica Barina 2025 §6 y lo repite Wikipedia**:
   copiamos bien una fuente arbitrada equivocada. *Es el tercer caso de la misma
   familia y el primero en el que el error nos favorecía — que es la dirección en
   la que nadie mira.*

2. **La marca «CITA SIN VERIFICAR» de Wu–Huang 2001 era el error, no la cita.**
   Existe: *Mathematica Applicata* (Wuhan) 14 (2001), supl., 21–25, MR 1885838,
   y está en la bibliografía anotada de Lagarias con los vectores de paridad
   textuales, que se recalculan bit a bit. **No estaba en Crossref porque es un
   suplemento de una revista china.** *Primera vez que se corrige una refutación
   propia y no una afirmación — o sea que el pendiente de «auditar las
   refutaciones» ya se cobró su primera pieza sin que nadie lo ejecutara a
   propósito.*

3. **Everett estaba mal traducido en las DOS frases**, y una de ellas
   (`«1,585 es el umbral verdadero»`) se contradecía con la sección de la lámina
   del propio documento. Lo correcto es `B/A > 1,73697`, y el `0,7369` es
   literalmente `1/L − 1`. **De ahí salió el hallazgo de la pasada**: el hueco
   `log₂(10/9) = 0,152` es el precio exacto de usar `5/3`, y los 24 números que
   Everett no certifica caen los 24 dentro.

4. **El criterio de fusión vale para `m ≥ 1`, no «para todo `m`».** Falla en
   `m = 0` en tres clases. **Y nadie lo vio porque `clasesfusion.py:202` dice
   `for m in range(1, 40)`** — la fuerza bruta no podía ver el único `m` que
   rompe. **Segunda vez del mismo patrón**, después del piso de la altitud.
   La cota del 43,57% no se mueve.

5. **«`T^k` es una biyección sobre `Z/2^k`» es falso al pie de la letra**, pero
   la conclusión estratégica se salva entera porque sólo usaba la versión
   verdadera. **El repo tuvo suerte**: la frase falsa estaba escrita al lado de
   la buena.

6. **Hercher tiene CORRIGENDUM (14-06-2026)** sobre el Teorema 21 — la pieza que
   `reimpl.py` marca como caja negra. Y **agradece el hallazgo a Xinjun Wang**,
   el mismo cuyo preprint este repo descartaba por «cero citas y metadatos
   descuidados». La Fase 3 del plan estaba calibrada sobre una impresión que hubo
   que revisar.

7. **`γ(ρ)` unifica cuatro entradas en una.** La identidad de `mapahilos.py` es
   exacta y es Terras en logaritmos; evaluada en `ρ = 1/2` da las tres constantes
   de parada, y el `1:2:3` es `ρ : 1 : 1+ρ`. **Pero no sirve para la fórmula**:
   para conocer `ρ` hay que haber terminado la trayectoria. Vale como
   unificación, no como vía.

8. **El `120` de `densidadfusion.py` es de Wu 1993.** Lo redescubrimos.

### Y lo que aguantó, que es la otra mitad

Trece piezas atacadas con implementación independiente, cero movidas: Terras
1.1, 1.2 y C1.4, la Tabla C, Gao 1993 (los 35.654 uno a uno sobre números de 151
cifras), Wu 1995, A076227, Elia–Tucker, la cota `5/3`, Eliahou, Sinisalo, el
`1,4784` y el Teorema 23. **Está en `CLAUDE.md`, en la sección nueva «La otra
mitad de la auditoría».**

**Y con ella el ANDAMIO**, que no se había escrito nunca: qué se cae si cae cada
pieza. De Terras 1.2 cuelgan seis ficheros, la cota del 43,57%, las dos
sucesiones de OEIS y el enunciado del cuarto camino — y por eso es la mejor
verificada. **De la traducción de Everett no cuelga nada, y por eso su error
vivió un año.** *Lo que sostiene mucho se delata solo; lo que no sostiene nada
hay que ir a auditarlo a propósito.*

### Estado de los pendientes de más abajo

- **La deuda de los siete `verificar_*.py`: SALDADA.** Están trackeados, y de
  paso se arregló el bug que uno de ellos tenía dentro (`frontera()` devolvía el
  último *jump value* en vez del último periodo, con las tres filas de su tabla
  cortas por 1,04× / 16,57× / 10,94×).
- **El pendiente de auditar las refutaciones sigue vivo y acaba de justificarse
  solo** con el caso de Wu–Huang. La tabla de las diez sigue sin ejecutarse.
- **El bloque 1 de la búsqueda web (la conjetura CST) tiene ahora un puntero
  desde la sección de las constantes**: `σ = χ` resultó ser esa conjetura, y el
  enunciado honesto (`E[χ]` es cota inferior demostrada de `E[σ]`) **mejora** la
  categoría de la constante de Wagon en vez de degradarla.
- **`oeis_borrador.txt` sigue sin enviarse**, pero ya no por la cita: la línea
  `%D` está completa. El bloqueo es el de `a(k)` idéntica para `3n+1` y `3n−1`.

---

## ⇢ LA AUDITORÍA DEL 01-08-2026: tres cosas que hay que decidir antes de nada

9 agentes, 3 fases, revisores adversariales, **20 correcciones a la propia
clasificación**. El informe entero está en el output del workflow `wkujctscn`.
Aquí va sólo lo que cambia decisiones.

### 1. `a(k)` ES IDÉNTICA PARA `3n+1` Y PARA `3n−1` — y eso toca el envío a OEIS

Verificado por el revisor con implementación propia, `k = 3…13`:
`1, 3, 8, 18, 39, 82, 170, 351, 721, 1476, 3012` — **los mismos términos con las
dos reglas**. El signo del `+1` es justo lo que convierte un mapa con **un**
ciclo en uno con **tres**; una cantidad invariante bajo esa simetría **no puede
ser evidencia sobre convergencia**.

El criterio de fusión sigue siendo **exacto y correcto** — es la regla `R3` de la
criba de Barina. Lo que se cae es su `sirve_para_la_formula`.

> **`oeis_borrador.txt` NO se envía hasta resolver esto.** Sería publicar una
> sucesión que no distingue el mapa de un ciclo del de tres.

*Pendiente: llegar a `k ≥ 20` y decidir si la coincidencia es un teorema o se
rompe. La biyección `r → 2^k−2−r` que se alegó **no se pudo confirmar**: los
cardinales coinciden, los conjuntos no.*

### 2. EVERETT ESTABA MAL TRADUCIDO, y la versión escrita era infalsificable

El `CLAUDE.md` decía `A/(A+B) < 0,5757 ⟺ B/A > 0,7369`, «más flojo que
`log₂3 = 1,585`». **Falso.** La `N` de Everett son pasos del **atajo**, donde
`X ≡ A` y `N ≡ B` exactamente (comprobado en 27, 221, 703, 9663, 100009,
63728127). La condición real es **`B/A > 1,73697`**, que es **más FUERTE** que
`log₂3`, no más floja.

Y muerde: el **27** (`B/A = 1,7073`) y el **63728127** (`1,6583`) **no la
cumplen y convergen igual** — que es exactamente lo que significa «casi todo `n`».

> Tal como estaba escrita, **toda trayectoria que llega a 1 la cumplía de sobra:
> una comprobación que no puede fallar.** Es justo lo que este repo se prohíbe.

### 3. UNA COTA NUEVA, Y ES MÁS FUERTE QUE LO QUE TENÍAMOS

De `C ≥ 0` en la identidad, sin asumir convergencia:

```
2^B · seq[j]  >=  3^A · seq[i]        para TODO par i<j de TODO n
si un tramo BAJA, entonces 2^B > 3^A
```

Verificado sobre **prefijos que nunca tocan el 1** (semillas de 20/60/200 bits):
356.850 pares, **0 fallos, 0 valores de `C` negativos**; y 272.063 tramos
descendentes, **0 violaciones**. **Convierte «el balance decide todo» de promedio
sobre trayectorias en cota por tramo.** Vive en `collazlamina.py`, en el cálculo
que el fichero hace antes de dibujar.

### Y el hueco, confirmado con números

`afirmaciones.db`: **5 filas `casi_todo_n`, las 5 con `fichero = NULL`.** Cero
instrumentos propios sobre densidad. Reparto: `todo_n` 17 · `clase_residual` 17 ·
`verificado_hasta` 15 · `promedio` 16 · `ciclos` 10.

**Y el repo tiene demostrado él mismo que el cuarto camino está vallado por los
dos lados:** `a(k) ≥ 1` para todo `k` (`descensoresto.py`) dice que la criba
modular **nunca se vacía**; la columna «ambiguo» de `redhilos.py` dice que ninguna
clase se decide antes del bit `k`. Lo que falta no es un pool más grande: es un
instrumento que mida **densidad logarítmica**, que hoy no existe en ninguna línea.

### Deuda inmediata

**7 ficheros `verificar_*.py` (5.034 líneas) están sin trackear en git.** Es el
mismo fallo del 30-07 —matemática fuera del repo— todavía a tiempo de evitarse.
**Nadie los ha auditado**: los escribió el workflow de lo ajeno mientras corría la
auditoría, y no entraban en su inventario.

> **⇢ SALDADA la misma noche (ver la entrada de arriba).** Están trackeados. Y el
> aviso de «nadie los ha auditado» resultó ser bueno: `verificar_terras.py [6](d)`
> tenía un bug —devolvía el último *jump value* que pasa en vez del último periodo
> `k`— que dejaba su tabla corta por factores de hasta 16,57×. Lo cazó
> `verificar_frontera_ciclos.py`, que es su revisión adversarial, y ya está
> arreglado con el hueco entre jump values comprobado en vez de supuesto.

---

## ⇢ PENDIENTE: convertir en `.py` lo que trajo la búsqueda web del 01-08-2026

Encargado el **01-08-2026**. Una búsqueda web cruzó los 63 puntos del repo contra
la literatura y trajo diez cosas. **Ninguna está comprobada con código propio, y
todas salen de fragmentos de búsqueda, no de haber leído los papers.** Es
exactamente el error de Wu–Huang otra vez si se construye algo encima sin
verificar. Un `verificar_*.py` por bloque, con revisor adversarial.

### Lo más importante que se encontró

**LA CONJETURA DEL *COEFFICIENT STOPPING TIME* (Terras 1976, bautizada por
Lagarias).** Es el cuarto camino enunciado por otro hace cincuenta años:

```
σ*(x) := min{ k >= 1 : 2^k > 3^{m_k(x)} }     <- solo el coeficiente
σ (x) := min{ k >= 1 : T^k(x) < x }           <- la parada de verdad
Siempre σ*(x) <= σ(x).   CST: son IGUALES para todo x >= 2.
```

- **Si CST es cierta, NO hay ciclos no triviales.**
- **Si CST es cierta, el conjunto de `n` con tiempo de parada `k` es exactamente
  una unión de clases de congruencia módulo `2^k`.**

Y en coordenadas del repo, `2^k > 3^{m_k}` es **`B/A > log₂3`**. La diferencia
entre `σ*` y `σ` es **exactamente el `C` de la identidad, o sea el `+1`**: `σ*`
ignora `C`, `σ` lo incluye. Luego **CST dice que el `+1` nunca cambia dónde cae
la primera bajada** — el objeto que este repo lleva tres sesiones midiendo sin
saber para qué servía.

### Los diez bloques a convertir en código

| # | resultado | qué comprobar |
|---|---|---|
| 1 | **CST** (Terras / Lagarias) | `σ*(n) == σ(n)` en los 11 hilos, los 243 récords y un barrido. Y medir la holgura `σ − σ*` |
| 2 | **Böhm–Sontacchi 1978**: `x = Σ 2^{m−b_k−1}·3^{k−1} / (2^m − 3^n)` | Es la misma familia que `pinzaciclos.py` (mismo denominador `2^m − 3^n`). Comprobar que las dos fórmulas dan lo mismo, y que recupera los tres ciclos negativos |
| 3 | **Bernstein–Lagarias 1996**: `Φ∘S∘Φ⁻¹ = T`, y `Q_∞` es homeomorfismo 2-ádico | Nuestra biyección finita mod `2^k` es su sombra. Verificar la conjugación a profundidad finita |
| 4 | **Monks 2006** (PAMS 134): **toda** progresión `A + BN` no constante es un conjunto suficiente | ⚠️ **doble filo**: legitima trabajar por clases, pero implica que **ninguna clase es más fácil que el problema entero** |
| 5 | **Krasikov–Lagarias 2003**: `#{n ≤ x que llegan a 1} ≥ x^0,84` | **Es la cota sobre densidad que el repo no tiene** (el hueco #64) |
| 6 | **Applegate–Lagarias 1995**: `π_a(x) ≥ x^0,81` para `a ≢ 0 (mod 3)` | la versión previa, por árbol |
| 7 | **Applegate–Lagarias 2003**: infinitos `n` con `σ_∞(n) > 6,14316·log n` | cota demostrada; nosotros sólo tenemos el promedio `10,428` |
| 8 | **Steiner 1977**: no hay 1-ciclos salvo el trivial | es la **base** de Simons–de Weger y Hercher. Tenemos el tejado sin cimientos |
| 9 | reducción a **`n ≡ 3 (mod 4)`** | las otras tres clases tienen secuencia finita que baja. Lo tenemos implícito y sin enunciar |
| 10 | **arXiv 2606.02621 (2026)**, Fibonacci vía estructura modular | puede ser nuestro `F(k+2)` de `mallaresiduos.py`, o algo mejor. **Leerlo entero** |

*Contexto: [ccchallenge.org](https://ccchallenge.org/) lleva 372 papers
catalogados y **1 formalizado**. Tao, Eliahou y Bernstein–Lagarias esperan
auditoría; Monks 2006 y Knight (2026) están en formalización.*

**Prioridad 1 es el bloque 1.** Si CST resulta ser lo que parece, deja de ser una
búsqueda difusa de «la fórmula» y pasa a ser un enunciado preciso con cincuenta
años, que el repo tiene el instrumental para atacar.

> **⇢ PRIMER CONTACTO CON EL BLOQUE 1 (01-08-2026, noche), y viene por un lado
> inesperado.** Auditando las constantes salió que el repo daba `σ = χ` por
> hecho, y **es precisamente la conjetura CST**: lo demostrado es `σ ≥ χ`.
> Medido: 0 diferencias en los impares hasta `2·10⁶`.
>
> **Y el enunciado honesto MEJORA la categoría de la constante de Wagon:**
> `E[χ]` es una **cota inferior demostrada** de `E[σ]`, no un «promedio». En la
> taxonomía de este repo eso vale más. *Es la única corrección de toda la pasada
> que sube algo de categoría en vez de bajarlo.* El puntero está escrito en la
> sección de las constantes de `CLAUDE.md`.

---

## ⇢ PENDIENTE PRIORITARIO: auditar las REFUTACIONES, no sólo las afirmaciones

Encargado el **01-08-2026**, para ejecutar **en cuanto terminen** los dos
workflows en curso (la auditoría del repo y la verificación de lo ajeno).

**El agujero, y es de método.** Este repo es adversarial con lo que afirma y
crédulo con lo que refuta. Las diez correcciones de *«lo que se creyó y era
falso»* se dieron por buenas en cuanto aparecieron, porque una corrección suena
a rigor. **Pero una refutación es una afirmación como cualquier otra**, y puede
tener los mismos defectos que ella denunciaba: confundir el mapa clásico con el
del atajo, comparar unidades distintas, tomar una muestra por una constante,
extrapolar de un rango a todos los `n`.

**El riesgo concreto: si una sola de las diez está mal, tiramos un dato bueno Y
anotamos una lección falsa.** Lo segundo es peor, porque la lección se aplica
después a otras decisiones.

**Cómo hacerlo:** un agente por corrección, aritmética exacta, y **revisor
adversarial detrás** — el mismo esquema que se usó con lo importado. Los dos
pools ya están en disco: los **once hilos de `hilos.db`** (el caso ordinario) y
los **243 récords de `records.json`** (el extremo). *Los extremos confirman; los
controles refutan.*

| # | la refutación a auditar | cómo se comprueba |
|---|---|---|
| 49 | el `0%` de encimadas de Harriss era falso | árbol inverso, claves módulo `Φ_N`, sin floats |
| 50 | el `1,7345` no es constante sino muestra | re-medir a `10³…10⁶` y ver si se asienta |
| 51 | «se escapan del rango» no discrimina | `3n+1` contra `3n−1` a cuatro tamaños |
| 52 | `2/ln(4/3)` es del atajo, no del clásico | **directo sobre los 11 hilos**: pasos / `ln(n)` en los dos mapas |
| 53 | al piso le faltaba `n impar` | **11 hilos + 243 récords**, forma entera exacta |
| 54 | el `45 = 3²·5` explicaba un nivel de 31 | `coralprimos.py`, primos vecinos del 45 |
| 55 | el `+1` aparece dos veces, no tres | **11 hilos** con `Fraction`: ¿`ε ≡ S` en todos? |
| 56 | el `0,2286` está en bits, no nats, y no es cota | **11 hilos**: `ε` de cada uno, en las dos unidades |
| 57 | el exponente de la criba es `0,108`, no `0,05` | `descensoresto.py` por tramos |
| 58 | la cita del `19.478.780.533` es 11× más débil | bibliográfica — **no** computacional, no forzarla |

**Ocho de las diez son computables, y cinco se pueden atacar directamente contra
los once hilos.** La 58 es bibliográfica y no hay que fingir que se verifica.

> **⇢ ESTE PENDIENTE ACABA DE JUSTIFICARSE SOLO (01-08-2026, noche).** Sin
> ejecutarlo, apareció el primer caso: **la refutación de la cita de Wu–Huang
> 2001 era la equivocada.** Se había dado por buena porque «no aparece en
> Crossref», y resulta que Crossref no indexa suplementos de revistas chinas de
> 2001. La cita existe, está catalogada, y sus datos se reprodujeron bit a bit.
>
> *O sea que la hipótesis de fondo de este pendiente —«una refutación es una
> afirmación como cualquier otra y puede tener los mismos defectos»— ya tiene un
> caso confirmado, y el defecto fue exactamente uno de los previstos: usar un
> instrumento fuera de su rango de validez.* **La tabla de las diez sigue sin
> ejecutarse, y ahora con más motivo.**
>
> *Y la 58 hay que releerla: el «11× más débil» de la cita de Laurore se calculó
> contra el `217.976.794.617` de Barina, que resultó ser el número equivocado.
> Contra la cota correcta el factor es **5,9**. La conclusión —cita válida pero
> débil, y publicada en mal sitio— no cambia.*

**Sólo después de esta pasada se borra el bloque E del resumen.** No antes.

> *Y si las diez aguantan, tampoco es tiempo perdido: pasan de «lo dijo Claude un
> día» a «verificado contra dos pools con revisor adversarial», que es la única
> forma en que este repo acepta algo.*

---

## 2026-08-01 (tarde) — el punto 5 cerrado, y una cita que existía y aun así sobraba

Mantenimiento otra vez, delegado a un agente como manda la regla de prioridad.
**Se cerraron las diez correcciones que quedaban del punto 5.** El detalle está
ahí abajo, en el propio punto 5. Lo que vale la pena contar aquí son las tres
cosas que salieron y no estaban previstas.

### 1. La cita fantasma existía. Y había que quitarla igual

El plan decía: *«localizar la cita del `≥ 19.478.780.533` o degradarla»*. Se
localizó — **Laurore, *Adv. Pure Math.* 15(6) (2025), DOI
`10.4236/apm.2025.156018`**, con DOI que resuelve en Crossref. Y aun así hubo que
sacarla, por tres razones acumuladas:

- editorial **SCIRP**, **cero citas**;
- el número es **5,86 veces más débil** que el estado del arte. O sea que el
  repo llevaba citada como *«lo que exige la literatura»* **una cota peor que la
  que ya se conocía**;
  > ⇢ **CORREGIDO el 01-08-2026 (noche): aquí decía «once veces», comparando
  > contra el `217.976.794.617` de Barina §6 — que resultó ser el número
  > equivocado** (exige `X₀ ≥ 2^71,884` y el récord es `2^71,019`). Con la cota
  > buena, `114.208.327.604` (atajo) / `186.265.759.595` (clásico), el factor es
  > **5,86**. La conclusión —cita válida pero débil, y en mal sitio— no cambia.
- **no encaja en la forma cerrada de Eliahou 1993** (`301994a + 17087915b +
  85137581c`, `b ≥ 1`, `a·c = 0`). Barrido exhaustivo propio: **0 soluciones**,
  mientras que `10.439.860.591`, `114.208.327.604` y `217.976.794.617` sí
  encajan.

> **La salida que faltaba en la lista.** Eran dos opciones —localizar o
> degradar— y resultan ser tres: **localizar y descartar igualmente.** Que una
> cita exista no la hace buena; hay que mirar dónde se publicó y si el número
> mejora o empeora lo que ya se sabía.

### 2. El `0,2286` no difería «en la tercera cifra». Estaba en otra unidad

El punto 5 decía que el grosor de la lámina y `ln(Res(993))` diferían en la
tercera cifra. **Es peor: uno está en bits y el otro en nats, y no miden lo
mismo.** `0,2286 bits = 0,158478 nats` contra `0,225654 nats = 0,325550 bits` —
factor **1,42**. Y el `0,2286` **ni siquiera es una cota**: su máximo se alcanza
en el par `(221 → 16)`, que es la trayectoria entera del 221, así que ese número
mide el 221 y nada más.

*Es la hermana exacta del acierto de `elmasuno.py` —allí dos números que parecían
distintos eran el mismo—, y las dos se arreglan igual: **traducir a las mismas
unidades antes de comparar.***

### 3. La frase de la holgura mezclaba TRES rangos, no dos

Lo que estaba anotado eran dos. Con `pisoaltitud.py` delante salieron tres: los
`99.999 casos` no son del enunciado de los impares (ése tiene **49.999**), son de
la variante del **atajo**. **Tercera aparición del mismo modo de fallo** — tomar
el valor de una muestra por una constante — después del `1,7345` del coral y del
`0%` de encimadas de Harriss.

### El saldo en código

`mapahilos.py` y `elmasuno.py` calculan `RES_993` en vez de copiarla (y el
segundo corta con `SystemExit` si alguien la vuelve a escribir a mano);
`guardarhilos.py` imprime por separado el hecho y la atribución;
`guardarafirmaciones.py` renombra el cuantificador a `clase_residual` y añade
tres correcciones y una constante. Los cuatro corridos, 0 fallos. Barrido cp1252
sobre los 35 `.py`: **0 hallazgos**.

---

## 2026-08-01 (mañana) — el día en que la documentación se editó a ciegas

Sesión corta y de mantenimiento. **El saldo es una regla nueva, y la pagó un
error propio.**

### El error, que es lo único que vale la pena contar

Se pidió una revisión del `CLAUDE.md`. Se revisó y se corrigió **sin hacer
`git fetch` antes**. El remoto tenía un commit de más (`b1b32f3`: 5.114 líneas,
siete `.py` nuevos y dos bases), y ese commit **ya había hecho las mismas
correcciones**. Todo el trabajo salió redundante y hubo que tirarlo y rehacerlo
contra la versión buena.

**Por qué no se vio:** `git status` a secas escribe `## main...origin/main` sin
flechas —que se lee como «sincronizado»— porque compara contra la última copia
*local* del remoto. El `[behind 1]` sólo aparece **después** del `fetch`.

> **Regla nueva, y va como PRIMERA sección del `CLAUDE.md`, antes de
> «Instalación»: `git fetch origin && git status -sb` antes de tocar nada.**
> Con el caso de hoy escrito como ejemplo, y la salida si ya editaste sin
> `fetch`: `stash` → `merge --ff-only` → mirar qué de lo tuyo sigue haciendo
> falta. Casi siempre es menos de lo que parece.

*Es el mismo tipo de trampa que las de cp1252 y la del estimador `B/A`: no es
falta de cuidado, es una herramienta que informa algo cierto y engañoso a la vez.
Por eso se anota, no se recuerda.*

### Lo que sí quedó arreglado (commit `d8b1d73`)

**Conteos.** El commit anterior decía *«conteos al día (28 .py)»* y **añadió
siete `.py` en ese mismo commit**, dejándolos desfasados en el acto:

| | decía | es |
|---|---|---|
| scripts | 28 | **35** |
| `numpy` | seis | **siete** (faltaba `descensoresto.py`) |
| `sqlite3` | dos | **cuatro** |
| `secuencia_de` | nueve | **diez** (faltaba `elmasuno.py`) |
| auto-verificados | 28 / 20 | **35 / 27** |

Barrido cp1252 rehecho sobre los 35: **0 hallazgos**.

**La Mitad C.** `guardarmallas.py` figuraba como *«el único programa cuyo
resultado no es una imagen»*. Hoy **19 de los 35 no dibujan** y sólo 16 abren
navegador o ventana. El caso por defecto de un script nuevo ya no es plotly, y
el documento ahora lo dice y manda copiar `pinzaciclos.py`.

**Dos correcciones del punto 5, consolidadas en la prosa** (estaban sólo en esta
bitácora, y la prosa seguía afirmando lo refutado):

- **El `45 = 3²·5` del coral**, que estaba presentado como *la candidata a nota
  original*. Corregido en los tres sitios donde vivía, con la ley que sí gobierna
  el umbral y la predicción fallida de los primos.
- **El `+1` aparece dos veces, no tres.**

Y **la Fase 1 del plan de la pinza** figuraba como pendiente teniendo ya
`reimpl.py` en el repo.

### Lo que NO se hizo, para que no se dé por cerrado

**El punto 5 quedó abierto: se cerraron 2 de sus 6 correcciones.** Quedaban la
holgura mínima del piso (1), el exponente de la criba (4), el `0,2286` contra
`ln(Res(993))` (5) y la errata de `RES_993` en `mapahilos.py` (6) — más las
cuatro cosas de la lista de abajo, de las que sólo se mencionó que las dos
discrepancias con Hercher existen, **sin escribir sus valores**. *(Las ocho se
cerraron esa misma tarde; ver la entrada de arriba.)*

*Nota de fechas: el punto 5 habla de «la sesión del 31-07-2026» y el commit que
la contiene está fechado el 30-07. No se tocó; queda anotado por si confunde.*

---

## 2026-07-30 — el día de las correcciones

Sesión larga. **El saldo real no son los hallazgos: son las siete correcciones a
cosas que el repo daba por buenas.** Ninguna la encontró nadie de fuera.

### Lo que se midió nuevo

| | |
|---|---|
| **El umbral de los 45 rumbos** | El coral de Harriss **sí** se vuelve a juntar. Primer choque exacto en profundidad **31**; a la 59 es el 1–1,5% de los nodos. Verificado con resto cero módulo `Φ₄₅` en aritmética entera. La causa es `45 = 3²·5`, o sea el ángulo, no Collatz |
| **Los negativos son `3n−1`** | Identidad exacta, 8.095.665 pasos, 0 fallos. Tres ciclos, ningún cuarto hasta 10⁶. Y las dos reglas ciclan en **lados opuestos de `log₂3`**, forzosamente |
| **Las constantes** | Wagon `9,4779555…` (con entrada en OEIS) medida a 0,064%. La escalera `1:2:3` de las constantes de parada |
| **El ajuste fino** | `q = 3` es el único impar que converge. Pero el umbral `4` resultó ser `f = 1/2` reescrito, o sea Terras otra vez |
| **Collatz contra la moneda** | Entropía de exactamente `k` bits hasta `k=12` y a profundidad 128; pero `P(impar\|impar) = 0` exacto y el patrón **se puede encargar** (`2^4000−1` da 3.999 impares seguidos) |
| **El piso de la altitud** | Una **cota**, no una tendencia. Lo único de la sesión con forma de teorema |
| **La pinza de ciclos** | Barrido de 2.147 millones de restos. Recuperó **los cuatro ciclos de Collatz sobre `Z`** sin que se le hablara de negativos |
| **`k = 32`** | La cota inferior demostrada sube a **43,5658%**. `a(32) = 1.871.137.623` |
| **Los récords publicados** | 243 récords de Roosendaal y Barina traídos y cruzados contra el repo. Nada se rompe |

### Las siete correcciones

1. El `0%` de encimadas del coral **era falso** — sólo valía hasta 3.000 semillas.
2. El `1,7345` del coral **no es una constante**, es el valor de una muestra (se asienta en `1,7320`).
3. La fila "se escapan del rango" del A/B **no discrimina**: mide el rango, no la regla.
4. `2/ln(4/3)` es la constante del **atajo**, no del mapa clásico.
5. El par `(8k+4, 8k+5)` es de **Garner**, no de Lagarias.
6. `Wu–Huang 2001` **no se pudo verificar**: sin DOI, no está en Crossref, y Elia–Tucker no la citan.
7. **Al piso de la altitud le faltaba la hipótesis `n impar`** — sin ella es falso en 28.325 de 50.000 pares.

**La séptima es la que más enseña.** El piso se probó contra los **243 récords
publicados** —los números que más suben y más tardan de todo lo conocido— y
**pasaron los 243**. Lo cazó el barrido de control sobre números corrientes.
*Los extremos confirman; los controles refutan.*

### Dos negativos nuevos

- **Ninguna constante de Collatz coincide con ninguna constante fundamental.**
  Test con modelo nulo: `p = 0,317`, y **sube a 0,45** al corregir el nulo.
- **La racha inicial no predice la altitud** (correlación 0,59). Lo que hace es
  ponerle un piso exacto — cota sí, tendencia no.

### Vías que quedaron cerradas, con su razón

- **El barrido de restos está muerto.** Terras excluyó en 1976 todos los bucles
  de periodo ≤ 2.592, y nuestro `k` *es* ese periodo. Todo su rango alcanzable ya
  es teorema. Para territorio virgen harían falta `2^2592` restos: 781 cifras.
  > ⇢ **CORREGIDO el 01-08-2026, y la conclusión se refuerza:** el 2.592 es una
  > **foto de 1976**, no la frontera. Con `X₀ = 2^71` el mismo argumento excluye
  > hasta periodo **114.208.327.603**; con sólo `X = 10⁶` ya llega a 4.700. Harían
  > falta `2^114208327603` restos, no `2^2592`.
- **Las cribas no sirven para ciclos, y es estructural.** `T^k` es una biyección
  sobre `Z/2^k`: cada vector de paridad es una clase única. No hay nada que
  descartar. Una criba necesita que muchas clases compartan destino.
  > ⇢ **CORREGIDO el 01-08-2026: las dos frases del medio eran falsas.** `T^k` **no**
  > es una biyección sobre `Z/2^k` —ni está bien definida ahí (`k=1`: `T(0)=0`,
  > `T(2)=1`, misma clase) ni `T` es inyectiva (`T(1)=T(4)=2`)—. Lo cierto es que
  > **resto → vector de paridad** es una biyección `Z/2^k → {0,1}^k`. Y clases que
  > descartar **las hay**: `pinzaciclos.py` descarta casi todas. Lo que no hay es
  > descarte **en bloque**. *La conclusión se salvó porque se apoyaba en la frase
  > de al lado, no en ésta.*
- **Los promedios no pueden demostrar nada** sobre un caso individual. La
  pregunta que queda como filtro permanente: **¿esto es un promedio o es una cota?**

---

## Lo que queda pendiente

> **⚠ ESTA SECCIÓN ERA UN FÓSIL, y lo cazó un adversario el 01-08-2026.** No
> estaba fechada, así que se leía como viva, y sin embargo era anterior al
> 30-07: sobrevivió a la purga, a las dos auditorías y a los dos tríos **sin que
> nadie la tocara**. **Siete de sus puntos mandaban hacer cosas ya hechas, ya
> refutadas, o sobre ficheros borrados.** Reescrita entera abajo.
>
> *Es exactamente el modo de fallo que el `CLAUDE.md` tiene documentado —«cuando
> se corrija algo, hay que buscar dónde más se afirmaba»— sólo que la lista
> estaba en el **otro** fichero, y por eso ninguna de las correcciones la
> alcanzó. **Una sección sin fecha se lee como vigente: o se fecha, o se
> revisa.***

### 1. El plan de la pinza, en tres fases

Lo que lo hace viable: **Hercher no *invoca* el teorema de Baker** — toda la
maquinaria diofántica entra como un número importado de Simons–de Weger.
*(Matiz obligatorio: la caja negra **sí** contiene trascendencia. Su Lema 12
sale de Rhin 1987. «No invoca Baker» es cierto de su artículo, no de la cadena.)*
Y la métrica del esfuerzo, medida: **60 líneas de stdlib excluyen `m ≤ 82`**;
todo el aparato del paper (dos programas en C++, cinco semanas de cómputo)
compra el tramo 82 → 91.

- **Fase 1 — ⇢ HECHA.** `reimpl.py` está en el repo: reproduce el Teorema 23
  **7/7** en 5,5 s, sin un float en la cadena que decide, y dejó **dos
  discrepancias contra lo publicado** (el `ε₇` y la fila `m = 276`), confirmadas
  después por segunda vía en `verificar_ciclos.py`.
- **Fase 2** — la escalera afín de Wang: un intervalo intersecado con una clase
  residual. *Eso es la pinza.* Media está construida en `clasesfusion.py`.
- **Fase 3** — **verificar a Wang**, no superarlo. Su preprint (`m ≤ 95`) no está
  arbitrado y nadie lo ha comprobado.
  > **Recalibrado (01-08-2026):** el **corrigendum de Hercher del 14-06-2026 le
  > acredita a este mismo Wang** el hallazgo del error del Teorema 21. Se
  > verifica porque es interesante y verificable, **no porque se sospeche de
  > él**: «cero citas» mide la edad del preprint y «metadatos descuidados» mide
  > su maquetación, y ninguna de las dos mide si tiene razón.

### 2. El resto de la cola

- **`clasesfusion.py` a `k = 34`.** Con `clasesparalelo.py` cuesta ~4× lo de
  `k=32`. No va a decidir la conjetura de Wu — los incrementos de la razón
  (`0,0050 → 0,0039 → 0,0037 → 0,0031 → 0,0027 → 0,0026`) encogen demasiado
  despacio para distinguir "geométrico" de "1/k" — pero alarga la única serie
  que puede. **Es el único pendiente de esta lista que sigue vivo tal cual.**
- **La recta del umbral del coral**, `(N+19)/2` si `N ≡ 1 (mod 4)` y `(N+11)/2`
  si `N ≡ 3`: está **medida y no demostrada**. Demostrarla sí tendría forma de
  cota. Es lo que quedó en pie de esa línea.
- **OEIS.** El borrador **ya no existe** (lo borró la purga del 01-08-2026), y
  **el motivo que lo mató se cayó** el mismo día: era *«`a(k)` sale idéntica para
  `3n+1` y `3n−1`»*, y con `espejoak.lean` eso pasó a ser **un teorema** — y el
  mismo criterio descalificaría a `A076227`, que sí está catalogada desde 2002.
  Lo único que queda es la decisión personal de abrir cuenta y firmar. **Si se
  retoma, hay que volver a redactar el borrador.**

**⇢ CERRADOS, y estaban aquí pidiendo trabajo ya hecho:**

- ~~**El número primo de rumbos**~~ — **HECHO, y la predicción FALLÓ**
  (`coralprimos.py`): el 43 y el 47 chocan *antes* que el 45. Es la única
  refutación ejecutable de una predicción propia que tiene el laboratorio.
- ~~**Colorear el árbol de `collazarbol.py`**~~ — **cerrado por la purga**: el
  fichero se borró porque el cierre lo ponía la esfera elegida a mano.
- ~~**El `+1` aparece tres veces**~~ — **aparece DOS** (`elmasuno.py`, 20.011
  casos con `Fraction`): el `ε` de la lámina y el sobrante `S` de la fracción
  impar son **la misma suma, término a término**. *(Y el `0,2286` que aquí se
  citaba como «grosor de la lámina» es el `ε` del 221 en **bits**, ni siquiera
  una cota.)*

### 3. La deuda de método

**La sesión del 30-07-2026 casi no dejó código.** Casi todo se midió en scripts
sueltos fuera del repo y sólo quedó escrito en el `CLAUDE.md`. Sobrevivieron
`pinzaciclos.py`, `cruzarecords.py`, `records.json` y `clasesparalelo.py`; el
resto de las mediciones **no se pueden reproducir**. Es la deuda más concreta
que tiene el laboratorio.

*(Parte de esa deuda se pagó el mismo día: `pisoaltitud.py`, `elmasuno.py`,
`reimpl.py` y `coralprimos.py` devolvieron cuatro de esas mediciones a fichero
ejecutable, y `afirmaciones.db` recoge los enunciados con su cuantificador.)*

### 4. LA PASADA CRUZADA — encargada a Fable 5, pendiente

**Qué hay que hacer.** Cruzar **cada una de las afirmaciones de
`afirmaciones.db`** contra **dos pools de datos a la vez**:

1. **Los once hilos de `hilos.db`** (100000 … 100010, con sus pasos, cruces,
   fusiones y cola común ya calculados). Son el caso ORDINARIO.
2. **Los 243 récords publicados de `records.json`** — retraso y altitud, de
   Roosendaal y Barina, hasta 2^71. Son el caso EXTREMO. `cruzarecords.py` ya
   sabe leerlos, así que el código de lectura está hecho.

Por cada pareja (dato, afirmación), decir si la cumple, la contradice, o si la
afirmación no aplica.

Nada hay que recalcular: las dos bases y el JSON están en el disco y
versionados. Se abren con `sqlite3` y `json.load` y se cruzan.

**Por qué los dos pools, y no uno.** Es la lección que dejó el piso de la
altitud el 30-07-2026, y es el mejor argumento que tiene este laboratorio:

> **Los extremos confirman; los controles refutan.**

Al piso lo probaron contra los 243 récords —los números que más suben y más
tardan de todo lo conocido— y **pasaron los 243**. El error del enunciado (le
faltaba la hipótesis `n impar`) lo cazó el barrido de números corrientes. Los
récords son tan raros que confirman casi cualquier cosa; los números del montón
son los que rompen.

Los once hilos aportan el montón, con casos incómodos a propósito: el `100009`
tarda 309 pasos y sube a 35 millones; el `100001` es el único solitario de los
once (todos sus cruces son cola común); y los seis del `100002` al `100007` se
funden con desfase cero. Los 243 récords aportan el rango: de 2 a 71 bits, que
es donde una cota se rompe si va a romperse por tamaño.

Si una afirmación falla en cualquiera de los dos pools, es un hallazgo. Si
aguanta en los dos, es un control de verdad.

**EL AVISO QUE NO SE PUEDE SALTAR, y es la razón de que la columna
`cuantificador` exista.** La pasada sólo significa algo para dos de los seis
cuantificadores:

| cuantificador | ¿tiene sentido cruzarlo contra 11 hilos? |
|---|---|
| `todo_n` | **Sí.** Once contraejemplos potenciales. Si falla uno, la afirmación es falsa |
| `clase_residual` | **Sí**, vía los restos de los once. Comprobación real. *(Se llamaba `clase_mod_2k` hasta el 01-08-2026; el módulo no siempre es `2^k`.)* |
| `casi_todo_n` | No. Once números no dicen nada de una densidad |
| `promedio` | **NO, y es peligroso.** Once trayectorias no estiman una media |
| `ciclos` | No aplica: ninguno de los once es un ciclo |
| `verificado_hasta` | No aplica: son afirmaciones sobre rangos, no sobre números |

**El modo de fallo concreto a evitar:** informar «11 de 11 confirmadas» sobre
una fila de tipo `promedio`. Eso no es confirmación, es ruido con forma de
tabla — el mismo error que produjo el `1,7345` del coral (valor de una muestra
tomado por constante) y el `+0,000002` de la holgura mínima del piso (dos
rangos distintos mezclados en la misma frase). La pasada tiene que **negarse a
evaluar** las filas de `promedio` y `casi_todo_n`, no evaluarlas y matizar.

**Y la trampa propia de estos once, que ya está medida:** las once trayectorias
comparten la cola `[16, 8, 4, 2, 1]` por obligación. 275 de los 1.258 cruces son
eso y no significan nada. `hilos.db` marca cada cruce con `es_cola` justamente
para esto; hay que usar esa columna y no contar la cola como coincidencia.

### 5. CONSOLIDAR EL `CLAUDE.md` — ⇢ CERRADO EL 01-08-2026

La sesión del **31-07-2026** dejó seis ficheros nuevos y **seis correcciones sin
escribir en el documento**, más cuatro cosas sueltas. **Las diez están hechas:**
la 2 y la 3 el 01-08-2026 por la mañana (commit `d8b1d73`), y las ocho restantes
esa misma tarde.

**Las seis correcciones al `CLAUDE.md`:**

1. ⇢ **HECHA. La holgura mínima del piso no es una constante.** Vale
   `log2(1 + 1/(3n))` y decrece con `n`. *Y la frase mezclaba **tres** barridos,
   no dos, que fue lo que apareció al mirarla con `pisoaltitud.py` delante:* los
   `99.999 casos` son del barrido a 100.000 **pero de la variante del atajo** —el
   enunciado de los impares tiene **49.999**—, el `+0,000002` es de un barrido a
   **200.000**, y el `28.325 de 50.000` es de 100.000. Verificado que la fórmula
   reproduce el mínimo medido: `log2(1+1/(3·99.997)) = +0,000004809` contra
   `+0,000004809` medido. *(Tercera vez del mismo modo de fallo; las otras dos
   son el `1,7345` del coral y el `0%` de encimadas de Harriss.)*
2. ⇢ **HECHA (`d8b1d73`). El `+1` aparece DOS veces, no tres.**
3. ⇢ **HECHA (`d8b1d73`). La explicación del coral era casi toda falsa.**
4. ⇢ **HECHA. El exponente de la criba `2^(−0,05k)` es el asintótico.** En el
   tramo `k = 20..40`, que es donde vive el `k = 34` de Barina, el decaimiento
   medido es **`0,108101`** — el doble. Cada bit extra elimina **7,2%** ahí y
   **3,4%** en el límite. La tabla por tramos de `descensoresto.py` (hasta
   `k = 1400`) está copiada al documento, con el aviso del signo: un exponente
   mayor significa que la densidad cae **más deprisa**.
5. ⇢ **HECHA, y salió peor de lo que decía este punto. El `0,2286` y el
   `ln(Res(993)) = 0,225654` no difieren «en la tercera cifra»: están en
   UNIDADES DISTINTAS.** El `0,2286` es `log₂` (bits) sobre los 6.555 pares del
   221; el `0,225654` es `ln` (nats) sobre trayectorias enteras. Traducidos:
   `0,2286 bits = 0,158478 nats` contra `0,225654 nats = 0,325550 bits`, factor
   **1,42**. Y el `0,2286` **ni siquiera es una cota**: el máximo sobre los pares
   del 221 se alcanza en el par `(221 → 16)`, que es su trayectoria entera, así
   que ese número es el `ε` del propio 221 en bits (`Res(221) = 1,17173`). Lo que
   sí vale es la desigualdad `h ≤ log₂(Res(seq[i]))`.
6. ⇢ **HECHA. Errata de constante.** `mapahilos.py` y `elmasuno.py` guardaban a
   mano `RES_993 = 1.2531421442887503`; ahora los dos la calculan como
   `2**61/(3**32*993)` y `elmasuno.py` corta con `SystemExit` si alguien vuelve a
   copiarla. Comprobado que no mueve nada: `mapahilos.py` sigue imprimiendo
   `techo = 0.225654` y `fallos: 0`.

**Y las cuatro cosas más que salieron al clasificar:**

- ⇢ **HECHA, con giro. La cita de `≥ 19.478.780.533 pasos` SE LOCALIZÓ, y hubo
  que quitarla igual.** Es **Laurore, *Adv. Pure Math.* 15(6) (2025) 351–389,
  DOI `10.4236/apm.2025.156018`** — el DOI resuelve en Crossref. Pero es de
  **SCIRP**, tiene **cero citas**, y sobre todo **el número es 11 veces más
  débil que el estado del arte**: Barina 2025 da `217.976.794.617` (atajo) y
  `355.504.839.929` (clásico). Además **no encaja en la forma cerrada de
  Eliahou 1993** (`301994a + 17087915b + 85137581c`, `b ≥ 1`, `a·c = 0`):
  barrido exhaustivo, **0 soluciones**, mientras que las tres cotas verificadas
  sí encajan. Sustituida por la de Barina en los dos sitios donde vivía.
  *Lección que no estaba prevista: la salida no era «localizar o degradar»,
  eran tres — faltaba **localizar y descartar igualmente**.*
- ⇢ **HECHA. La comprobación 4 de `guardarhilos.py`.** Separadas las dos cosas
  en el `CLAUDE.md` y en el `print()`: **el hecho es cierto y es propio**
  (`clasesfusion.py` lo rederiva desde Terras y decide los infinitos `m >= 1`), **la
  atribución a Wu–Huang 2001 sigue pendiente de localizar**. Quitada la frase
  «la literatura predijo nuestro hallazgo».
- ⇢ **HECHA. El vocabulario de `afirmaciones.db`.** `clase_mod_2k` renombrado a
  **`clase_residual`** en las 23 apariciones, con la razón escrita en la
  cabecera: la categoría es la **forma** del argumento —una comprobación finita
  que decide para los infinitos números de una clase de resto— y el módulo es un
  detalle del enunciado. Las dos filas que lo motivaron (la rueda del árbol, mod
  3/9/27; y los evitados de `2n mod 27`) ya no llevan una nota pidiendo perdón
  por la casilla. Base regenerada: **80 afirmaciones, 22 correcciones, 20
  constantes, las tres comprobaciones a 0 fallos.**
- ⇢ **HECHA. Las dos discrepancias con Hercher**, con sus valores y con la
  explicación de por qué ninguna mueve el resultado. El séptimo `ε` sale
  `1,2298e-43` contra `1,11e-43` (el nuestro es **más conservador**, y el
  denominador mínimo es **plano** en todo el rango: seis valores de `ε` entre
  `8e-44` y `5e-43` dan el mismo `7.941.964.418.702.608.664.581`). La fila
  `m = 276` de la Tabla 1 sale `4,640282e+18` contra `4,68e18`, y ahí la
  sospecha va contra el papel: `4,68e18` **no es denominador de ninguna
  semiconvergente de `log₂3`**, luego no es alcanzable por el método.

**Y la observación estructural que más importa para el objetivo elegido:** de las
**80** afirmaciones de la base, el bucle `casi_todo_n` tiene **5 filas y las 5 sin
fichero detrás**. El repo **no tiene ni una línea de código propio** que verifique
nada de tipo «casi todo `n`» — todo es literatura ajena (Everett, Tao). Y ése es
justo el hueco «casi todos → todos» donde se decidió apuntar. Hay **34** piezas
que componen sobre clases y **cero instrumentos propios sobre densidad**.
*(Conteos reverificados contra `afirmaciones.db` el 01-08-2026; los que había
—72, 3 sin fichero, 31 piezas— estaban desfasados.)*

---

## El objetivo, reformulado

> **No vamos a encontrar un número que haga bucle. Ni a demostrar que todos bajan
> a 1. Ni que exista uno que suba para siempre.**
>
> **Lo que sí se puede buscar es el cuarto camino: las reglas que generan todos
> los números de la secuencia de Collatz, sin generar la secuencia.**

Es alcanzable, se puede contradecir, y el repo ya tiene cuatro piezas antes de
que tuviera nombre: `mallaresiduos.py`, `clasesfusion.py`, `mallascerradas.py`, y
el Lema 8 de Hercher, que resultó ser el mismo objeto. Para calibrar: el
resultado más fuerte que existe sobre Collatz, **Tao 2019**, es de este tipo.
