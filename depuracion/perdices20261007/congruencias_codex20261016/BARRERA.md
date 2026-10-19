# Perdices: barrera de tres ventanas y transporte ponderado

16-10-2026. Continuación de [Ventanas conjuntas](CONJUNTAS.md), en la
misma ruta local. Se conserva Perdices; no se reivindica prioridad bibliográfica.
Reanudación del 18-10: conciliación de la evidencia Lean e incorporación
de la suma ponderada, sin cambiar el umbral ni afirmar el presupuesto (P).

**Resultado:** entre tres partes impares compartidas consecutivas hay una
cuyo exceso residual es al menos 17. Se obtiene una condición necesaria
conjunta desde la semilla original, con un peso explícito del reloj.
Ese peso impide deducir de esta condición el presupuesto global (P).

## 1. Dominio y enunciado

`T(x)=x/2` si x es par y `(3x+1)/2` si es impar, x entero positivo.
A=1 y B=110 son paridades efectivas. Usar exactamente el dominio de
[Conjuntas, §1](CONJUNTAS.md#1-dominio-y-enunciado):

```text
U B^a0 A^b1 B^a1 ... A^b(m+1) B^a(m+1) V,
m>=1, a_i>=1, b_i>=0, U,V arbitrarias.
x_i = entrada de A^b_i, i=1,...,m,
r_i = (x_i+1)/2^(b_i+2),
rho = (71,13,47,37,23,61),
r_i = rho[b_i mod 6] + 72*k_i, k_i natural.
```

El tramo adicional permite aplicar la congruencia también a r_m. Los
exponentes cuentan bloques; los relojes de abajo cuentan pasos de T y
entradas impares. No intervienen probabilidades ni condicionamientos.

Para todo i con i+2<=m:

```text
max(k_i,k_(i+1),k_(i+2)) >= 17.                         (1)
```

Agrupando ternas disjuntas, para cualquier m:

```text
suma k_i >= 17*floor(m/3),
suma r_i >= suma rho[b_i mod 6] + 1224*floor(m/3).      (2)
```

Hay al menos floor(m/3) índices con k_i>=17. La cota anterior
`suma k_i>=floor(m/2)` sigue siendo útil para m<3. No se afirma que
17 sea óptimo: n=6139 realiza `BBBABB` con partes (1727,1943,1093)
y excesos (23,26,15). La mejor constante universal de (1), si se busca,
está por tanto entre 17 y 26. Ese testigo admite A vacías.

## 2. Certificado de transiciones, sin acotar exponentes

Dos partes vecinas satisfacen la identidad orbital exacta

```text
9^c*(3^b*r+1) = 8^c*(2^d*v+1),
r=rho[b mod 6]+72*k, v=rho[d mod 6]+72*j, c>=1.         (3)
```

Suponer k,j<=16. Una arista es (b,c,d,k,j), con los tres exponentes
reducidos módulo p y las cargas k,j **sin reducir**. Se usan estos
periodos comunes de 2,3,8,9, múltiplos de seis:

| p | M=gcd(2^p-1,3^p-1) | Candidatos revisados | Supervivientes |
| --- | --- | --- | --- |
| 6 | 7 | 62424 | 8892 |
| 12 | 455 | 71136 | 1097 |
| 36 | 23350145 | 29619 | 47 |
| 108 | 2545165805 | 1269 | 147 |
| 324 | 414862026215 | 3969 | 105 |

La primera fila recorre todas las clases y las dos cargas; cada fila
siguiente levanta las tres coordenadas exponenciales de los supervivientes.
La cobertura se demuestra usando cociente y resto. Así, el certificado
cubre todos los exponentes naturales de (3), no sólo los menores que 324.

Si c mod 324 no es 1, c>=1 implica c>=2. Como 8 y 9 son coprimos,
(3) obliga entonces a

```text
16 divide 3^b*r+1,    81 divide 2^d*v+1.              (4)
```

Estas condiciones también pueden evaluarse con b,d módulo 324:
`3^324=1 mod 16` y `2^324=1 mod 81`. Para c mod 324=1 no se añade
esta restricción; admitir aristas de más mantiene la cobertura necesaria.
Después de (4) quedan trece aristas:

```text
(b,c,d,k,j):
(0,1,0,7,8),       (0,1,1,10,6),       (0,1,2,12,3),
(1,1,0,1,3),       (1,1,2,16,13),      (2,1,2,0,1),
(109,1,72,1,3),    (213,3,140,12,10),   (218,1,218,0,1),
(316,6,315,1,7),   (320,4,317,4,12),   (321,219,31,6,11),
(322,3,321,4,5).
```

Una arista termina en el estado (d,j); la siguiente debe empezar en
ese mismo estado (b,k). Ninguna de las trece termina donde empieza
otra. Si tres cargas fueran <=16, sus dos empalmes orbitales producirían
dos aristas enlazadas, contradicción. Esto prueba (1).
Las aristas son condiciones necesarias; no se afirma que todas se realicen.

## 3. Consecuencia desde la semilla original

Sea n_i la entrada del **último B** inmediatamente anterior a A^b_i.
Sea U_i el prefijo desde la semilla original n hasta n_i; escribir
P_i=largo(U_i), S_i=impares(U_i). No se reinicia n en las ventanas.

Si k_i>=17, entonces r_i>=13+72*17=1237. La identidad y el transporte
orbital dan

```text
9*(n_i+5)=32*(2^b_i*r_i+1),
2^(b_i+12)<n_i+5,    b_i+13<=ceil(log2(n_i+5)),
2^(P_i+b_i+12)<3^S_i*(n+5).                           (5)
```

En cada terna consecutiva al menos uno de sus índices cumple (5).
Para combinar todas las ventanas sin sumar alturas, definir el racional
positivo `W_m = suma 3^S_i / 2^(P_i+b_i)`. Dividir las mismas identidades
por 2^b_i y usar `2^P_i*(n_i+5)<=3^S_i*(n+5)` produce

```text
suma r_i + suma 2^(-b_i) <= (9/32)*(n+5)*W_m.
```

Por (2), la condición necesaria conjunta es

```text
suma rho[b_i mod 6] + 1224*floor(m/3) + suma 2^(-b_i)
    <= (9/32)*(n+5)*W_m.                              (6)
```

Todos los sumandos corresponden a la misma órbita y semilla. La
derivación alternativa consiste en sustituir cada r_i directamente por
`(9*(n_i+5)/32-1)/2^b_i`; da la misma desigualdad sin multiplicar
presupuestos locales. (6) se contrasta con `Fraction` y está formalizada en
[PerdicesBarreraPonderada.lean](PerdicesBarreraPonderada.lean) para listas
de ventanas realizadas desde el mismo n y enlazadas por (3).
La extracción de esa lista desde la palabra arbitraria sigue por escrito.

**Límite comprobable:** en la palabra B^(m+2), con todas las A vacías,
los prefijos elegidos tienen P_i=3(i-1), S_i=2(i-1), de modo que
`W_m=8*((9/8)^m-1)`. La cota que (6) da para n+5 es

```text
(32/9)*(72*m+1224*floor(m/3)) / (8*((9/8)^m-1)).        (7)
```

Para m=96, (7) ya es menor que 1, mientras la menor semilla real
satisface n+5=8^98. Los dos métodos de cilindros y T literal comprueban
este contraste. Así, (6) sola pierde información incluso en una familia
elemental: el peso puede dominar la ganancia de (2). Esto no refuta P.
No demuestra una cota de L o v_fin, salida del piloto, descenso ni Collatz.

## 4. Evidencia y siguiente obligación

[Tablas Lean](PerdicesBarreraTablas.lean) y [barrera Lean](PerdicesBarreraTres.lean):
enumeración, levantamientos, reducción por periodos, filtro de divisibilidad,
imposibilidad de empalmar, barrera sobre caminos reales, altura, transporte
desde n y suma para listas. Las tablas se dividen por carga y se comprueban
con `decide +kernel`. La compilación de estos módulos ya estaba registrada
en el commit `6b01e8b`; la nota y el verificador de sesión habían quedado
desfasados tras el cierre anterior. Se corrige ese estado, conservado en Git.

[Suma ponderada](PerdicesBarreraPonderada.lean) añade siete lemas. `Realizada n v`
exige el camino desde n y la identidad exacta de la entrada B de la ventana;
`Enlazadas` exige (3) para cada par vecino, con c>=1. `enlaces_barrera`
deduce la condición de ternas; `exceso_partes` y `barrera_ponderada` llevan
esa condición a (2) y (6), también para listas vacías o de longitud menor
que tres. No se supone la desigualdad que se quiere concluir.

[Evidencia Lean](evidencia_barrera.json) y [salida](evidencia_barrera.txt):
siete módulos recompilados desde fuente, Lean 4.32.2, Mathlib fijado,
**70 consultas de axiomas**, sólo `propext`, `Classical.choice` y `Quot.sound`;
sin `sorryAx`. Se comprueban imports directos y sus huellas, no toda la
cadena transitiva de Mathlib. Las 44 consultas anteriores permanecen
certificadas en [su evidencia](evidencia_conjuntas.json).
La descomposición de una palabra arbitraria en las partes normalizadas
usa los lemas orbitales anteriores; la construcción completa de la lista
de ventanas y sus enlaces sigue desarrollada por escrito.

[Certificado independiente](certificado_barrera.json): en cada periodo se
cotejan el levantamiento y una búsqueda sobre el periodo completo mediante
un índice modular inverso; sus resultados coinciden.
[Cotejo orbital](cotejo_barrera.json): 18144 cadenas y 33696 ternas;
15584 cadenas tienen A vacías y 9072 tienen prefijo interior no vacío.
Dos algoritmos independientes construyen cada cilindro; T literal
verifica fronteras, cargas, (1), (2), (5) y (6). Se incluyen el testigo
n=6139 y seis casos de (7), hasta m=96. Este contraste es finito;
la universalidad procede de la cobertura modular y la prueba.
[Cotejo de la suma](cotejo_ponderada.json): 680 controles racionales, con
8 listas vacías, 32 de una ventana, 128 de dos y 512 de tres. Dos
construcciones de cilindros y T literal comprueban (6) y sus bordes.

**Continuación:** [Reloj terminal](RELOJ_TERMINAL.md) convierte la carga V
en exactamente V pasos adicionales desde n. Por ello P equivale a un reloj
uniforme L<=C*ell(n)+D; queda por demostrar ese reloj. Elevar un
umbral constante de cargas no basta para vencer el peso geométrico de (6).
No se adopta como siguiente paso un mero aumento de ese umbral.
La comprobación formal queda cerrada con el alcance indicado. Las tres
[altas](alta_registro.json) se integran en el registro versionado y el catálogo
generado, que alcanzó 352 filas. La continuación añade una cuarta alta sin
alterar esas 352 afirmaciones ni respuestas.db, según [el cotejo](evidencia_registro.json).
El [verificador de sesión](verificar_sesion.py) comprueba ahora la evidencia
de la barrera, sus axiomas e imports; ya no arrastra el rótulo de pendiente.

```powershell
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/certificar_barrera.py --limite 16 --salida depuracion/perdices20261007/congruencias_codex20261016/certificado_barrera.json --lean depuracion/perdices20261007/congruencias_codex20261016/PerdicesBarreraTablas.lean
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/comprobar_barrera.py --salida depuracion/perdices20261007/congruencias_codex20261016/evidencia_barrera.json
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/cotejar_barrera.py --ventanas-max 4 --racha-a-max 2 --racha-b-max 2 --traslados 2 --salida depuracion/perdices20261007/congruencias_codex20261016/cotejo_barrera.json
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/cotejar_ponderada.py --ventanas-max 3 --racha-a-max 1 --racha-b-max 2 --traslados 2 --salida depuracion/perdices20261007/congruencias_codex20261016/cotejo_ponderada.json
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/verificar_alta.py --integrar --salida depuracion/perdices20261007/congruencias_codex20261016/evidencia_registro.json
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/verificar_sesion.py --salida depuracion/perdices20261007/congruencias_codex20261016/evidencia_sesion.json
```
