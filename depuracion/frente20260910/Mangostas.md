# Reloj de las Mangostas

Continuacion: [Puente de las Gacelas](Gacelas.md). El cambio armonico
conserva esta ley; el condicionamiento futuro finito puede sesgarla.
Se deriva una cota condicionada con pago de horizonte y se controla
directamente la parte multiplicativa, sin cerrar P2.

10-09-2026. Ley de la racha completa mediante valuacion truncada.
Nombre local; no se reclama novedad bibliografica.

## Resultado

Fijar una altura k>=2 y un estado entero c. Usar bits futuros justos,
independientes del pasado. L es el numero de pasos compartidos hasta
que c se vuelve impar; NO incluye el siguiente paso mixto. Si c ya
es impar, L=0. Mientras dura la racha k no cambia. Definir

    D=3^k-1, A=v2(D)>=1,
    r=min(v2(c),A), con r=A cuando c=0.

Entonces, condicionando al estado de entrada COMPLETO:

    r<A: L=r determinista;
    r=A: L=A+G, donde P(G=s)=2^(-s-1), s=0,1,2,... .          (M1)

En particular, para s>=0 entero,

    P(L>=A+s | k,c) <= 2^(-s),     E[L | k,c] <= A+1.        (M2)

En la segunda rama de (M1) hay igualdad en la cola. La ley depende
solamente de k y c modulo 2^A. NO depende de las valuaciones superiores
de entrada o de las recargas individuales. Esto no acota sus saltos
deterministicamente ni afirma L-v2(c)<=A-1.

## Prueba del mecanismo

Los dos pasos compartidos son c/2 y (3c-D)/2.

1. Si 0<r<A, escribir c=2^r*u con u impar, D divisible por 2^(r+1).
   Ambos hijos son 2^(r-1) por un impar: el nivel baja exactamente uno,
   cualquiera que sea el bit. Desde este momento nunca vuelve a subir.
2. Si 2^A divide c, escribir c=2^A*u y D=2^A*d, d impar. Los hijos son

       2^(A-1)*u,     2^(A-1)*(3u-d).

   Los factores u y 3u-d tienen paridades OPUESTAS. Exactamente una rama
   permanece divisible por 2^A y la otra cae al nivel A-1. La rama que
   permanece puede ser bit 0 o bit 1, segun el estado; no se fija de antemano.
3. Mientras estamos arriba, cada bit fresco ofrece probabilidad 1/2 de
   permanecer arriba. El numero G de permanencias antes de la primera
   bajada tiene la ley de (M1), incluso si los valores de c cambian.
   La bajada consume un paso y faltan A-1 pasos deterministas: L=G+A.

Esto incluye c=0, valores negativos y recargas repetidas. Hay palabras
infinitas excepcionales que nunca bajan; su probabilidad es cero. No se
afirma una cota determinista de duracion sobre todas las palabras.

## Conteo finito y alcance de Lean

El automata tiene niveles 0..A. El 0 termina; un nivel 0<r<A tiene dos
ramas hacia r-1; el nivel A tiene una rama hacia A y otra hacia A-1.
Sea V(A,r,n) el numero de palabras de n bits cuyo estado sigue PAR
despues de esos n pasos. Exactamente:

    r<A: V = 2^n si n<r, y 0 si n>=r;
    r=A: V = 2^n si n<A, y 2^(A-1) si n>=A.                 (M3)

La conversion correcta es P(L>=j)=V(A,r,j-1)/2^(j-1), j>=1.
No confundir L>=n con "sigue par despues de n pasos", que es L>n.

`rachas.lean` demuestra el algebra con division entera y paridades,
y (M3) para TODOS los parametros del automata por induccion. Incluye
tres comprobaciones del ejemplo adversarial siguiente. Once resultados
sin `sorryAx`, Lean 4.32.2, nucleo sin Mathlib ni `native_decide`.

Limite de formalizacion: la identificacion global del arbol entero con
el automata, mediante los testigos de divisibilidad y la permutacion
adaptada de ramas, se explica arriba y se cruza en Python; no se ha
ensamblado como un unico teorema Lean sobre la cadena original. Tampoco
se formaliza una biblioteca de probabilidad. Sin revision externa ciega.

## Correccion del ejemplo de racha forzada

Desde (2,1398101), el mixto bit 0 produce (3,2^21). A la NUEVA altura
k=3, A=v2(27-1)=1. Por (M1), la racha realizada es 1+G, no 21 pasos
forzados. En concreto,

    P(L>=21 | esa entrada) = 2^(-20), no 1.

Un bit compartido 1 inmediato produce c=3145715, impar: L=1.
La palabra de ceros si realiza 21 pasos; no es la duracion minima.
La lectura de `lecturaracha.lean` sigue siendo aritmeticamente valida
para v2 del hijo. Sus congruencias NO identifican por si solas la racha
realizada ni su minimo sobre todas las palabras. Este ejemplo corrige
esa interpretacion de los comentarios de `equidistribucionmixto.py` y
del tramo "forzado" del antiguo ensamblaje; no invalida las congruencias.

## Reduccion exacta para una mezcla de entradas

Sea mu CUALQUIER ley de entradas (k,c), conocida antes de los bits
futuros. Para j>=1, (M1) da

    2^j P_mu(L>=j) =
      2^j mu(A>=j, 2^j divide c)
      + E_mu[2^A * 1_{A<j, 2^A divide c}].                  (M4)

Para A>=j, la duracion >=j equivale a la divisibilidad inicial; para
A<j, una entrada al nivel alto paga exactamente 2^(A-j). Las entradas
bajas no contribuyen a ese segundo termino.

Si la ley de alturas tiene maximo Amax, para TODO j>Amax la expresion
normalizada es la MISMA constante exacta

    C_cola = E_mu[2^A * 1_{2^A divide c}].                  (M5)

Ya no se necesita inspeccionar c modulo potencias arbitrariamente
grandes para estudiar la cola completa. Basta divisibilidad hasta A.
La identidad A=1 para k impar y A=2+v2(k) para k par da
2^A<=4k: los modulos de entrada necesarios son a lo sumo lineales en k.
Esta identidad se obtiene factorizando 3^(2h)-1 y separando h par/impar;
el Python tambien la cruza en sus alturas, pero no se formaliza aqui.

Esto NO prueba una constante C uniforme para todas las mezclas: una
entrada con 2^A|c y A grande tiene P(L>=A)=1 y exige C>=2^A.
Queda estimar los DOS terminos de (M4) en la ley pertinente al programa.

## Un control del reloj que ya no necesita mezcla

Corolario escrito de (M2), sin formalizacion probabilistica integral:
partir de altura k0>=2 y contar n pasos MIXTOS, o detenerse antes si
la excursion sale. Sea T_n el tiempo de ese evento, contando las rachas
compartidas previas y los mixtos. Las rachas inexistentes tras salir
aportan cero. Cada altura de entrada es <=k0+n. Poner

    a_n = 2+piso(log2(k0+n)).

Para cualquier entero s>=0, la union de las n cotas CONDICIONALES (M2)
entrega, sin asumir independencia entre rachas,

    P(T_n > n*(a_n+s+1)) <= n*2^(-s).                       (M6)

En efecto, salvo un evento de esa probabilidad, cada racha mide menos
de a_n+s y cada bloque racha+mixto cabe holgadamente en a_n+s+1.
Con s=techo(3 log2(n+1)), es un control O(n log n) con error <=n/(n+1)^3,
uniforme en c0. Cuenta pasos mixtos de UNA excursion, NO visitas al
fondo de la cadena completa. No se sustituye automaticamente el reloj
de Tortugas ni el lema P2 por (M6).

## Comprobaciones reproducibles

```powershell
python depuracion/frente20260910/rachas.py
python depuracion/frente20260910/rachas.py --pasos 24 --semillas 999999937
lean +v4.32.2 depuracion/frente20260910/rachas.lean
```

33.371 celdas de conteo hasta n=16, k=2..16, signos, cero y entradas
grandes; 16 arranques por 1.024 palabras mediante pares positivos y
5.680 controles de la cadena. No hay filtros de granularidad.

El barrido por defecto calcula 16 mezclas: cuatro semillas, t=8,12,16,20.
La mezcla selecciona padres impares en ese tiempo y su proxima rama
mixta viva, con ambos bits y sus pesos; descarta la bajada k=2->1.
NO es una muestra en epocas mixtas ni se condiciona a supervivencia
posterior. Cruza cinco bits futuros por la cadena contra (M4).

En esas mezclas, C_cola va de 33/47 a 202/191 (aproximadamente
0,702128..1,057592). Son valores medidos de (M5), no una cota universal.
Se compara j=1..32, pero la constancia para j>Amax procede de (M4),
no de extrapolar 32 observaciones. Las probabilidades incluyen bits
futuros nuevos: no se las confunde con divisibilidad en un censo fijo.
Ver `rachas_salida.txt`, `rachas_ampliada.txt` y `rachas_lean.txt`.

## Proximo paso y revision

Revisar el enlace entre el automata y la cadena original, el desfase
entre L>=j y V(n), y la medida de entrada de (M4). Atacar el paso de
(M2) a (M6) en tiempos de parada. Condicionar a sobrevivir un horizonte
FUTURO puede sesgar los bits y requiere otro argumento; no esta incluido.

Despues: contrastar el control (M6) con la transferencia que pide P2,
o acotar directamente (M4) bajo su pasado grueso. Se ha eliminado la
necesidad de modelar las recargas individuales para este control de
duracion, no todos los huecos del ensamblaje. No hay aun nueva cota de
densidad ni prueba de P2 o Collatz.
