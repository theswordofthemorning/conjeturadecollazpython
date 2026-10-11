# Perdices: repetir un bloque consume una divisibilidad finita

10-10-2026. Continúa [Mínimos futuros](MINIMOS.md) y el levantamiento
de [Semilla](SEMILLA.md). Se obtiene un límite exacto para repetir un
bloque expansivo desde **una misma semilla**, y se identifica el término
que impide sumar ese límite al cambiar de bloque. Catorce lemas nuevos
en Lean; el criterio completo sobre palabras conserva prueba escrita.

No se reclama prioridad ni se vuelve a presentar como nuevo que una
fuga pura no puede tener paridades eventualmente periódicas: eso ya
está en `CasaRetrato.rasgo_no_periodico`. Aquí se cuantifica la longitud
de una repetición finita y se examina su interrupción. **MuroB y
Collatz siguen abiertos.**

**Continuación:** [Cancelaciones](CANCELACIONES.md) formaliza la
resonancia de G y comprime los cambios en F. Su crecimiento y perfil
de salida no excluyen todavía una trayectoria infinita de la clase.

## 1. Mapa, bloque y semilla

Atajo T sobre naturales: n/2 para par y (3n+1)/2 para impar.
Una palabra w no vacía tiene d pasos, s unos y datos

```text
N=2^d, D=3^s, N y=D x+E.
```

E es la suma de `2^i 3^(unos posteriores a i)` sobre las posiciones
impares i de la palabra, indexadas desde cero. Suponemos **D>N** y
ponemos `C=D-N`. Entonces C es impar positivo y E>0. No se presupone
fuga ni inyectividad para los resultados finitos. Se permite x=0.
No hay ley aleatoria ni condicionamiento probabilístico.

El caso alcanza los bloques entre mínimos futuros distintos de P:
su factor D/N es >1. La igualdad entre potencias de 2 y de 3 no puede
darse en un bloque no vacío. Pero los resultados valen también para
otras palabras expansivas que no sean bloques entre mínimos.

## 2. Un potencial que conserva exactamente los factores impares

Multiplicar la identidad afín por C y usar D=N+C da

```text
N(C y+E)=D(C x+E).
```

Si una misma órbita realiza r copias consecutivas de w desde x,
con valores x_j al terminar j copias, entonces

```text
N^r(C x_r+E)=D^r(C x+E),
2^(dr) divide C x+E,
2^(dr) <= C x+E.                                       (1)
```

D es impar, por lo que se cancela en la divisibilidad. La última
desigualdad usa **C x+E>0**. Las tres afirmaciones están en Lean,
con las ecuaciones afines de cada bloque como hipótesis explícitas.
No se suponen ecuaciones para bloques que la semilla no realiza.

### Cuántos pasos coinciden: criterio completo escrito

Sea `v2(a)` la mayor potencia exponente de 2 que divide al entero
positivo a. El prefijo real de x coincide con la palabra periódica
`wwww...` durante exactamente

```text
v2(C x+E) pasos;
floor(v2(C x+E)/d) copias completas.                    (2)
```

Prueba independiente de (1): para w^r, el aditivo E_r satisface
`C E_r=E(D^r-N^r)`. Su congruencia
`D^r x+E_r=0 mod N^r` equivale a `C x+E=0 mod N^r`, ya que
C y D son impares. La biyección entre residuos y palabras de
paridades ya documentada en Semilla identifica así el residuo
con `-E/C mod 2^(dr)`. Para cualquier corte k, tomar dr>=k y
reducir módulo 2^k. La coincidencia dura mientras `2^k | C x+E`.

Este argumento también prueba la suficiencia y localiza el primer
bit distinto. **La biyección aplicada a todas estas palabras y la
igualdad con v2 no se formalizan de nuevo en este módulo.** (2)
tiene prueba escrita general y cotejo orbital independiente.

El representante mínimo r_j de w^j cumple
`2^(dj)<=C r_j+E`, luego crece sin cota al prolongar la palabra.
Una semilla natural fija no puede sostener esa repetición indefinida.
Esto cuantifica el mecanismo de levantamiento; no lo extiende todavía
a concatenaciones de palabras distintas.

No omitir el signo: para w=10, D=3<N=4 y x=1, el potencial
`(D-N)x+E` vale cero. La órbita 1,2 repite 10 indefinidamente.
No contradice (1)–(2), cuyas hipótesis expansivas no cumple.

## 3. Presupuesto desde el reloj y desde el cohete

Para cualquier órbita natural, sin inyectividad,

```text
2^u (T^u(n)+1) <= 3^u(n+1).
```

Es consecuencia de la cota afín de Colisiones y S_u<=u. Aplicando
(1) en x=T^u(n), con `H=max(C,E)`, queda formalizado

```text
2^(u+dr) <= H 3^u(n+1).                                (3)
```

En particular, si dr>=u,

```text
4^u <= H 3^u(n+1).                                     (4)
```

Para w y n fijos, (4) sólo permite u acotado. No pueden aparecer
arbitrariamente tarde repeticiones de **ese mismo bloque** cuya
duración iguale o supere todo el tiempo anterior. La escritura
`dr <= u log2(3/2)+log2(H(n+1))` de (3) es una traducción escrita;
Lean conserva las desigualdades enteras, incluidos u=0 y r=0.

Si además n>0 y su órbita es inyectiva, la cota de Cola
`(x_u+1) I_u<=ξ(n)` da una versión más ajustada, también en Lean:

```text
2^(dr) I_u <= H ξ(n),     I_u=1/P_u.                    (5)
```

La cota usa la misma ξ y la misma n en todos los reinicios. No
introduce una tasa de crecimiento de P. H depende del bloque:
no se puede dejar fijo al variar arbitrariamente w.

## 4. El término que aparece al cambiar de bloque

Para un potencial fijo `C x+E`, pero un nuevo bloque
`N y=D x+F`, la identidad correcta es

```text
N(C y+E)=D(C x+E)+delta,
delta=C F-E(D-N).                                      (6)
```

Está formalizada sobre enteros. Sólo cuando delta=0 se conserva
el presupuesto de divisibilidad anterior. Por ejemplo, con
`A=1`, `B=110` y potencial x+1,

```text
A: 2(y+1)=3(x+1),
B: 8(y+1)=9(x+1)+4.                                    (7)
```

Con el potencial x+5, B tiene defecto cero y A tiene defecto -4.
Cambiar de potencial para cada bloque no elimina estos términos.
La cantidad de cambios o su signo, por sí solos, no acotan las
cancelaciones 2-ádicas que permiten nuevas repeticiones.

### Una transición exacta para estudiar esas cancelaciones

En una concatenación infinita formada sólo por A y B, tiene que
haber infinitos B: una cola de A queda excluida por (2).
En la entrada de B, `x=4z-1` con z impar positivo. Después de B,
`y+1=(9z+1)/2`. Si siguen a copias de A antes del siguiente B,
la siguiente entrada `x'=4z'-1` satisface

```text
2^(a+3) z'=3^a(9z+1),
a=v2(9z+1)-3,
z'=G(z)=3^(v2(9z+1)-3) (9z+1)/2^v2(9z+1).             (8)
```

Necesariamente `v2(9z+1)>=3`, equivalente a `z=7 mod 8`.
Es también suficiente para realizar B seguido de esas a copias
de A y alcanzar otra entrada de B: cada A reduce en uno la
valuación de x+1, y B exige que esa valuación sea exactamente 2.
Por tanto una concatenación infinita de esta clase equivale, tras
su primer B, a una órbita positiva de G que permanezca en `7 mod 8`.
Además `G(z)>(9/8)z`; no puede cerrarse en un ciclo.

Ejemplo: z=7 da a=3 y G(7)=27, que sale de esa clase. Corresponde
en T a la transición desde x=27 hasta la siguiente entrada x'=107.
**No se prueba que toda semilla salga.** Este mapa es un caso de
prueba para las cancelaciones, no una sustitución del MuroB general.
Las identidades de salto de (8) están en Lean; su caracterización
completa mediante valuaciones y lenguaje conserva prueba escrita.

## 5. Ni un catálogo finito ni una cola acotada fuerzan periodicidad

La distinción se puede verificar sin suponer integridad infinita.
Tomar cualquier sucesión de A=1 y B=110 y seguir en los reales las
ramas afines indicadas. **No es T** si una entrada deja de ser un
entero de la paridad requerida. Los factores por bloque son 3/2
y 9/8; ambos crecen y sus fronteras son mínimos de todo P futuro.

Para la cola en esas fronteras, las aplicaciones hacia atrás son

```text
f_A(t)=(1+2t)/3,       f_B(t)=(5+8t)/9.
```

Ambas llevan [1,5] dentro de [1,5], como certifica Lean. Las
imágenes de ese intervalo bajo los primeros q bloques son
anidadas y tienen longitud <=`4(8/9)^q`; su intersección determina
una única cola inicial theta. En todas las fronteras queda
`1<=theta_j<=5`; dentro de B las colas intermedias son
`(1+4t)/3` y `2t`, y todas quedan entre 1 y 10.

Para cualquier entrada real n>0, `ξ=n+theta`, `R_k->ξ`,
`P_k->infinito` y `t_k/x_k->0`. También
`sum 1/x_k<=27/n`: cada bloque tiene a lo sumo tres pasos y
`x_k>=n(9/8)^q` durante el bloque q. La construcción infinita
mediante intervalos tiene prueba escrita, no formalización Lean
en este módulo.

Se puede elegir B en los índices cuadrados y A en los demás.
Los huecos entre ceros son no acotados y hay infinitos ceros:
el itinerario no es eventualmente periódico. De modo que un
catálogo finito de bloques y una cola real acotada **no fuerzan
periodicidad a nivel simbólico**. No se afirma que esa elección
proceda de una semilla natural fija, ni que satisfaga (8).

Como control entero finito, w=B^r admite
`n_r=8^r-5` y `x_(3j)=9^j 8^(r-j)-5` para j<=r. Con parámetro
`ξ_r=n_r+5`, las colas son 5,7,10 en cada bloque. Realiza
exactamente r copias: la siguiente entrada es par. La prolongación
periódica exige el levantamiento 7:
`n_(r+1)=n_r+7*8^r`. Varía la semilla; no es una fuga infinita.

## 6. Evidencia y siguiente trabajo

[PerdicesRepeticiones.lean](PerdicesRepeticiones.lean) contiene
14 lemas. [comprobar_repeticiones.py](comprobar_repeticiones.py)
audita 25 módulos previos y compila sólo el nuevo: 26 módulos,
309 consultas, Lean 4.32.2 y únicamente axiomas estándar, sin
avisos ni pruebas incompletas. [Registro](evidencia_repeticiones.json)
y [salida](evidencia_repeticiones.txt). Revisión humana pendiente.

[cotejar_repeticiones.py](cotejar_repeticiones.py) usa enteros y
Fraction, suma cerrada para E e iteración directa independiente:

- 68 palabras expansivas de longitudes 1..7, 6596 semillas 0..96:
  primera discrepancia exacta y máximo de copias coinciden con (2).
- 884 combinaciones de palabra y número de copias r=0..12,
  1768 representantes: congruencia, potencial y primer fallo.
- 8539 presupuestos desde la misma semilla, reinicios u=0..64.
- 511 mezclas de hasta ocho bloques: 1022 extremos de intervalos,
  15366 cortes y 1291 transiciones de (8). Cada mezcla conserva
  su semilla durante todos sus cortes; varía entre mezclas.
- Familia B^r, r=1..12; bordes r=0, semilla cero, palabra unitaria,
  mezcla vacía y el ciclo contractivo 10 que queda fuera del teorema.

[Cotejo](cotejo_repeticiones.json). Ninguno de esos barridos decide
si existe una concatenación infinita desde un natural fijo.

El [registro versionado](../coherencia20260913/registro.json) añade
`perdices_repeticiones_presupuesto` y `perdices_repeticiones_mezcla`,
con sus límites formales explícitos: 312 afirmaciones, 206 demostradas,
86 medidas, 12 conjeturadas y ocho refutadas. Se regenera
`afirmaciones.db` con el generador existente; se conservan las
entradas anteriores y `respuestas.db`.

**Continuación ejecutada:** [Cancelaciones](CANCELACIONES.md) obtiene
la restricción aritmética de (8) y el mapa de reinicios. Queda buscar
una cota para historias no periódicas de una misma semilla antes de
generalizar a todos los bloques entre mínimos. Las congruencias de
cualquier historia finita siguen admitiendo representantes naturales;
excluir repeticiones de un único bloque no resuelve este paso.

```powershell
python -B -X utf8 depuracion/perdices20261007/comprobar_repeticiones.py --compilados "$env:TEMP/perdices_cruce_20261010" --salida depuracion/perdices20261007/evidencia_repeticiones.json
python -B -X utf8 depuracion/perdices20261007/cotejar_repeticiones.py --dmax 7 --nmax 96 --rmax 12 --qmax 8 --pasos 64 --salida depuracion/perdices20261007/cotejo_repeticiones.json
```

Si faltan objetos previos, reproducir primero [Mínimos](MINIMOS.md).
