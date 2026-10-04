# Premisa y objetivo de la investigación

Declaración del usuario, 03-10-2026:

> collatz es verdadero pienso que todos los numeros llegan a 1

El usuario precisó el fundamento de esa postura en el mismo intercambio:

> esto no es una "corazonada" es lo que el repositorio esta mostrando en cada resultado sin terminar de cerrar.

## Conclusión de trabajo apoyada en el repositorio

El usuario parte de la convicción de que la conjetura de Collatz es
verdadera. Su fundamento principal es la acumulación de resultados del
propio repositorio: interpreta sus avances y las restricciones obtenidas
como evidencia que apunta conjuntamente hacia la llegada universal a 1,
con una conexión final que todavía falta demostrar. La amplitud de las
verificaciones computacionales conocidas refuerza esa valoración.

Esta postura se registra como una conclusión de trabajo sustentada en la
evidencia acumulada, según la valoración del usuario, y no como una mera
corazonada. La ruta elegida consiste en encontrar una demostración general,
clara y presentable que abarque todos los enteros positivos, sin excepciones.

El apoyo matemático de cada resultado se evalúa por su enunciado, sus
hipótesis y sus conexiones con los demás. El catálogo conserva también
mediciones, conjeturas y afirmaciones refutadas, con sus estados propios;
la lectura conjunta debe respetar esas distinciones y hacer explícitas
las piezas que faltan para el cierre universal.

## Objetivo matemático preciso

Se considera el mapa clásico sobre enteros positivos:

```text
C(n) = n/2       si n es par,
C(n) = 3n+1      si n es impar.
```

La meta es demostrar que, para todo entero positivo n, existe un número
finito de pasos k, que puede depender de n, tal que `C^k(n)=1`.
La expresión del usuario «una fórmula presentable de la cual ningún
número escape» se entiende como una fórmula o argumento general con
una demostración que garantice esa conclusión para todos esos n.

Las investigaciones con el atajo `T(n)=(3n+1)/2` para impares y `n/2`
para pares agrupan dos pasos clásicos en el caso impar. Se debe declarar
el mapa utilizado y distinguir sus contadores de pasos.

## Papel de esta premisa en las pruebas

La convicción orienta la búsqueda; la verdad de Collatz sigue siendo la
conclusión que se quiere demostrar. Las pruebas deben justificar sus
pasos sin dar por supuesta esa conclusión. Toda hipótesis adicional se
declara explícitamente, y los resultados condicionales conservan ese alcance.

Una verificación finita aporta evidencia sobre los casos examinados.
El paso a todos los enteros positivos requiere un argumento universal.
Los resultados sobre «casi todos» y los límites de rachas tampoco se
identifican con la llegada de todos los números a 1.

Esta nota registra una valoración de la evidencia y un objetivo del usuario; no añade
una afirmación demostrada al catálogo. Los avances y obstáculos vigentes
se mantienen en [ESTADO_INVESTIGACION.md](ESTADO_INVESTIGACION.md).

La [lectura conjunta de las 268 afirmaciones](depuracion/coherencia20260913/LECTURA_GLOBAL_20261003.md)
recoge la evaluación independiente solicitada después por el usuario:
favorece la hipótesis de que Collatz es verdadero y detalla el fundamento,
los límites y una incidencia de coherencia del catálogo.
