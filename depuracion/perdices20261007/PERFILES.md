# Perdices: perfiles finitos que se conservan mientras la órbita crece

14-10-2026. Continuación de [Recargas](RECARGAS.md) y de la
[ruta acordada](../coherencia20260913/RUTA_339_20261012.md#4-dónde-pondría-el-esfuerzo-principal).

**Resultado:** ninguna cantidad de la forma

```text
R(x) = H(x) + F(v2(u_1*x+v_1), ..., v2(u_m*x+v_m)),      (1)
```

con H no decreciente y una lista finita fija de formas afines no nulas con
coeficientes naturales, puede disminuir estrictamente en cada bloque real
A=1 y B=110. F es una función real arbitraria, no necesariamente lineal.
Para cada lista construimos prefijos reales arbitrariamente largos cuyos
perfiles coinciden en todas las fronteras de un mismo bloque compuesto,
mientras el valor de x aumenta. Las semillas dependen de la longitud.

La barrera general tiene **prueba escrita**. Lean certifica una familia
infinita para las dos formas x+1 y x+5 y la inexistencia del rango (1) para
esas formas, sobre valores reales. No se refuta el presupuesto global (P),
ni se construye una órbita positiva infinita. Sin pretensión de prioridad
bibliográfica; revisión humana pendiente.

## 1. Dominio y motivo de esta comprobación

Trabajamos con el atajo T(x)=x/2 si x es par y (3x+1)/2 si x es impar,
x entero positivo. A tiene un paso; B tiene tres con paridades 110.
Se exige la admisibilidad real desde una misma semilla durante todo el
prefijo. No hay ley aleatoria ni independencia entre bloques.

Una manera de intentar demostrar (P) sería construir un rango local,
acotado inferiormente y con pérdida uniforme por bloque. Antes de buscar
coeficientes para combinar logaritmos y valuaciones, esta nota comprueba
si esa familia puede funcionar. (P) no exige tal rango, por lo que una
obstrucción al rango no constituye una refutación de (P).

Los coeficientes u_i,v_i son naturales con u_i+v_i>0; por ello cada forma
es positiva en x>=1. Se permiten constantes positivas, factores comunes
pares, formas repetidas y la lista vacía. Las valuaciones son exactas.

## 2. Un certificado pequeño y su familia infinita

Para todo entero k>=0, el atajo realiza

```text
256k+231 -> 384k+347 -> 576k+521 -> 864k+782 -> 432k+391.
```

Las paridades son 1110, es decir AB. La diferencia entre la salida y la
entrada es 176k+160>0. En ambos extremos:

```text
(v2(x+1), v2(x+5)) = (3,2).
```

Se comprueba sin logaritmos: los cuatro potenciales son
8(32k+29), 4(64k+59), 8(54k+49), 4(108k+99); los factores entre
paréntesis son impares. Para cualquier H no decreciente y cualquier F,
el rango en la salida es mayor o igual que en la entrada. Si disminuyese
en A y en B, la composición impondría la desigualdad contraria.

[PerdicesPerfiles.lean](PerdicesPerfiles.lean) certifica las paridades,
los cuatro pasos de T, las valuaciones reales mediante padicValNat y la
obstrucción, para todo k. No se limita a evaluar el ejemplo k=0.

El resultado tampoco prohíbe que las valuaciones cambien entre fronteras:
se conserva el perfil al completar AB, no en cada paso interno.

## 3. Cualquier lista finita deja un punto fijo sin observar

Para a>=1, tomar W_a=A^a B. Tiene d=a+3 pasos, a+2 impares, y

```text
N=2^(a+3),   D=3^(a+2),   E=D-N/2,   C=D-N>0,
W_a(x)=(D*x+E)/N,
N(C*W_a(x)+E)=D(C*x+E).                                (2)
```

Derivación independiente: después de A^a se tiene
y+1=3^a(x+1)/2^a; B(y)=(9y+5)/8. La composición da (2).
C y E son impares. El punto fijo racional es

```text
q_a=-E/C=-1-1/(2*((9/8)*(3/2)^a-1)).                   (3)
```

Estos puntos son distintos, pues (9/8)(3/2)^a crece estrictamente. Cada
forma no constante u_i*x+v_i se anula en a lo sumo uno de ellos; una
constante positiva no se anula en ninguno. Entre a=1,...,m+1 hay, por
tanto, uno para el cual

```text
delta_i=C*v_i-u_i*E != 0   para todo i.                 (4)
```

Fijar ese a. Definir k_i=v2(abs(delta_i)), K=max_i k_i, con K=0 si la
lista es vacía. Se trata de constantes calculadas desde la lista, no
desde un tiempo de salida desconocido.

## 4. Cilindro real con perfil constante durante r repeticiones

Sea r>=1 cualquiera y h=d*r+K+1. Como C es impar, existe una única
clase rho módulo 2^h tal que

```text
C*rho+E = 0 mod 2^h.
```

Tomar cualquier n positivo de esa clase. El residuo mínimo ya es impar
y positivo, porque C y E son impares. Se pueden sumar múltiplos de 2^h.

**Admisibilidad.** Si 2^d divide C*x+E, también divide D*x+E. Puesto que
E=D-N/2 y D es impar, esto equivale a

```text
x+1 = 2^(a+2) mod 2^(a+3),   v2(x+1)=a+2.
```

Las primeras a aplicaciones de A son reales y dejan valuación 2 en
y+1, o sea y=3 mod 8. Este residuo realiza exactamente B=110. Así (2)
corresponde al mapa T y no sólo a una fracción formal.

Sean x_j=W_a^j(n). Por inducción en j, (2) consume d unidades de
divisibilidad en cada repetición y permite realizar las r copias:

```text
v2(C*x_j+E) >= h-d*j >= K+1,       0<=j<=r.            (5)
```

En los comienzos j<r queda además divisibilidad por 2^d, que habilita la
siguiente copia. Cada x_(j+1)>x_j, porque D>N y E>0.

**Estabilidad del perfil.** Para cada forma se tiene

```text
C*(u_i*x_j+v_i) = u_i*(C*x_j+E) + delta_i.             (6)
```

El primer sumando es divisible por 2^(K+1), incluso si u_i=0. El segundo
tiene valuación exacta k_i<=K. Su suma tiene entonces valuación k_i.
Como C es impar, resulta

```text
v2(u_i*x_j+v_i)=k_i,   para todos i y 0<=j<=r.          (7)
```

Esto prueba la construcción para **toda** lista finita y **todo** r.
El margen K+1 es necesario para este argumento: con las formas x+1,x+5,
W_1=AB y una unidad menos de precisión, 103 realiza AB hasta 175, pero
el perfil cambia de (3,2) a (4,2).

## 5. Obstrucción al rango y límites exactos

En las fronteras construidas, F recibe siempre el mismo argumento y H
no disminuye. Por (1), R(x_(j+1))>=R(x_j). Una disminución estricta de R
en cada A y cada B obligaría a R(x_(j+1))<R(x_j). Contradicción.

También quedan excluidos los rangos globalmente acotados inferiormente
de la forma c*log2(x)+F(perfil), con cualquier c real: si c>=0, se aplica
lo anterior. Si c<0, mantener una clase n=rho+t*2^h con perfil fijo y
dejar t crecer hace que R(n) tienda a menos infinito. Este último
corolario conserva prueba escrita, sin formalización específica.

La barrera no abarca funciones arbitrarias del valor entero, de las
partes impares o de la historia, ni rangos matriciales o lexicográficos.
No excluye una estimación acumulada que dependa de la semilla inicial.
La existencia de prefijos tan largos como se quiera, con semillas
distintas, no produce una semilla que permanezca para siempre.

**Pendiente principal:** (P) con epsilon=1/2 y K=2*ceil(log2(n+5)) sigue
sin prueba ni contraejemplo. El cotejo de los 34 testigos guardados
recorre sus 1817 prefijos de bloques completos y no encuentra fallos;
esto no mejora su estado lógico. No se ha ampliado el censo.

La siguiente obligación es estudiar el acoplamiento de las partes
impares en los cambios, conservando el balance R de Recargas y la semilla
original. Escribiendo q como la parte impar del potencial a la entrada
del bloque anterior, para A a B el nuevo potencial tiene parte impar
(3q+1)/2^eta_AB; para
B a A con v2(x+5)=5, pasa a (9q-1)/2^eta_BA. Son dos ramas distintas,
con las otras transiciones de [Recargas, sección 2](RECARGAS.md#2-recargas-de-ambos-cambios-incluidas-las-cancelaciones).
Hace falta una cota **acumulada** que use esas restricciones enlazadas;
no bastaría otra función de un catálogo fijo de valuaciones. Esta nota
no demuestra esa cota ni una equivalencia con el Collatz general.

## 6. Evidencia y reproducción

Continuación: [Transporte impar](TRANSPORTE_IMPAR.md) acota el factor de
los cambios y prueba el presupuesto doble para prefijos con hasta un
cambio. La estimación acumulada para varias alternancias sigue abierta.

- [Cotejo independiente](cotejo_perfiles.json): 162 cilindros construidos,
  729 fronteras, con hasta seis formas que anulan los primeros puntos
  fijos, seis repeticiones y tres representantes por clase. Incluye lista
  vacía, constantes, factores pares, descarte de delta=0 y el borde de
  precisión. Además, 66 miembros de la familia 256k+231, incluidos
  k=2^20 y k=2^80. Se comparan T paso a paso, fórmulas afines y dos
  implementaciones de valuación. Estos controles no sustituyen la prueba.
- [Lean](evidencia_perfiles.json) y [salida](evidencia_perfiles.txt):
  versión 4.32.2; doce consultas con sólo propext, Classical.choice y
  Quot.sound; sin sorryAx. Compilación desde fuente e imports directos
  cotejados con Mathlib fijado. Sin reconstrucción transitiva completa.
  La construcción para una lista finita arbitraria permanece escrita.
- [Conservación y mantenimiento](evidencia_sesion_perfiles.json),
  [auditoría del mapa](auditoria_mapa_perfiles.json): se conserva el
  catálogo previo y se incorpora una afirmación con alcance explícito.

```powershell
python -B -X utf8 depuracion/perdices20261007/cotejar_perfiles.py --formas-max 6 --repeticiones-max 6 --traslados 3 --familia-k-max 63 --salida depuracion/perdices20261007/cotejo_perfiles.json
python -B -X utf8 depuracion/perdices20261007/comprobar_perfiles.py --salida depuracion/perdices20261007/evidencia_perfiles.json
```
