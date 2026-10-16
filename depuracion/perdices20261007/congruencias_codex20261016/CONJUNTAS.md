# Perdices: mínimos incompatibles en ventanas consecutivas

16-10-2026. Continuación de [Órbitas](ORBITAS.md). Ruta local de Codex,
conservando el nombre Perdices; sin reivindicar prioridad bibliográfica.

**Resultado:** dos partes impares compartidas consecutivas no pueden
alcanzar simultáneamente sus mínimos módulo 72. Cada pareja disjunta
aporta un exceso de al menos 72. La constante es óptima. El resultado
vale con cualquier número de alternancias; no cierra el presupuesto (P).

## 1. Dominio y enunciado

Usamos `T(x)=x/2` para x par y `(3x+1)/2` para x impar, n>=1, con
paridades reales A=1 y B=110. Los exponentes cuentan bloques, no pasos
de T; un A consume un paso y un B tres. No hay ley aleatoria ni
condicionamiento probabilístico.

Considerar una misma órbita que realiza

```text
U B^a0 A^b1 B^a1 ... A^b(m+1) B^a(m+1) V,
m>=1, todos los a_i>=1, todos los b_i>=0; U,V arbitrarias.
```

Sea x_i la frontera de entrada de A^b_i. Para i=1,...,m definir

```text
r_i = (x_i+1)/2^(b_i+2),
rho=(71,13,47,37,23,61),
k_i = (r_i-rho[b_i mod 6])/72.
```

La [prueba orbital anterior](ORBITAS.md) demuestra que r_i es impar
positivo y `r_i=rho[b_i mod 6] mod 72`; por tanto k_i es un natural.
El tramo adicional `A^b(m+1) B^a(m+1)` permite aplicar esa prueba también
a la última r_m. Para i=1,...,m-1 se obtiene ahora

```text
k_i+k_(i+1)>=1,
r_i+r_(i+1)>=rho[b_i mod 6]+rho[b_(i+1) mod 6]+72.       (1)
```

Emparejar (1,2),(3,4),... da, sin solapamientos,

```text
suma k_i >= floor(m/2),
suma r_i >= suma rho[b_i mod 6] + 72*floor(m/2).         (2)
```

También hay al menos floor(m/2) índices con k_i>=1. No se están sumando
las cotas de altura de ventanas solapadas: se cuentan partes compartidas
distintas y se usan parejas disjuntas.

## 2. Identidad entre vecinas y certificado universal

Escribir b=b_i,c=a_i,d=b_(i+1),r=r_i,v=r_(i+1). Las identidades afines
de A^b y B^c sobre sus fronteras comunes dan exactamente

```text
9^c(3^b r+1) = 8^c(2^d v+1).                          (3)
```

Para probar (1) basta descartar r=rho[b mod 6] y v=rho[d mod 6]. No se
acotan b,c,d. Reducimos sus exponentes por periodos comprobados para
2,3,8,9. Cada periodo es múltiplo de seis y conserva también rho:

| Periodo p | Módulo M | Candidatos supervivientes (b,c,d) módulo p |
| --- | --- | --- |
| 12 | 455 | (0,0,0), (5,1,3), (11,2,1), (3,6,7), (1,10,9) |
| 36 | 23350145 | (0,0,0), (35,2,1) |
| 108 | 2545165805 | (0,0,0), (0,0,36), (0,0,72), (107,2,1), (107,2,37), (107,2,73) |
| 324 | 414862026215 | (0,0,0), (108,0,216), (216,0,108), (323,2,1), (0,216,36) |

En cada fila `2^p=3^p=8^p=9^p=1 mod M`. La primera comprueba las 1728
ternas; las siguientes levantan cada superviviente con tres opciones
por coordenada: 135,54,162 comprobaciones. No se presume que sobreviva
cualquier terna descartada antes. El certificado incluye las tablas y
su cobertura, no sólo la ausencia observada de soluciones pequeñas.

Las cinco clases finales son imposibles:

- En cuatro, b=0 mod 4 y mod 6. Además c>=1 y su clase obligan c>=2.
  Así `3^b*rho+1 ≡ 72 ≡ 8 (mod 16)`. Multiplicar por 9^c conserva ese residuo,
  mientras 8^c hace cero el lado derecho de (3) módulo 16.
- En (323,2,1), c>=2 y d=1 mod 54. El lado izquierdo es divisible por
  81. Como 8 es coprimo con 81, también debería serlo `2^d*13+1`.
  Pero `2^54=1 mod 81` y ese número es 27 módulo 81.

Queda descartada la igualdad de ambos mínimos para **todos** b,d>=0,
c>=1. Puesto que los excesos son múltiplos de 72, se obtiene (1).

## 3. Borde óptimo y consecuencia sobre la altura

La semilla **667** realiza `B A^2 B A^2 B B`. Sus dos partes compartidas
son 47 y 119; sus residuos mínimos son 47 y 47. En (3), ambos lados
son 3816. El exceso total es exactamente 72: no puede sustituirse por
una constante mayor en (1).

Si una ventana tiene k_i>=1, entonces r_i>=85. Tomando n_i como la
entrada del último B inmediatamente anterior a A^b_i, se conserva

```text
9(n_i+5)=32(2^b_i*r_i+1),
2^(b_i+8)<n_i+5,  luego b_i+9<=ceil(log2(n_i+5)).       (4)
```

Esto mejora el sobrecoste individual delta, que estaba entre seis y
ocho, en al menos una ventana de cada pareja. Aplicar el transporte
orbital anterior lleva (4) a la semilla original con su reloj P,S.
Pero ese reloj sigue creciendo: **(2) no es una cota sobre el tiempo
total ni sobre la valuación terminal**. No se demuestra P, salida de
1/110, descenso ni Collatz.

## 4. Formalización, contraste y siguiente paso

[Fuente Lean](PerdicesVentanasConjuntas.lean): certificado modular por
reducción en el núcleo (`decide +kernel`, sin evaluación nativa), descarte
de las cinco clases, enlace entre las mismas fronteras orbitales,
exceso por pareja, consecuencia (4) y suma para listas de excesos sin
ceros vecinos. La identificación de una cadena arbitraria de ventanas
con esa lista se hace por escrito en §1, aplicando el lema orbital a
cada pareja. No se formaliza aquí un nuevo tipo de caminos infinitos.

[Evidencia Lean](evidencia_conjuntas.json) y [salida](evidencia_conjuntas.txt):
Lean 4.32.2, quince lemas nuevos y 44 consultas contando dependencias,
sólo axiomas estándar, sin `sorryAx` ni avisos. Se recompilan los cuatro
módulos desde fuente. Se comprueban los imports directos y sus objetos; no se
afirma auditoría transitiva completa de Mathlib.

[Cotejo independiente](cotejo_conjuntas.json): cada tabla se calcula de
dos maneras, levantando clases y buscando en todo el periodo mediante
un índice modular. Se recorren además 9324 cadenas construidas con dos
algoritmos independientes de cilindros y T literal; 26136 parejas y
7964 cadenas con rachas A vacías. Son contrastes finitos del enlace,
distintos de la prueba universal de periodicidad y cobertura.
Las tres [altas versionadas](alta_registro.json), incluida la continuación,
pasan por el generador en una copia temporal: 349 afirmaciones previas conservadas y 352 en
la copia ampliada. [Evidencia de conservación](evidencia_registro.json).

**Continuación:** [Barrera de tres ventanas](BARRERA.md) mejora la suma y
obtiene una condición ponderada desde n, con prueba escrita y contraste
exacto; su nuevo Lean queda pendiente. El peso geométrico todavía impide
controlar L o v_fin. La suma de partes por sí sola no cierra ese puente.

```powershell
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/comprobar_conjuntas.py --salida depuracion/perdices20261007/congruencias_codex20261016/evidencia_conjuntas.json
python -B -X utf8 depuracion/perdices20261007/congruencias_codex20261016/cotejar_conjuntas.py --ventanas-max 4 --racha-a-max 2 --racha-b-max 2 --traslados 2 --salida depuracion/perdices20261007/congruencias_codex20261016/cotejo_conjuntas.json
```
