# Perdices: un criterio de cruce por frecuencias de una misma órbita

25-10-2026. Continúa [Sesgo de frontera](SESGO_FRONTERA.md), cambiando
explícitamente el objeto: ahora se cuentan **tiempos de una semilla fija**.
Se conserva Perdices, sin reivindicar prioridad bibliográfica.

**Resultado condicional:** si K>=163 y la distribución empírica de
`n,T(n),...,T^(K-1)(n)` módulo 9 está a distancia TV<=1/100 de nu_2,
entonces `3^S_K(n)<2^K`. Se obtiene un cruce del producto en tiempo K.
El criterio orbital con tres desigualdades marginales se formaliza
completo en Lean. No se demuestra que todo fugitivo satisfaga la
hipótesis de frecuencias. El balance también vale para cadenas
modulares con ramas prescritas: **no aporta por sí solo la integridad
que faltaba en el testigo racional de 23**.

La [extensión ternaria general](OBSERVABILIDAD_TERNARIA.md) identifica
este balance como el caso m=2, prueba su versión orbital para todo m
y determina la ambigüedad exacta de los flujos estacionarios.

## 1. Dominio, tiempos y medida

T(n)=n/2 para pares y (3n+1)/2 para impares, n>=1. Fijar una sola
semilla y x_j=T^j(n). S_K cuenta los impares entre x_0,...,x_(K-1).
Para K>=1 definir

```text
mu_K(r)=#{0<=j<K:x_j=r mod 9}/K,    0<=r<9.
nu_2=(0,8,16,0,11,4,0,2,22)/63.
TV(mu,nu)=(1/2) sum_r |mu(r)-nu(r)|.
```

mu_K es una distribución empírica temporal determinista. No se escoge
una semilla al azar ni se condiciona por supervivencia.
nu_2 es la estacionaria del proceso modular que escoge cada rama con
probabilidad 1/2; se verifica sumando sus dos imágenes módulo 9.
Se utiliza como referencia, no como ley demostrada de la órbita.

Denotar por C1 el número de tiempos con x_j=1 mod 3, por C2 los de
x_j=2 mod 3 y por C9 los de x_j=2 mod 9. Todos usan j<K.

## 2. Una identidad local y su telescopio

Definir `Phi(x)=1_(x=2 mod 9)+1_(x=2 mod 3)`, con 0<=Phi<=2.
Para cada entero n>=0 vale

```text
1_(n impar)+1_(n=4 mod 18)+1_(n=1 mod 3)=Phi(T(n)).       (1)
```

Es una identidad exacta de las dieciocho clases módulo 18, no una
medición. También se obtiene escribiendo por separado las dos ramas
módulo 9. Lean la demuestra para todo n con la definición literal de T.

Al sumar (1), sea E4 el número de tiempos con x_j=4 mod 18. Resulta

```text
S_K+E4+C1+Phi(x_0)=C9+C2+Phi(x_K),
S_K+C1 <= C9+C2+2.                                     (2)
```

No aparece un coeficiente dependiente del número de cambios A/B.
Pero (2) es un balance, no una estimación de sus frecuencias.

## 3. El puente cuantitativo desde una hipótesis temporal

Si TV(mu_K,nu_2)<=d, cada uno de los tres eventos anteriores difiere
de su masa de referencia en a lo sumo d. Sus masas bajo nu_2 son
1/3, 2/3 y 16/63. De (2),

```text
S_K/K <= 37/63+3d+2/K.                                (3)
```

Con d=1/100, la parte constante es 3889/6300. Para K>=163,

```text
3889/6300+2/K < 17/27 < log(2)/log(3),
27 S_K < 17 K,       3^S_K < 2^K.                       (4)
```

La última implicación se basa en 3^17<2^27, sin logaritmos numéricos.
El enunciado Lean usa las tres desigualdades enteras suficientes:

```text
97 K<=300 C1,   300 C2<=203 K,   6300 C9<=1663 K.
```

Formaliza desde ellas, y desde la trayectoria real, hasta el cruce.
El paso estándar de TV a las tres desigualdades de eventos conserva
prueba escrita; no se atribuye al módulo Lean.
La conclusión formal es el cruce del producto; no se sustituye por
`T^K(n)<n`, que requeriría controlar también el término afín.

Como consecuencia necesaria, si el producto final es >=1,

```text
TV(mu_K,nu_2) >= 8/567 - 2/(3K).                        (5)
```

En efecto `S_K/K>17/27`, y (3) con d=TV da (5).
Para un prefijo real A/B completo de L pasos, S_L>=2L/3, lo que da
la cota algo mayor `TV>=5/189-2/(3L)`.
Un hipotético fugitivo puro debe mantener esta desviación temporal;
no basta conocer las leyes terminales de poblaciones distintas.

## 4. Un ejemplo real que satisface la hipótesis

El criterio no es vacío. El programa construye un circuito euleriano
en las seis clases no nulas de nu_2. Usa, para cada rama de cada estado
r, exactamente `63 nu_2(r)` aristas. Tiene 126 pasos, 63 impares y
frecuencias exactamente nu_2. Repetirlo dos veces da K=252.

Dos constructores independientes del cilindro de paridades y CRT
módulo 9 producen una **semilla entera positiva** que realiza esos
252 pasos desde el estado 1 mod 9. T literal verifica toda la órbita;
mu_252=nu_2 y su producto es 3^126/2^252<1. La semilla se conserva en
el [resultado exacto](cotejo_frecuencias.json), no se toma una cadena
modular como si fuese por sí sola una órbita entera.

Es una construcción de un ejemplo finito. No demuestra la hipótesis
del criterio para una semilla arbitraria o para un fugitivo.

## 5. Control adverso: la integridad no se recupera con este balance

Para la palabra histórica de 53 pasos
`AABAAABBAAAAAABAAAAABABAAABAAABBB`, la semilla mínima real es 6416623.
El recorrido de ramas prescritas desde 23 pasa por 23,35,53 y después
produce 241/4 al completar B: no es una órbita entera.

Sin embargo, sus denominadores son potencias de 2 y se pueden reducir
módulo 9. Desde las dos primeras subidas, sus estados módulo 9 coinciden
con los de la semilla real durante todo el resto de la palabra. Es el
olvido ternario de Perdices: las diferencias se multiplican por 3 en
cada subida y dos subidas anulan la dependencia inicial módulo 9.

La versión modular de (1), con el bit prescrito y la marca de rama
par en estado 4, se cumple en ambos recorridos. Por tanto este balance
**no pasa como nueva restricción de integridad** frente al testigo 23.
Su utilidad es especificar una transferencia condicional y el tamaño
de la desviación necesaria; no cerrar la obligación aritmética de A/B.

La ley temporal usada aquí tampoco es la ley pi_K de Sesgo de frontera.
Intercambiar sus cuantificadores borraría precisamente el paso pendiente.
La mezcla temporal hacia nu_2 para todo n no es una propuesta válida:
las órbitas que llegan a 1 terminan alternando 1 y 2. Si se investigara
una hipótesis de mezcla, habría que restringirla y demostrarla para las
órbitas excepcionales hipotéticas, sin presuponer su inexistencia.

## 6. Evidencia y límite formal

[Cotejo](cotejar_frecuencias.py), [resultado](cotejo_frecuencias.json):
24636 balances orbitales, con 127 semillas durante 192 pasos y el
ejemplo construido de 252 pasos. La estacionaria se calcula por suma
geométrica y se verifica por propagación; el cilindro se obtiene por
composición afín y por levantamientos con T literal. Se contrasta
también el recorrido racional de 23, que este balance no excluye.

```powershell
python -B -X utf8 depuracion/perdices20261025/cotejar_frecuencias.py --semillas-max 127 --pasos 192 --periodos-euler 2 --salida depuracion/perdices20261025/cotejo_frecuencias.json
```

[Lean](PerdicesFrecuencias.lean) contiene siete consultas compiladas
con Lean 4.32.2 y axiomas estándar, sin sorryAx: identidad local,
telescopio de una trayectoria arbitraria, cota y criterio orbital hasta
el cruce. La conversión desde TV, las cotas de discrepancia (5), el
ejemplo euleriano y la interpretación del control racional conservan
prueba escrita y cotejo, no formalización completa.
[Evidencia](evidencia_lean_frecuencias.json) y [salida](evidencia_lean_frecuencias.txt):
imports directos y sus objetos cotejados con Mathlib fijado; no auditoría
transitiva completa. La revisión humana sigue pendiente.

```powershell
python -B -X utf8 depuracion/perdices20261025/comprobar_lean.py --lean C:/Users/Home/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean.exe --modulo PerdicesFrecuencias --salida depuracion/perdices20261025/evidencia_lean_frecuencias.json
```

La tercera [alta versionada](alta_registro.json) declara el cuantificador
condicional. La [conservación](evidencia_registro.json) coteja el catálogo
con el generador y mantiene intactas las 360 afirmaciones anteriores
a la sesión y respuestas.db.
