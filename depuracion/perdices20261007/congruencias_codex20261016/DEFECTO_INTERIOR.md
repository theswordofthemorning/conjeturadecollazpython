# Perdices: defecto interior fijo después de un prefijo arbitrario

18-10-2026. Continuación de [Reloj por rachas](RELOJ_RACHAS.md).
Se conserva Perdices, sin reivindicar prioridad bibliográfica.

**Resultado:** cualquier palabra prefijada U que termine en B admite
infinitas semillas positivas cuyo recorrido contiene U A^k B, con k
arbitrariamente grande. En la racha A interior, el defecto del presupuesto
de tamaño es una constante que depende de U, no de k. Su proporción respecto
al presupuesto tiende a cero. Es una obstrucción en órbitas reales, no sólo
en la relajación lineal. **No excluye una cota conjunta de defectos ni prueba
el reloj uniforme.**

## 1. Dominio y enunciado exacto

T(n)=n/2 para n par y (3n+1)/2 para n impar; n es entero positivo.
A=1, B=110 son bloques de paridades efectivamente realizadas. Sea U una
palabra finita que termina en B, P su número de pasos T y S su número de
pasos impares. Escribir su fórmula afín como

```text
T^P(n) = (D*n+E)/N,    N=2^P, D=3^S,
d=floor(log2 D),        R=N+E, C=5D-R.
```

La fórmula sólo representa T en el cilindro de U. No se aplica a semillas
arbitrarias. No hay ley aleatoria ni condicionamiento probabilístico.

Existe una clase k=k_0 mod (2*3^(S-1)) tal que, para todos sus k
suficientemente grandes,

```text
n_k = (2^(P+k+2)-R)/D
```

es entero positivo y realiza U A^k B. Además,

```text
ell(n_k) = P+k+2-d,           L = P+k+3,
L-ell(n_k) = d+1,
H_A = ell(n_k)+(27/17)*S-P,
delta_A = H_A-k = 2+(27/17)*S-d.                      (1)
```

H_A es exactamente el presupuesto de la racha A en Reloj por rachas:
la contribución de U es (10/17) por paso A y (1/17) por paso B.
La racha A es interior porque tiene un B inmediatamente antes y otro
después, y k>=1. El número de rachas de U puede ser tan grande como se desee.
La semilla cambia con k: no se construye una órbita infinita desde un n fijo.

## 2. Construcción modular y realización

Los coeficientes de una composición satisfacen

```text
D-N <= E <= 5*(D-N),       4N <= C <= 4D.             (2)
```

Se comprueba por inducción: al añadir un bloque con coeficientes
(N_b,D_b,E_b), el nuevo aporte es D_b*E+E_b*N, y
D_b-N_b<=E_b<=5*(D_b-N_b). Para el último B, si los coeficientes anteriores
son (N_0,D_0,E_0), tenemos R=13N_0+9E_0. Así 3 no divide R.

**Levantamiento elemental.** Las potencias de 2 recorren todas las unidades
módulo 3^S. Para verlo sin suponer un logaritmo discreto solucionable,

```text
2^(2*3^(j-1)) = 1+3^j*u_j,   3 no divide u_j, j>=1.
```

El caso j=1 es 4=1+3. Al elevar al cubo,
u_(j+1)=u_j+3^j*u_j^2+3^(2j-1)*u_j^3, que sigue siendo una unidad.
Si e resuelve 2^e=R mod 3^j, sus tres extensiones
e+t*2*3^(j-1), t=0,1,2, recorren las tres unidades sobre ese residuo
módulo 3^(j+1). Exactamente una es R. El inicio módulo 3 es e=0 o 1.
Esto produce e módulo Q=2*3^(S-1), con 2^Q=1 mod 3^S.

Tomar k=e-P-2 mod Q. Entonces D divide 2^(P+k+2)-R; para k grande
el cociente n_k es positivo y

```text
D*n_k+E = N*(2^(k+2)-1).                             (3)
```

La divisibilidad por N identifica el cilindro correcto de U. Justificación:
una palabra de P paridades tiene una sola clase de semillas módulo 2^P.
En cada paso, la pendiente impar del numerador hace que exactamente una
de las dos extensiones del residuo tenga la siguiente paridad. Esa clase
anula D*n+E módulo 2^P; como D es impar, no hay otra clase que lo anule.
Por tanto (3) realiza U desde n_k y llega a x=2^(k+2)-1.

Desde x, A^k está permitido y llega a z=4*3^k-1. Como z=3 mod 8, B es
realizable y llega a y=(3^(k+2)-1)/2. Son fórmulas contrastadas también
con T paso a paso. En particular, la parte impar de x+1 es **1**, aunque
el prefijo U tenga muchas rachas. El n_k es además el mínimo positivo de
su cilindro U A^k B: pertenece a él y 0<n_k<2^(P+k+3).

## 3. Altura exacta y alcance de la obstrucción

Sea M=P+k+2 y h=M-d. La identidad independiente de tamaño es

```text
D*(n_k+5)=2^M+C.
```

D no es una potencia de 2, pues S>=2. Así 2^d<D<2^(d+1).
Para k grande, h>=1 y C<=2^h*(D-2^d). Estas dos condiciones implican
2^(h-1)<n_k+5<=2^h, de donde ell=h. Un umbral explícito suficiente
para la segunda condición es h>=bit_length(C); además se exige n_k>0.
Esto prueba (1) sin aproximaciones logarítmicas.

Como 27/17>log2(3), delta_A es positivo y fijo, mientras H_A=k+delta_A
tiende a infinito. Por tanto, para todo eta>0 y para todo prefijo U terminado
en B, algún miembro de esta familia satisface delta_A<eta*H_A. No existe una
pérdida proporcional positiva **en cada racha interior**, ni se obtiene
suponiendo sólo que ya hubo un número prefijado de cambios.

El fenómeno tampoco procede sólo del redondeo o de usar 27/17. Con el
presupuesto exacto H_A^*=log2(n_k+5)+S*log2(3)-P se tiene

```text
H_A^*-k = 2+log2(1+C/2^(P+k+2)) -> 2.                (4)
```

**Lo que no se deduce:** ni una caída de la suma ponderada de todos los
defectos, ni una refutación de la pendiente 3, ni una cota uniforme de L.
Los defectos de las rachas anteriores dependen de ell(n_k), que crece con k;
pueden compensar el pequeño defecto relativo de esta racha. En cada familia
con U fijo, L/ell tiende a 1. U tampoco se prolonga aquí desde una semilla
previamente fijada. La siguiente obligación sigue siendo relacionar las
pérdidas de varias rachas **desde la misma semilla**, admitiendo estas
rachas interiores casi saturadas. Las barreras de ventanas con más futuro
no se contradicen: la A construida sólo tiene un B a su derecha.

La continuación [Contexto interior](CONTEXTO_INTERIOR.md) precisa este
límite: esta familia de parte impar 1 termina tras B y, como mucho, un A.
Una nueva familia de parte impar 13 realiza `U A^a B A^2 V` para contextos
U,V arbitrarios (U termina en B), todavía con defecto central fijo.
Así tampoco basta exigir muchos cambios futuros para una pérdida por
racha. Las pérdidas conjuntas siguen abiertas.

## 4. Evidencia y frontera formal

[PerdicesDefectoInterior.lean](PerdicesDefectoInterior.lean) certifica seis
lemas: cola A^k B, concatenación con un camino dado, largo, altura exacta
bajo la identidad y el umbral indicados, defecto fijo y exceso fijo.
**El levantamiento modular, la extracción del cilindro para U arbitrario,
la existencia de infinitos k y las conclusiones de límite mantienen prueba
escrita; no se atribuyen a Lean.**

[Compilación](evidencia_defecto.json) y [salida](evidencia_defecto.txt): tres
módulos recompilados desde fuente, 28 consultas; Lean 4.32.2/Mathlib fijados,
sólo axiomas estándar, sin sorryAx. Se cotejan los imports directos.
[cotejar_defecto.py](cotejar_defecto.py) y [resultado](cotejo_defecto.json)
comprueban 16 prefijos, 48 miembros y 15 bordes pequeños, incluida la cola
con k=0 y sin prefijo. Los prefijos son
todos los terminados en B de hasta cuatro bloques, además de ABABAB.
Se comparan levantamiento ternario y ciclo modular completo; inversa literal
y recorrido T; dos constructores de cilindros; altura, defecto y mínimo
con enteros o Fraction. Es un contraste finito de la prueba escrita.

```powershell
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/comprobar_defecto.py --salida depuracion/perdices20261007/congruencias_codex20261016/evidencia_defecto.json
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/cotejar_defecto.py --prefijos-max 4 --miembros 3 --salida depuracion/perdices20261007/congruencias_codex20261016/cotejo_defecto.json
```
