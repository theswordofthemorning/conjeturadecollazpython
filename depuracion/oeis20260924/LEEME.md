# Rechazo de los tres estratos en OEIS — 24-09-2026

Hecho externo comprobado el 24-09-2026 en oeis.org con la cuenta del
usuario: **A399819, A399820 y A399821 fueron rechazadas y sus números
reciclados.** No se tomó ninguna acción externa en esta sesión.

## Veredicto literal

Firma: Sean A. Irvine. NOGI = *not of general interest*.

| Ficha | Marca | Texto del editor |
|---|---|---|
| A399819 | 24-09, 16:46 EDT | «Rejected, NOGI.» |
| A399820 | 24-09, 16:46 EDT | «Rejected, NOGI.» |
| A399821 | 24-09, 16:45 EDT | «I have decided to reject this submission of insufficient general interest. Nothing is offered here that could help with the Collatz conjecture and the presence of arbitrary constraints like "exactly 12 positions" detract from its general value.» |

El aviso llegó por correo («Sean A. Irvine reverted your changes to
A399819 and commented: Rejected, NOGI.»), pero lo anterior está tomado
del historial de OEIS, no del correo.

## Estado resultante de las páginas

Las tres quedan con `KEYWORD recycled` y `STATUS approved`, sin nombre,
datos, comentarios, ejemplos ni programa: sólo «Table of n, a(n) for
n=1..0». La cuenta muestra «My Drafts (0)».

Revisiones verificadas literalmente: A399819 #13 (16:46:00, reversión de
todos los campos a «allocated for Omar Said») y #14 (16:46:03, `allocated`
→ `recycled`); A399821 #12 (16:45:06) y #13 (16:45:09). De A399820 se
comprobaron la página final y el veredicto, no los números de revisión.

Un número reciclado vuelve al fondo común y puede reasignarse a otra
persona. **Toda cita futura de A399819–A399821 apuntaría a material
ajeno**: no deben aparecer en el paper, ni como nombre de b-file, ni en
tablas de estado. Los b-files `../../../zootheorem/seqs/b39982*.txt`
y `b399819.txt` conservan datos válidos con un nombre ya muerto;
renombrarlos toca `verify/verify_strata.py` y `sincronizar_zoo.py`,
y queda pendiente de decisión.

## Lo que no cambia

- A398792, A398793, A398794 y A398795 siguen **approved** e intactas
  (comprobado el mismo día: `author:"Omar Said"` da cuatro resultados).
  El propio Irvine aportó a(23)–a(29) a A398794 el 23-08 y a A398795 el
  28-08: el rechazo es a estas tres fichas, no al programa ni al autor.
- El rechazo es editorial. Nadie objetó un número, un offset, un ejemplo
  ni un programa. El control directo (n<=13 exhaustivo, n<=20 histórico)
  y Lean 4.32.2 sin `sorryAx` siguen en pie.
- La identidad `sum_j e_j(n) = A398793(n-1)` no dependía de OEIS, y el
  objetivo `phi=1` tampoco: el estado ya registraba que la aprobación no
  demuestra la densidad. Simétricamente, el rechazo no refuta nada.

## Motivo citado y lectura

La objeción escrita tiene dos mitades. La de forma —«arbitrary
constraints like "exactly 12 positions"»— es exacta: tres entradas con j
fijo recortan un parámetro sin razón interna, y el corte 8/10/12 no se
justificaba dentro de las fichas. La de fondo —«nothing ... that could
help with the Collatz conjecture»— coincide con lo que las propias
fichas declaraban: «They do not establish that lim A398792(n)/2^n = 1».

Secuencia de la revisión: Marcus (13-09: offset y ejemplo), Irvine
(17-09, 00:13 y 00:14: «This is incomprehensible», «How does any of this
help with the Collatz problem?»), Howroyd (17-09, 18:47 y 18:49:
terminología propia sin definir). Las tres objeciones se respondieron el
17-09 y las fichas volvieron a *proposed*; el rechazo llegó siete días
después. Lo que las respuestas arreglaron fue la exposición, no la
objeción de fondo, que nunca se contestó: por qué j = 8, 10, 12.

## Efecto lateral aprovechable

El límite de tres ediciones activas bloqueaba abrir A398792 para publicar
las correcciones ya preparadas de las cuatro entradas publicadas
(`zootheorem/drafts/CORRECCIONES_PUBLICADAS_20260917.md`). Con las tres
fichas cerradas la cuenta queda sin borradores y el slot está libre.
Enviarlas exige autorización expresa: el estado vigente prohíbe enviar a
OEIS o contactar personas sin ella.

## Opciones sobre la mesa (ninguna decidida ni ejecutada)

1. **Archivar.** Conservar los datos como material propio sin A-number,
   citarlos desde el paper como cálculo verificado y seguir con la ruta
   CF_F. Coste cero; no toca la relación con los editores.
2. **Reformular como una sola tabla.** Triángulo T(n,j) leído por filas,
   con todas las j a la vez y `keyword:tabl`, que elimina literalmente la
   objeción citada (el j fijo) y la terminología propia. Antes de gastar
   otro número conviene preguntar —SeqFan o los propios editores— si esa
   forma tendría interés; reenviar tras un NOGI sin cambio de objeto
   gasta credibilidad.
3. **Apelar.** El motivo es un juicio editorial, no un error localizable;
   sin objeto nuevo la reconsideración tiene poco recorrido.

Las tres requieren autorización del usuario. Prioridad matemática sin
cambios: primera obligación de `ESTADO_INVESTIGACION.md` (reloj global y
entradas admisibles), que no toca nada de esto.

## Continuación del mismo día: hay objeto nuevo

Buscando qué tiene de no arbitrario el parámetro `j`, salió que no puede
tomar cualquier valor: `e_j(n) = 0` para todo `j` impar, demostrado, y
`j >= 2` siempre. Está en [`Garzas.md`](Garzas.md), con verificador
independiente en [`garzas.py`](garzas.py).

Después salió un tercer resultado, también demostrado: **`e_2(n) = 1`**
para todo `n >= 4`, con el único par en forma cerrada
(`2^(n-2)-2` si `n` es par, `3·2^(n-2)-2` si es impar) y punto de fusión en
los repdígitos de base 9 (A125857), vía los repunits de base 3 (A003462).

Y una recursión que estructura toda la tabla: para `r = 1 (mod 4)`,
`n(r) = 2 + n((3r+1)/4)` y `j(r) = 2 + j((3r+1)/4)`, conservando el
balance. De ella sale que `j = 4` obliga a `r = 5 (mod 8)`, y que hay a lo
sumo un par con `j = 4` en esa clase por nivel. Para cerrar `e_4(n) = 1`
falta sólo descartar `r` par y `r = 3 (mod 4)`.

Y el contraste con la literatura, que es lo que más pesa: **las dos
columnas extremas son las familias clásicas**. `j = 2` es la familia de
Garner `(8k+4, 8k+5)` y `j = 4` son las de Wu y Huang `(32m+5)`,
`(64m+45)`, `(128m+29)`, término a término. Además el parámetro `j`
sobrevive donde falla la caracterización clásica: Elia y Tucker
(*Integers* 16 (2016) #A80) dieron contraejemplos infinitos a la conjetura
de Garner, `2^19 m + 3067`, y todos quedan clasificados aquí sin incidente
(paso 18, `j = 8`, punto de fusión 692 ≡ 2 mod 3). Su Teorema 2.1 se
reproduce sin fallos y hay que citarlo como suyo.

Esto cambia el peso de la opción 2 de la lista anterior. La tabla `T(n,j)`
ya no es «los mismos cortes con otra ropa»: tiene la mitad de las columnas
nulas por un teorema elemental, dos columnas constantes con forma cerrada
conjeturada y `130` testigos mínimos certificados. Sigue sin decidirse
nada, y sigue sin enviarse nada; pero la objeción citada —restricciones
arbitrarias— ya tiene respuesta que no existía esta mañana.

## Noche del 24-09: una sola propuesta, lista y sin enviar

El usuario decidió proponer **una sola** secuencia y enviarla él mismo el
25-09. Es el tiempo de encuentro de los pares de A078417:
`a(n)` = primer `k` con `C^k(m) = C^k(m+1)`, `m = A078417(n)`, con el mapa
clásico A006370. El texto listo para pegar, con la búsqueda de duplicados
(«No results» en cuatro consultas, control Fibonacci correcto), está en
`../../../zootheorem/drafts/PROPUESTA_ENCUENTRO_20260924.md`.

Sustituye a la «Propuesta 1» de `TRES_PROPUESTAS_20260924.md`, que usaba
A014682 y contaba como encuentros los que ocurren dando vueltas en el ciclo
1 -> 2 (7 y 8 «se encuentran» en el paso 10). El triángulo `T(n,j)` sigue
descartado.

Lo que se afirma y cómo se sostiene:

- **Gao, literal.** Para `m >= 2`, el conjunto de Gao
  `{m : C^k(m) = C^k(m+1) para algún k <= log2 m}` es exactamente
  `{A078417(n) : a(n) <= log2 A078417(n)}`. Prueba: la altura cumple
  `h(x) >= log2 x`, con igualdad sólo en potencias de 2, así que un encuentro
  tan temprano ocurre antes de llegar a 1. Cotejo directo sin discrepancias
  en `m = 2..199999`.
- **Cota de Gao.** `A398792(j)/2^j` acota por debajo la densidad inferior de
  ese conjunto: una clase contada allí se encuentra en `j` pasos de A014682,
  es decir en `j + s <= 2j` pasos de `C`, y `2j <= log2 m` para `m >= 4^j`.
  Con `j = 32`, `0,4356... > 0,389`.
- **`a(n) >= 3`, con igualdad exactamente si `m = 4 (mod 8)`** (pares de
  Garner). Prueba por casos: si `C(x) = C(y)` con `x != y`, entonces
  `{x,y} = {2v, (v-1)/3}`; ningún par consecutivo es así (`5v+1 = ±3`), el
  paso 2 no tiene solución y en el paso 3 sólo sobrevive `m/4` impar.
  Cotejado en los 10 000 términos.

Verificador: [`encuentro.py`](encuentro.py), salida en
[`encuentro_salida.txt`](encuentro_salida.txt), b-file en `b_encuentro.txt`.
`b078417_oficial.txt` es copia de la b-file de A078417 (Eric M. Schmidt,
oeis.org/A078417/b078417.txt, licencia CC BY-SA 4.0 de OEIS), usada sólo
para el cotejo.
