# Respuesta a Sean Irvine y aclaración de los tres estratos — 17-09-2026

Se revisaron el estado del laboratorio, el plan de zootheorem, el paper 01,
los borradores vigentes y las discusiones reales de las tres fichas en Chrome.
Irvine escribió en A399819, a las 00:13 y 00:14 EDT del 17 de septiembre:
«This is incomprehensible.» y «How does any of this help with the Collatz problem?».
No se observó un rechazo; las tres estaban propuestas.

## Resultado externo comprobado

Se aclararon los comentarios de las tres fichas y se añadió la referencia
a Gao. A399819 también recibió el enlace a Elia y Tucker y el ejemplo 3067–3068.
Los datos, offsets, nombres, ejemplos originales y programas se conservaron.
Los comentarios antiguos sobre las fórmulas de los estratos inferiores se
sustituyeron por la definición directa, la descomposición y su motivación.

Se publicó la [respuesta completa](respuesta_irvine.txt) en
[A399819](https://oeis.org/draft/A399819), a las 16:35 EDT.
Las [notas compañeras](respuesta_companeras.txt) se publicaron en
[A399820](https://oeis.org/draft/A399820) y
[A399821](https://oeis.org/draft/A399821).
Las tres se reenviaron y se comprobó **proposed**, con revisiones finales
#10, #9 y #9, respectivamente. Esto no significa aprobación.

`A*_antes.txt` captura los textos internos antes de editar;
`A*_vigente.txt` captura los textos después de guardar y reenviar;
`A*_final.txt` conserva las páginas con discusión y estado.
`A*_formulario.txt` documenta el cotejo anterior a guardar.
La lectura de las páginas muestra juntas inserciones y supresiones;
para interpretar el texto actual usar las capturas de formato interno.
No se modificó `respuestas.db` ni se reconstruyeron conversaciones.

## Argumento matemático usado

El mapa es `T(x)=x/2` para x par y `(3x+1)/2` para x impar.
Para `0<=r<2^n`, e_j(n) cuenta primeras fusiones de (r,r+1) al paso n,
con iguales conteos impares y exactamente j desacuerdos de paridad entre
los dos valores de entrada. Los pasos se numeran 1..n, incluida la fusión.
A399819, A399820 y A399821 corresponden a j=8,10,12.

Terras da `T^n(r+2^n*m)=T^n(r)+3^s*m` para el conteo impar s.
Igual s conserva la fusión al levantar el residuo, así que cada clase
representa infinitos pares. Una fusión anterior con conteos desiguales
no puede volverse balanceada después: a partir del encuentro ambos
conteos aumentan por igual. Tampoco puede aparecer una primera fusión
anterior sólo al levantar: las paridades y sus conteos se conservan, y
con pendientes iguales la diferencia afín anterior permanece no nula.

Sea A(n)=A398792(n), con A(1)=0. Cada clase ya fusionada tiene dos
levantamientos al siguiente nivel; las nuevas se reparten por j, luego

    sum_j e_j(n) = A(n)-2*A(n-1) = A398793(n-1),  n>=2.

Por telescopado, para N>=2,

    A(N)/2^N = sum_{n=2}^N sum_j e_j(n)/2^n.

El límite monótono de estas sumas es phi. Las tres sucesiones son
componentes de esta distribución, no una demostración de phi=1.
El número j es par porque los pasos compartidos aportan igual a ambos
conteos y las dos orientaciones mixtas deben compensarse.
El borde r=2^n-1 no puede contribuir: sus n entradas son impares,
mientras que las del vecino 2^n son pares. Por eso el programa OEIS
puede omitir ese residuo sin alterar la definición.

Para F, la unión de las clases balanceadas, cada aproximación periódica
tiene densidad A(n)/2^n y está contenida en F. Por ello
`densidad inferior(F)>=phi`; si phi=1, F tiene densidad natural 1.
No se afirma `densidad(F)=phi` en general. Para m>=1, las trayectorias
levantadas no llegan a 1 antes de n, pues `T^i(x)>=x/2^i>1` para i<n.
Iguales n y s dan iguales n+s pasos clásicos hasta el encuentro.
La igualdad de tiempos **finitos** a 1 exige que la cola común converja.
No se identifica sin más esta formulación con cada versión histórica
de la conjetura de Gao, ni se afirma resolver Collatz.

## Vínculo bibliográfico y comprobaciones

[Elia y Tucker, §4](https://arxiv.org/abs/1511.09141) emplean
3067–3068 como primer contraejemplo a la conjetura de Garner y levantan
la familia `2^19*m+3067`. El cálculo propio da primera fusión bajo T
en 18 pasos, valor 692, diez entradas impares por lado y desacuerdos en
1,2,3,6,9,14,15,18. Esta clase pertenece a e8(18)=237; el término 237
ya estaba en los datos auditados. Terras extiende el patrón a toda su
familia, con encuentro `2*3^10*m+692`.

- [Control independiente acotado](verificar_respuesta.py) y
  [salida](verificacion.txt): todas las clases en n=1..13 contra el
  algoritmo simbólico; identidades con `Fraction`; testigos iniciales
  de las tres fichas; par 3067–3068 y cinco levantamientos.
- Verificación histórica conservada: iteración directa hasta n=20;
  n=21..29 mantiene procedencia simbólica. No se repitió ese censo.
- Lean 4.32.2 ejecutó `zootheorem/lean/mirror_theorem.lean` correctamente.
  `#print axioms` de `terras`, `borde`, `periodico` y `espejo` mostró
  sólo `propext` y `Quot.sound`, sin `sorryAx`. La descomposición y
  el argumento de densidad anteriores son pruebas escritas, no nuevos
  teoremas formalizados en esta sesión. El primer intento sin fijar
  versión inició la descarga de 4.34.0 y se canceló; se usó la instalada.
- [Preparación](preparar.py): cotejo literal de los campos preservados.
  Los textos finales extraídos de OEIS coincidieron con los preparados,
  salvo la línea de revisión `%I` que actualiza el servidor.
  Al sincronizar zootheorem se reunieron `%S/%T` en una sola línea `%S`:
  el lector local separaba dos veces las comas de continuación de OEIS.
  Los enteros y offsets coinciden con los b-files; las capturas literales
  conservan por separado el formato original del servidor.

Siguiente acción editorial: atender la próxima respuesta; aprobación
pendiente. Siguiente acción matemática: P1 del estado del laboratorio.
No hubo commit ni push a GitHub en esta sesión.
