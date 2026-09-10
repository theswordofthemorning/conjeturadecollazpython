# Puente de las Gacelas

10-09-2026. Continuacion de Mangostas: supervivencia futura y transferencia.
Nombre local, sin reclamacion de novedad bibliografica. Pruebas escritas,
ingredientes Lean y controles exactos; sin revision externa ciega.

## 1. Las medidas no son intercambiables

P es la cadena entera con bits justos independientes, desde z0=(2,c0).
tau es el primer paso que alcanza k=1; NO significa fusion del par.
S_t(z)=P_z(tau>t). En estados vivos poner h(k,c)=k-1, y h=0 al salir.
Ambas ramas compartidas conservan h; las mixtas tienen pesos h+1,h-1.
Por tanto Ph=h, incluso en k=2. Definir la cadena Q por

    Q(z,z') = P(z,z') h(z')/h(z).

Las probabilidades de ramas bajo Q son EXACTAMENTE:

- Compartido: 1/2, 1/2, sin cambiar c ni sus formulas de evolucion.
- Mixto: k/[2(k-1)] hacia arriba, (k-2)/[2(k-1)] hacia abajo.
  Desde k=2 la bajada tiene probabilidad cero.

La ley completa de Mangostas y su reloj M6 valen tambien bajo Q:
durante cada racha los bits siguen siendo justos dado el pasado.
Esto es un cambio de medida hacia DELANTE. NO se ha identificado Q
con la reversion de una excursion real ni con el limite al condicionar
supervivencia lejana. El h-transform de alturas en V2 ya figuraba en
Truchas; aqui se comprueba la cadena ENTERA, con el reloj endogeno.

Para cualquier prefijo vivo de longitud r, su peso bajo Q es su peso
bajo P multiplicado por h(z_r)/h(z0). Si 0<=r<=H, entonces

    d P(. | tau>H) / d Q  sobre el prefijo =
       h(z0) S_(H-r)(z_r) / [h(z_r) S_H(z0)].              (G1)

No se puede borrar el factor S_(H-r)(k,c): depende del estado completo.
Contraejemplo concreto: desde (2,0), S_4=12/16; de las 12 palabras
supervivientes, ocho empiezan en bit 0 y cuatro en bit 1. Asi,

    P(bit 0 | tau>4) = 2/3, mientras Q(bit 0)=1/2.

Ambas primeras ramas son COMPARTIDAS. Condicionar al futuro puede sesgar
precisamente los bits que eran libres antes de condicionar.

## 2. Supervivencia y reloj condicionado: una cota que si vale

Cada racha termina casi seguramente por Mangostas. El bit del siguiente
mixto es fresco: el instante se decide antes de leerlo. Por iteracion,
las alturas vistas en pasos mixtos forman un paseo simple simetrico,
desde altura relativa 1, absorbido en 0. No se afirma independencia
entre ese paseo y las duraciones compartidas.

Ese paseo se absorbe casi seguramente. Prueba breve: en cualquier tira
finita sale casi seguramente (bloques de suficientes bajadas tienen
probabilidad positiva uniforme). La probabilidad de llegar a altura
relativa R antes de 0 es 1/R, por la ecuacion lineal de ruina. No salir
nunca por 0 exige llegar a cada R; su probabilidad es cero. Cada numero
finito de mixtos consume tiempo finito casi seguramente, luego tau<inf
tambien para la cadena original. No confundir este retorno con Collatz.

En t pasos reales hay a lo sumo t mixtos. Acoplando con la sucesion
infinita de monedas mixtas, la supervivencia satisface

    S_t(2,c0) >= q_t = 2^-t binom(t, floor(t/2))
                   >= 1/sqrt(2t+3).                       (G2)

La primera formula se obtiene contando los caminos positivos: para
cada altura final j>=1, reflejar en el primer paso por 0 resta los
conteos binomiales de caminos desde -1 a los de caminos desde 1;
al sumar en j la diferencia telescopa al coeficiente central.
Para la segunda desigualdad, a_m=binom(2m,m)/4^m satisface
a_0=1 y a_(m+1)/a_m=(2m+1)/(2m+2). La identidad

    (2m+1)^2(4m+5) - (2m+2)^2(4m+1) = 1

prueba a_m>=1/sqrt(4m+1) por induccion. Usar q_(2m)=a_m y
q_(2m+1)=a_(m+1). La cota es uniforme en c0, incluidos cero y signos.

Dividir M6 por S_H permite una version condicionada LEGITIMA:
para n>=1, H,s>=0 enteros, a_n=2+floor(log2(2+n)),

    P(T_n>n(a_n+s+1) | tau>H) <= n sqrt(2H+3) 2^-s.        (G3)

T_n sigue siendo el tiempo del n-esimo mixto o la salida anterior.
No se presupone independencia. Esta cota paga un factor de horizonte:
un s adicional de orden log H lo absorbe. NO da un reloj geometrico
uniforme sin ese pago, ni el LLT/reversion de Truchas.

## 3. La parte multiplicativa no necesita ese traslado

En TODOS los pasos vivos, incluidos el absorbente, Aranas escribe

    u_(t+1) = A_(t+1) u_t + delta_(t+1),
    u=c/3^k, A=1/2 si bit 0, A=3/2 si bit 1.

Sea Pi_t el producto de los A. Bajo P los bits completos son iid:
se pueden prolongar independientemente despues de la salida. No se
condiciona al reloj, al camino de alturas ni a tau para estimarlos.
Con lambda=E[sqrt(A)]=(1+sqrt(3))/(2sqrt(2)), Markov da

    P(Pi_t > (31/32)^t)
        <= [lambda/sqrt(31/32)]^t <= (61/62)^t.

Certificados: lambda^2=(2+sqrt(3))/4<15/16, porque sqrt(3)<7/4;
(15/16)/(31/32)=30/31<(61/62)^2. Union sobre TODOS los t>=T:

    P(existe t>=T: Pi_t>(31/32)^t) <= 62(61/62)^T.          (G4)

Asi se puede evaluar en el tiempo dependiente tau sin parada opcional
de un producto ni monedas supuestamente libres tras condicionar.
Para x>=1 y entero T>=log(x)/log(32/31), (G2)-(G4) prueban

    P(tau>T y Pi_tau*x<=1)
        >= 1/sqrt(2T+3) - 62(61/62)^T.                     (G5)

Para todo T>=1024, el segundo termino es a lo sumo la mitad del primero.
Se comprueba al cuadrado en T=1024 con enteros y se propaga porque
61^2(2T+5)<=62^2(2T+3) para T>=29. En particular, tomando

    T=max(1024, ceil(log(x)/log(32/31))),

(G5) da un piso 1/[2sqrt(2T+3)], del orden 1/sqrt(log x) al crecer x.
Aplicar x=max(1,|c0|/9) controla la contribucion del arranque real u0.
Constantes holgadas, no optimizadas. Es una conclusion sobre PRODUCTOS,
no una nueva cota de densidad. No impone tau<=2T.

## 4. Lo que falta para P2

Al salir, u_tau=Pi_tau*u0+W_tau, donde

    W_tau = sum_(j=1)^tau delta_j prod_(i=j+1)^tau A_i.

Aunque el primer sumando sea pequeno, el segundo puede ser grande.
Falta una constante M INDEPENDIENTE del arranque y suficiente masa
CONJUNTA del evento de (G5) con |W_tau|<=M. Una mediana marginal o una
medicion de desplazamiento del 5% no prueba esa interseccion.

Tampoco Q soluciona esto automaticamente: (G1) trata prefijos hacia
delante; el W de salida depende de sufijos y de la absorcion. En V2
la comparacion de sufijos usa un reloj independiente y un nucleo LLT
de alturas. Aqui su analogo puede depender tambien de c.

Siguiente obligacion concreta: formular y contrastar un control conjunto
de W_tau y Pi_tau bajo la ley REAL de salida. Primero buscar un argumento
directo o un contraejemplo a uniformidad, antes de importar la reversion
de V2. El reloj ya aporta (G3), pero no es por si solo la transferencia.

## 5. Verificacion y alcance formal

```powershell
python depuracion/frente20260910/transferencia.py
python depuracion/frente20260910/transferencia.py --pasos 20 --semillas 999999937
lean +v4.32.2 depuracion/frente20260910/transferencia.lean
```

Lean demuestra ocho resultados sin `sorryAx` ni `native_decide`:
masa armonica para todo n,k>=1,c sobre el arbol entero, numeradores
de Q, identidad inductiva de balota, certificados de la cota exponencial
y su umbral, y conteos completos del contraejemplo condicionado.
Las probabilidades, el acoplamiento, (G1)-(G5) y las raices/limites
estan demostrados POR ESCRITO, no formalizados integralmente en Lean.

Python cruza P y Q exactas para seis semillas hasta t=16, y el puente
r=6,H=12 estado por estado. Verifica balota hasta 200 y cola binomial
hasta 400, 5.680 transiciones contra pares y 1.536 palabras de ocho
bits para la identidad afin, incluyendo salida, cero y signos. El cruce
por pares no usa la funcion de hijos, pero no es una auditoria ciega.
Los barridos NO prueban las cotas infinitas. Salidas en `transferencia_*.txt`.
