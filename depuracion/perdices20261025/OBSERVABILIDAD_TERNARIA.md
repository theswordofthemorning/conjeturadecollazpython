# Perdices: qué determina una distribución temporal módulo 3^m

25-10-2026. Extiende el [criterio módulo 9](FRECUENCIAS_TEMPORALES.md).
Se conserva Perdices y no se reivindica prioridad bibliográfica.

**Resultado:** hay un balance exacto para cualquier trayectoria natural
y cualquier resolución m. Para la distribución estacionaria libre nu_m,
las frecuencias de estados determinan todas las frecuencias de ramas
salvo una: la de impares en la clase c_m=(3^m-1)/2. La ambigüedad restante
se acota y tiende a cero al aumentar m. Esto precisa el puente condicional;
**no demuestra mezcla temporal para un fugitivo ni la integridad A/B**.

## 1. Mapa, resolución y cantidades temporales

Usamos T(n)=n/2 si n es par y (3n+1)/2 si es impar, n>=1.
Fijar una sola semilla n, x_j=T^j(n), K>=1, m>=1 y M=3^m.
S_K cuenta impares entre x_0,...,x_(K-1). mu_K es la distribución empírica
de esos mismos K estados módulo M. No hay muestreo de semillas ni
condicionamiento por supervivencia.

Para un entero positivo a, v_3(a) cuenta sus factores 3. Definir

```text
c_m=(M-1)/2,
d_m(x)=m-min(m,v_3(2x+1)),       0<=d_m(x)<=m,
g_m(x)=d_m(x)-d_m(2x),
O_*(K)=#{j<K: x_j impar y x_j=c_m mod M}.
```

d_m y g_m dependen sólo del residuo módulo M. Es equivalente pedir
x=c_m mod M o v_3(2x+1)>=m.

Las ramas modulares son F_0(r)=r/2 y F_1(r)=(3r+1)/2, con inverso de 2
módulo M. Coinciden exactamente cuando 2r+1=0 mod M, es decir r=c_m.
Observar estados consecutivos determina la rama fuera de esa clase;
dentro de ella ambas etiquetas producen el mismo estado siguiente.

## 2. Identidad universal y telescopio

Para todo entero n>=0,

```text
v_3(4T(n)+1)=v_3(2n+1)+(n mod 2).                       (1)
```

Si n es par, 4T(n)+1=2n+1. Si es impar, 4T(n)+1=3(2n+1).
Truncar ambas valoraciones a m da

```text
d_m(n)-d_m(2T(n))=1_(n impar y n!=c_m mod M).
```

Sumando sobre una misma trayectoria y separando los extremos,

```text
S_K-O_*(K)=sum_(j<K) g_m(x_j)+d_m(2x_0)-d_m(2x_K).     (2)
```

No se ha aproximado ningún término. Lean formaliza (1), la identidad
truncada y el balance (2) para todo m,K y toda trayectoria natural;
su marca crítica se expresa mediante la valoración >=m.

## 3. Consecuencia bajo una hipótesis de frecuencias

nu_m es la estacionaria de las ramas libres con probabilidad 1/2,
definida y probada en [Perdices, estacionaria](../perdices20261007/LEEME.md#estacionaria-y-arranques-enteros).
Sea a_m=nu_m(c_m), y TV la mitad de la suma de diferencias absolutas.
La estacionariedad y la identidad local implican

```text
E_nu[g_m]=(1-a_m)/2.
```

El rango de g_m tiene amplitud 2m. El de g_m+1_(r=c_m) tiene amplitud
2m-1: la marca eleva el mínimo -m a 1-m, sin cambiar el máximo m.
Esto también se ve escribiendo
g_m(r)=min(m,v_3(4r+1))-min(m,v_3(2r+1)); las dos valoraciones no
pueden ser positivas a la vez. Usar 0<=O_*<=K mu_K(c_m) y el borde
acotado por m en (2) da, para D=TV(mu_K,nu_m),

```text
(1-a_m)/2 - 2m D - m/K <= S_K/K
                         <= (1+a_m)/2 + (2m-1) D + m/K.       (3)
```

Se usa la desigualdad de eventos o, equivalentemente,
|E_mu f-E_nu f|<=amplitud(f)*TV(mu,nu). Para m=2, la cota superior
es exactamente 37/63+3D+2/K, ya registrada en el criterio módulo 9.

La representación geométrica de nu_m da además

```text
max_r nu_m(r)<=(2/3)^m,       a_m<=2^(m-1)/3^m.          (4)
```

En efecto, para una salida r fija y una longitud a>=1 del último hueco,
la ecuación 3x+1=2^a r mod 3^m determina a lo sumo un x módulo 3^(m-1).
Sólo una paridad de a es posible. La suma de los pesos 2^(-a) es
2/3 para a impares y 1/3 para a pares. La recurrencia para el máximo,
desde nu_0, prueba la primera cota. Para c_m=1 mod 3 sólo sirven los
a pares, lo que prueba la segunda.

Si para una misma órbita se demostrara mu_K -> nu_m para cada m fijo,
(3), primero con K->infinito y después m->infinito, forzaría S_K/K->1/2.
**Ese antecedente sigue sin demostrarse para las órbitas excepcionales.**
Tampoco vale para todas las semillas: las que llegan a 1 alternan 1 y 2.

Valores exactos de la cota superior cuando D=0 y se omite el borde:

| m | a_m | (1+a_m)/2 |
| --- | --- | --- |
| 1 | 1/3 | 2/3 |
| 2 | 11/63 | 37/63 |
| 3 | 23285/262143 | 142714/262143 |

Por ejemplo, m=3, K>=86 y D<=1/100 bastan para 27S_K<17K y
3^S_K<2^K. El margen exacto a 17/27 en K=86 es
75101/225442980>0. Exige información módulo 27, más fuerte que módulo 9;
no es una mejora gratuita para la misma hipótesis.

## 4. La ambigüedad de la clase crítica es exacta

Considerar ahora un flujo modular estacionario: mu(r) es la frecuencia
del estado r y o(r) la frecuencia de su rama impar, con 0<=o(r)<=mu(r).
Este es un objeto distinto de una órbita entera infinita.

Poner F(r)=3r+1 mod M. El balance de entradas en r/2 dice

```text
o(r)-sum_(F(s)=r) o(s)=mu(r)-mu(r/2).                   (5)
```

Para dos soluciones con la misma mu, su diferencia h satisface
h=F_*h. Pero F^m(r)=c_m para todo r; iterar m veces da
h=(sum_r h(r))*delta_(c_m). No hay otra libertad.

Con mu=nu_m, el flujo o(r)=nu_m(r)/2 es una solución. Por tanto
todos los flujos posibles tienen o(r)=nu_m(r)/2 para r!=c_m, y sólo
o(c_m) puede recorrer [0,a_m]. Las proporciones totales de impares son
exactamente el intervalo

```text
[(1-a_m)/2, (1+a_m)/2].                                (6)
```

Los extremos son realizables como flujos: cambiar la etiqueta en c_m
no altera el destino. El programa realiza ambos extremos módulo 9
mediante circuitos eulerianos de 126 pasos repetidos dos veces y CRT.
Obtiene dos semillas enteras positivas y verifica sus 252 pasos con T
literal. Ambas tienen mu_252=nu_2; sus frecuencias de impares son,
respectivamente, 26/63 y 37/63. Las semillas figuran en la evidencia.

Son ejemplos finitos. Repetir más veces el circuito exige construir
otra semilla; no se infiere una órbita entera infinita del flujo modular.

## 5. Límite frente a la obligación aritmética

La identidad también vale en el modelo modular de ramas prescritas.
Para cualquier m fijo, después de m subidas los recorridos prescritos
desde 23 y desde 6416623 coinciden módulo 3^m: su diferencia contiene
el factor 3^m y sus denominadores son potencias de 2. El primero
sigue sin ser una órbita entera. El cotejo lo comprueba para m=1,...,4.
El argumento del factor 3^m es general, no depende de ese barrido.

Aumentar la resolución reduce la ambigüedad del flujo libre, pero no
restituye la integridad binaria del recorrido racional ni demuestra
que la órbita real tenga las frecuencias libres. Para excluir A/B falta
una estimación aritmética de las cuentas de una misma semilla, además
de estos balances. Esta nota no cierra ninguno de esos dos pasos.

## 6. Evidencia y alcance

[Cotejo exacto](cotejar_valuaciones.py), [resultado](cotejo_valuaciones.json):
32512 balances orbitales, cuatro resoluciones, propagación independiente
de las estacionarias, extremos de flujos y dos semillas reales con las
frecuencias extremas módulo 9. Se comprueba también el testigo racional.
Enteros y Fraction; no se importan experimentos antiguos.

```powershell
python -B -X utf8 depuracion/perdices20261025/cotejar_valuaciones.py --modulo-max 4 --semillas-max 127 --pasos 64 --vueltas-extremos 2 --salida depuracion/perdices20261025/cotejo_valuaciones.json
```

[Lean](PerdicesValuaciones.lean), [evidencia](evidencia_lean_valuaciones.json)
y [salida](evidencia_lean_valuaciones.txt): cinco consultas con Lean 4.32.2,
axiomas estándar y sin sorryAx. Certifica el balance orbital para todos
m,K. **No formaliza** la identificación de la marca por congruencias,
las medidas y TV, la caracterización completa de flujos estacionarios
ni los ejemplos CRT; conservan prueba escrita y contraste independiente.
Imports directos cotejados; no auditoría transitiva completa.
Revisión humana y prioridad pendientes.

```powershell
python -B -X utf8 depuracion/perdices20261025/comprobar_lean.py --lean C:/Users/Home/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean.exe --modulo PerdicesValuaciones --salida depuracion/perdices20261025/evidencia_lean_valuaciones.json
```

Cuarta [alta versionada](alta_registro.json), integrada mediante el
generador con [conservación de las 360 afirmaciones anteriores](evidencia_registro.json).

## 7. Contraste externo acotado

Se buscaron cotas individuales que pudieran suministrar la premisa
pendiente. [Monks–Yazinski, teorema 2.7(b)](https://monks.scranton.edu/files/pubs/AutoConjV13.pdf)
da `liminf S_K/K>=log(2)/log(3)` para una órbita divergente racional
de denominador impar. Es una cota inferior compatible con A/B.
Su teorema 2.1 hace la racionalidad de la autoconjugación sobre los
enteros positivos equivalente a la ausencia de órbitas divergentes;
no suministra ese antecedente. Se cotejaron los enunciados y sus pruebas
§§4.1–4.2 del preprint de 2002, publicado en 2004.

[Kontorovich–Lagarias, §§10–11.2](https://arxiv.org/html/0910.1944)
explica que las extensiones 2-ádicas de 3x+1 y 5x+1 comparten la dinámica
ergódica, mientras los enteros forman un conjunto de medida cero.
Su análisis de modelos no transfiere automáticamente las predicciones
a cada entero. **Conclusión de esta revisión:** estos pasajes no cierran
la hipótesis temporal excepcional. No es una revisión exhaustiva ni
una afirmación de inexistencia de otros resultados aplicables.
