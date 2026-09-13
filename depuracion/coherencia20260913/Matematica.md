# Correcciones y deducciones del frente — 13-09-2026

Auditoría local. Se separan pruebas escritas, ingredientes Lean y controles
finitos. No es una prueba de P2, densidad uno o Collatz. Los nombres animales
de los corolarios remiten a las piezas existentes, sin reclamar novedad.

## 1. Pandas y Jirafas: límite correcto de densidad

Sea F_n la unión periódica de clases que funden balanceadas antes o en n,
de densidad `a(n)/2^n`, y F su unión. Para cada n fijo, F_n está contenido
en F. Por tanto `densidad inferior(F)>=a(n)/2^n`; tomando el supremo,

    densidad inferior(F) >= phi.
    phi=1 => F tiene densidad natural 1.

La igualdad para un phi arbitrario no se deduce de monotonía. Para j>=1,
poner `C_j={n>=1:n=j mod 2^(j+2)}` y `E_m=union_{j<=m} C_j`.
Cada E_m es periódico y tiene densidad menor que
`sum_{j>=1}2^(-j-2)=1/4`. Pero `union_m E_m=N_+`, pues n pertenece a C_n.
La unión tiene densidad 1. Esto refuta la regla de intercambio de límites
usada en `lemadepandas.txt`; no refuta una igualdad particular de Collatz.

La caracterización algebraica de Jirafas se conserva: pendientes iguales
en la fórmula de Terras hacen que una fusión balanceada sea de clase.
Pandas se conserva en su dominio: ambos tiempos hasta 1 finitos y
`1<=Res(n),Res(n+1)<3`, con igual altura clásica, implican iguales tiempos
de atajo y conteos impares. La razón de identidades da
`6^d=(n/(n+1))*Res(n)/Res(n+1)`; para n>=2 queda estrictamente entre
1/6 y 3 y su única potencia entera de 6 es 1. n=1 no tiene alturas iguales.

La dirección fusión -> igual altura finita exige que el encuentro no sea
posterior a una primera llegada de solo uno a 1 y que la cola común
converja. Para una clase a nivel n, los levantamientos `2^n*m+r`, m>=1,
no llegan a 1 antes de n, porque `T^j(x)>=x/2^j>1` para j<n. La fusión
en sí vale también en m=0. Las excepciones de primeras llegadas no
contradicen la identidad de Terras.

## 2. Un riesgo que desaparece no decide la absorción

No vale `p_i -> 0 => probabilidad de absorcion < 1`. Por ejemplo, para
riesgos condicionales `p_i=1/(i+1)`, i>=1,

    P(sobrevivir las primeras N oportunidades)
        = product_{i=1}^N (1-p_i) = 1/(N+1) -> 0.

Los riesgos tienden a cero y la absorción es casi segura. Para el
programa hay que demostrar divergencia de la suma de probabilidades
**condicionales a cada visita real**, no extrapolar p_t medidos por nivel.
El p_t del censo y ese riesgo por visita no son automáticamente iguales.

Tampoco `b(n+1)/b(n)->2` identifica el valor de la suma ponderada que
define phi. Multiplicar términos por una constante conserva el cociente
y cambia su suma. Un ejemplo entero con razón 2 y masa menor que 1 es
`b_n=floor(2^n/(n+1)^2)`: la suma `sum_{n>=1} b_n/2^(n+1)` es menor que
`(1/2) sum_{n>=1}1/(n(n+1))=1/2`. Es un contraejemplo al argumento de
la razón, no un modelo de los conteos Collatz.

## 3. Corolario del reloj de Mangostas y Gacelas

Usar exactamente P de Gacelas: bits justos independientes, arranque
`(2,c0)`, c0 entero y tau primera llegada a k=1. M es el número total
de mixtos de la excursión; T_n es el tiempo del n-ésimo mixto o de
la salida anterior. Gacelas identifica las alturas en los mixtos con
un paseo simple absorbido y demuestra que las rachas terminan casi
seguramente. Por tanto

    P(M>n)=q_n=binom(n,floor(n/2))/2^n.

Si M<=n, T_n=tau. De ahí la inclusión
`{tau>t} subset {M>n} union {T_n>t}`. Aplicando Mangostas (M6), con
`a_n=2+floor(log2(n+2))`, s>=0 entero,

    P_(2,c0)(tau>n*(a_n+s+1)) <= q_n+n*2^(-s).       (R1)

No se presupone independencia del paseo y las rachas. Tomar
`s=ceil(3 log2(n+1))`: el error es <=n/(n+1)^3 y el horizonte es
O(n log n). Como `q_n=O(n^(-1/2))`, al invertir ese horizonte:

    P_(2,c0)(tau>t) <= C sqrt(log(t+2)/(t+1)), t>=1,  (R2)

con C absoluta y uniforme en c0. Para precisar la inversión, tomar
`B=1+floor(log2(t+2))`, `n=floor(t/(8B))` para t>=128.
Se tiene t>=16B, n>=t/(16B), a_n<=B+1 y s<=3B. Por tanto el
horizonte es <=n*(4B+2)<=8Bn<=t. Ajustar C para los tiempos menores.

Si Delta_i son duraciones de excursiones de este tipo comenzadas en
tiempos de parada, (R2) vale dado el pasado para cualquier c_i. Para
eps>0, la serie de probabilidades `P(Delta_i>i^(2+eps))` converge:
su término es O(sqrt(log i)/i^(1+eps/2)). Borel–Cantelli entrega esa
cota eventual sin independencia entre excursiones. Esto controla los
tramos `(2,c_i)->k=1`; no incluye las estancias de frontera ni identifica
Delta_i con el tiempo global de la visita i.

Formalización: R1-R2 y Borel–Cantelli están escritos aquí, no ensamblados
en Lean. Los ingredientes aritméticos del reloj y de la balota sí están
en los archivos del frente. Los controles finitos de esta tanda no son
prueba del paso asintótico.

## 4. El blanco suficiente para W

Gacelas da `u_tau=Pi_tau*u0+W_tau`, con `u0=c0/9`. Para
`x=max(1,|u0|)` y `T>=log(x)/log(32/31)`, (G2) y (G4) implican

    P(Pi_tau*x>1 | tau>T)
        <= epsilon_T = 62*(61/62)^T*sqrt(2T+3).

Es suficiente encontrar M finito y p positivo uniformes en el dominio
de arranques, para el horizonte elegido, con

    P(|W_tau|<=M | tau>T(c0)) >= p.                 (W)

Si epsilon_T<=p/2, la intersección con `Pi_tau*x<=1` tiene probabilidad
condicional >=p/2, por una resta de probabilidades. Multiplicar por
`P(tau>T)>=1/sqrt(2T+3)` da una masa del orden `1/sqrt(log x)` en
`|u_tau|<=M+1`. No requiere independencia de W y Pi.

**W sigue abierto.** Una mediana sin ese condicionamiento no prueba W.
El cambio h=k-1 de medida hacia delante no identifica por sí solo la
ley de los sufijos leídos desde la absorción. El horizonte aquí no
impone `tau<=2T`; no importar un resultado para otra ventana sin justificarlo.

## 5. Qué aceptar de la revisión 12

Las cinco tandas cuentan con actas en `revision12_adv1/`. La afirmación
de que la media medida de A a tiempo 24 convierte el reloj en O(n)
no es una demostración: falta una cota para `sum_i A(k_i)` a lo largo
del paseo y bajo la ley pertinente. Se mantiene el reloj probado en
(M6) y se usa su corolario R1-R2, que no necesita esa mejora.

Sí se puede mejorar la caja de Erizas usando Gacelas: con
`R_t=ceil(sqrt(2t+3))`, escoger

    h_t=ceil((4*(t+1)*(3t+1)*R_t)^(1/4)),
    J_t=4*R_t*(|c0|+t+1), L_t=J_t*3^(h_t+1).

El mismo argumento de Markov da al menos media masa en la caja.
Ahora `h_t=O(t^(5/8))`, de modo que `log D_t=O_c0(t^(5/8)+log(t+2))`.
Es un corolario escrito de las dos notas; los archivos originales y
sus certificados para la caja anterior conservan su alcance. No se
afirma que 5/8 sea óptimo ni se convierte esta obstrucción en P2.

## 6. Momento uno y deriva logarítmica

Para la moneda {1/2,3/2}, `E[m]=1` pero
`E[log m]=(1/2)log(3/4)<0`. No es el caso `E[log m]=0` de la
literatura de Babillot–Bougerol–Élie; esa diferencia se explicita en
el paper público 03. Fuente primaria consultada:
[Brofferio, Buraczewski y Damek](https://arxiv.org/abs/0809.1864).
La cota fraccionaria usa Jensen estricto para x^theta y subaditividad;
no demuestra una cola estacionaria 1/x para la cadena dependiente.

También se corrige el alcance de la referencia a Tao en el catálogo:
su resultado para cualquier función f(N) que tienda a infinito se formula
en **densidad logarítmica**, no en densidad natural ni como llegada a 1.
Fuente primaria: [Tao, Almost all orbits of the Collatz map attain almost
bounded values](https://arxiv.org/abs/1909.03562).

## 7. Cabras: conservar el signo de la coordenada

Desde la frontera (0,g), g positivo impar, las dos entradas a la torre
son c=(3g+1)/2 y c=(1-3g)/2. **Ambas son 2 módulo 3**. La clase 1
de la segunda aparece sólo al tomar su valor absoluto, que cambia la
coordenada de la torre. Los constructores de `cabras.lean` conservan
correctamente el signo; se corrige su comentario de procedencia.

No es cierto que sólo la puerta con vuelco pueda fundir. El camino
`(0,1) --0--> (1,2) --0--> (1,1) --1--> fusion` empieza por la otra
puerta; el par real (4,5) lo realiza. Se conserva la obstrucción
demostrada: ningún estado alcanzable de torre tiene c divisible por 3.
