# Perdices: reloj por rachas y límite de las reservas constantes

18-10-2026. Continúa [Pendiente uno](PENDIENTE_UNO.md) y usa la cota
entera de [Dos cambios](../DOS_CAMBIOS.md#2-una-cota-de-tamaño-con-coeficientes-enteros).
Se conserva Perdices, sin reivindicar prioridad bibliográfica.

**Resultado:** conservar el crecimiento del prefijo da un reloj explícito
para cualquier número fijado de rachas. Con hasta tres rachas,
`L+v_fin <= (1234/289)*ell`; con hasta cuatro,
`L+v_fin <= (34100/4913)*ell < 7*ell`.
El coeficiente general crece geométricamente. Se demuestra además que
la relajación lineal empleada sigue sin admitir un coeficiente uniforme
aunque se imponga una reserva constante arbitrariamente grande en cada racha.
**El reloj uniforme y la pendiente 3 continúan abiertos.**

## 1. Dominio y transporte desde la misma semilla

T es el atajo sobre enteros positivos: x/2 si x es par y (3x+1)/2 si es impar.
A=1 y B=110 son bloques de paridades realizadas. Una racha reúne bloques
consecutivos del mismo tipo; las rachas máximas alternan A y B. `d_i` cuenta
pasos T: k para A^k y 3k para B^k. `L=sum d_i`,
`ell=ceil(log2(n+5))`; v_fin usa 1 si la última racha es A y 5 si es B.
La palabra vacía tiene L=0 y se trata aparte, sin asignarle v_fin.
No hay ley aleatoria ni condicionamiento probabilístico.

Antes de la racha i sean P_i y S_i los pasos T y los pasos impares del
prefijo, y x_i su frontera. Con c_i=1 o 5 según el tipo, el encaje y el
consumo exacto dan

```text
2^P_i * (x_i+c_i) <= 3^S_i * (n+5),
d_i + v2(x_(i+1)+c_i) = v2(x_i+c_i),
17*(P_i+d_i+v2(x_(i+1)+c_i)) <= 27*S_i+17*ell.       (1)
```

La última desigualdad usa `3^17<2^27`, ya certificado; no es una nueva
estimación aritmética para las partes impares. Se mantiene n en todas
las fronteras. Poner

```text
gamma_A=10/17, gamma_B=1/17,
H_1=ell,       H_i=ell+sum_(j<i) gamma_(p_j)*d_j.
```

Como un paso A aporta un impar y tres pasos B aportan dos, (1) implica
`d_i<=H_i`, y en la última racha `d_r+v_fin<=H_r`. Para incluir esa carga
se reemplaza únicamente la última duración por d_r+v_fin. No se altera
ningún presupuesto anterior. Así se obtiene el sistema racional

```text
0<=d_i<=H_i,             H_(i+1)=H_i+gamma_(p_i)*d_i. (2)
```

No se multiplican mínimos de palabras diferentes.

## 2. Coeficiente explícito para todas las cantidades de rachas

Para una lista de tipos p, definir

```text
C([])=0,
C(p::resto)=1+(1+gamma_p)*C(resto).                   (3)
```

Entonces todo sistema (2) satisface `sum d_i<=C(p)*H_1`.
Por inducción, el coste después de la primera racha es como máximo
`C(resto)*(H_1+gamma_p*d_1)`. El coeficiente de d_1 en el coste total es
`1+gamma_p*C(resto)>=0`, así que se sustituye d_1 por H_1. Esto da (3).

Es también el máximo exacto de **esta relajación**: d_i=H_i alcanza
igualdad en cada paso. No se afirma optimalidad para órbitas enteras.
Sea q=486/289 y `S_m=sum_(j=0)^(m-1) q^j`, con S_0=0. Para tipos alternantes:

```text
C_A(2m)   = (44/17)*S_m,   C_A(2m+1) = (44/17)*S_m+q^m,
C_B(2m)   = (35/17)*S_m,   C_B(2m+1) = (35/17)*S_m+q^m.       (4)
```

La fórmula se obtiene agrupando los factores 27/17 y 18/17 de (3).
C_A domina a C_B y aumenta con r; por tanto sirve para **hasta r** rachas.

| Número de rachas | Empieza A | Empieza B |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 44/17 | 35/17 |
| 3 | 1234/289 | 1081/289 |
| 4 | 34100/4913 | 27125/4913 |

Cada entrada multiplica ell y acota L+v_fin. La cota de cuatro rachas es
menor que 7 porque 34100<7*4913. Mejora el **reloj** L<=39*ell deducido
de P13 en [Tres cambios](../TRES_CAMBIOS.md); no se afirma que mejore P13
con K=2*ell ni que resuelva el candidato epsilon=7/17 de aquella nota.
Es un corolario de las herramientas de tamaño existentes, no una solución
de la obligación aritmética global.

## 3. Una reserva constante tampoco cierra este modelo

Sea K>=0 cualquier constante racional, o entera si se prefieren unidades
discretas, y escoger H_1>K. Exigir incluso `d_i<=H_i-K` en **todas** las
rachas sigue sin dar un reloj uniforme en su número. En efecto elegir

```text
d_i=H_i-K,
H_(i+1)-K=(1+gamma_(p_i))*(H_i-K)
```

produce

```text
sum d_i=C(p)*(H_1-K).                                (5)
```

C(p)>=r y, para tipos alternantes, (4) crece geométricamente. Para
cualesquiera constantes reales C*,D se elige r con C(p)>C* y después
H_1 suficientemente grande: (5) supera C*H_1+D. Si se requieren duraciones
enteras y múltiplos de tres en B, basta tomar H_1-K múltiplo positivo
de `3*17^r`, con K entero. No es un efecto del redondeo.
Una reserva real fija queda cubierta imponiendo una reserva entera mayor.

**Son modelos del sistema de desigualdades, no órbitas de Collatz.**
Pueden incumplir las congruencias de realización; no refutan el reloj
orbital. Tampoco afirman que toda condición modular se reduzca a una
reserva constante. Demuestran que usarla sólo de esa forma resulta insuficiente.

## 4. La obligación aritmética que queda

En (2), definir `delta_i=H_i-d_i>=0` y
`w_i=1+gamma_(p_i)*C(p_(i+1),...,p_r)`. La misma inducción da la identidad

```text
L+v_fin = C(p)*ell - sum_i w_i*delta_i.               (6)
```

Para lograr un reloj uniforme C*,D haría falta probar en las **órbitas reales**

```text
sum_i w_i*delta_i >= (C(p)-C*)*ell-D.                (7)
```

(7) es una reformulación exacta del objetivo, **no un lema ya demostrado**.
El punto útil de (5) es descartar que unas pérdidas aditivas fijas, por
grandes que sean, basten en este modelo. La siguiente búsqueda debe controlar
conjuntamente las partes impares y los mínimos globales, con una pérdida
que compense la altura transportada. Reducir otra vez el coeficiente para
un número fijo de cambios no resuelve esa obligación.

La continuación [Defecto interior](DEFECTO_INTERIOR.md) muestra que una
racha interior real puede tener defecto fijo y duración arbitrariamente
grande después de cualquier prefijo terminado en B. Descarta exigir una
pérdida proporcional en cada racha; no descarta (7), que es conjunta.
Con [contexto a ambos lados](CONTEXTO_INTERIOR.md), la parte impar 13
permite también prescribir un futuro arbitrario tras B A². Exigir una
cantidad fija de cambios posteriores tampoco rescata la pérdida por racha.

[Compensación relativa](COMPENSACION_RELATIVA.md) añade una limitación
del modelo: aun imponer `delta_i>=eta*H_i+K` para cualquier eta<1 fijo
y K>=0, y una pérdida relativa eta en todas las ventanas, permite
coste ilimitado con altura inicial fija. La realización orbital aporta
restricciones adicionales; la repetición real AB excluye esos modelos
por divisibilidad. El objetivo (7) exige controlar el residuo absoluto.

## 5. Evidencia y frontera formal

[PerdicesRelojRachas.lean](PerdicesRelojRachas.lean) formaliza dieciséis
lemas nuevos: balance y consumo de una racha real, (1) con prefijo arbitrario,
conteo de impares, las cuatro cotas orbitales ABA/BAB/ABAB/BABA, cota y
saturación de la relajación racional, C>=r, identidad de defectos y reserva
constante. Las cuatro cotas parten de caminos reales enlazados por las
mismas fronteras; admiten multiplicidades cero.

La extracción de una lista arbitraria de rachas, su conexión general con
(2), las fórmulas cerradas (4) y la conclusión cuantificada con C*,D en (5)
conservan la prueba escrita anterior; no se atribuyen a Lean.
[Compilación](evidencia_rachas.json) y [salida](evidencia_rachas.txt): cuatro
módulos desde fuente, 46 consultas, Lean 4.32.2/Mathlib fijados, sólo axiomas
estándar. Se verifican imports directos, no toda su cadena transitiva.

[cotejar_rachas.py](cotejar_rachas.py) y [resultado](cotejo_rachas.json):
1023 palabras de hasta nueve bloques, dos representantes por cilindro,
2046 recorridos y 324 bordes de cuatro rachas con multiplicidades 0..2.
Dos constructores independientes de cilindros y T literal contrastan
consumo, transporte y relojes. Se comprueban además 1020 vértices racionales
de (2), 64 modelos saturados hasta 32 rachas y 256 con reservas 0,1,17,1224.
Los cálculos usan enteros o Fraction; son controles finitos. No se repite
el censo de Salidas ni se deduce de ellos una cota universal.

```powershell
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/comprobar_rachas.py --salida depuracion/perdices20261007/congruencias_codex20261016/evidencia_rachas.json
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/cotejar_rachas.py --bloques-max 9 --rachas-modelo-max 32 --vertices-max 8 --traslados 2 --salida depuracion/perdices20261007/congruencias_codex20261016/cotejo_rachas.json
```
