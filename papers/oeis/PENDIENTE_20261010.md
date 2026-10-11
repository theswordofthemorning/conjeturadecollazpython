# OEIS: tres cupos previstos para la próxima sesión — 10-10-2026

No se envió, reservó ni editó nada en OEIS en esta sesión. El usuario dejó
las tres actuaciones para la próxima sesión y pidió cerrar ahora con commit
y push. Al reanudar, comprobar primero el estado vivo de las fichas y los
cupos; la instrucción de hoy fue documentar el plan, no ejecutar envíos hoy.

## Estado que conviene comprobar al reanudar

- [A078441](https://oeis.org/A078441) y
  [A400486](https://oeis.org/A400486) están aprobadas. La ficha pública de
  [A400487](https://oeis.org/A400487) también está aprobada: revisión #9,
  07-10-2026, con palabra clave `new`. El antiguo estado «proposed» del
  [índice histórico](LEEME.md) ya no rige.
- **Tres cupos previstos, no verificados en la cuenta.** La lectura por
  accesibilidad de la ventana Chrome abierta no encontró el documento OEIS;
  la aprobación pública de las fichas conocidas no excluye otros borradores.
  Abrir `My Drafts` y confirmar el cupo antes de comenzar.
- Leer las fichas vivas y sus discusiones antes de editar. Seguir el
  [procedimiento operativo](../../../zootheorem/drafts/PROCEDIMIENTO_OEIS.md),
  conservar las aportaciones editoriales y distinguir `proposed` de
  `approved`.

## Orden propuesto para los tres cupos

1. **Corregir [A398792](https://oeis.org/A398792).** Su comentario vigente
   presenta `a(n)/2^n` como cota de densidad de pares con igual altura de
   Collatz sin condicionar la llegada a 1 de todos los levantamientos. La
   cuenta exacta de clases que se encuentran sí está demostrada. Usar el
   texto preparado en
   [CORRECCIONES_PUBLICADAS_20260917.md](../../../zootheorem/drafts/CORRECCIONES_PUBLICADAS_20260917.md),
   contrastándolo con la ficha viva antes de guardar.
2. **Corregir [A398793](https://oeis.org/A398793).** El comentario vigente
   equipara que `a(n+1)/a(n)` tienda a 2 con que la cota anterior llegue a
   la densidad plena. Esa equivalencia no se desprende del cociente; el
   borrador citado da una identidad telescópica y retira la inferencia.
   También corrige el índice del último cociente mostrado. La corrección
   es una edición de la ficha existente, no una sucesión nueva.
3. **Proponer una sola sucesión nueva:** el primer paso del mapa clásico
   `f(x)=x/2` para `x` par y `f(x)=3x+1` para `x` impar en que se encuentran
   `m=A078417(n)` y `m+1`. El [borrador de encuentros](../../../zootheorem/drafts/PROPUESTA_ENCUENTRO_20260924.md)
   contiene nombre, definición, comentarios, ejemplo, programa y los
   primeros 120 términos (`3,9,5,3,7,3,10,5,3,6,3,8,...`). La
   [b-file de 10 000 términos](../../../zootheorem/seqs/bfile_meeting_equal_height_3x1.txt)
   está preparada. La función está bien definida: cada `m` de A078417 y
   `m+1` llegan a 1 tras igual número de pasos. Su utilidad es registrar
   *cuándo* se encuentran esos pares y relacionarlo con el umbral de Gao;
   no demuestra la conjetura de Collatz ni asegura aceptación editorial.
   Antes de proponerla, comprobar si procede añadir la referencia cruzada
   a A400486 y sustituir los marcadores `A000000` sólo después de asignar
   un número real.

## Evidencia y límite de la comprobación

La consulta pública de OEIS del 10-10 mostró A400487 aprobada. Las fichas
vivas de A398792 y A398793 aún contienen los comentarios por corregir. La
b-file vigente de A078417 (10 000 entradas) coincide con la copia local;
los 120 términos del borrador nuevo coinciden con su b-file y con un cálculo
directo independiente de las dos trayectorias. Las búsquedas por los primeros
12 términos y por la definición no devolvieron duplicado; eso no equivale
a una búsqueda exhaustiva. No se repitió ningún censo caro.

Si hay menos de tres cupos, conservar el orden de prioridad y dejar el resto
pendiente. OEIS exige interés general y una
definición clara; el rechazo NOGI de las tres series con parámetro fijo
`j=8,10,12` ([acta](../../depuracion/oeis20260924/LEEME.md)) aconseja
proponer sólo la sucesión que complementa A078417, sin reciclar aquellos
estratos. Registrar cada envío y cualquier respuesta editorial cuando ocurra.
