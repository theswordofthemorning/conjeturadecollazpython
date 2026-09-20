# Corolario cuantitativo candidato de Moscas, Mangostas, Gacelas y Hormigas

20-09-2026, segunda auditoría. Se sustituye el último ensamblaje casi
seguro por una desigualdad a tiempo finito. **Candidato en revisión**:
la aritmética de parámetros y C1 sobre el árbol finito de la cadena
están certificados. El resto del ensamblaje probabilístico sigue siendo
prueba escrita pendiente de formalización integral.

No se ejecuta un censo a los horizontes gigantes que aparecen abajo.

Ruta posterior de formalización: [CF_H armónica](Ventana_armonica.md)
evita la fórmula binomial y cambia explícitamente Q, G, D y p. Este
archivo conserva los parámetros de CF original y su evidencia.

## 1. Enunciado preciso

Cadena absorbente original desde `(0,1)`, bits iid justos y filtración
natural. Sea sigma el instante de fusión. Para un entero m>=10 poner

    N=2^m,       h=N^6,       U=h^4,       C_m=9U,
    r=24m+4,    d=N^4(10m+3),
    B=(24m+5)(48m+7).

Aplicar los parámetros de [Salida_ampliada.md](Salida_ampliada.md) a
la semilla C_m, con `s=3 ceil(log2(n+1))`. Denotar sus resultados por
`T_m,H_m,Q_m,R_m,G_m`. El símbolo h es el horizonte **global**, mientras
que H_m es la ventana de una excursión seleccionada. Definir

    D_m=16(ceil(log2(G_m+2))+1)^2,
    p_m=2^(-D_m)/(4Q_m),
    J_m=floor((N-1)/(D_m+2)).

La desigualdad candidata es

    P(sigma>h) <= 3/N + 66/h + 1/(4h^3) + (1-p_m)^J_m.  (CF)

Cuando J_m=0 se interpreta el último término como 1. La cota puede
ser trivial para m pequeños, pero todos sus parámetros están definidos.

Si se valida CF, como `T_m=768m+128`, `D_m=O((log(m+2))^2)` y
`Q_m=O(sqrt(m+1))`, resulta `J_m p_m -> infinito`. El lado derecho
tiende a cero. El [puente de cilindros](Cilindros.md) daría phi=1 y
densidad natural uno de fusión clásica dentro de log2(n).

## 2. Un evento bueno con probabilidad explícita

Todos los controles siguientes se toman bajo la ley original, sin
condicionar a que el evento bueno se cumpla.

**Magnitud hasta h.** Moscas da `E sqrt(|u_t|)<=33`, con `u=0` después
de absorber y `u_0=1`. Por Markov y unión sobre t=0..h,

    P(existe t<=h: |u_t|>U) <= 33(h+1)/h^2 <= 66/h.       (C1)

Certificado nuevo: [Momentos.lean](formal/Momentos.lean) importa la
transición completa y prueba una cota de momento 32 desde `(0,1)`.
`alcanza_conteo` identifica la probabilidad de cruce con el número de
hojas marcadas dividido por `2^h`; `envolvente_cf` demuestra C1 para
todo entero h>=1. El evento incluye los instantes 0..h y conserva la
absorción. No se evalúan las `2^h` hojas: se prueba por inducción.
Se conserva el término holgado 66/h del enunciado CF.

**Rachas de frontera.** En cada tiempo determinista t<=h, si la cadena
está en k=1, L_t es el número de compartidos que faltan hasta c impar.
Si está en k=0 o 1, J_t es el número de futuros mixtos de k=1 hasta
entrar en k=2 o absorber. Poner ambas variables en cero cuando el
estado no corresponda. Por las leyes de frontera de Reloj_global,

    P(L_t>r | F_t)<=2^-r,     P(J_t>r | F_t)<=2^-r.

Son variables de la continuación original, aunque su final pueda estar
después de h. La unión sólo enumera los **inicios** t=0..h. Su coste es

    2(h+1)2^-r <= 1/(4h^3), pues 2^r=16h^4.             (C2)

**Primeras N excursiones interiores.** Sean S_i las entradas a k=2
desde k=1, y D_i su duración hasta k=1. Si no existe S_i, ignorar ese
índice. R1, con n=N^4, a=4m+2 y s=6m, da, condicionado al pasado de
cualquier entrada finita,

    P(D_i>d | F_(S_i)) <= q_(N^4)+N^4*2^(-6m)
                         <= (sqrt(2)+1)/N^2 < 3/N^2.

No depende del offset de entrada. Por unión de los N índices,

    P(existe i<=N con S_i finito y D_i>d) <= 3/N.         (C3)

La evaluación condicionada en S_i se justifica directamente por bits
futuros iid en una parada discreta: descomponer por `S_i=t` y por los
prefijos de t bits. No se condiciona a D_i, a supervivencia futura ni
al evento bueno. Este argumento vale también si S_i puede ser infinito.

Sea E_m la intersección de los complementos de C1–C3. Entonces

    P(E_m^c) <= beta_m := 3/N+66/h+1/(4h^3).             (C4)

## 3. Reloj finito sin argumento circular

En E_m, cada racha de gap en k=0 que empiece antes de h dura como
máximo `v2(g)<=log2(U)=24m`; eso depende del gap **al inicio**.
Cada racha de k=1 que empiece antes de h dura a lo sumo r, y cada
tramo de frontera con inicio antes de h tiene a lo sumo r mixtos de k=1.

Por ello, la porción antes de h de cualquier tramo de frontera mide
a lo sumo B: como máximo r+1 rachas de gap, r rachas de k=1, y 2r+1
cambios de piso. Esta afirmación también vale para un tramo aún
incompleto en h. Sólo emplea rachas cuyos inicios son <=h.
No se extiende C1 a tiempos mayores que h.

Si sigma>h pero S_N>h, el prefijo de h pasos contiene a lo sumo N
porciones de frontera y N porciones de excursiones de índices <=N.
Estas últimas duran como máximo d, incluso si una no ha concluido en h,
por C3. En consecuencia `h<=N(d+B)`.

Pero `N(d+B)<h` para m>=10. Una verificación universal holgada:

    2^m >= 64(m+1),
    10m+3 <= 16(m+1) <= N/4,
    B <= 2048(m+1)^2 <= N^2/2.

La primera desigualdad se demuestra por inducción desde m=10.
Así `Nd<=N^6/4` y `NB<=N^3/2<=N^6/4`, porque N>=2.
Resulta `N(d+B)<=h/2<h`, contradicción. Se ha probado

    E_m y sigma>h => S_N<=h y |c_(S_i)|<=9U=C_m
                    para cada i<=N.                     (C5)

No se necesitó el reloj casi seguro ni su constante aleatoria.

## 4. Ensayos con guardia, sin condicionar al evento bueno

Usar el protocolo del candidato, con esta definición precisa de cierre.
En una entrada A_j=S_(I_j), esperar su salida R. Si cumple la ventana
de V3 para su offset inicial x_j, observar una palabra de Hormigas
de longitud calculada en R; si no, observar cero bits adicionales.
Después, esperar la primera nueva entrada a k=2 **estrictamente**
posterior al final de la palabra, o la absorción si ocurre antes.
Ese tiempo es A_(j+1). El éxito E_j es la absorción entre A_j y A_(j+1).
Tras absorber, repetir la parada absorbente y poner E_j falso.

Las paradas A_j son finitas casi seguramente: cada excursión retorna
y cada frontera termina; una palabra tiene longitud finita. Si termina
dentro de una excursión, se espera el retorno de esa excursión.
La filtración G_j=F_(A_j) cumple E_j medible en G_(j+1).

Añadir una guardia: el ensayo se admite sólo si está vivo y `|x_j|<=C_m`.
Con esa información conocida en G_j, los parámetros de V3 y V4 son
monótonos en |x_j| y la probabilidad de éxito satisface

    P(E_j | G_j) >= 2^(-D_m)/(4Q_m)=p_m.                 (C6)

Esto proviene de V3 y los bits de la palabra observada después de R.
El éxito definido incluye otras posibles absorciones, por lo que no
reduce ese piso. **No se afirma C6 condicionado a E_m.**

Sea A(j) el evento de que los primeros j ensayos sean admitidos y todos
fallen. A(j-1) y la guardia del ensayo j son conocidos en G_j. Entonces

    P(A(j)) <= (1-p_m) P(A(j-1)),
    P(A(j)) <= (1-p_m)^j.                                (C7)

La cota no exige independencia de ensayos ni que el suceso de pasar
las guardias sea independiente del éxito.

## 5. Cuántos ensayos caben

Mientras las entradas tengan offsets <=C_m, las palabras observadas
consumen a lo sumo D_m bits. La excursión principal no contiene otra
entrada desde k=1. Una palabra de longitud L contiene como máximo L
nuevas entradas; la espera posterior añade a lo sumo una entrada.
Incluso descartando una entrada que coincida con el final de palabra,

    I_(j+1) <= I_j+D_m+2.

En E_m y sigma>h, las primeras N entradas existen antes de h por C5.
La inducción anterior muestra que los primeros J_m ensayos son
admitidos y terminan sin absorción antes de S_N, porque
`I_1=1` y `1+J_m(D_m+2)<=N`. Si hubiera terminado una palabra después
de S_N, habría saltado más de D_m entradas, imposible en D_m pasos.

Por tanto `{sigma>h} intersect E_m` está contenido en A(J_m). C4 y C7
prueban exactamente CF. No se usaron riesgos condicionados a visitas
futuras, a E_m o al evento de no absorber nunca.

## 6. Conversión a una cota fácil de calcular

Sean `b_m=ceil(log2(4Q_m))`, `ell_m=ceil(log2(D_m+2))` y
`z_m=m-ell_m-1-D_m-b_m`. Si m>=ell_m+1,

    J_m >= 2^(m-ell_m-1),     p_m >= 2^(-D_m-b_m),
    (1-p_m)^J_m <= exp(-2^z_m).

También `beta_m<=4*2^-m` para m>=10. Así CF implica

    1-a(2^(6m))/2^(2^(6m)) <= 4*2^-m + exp(-2^z_m).     (CF2)

Como `D_m=O(log(m+2)^2)`, `b_m,ell_m=O(log(m+2))`, tenemos
`z_m -> infinito`. Esto es la deducción asintótica; no una extrapolación
de valores calculados. En m=1.000.000 la aritmética da
`D_m=627264`, `b_m=18`, `ell_m=20`, `z_m=372697`.
Ese dato verifica constantes, no el conteo a ese nivel.

## 7. Qué aporta y qué sigue pendiente

CF reemplaza la supermartingala infinita y los crecimientos aleatorios
del cierre anterior por dos uniones y una inducción finita de riesgos.
Los momentos y la cola R1 siguen siendo deducciones probabilísticas
escritas. El candidato debe revisarse como un todo antes de atribuir
una solución a Gao. Su texto original aún no se ha recuperado.
