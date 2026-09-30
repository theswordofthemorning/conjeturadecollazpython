# Ocelotas: reducción universal desde la órbita — 30-09-2026

**Avance formal:** [OcelotasTrayectorias.lean](OcelotasTrayectorias.lean)
deduce de las paridades reales las congruencias, la criba y, bajo
`RhinEntera`, la cota **k < 131072** para cualquier fallo con entre una y
diez rachas. Incluye las desigualdades que enlazan con el certificado
finito. **No es todavía el teorema completo de descenso para diez rachas:**
al cerrar esta tanda, la enumeración y el descenso finito seguían fuera
de Lean. La [tercera tanda](FINITO_LEAN.md) ya certifica el descenso
finito y el ensamblaje sujeto a una obligación aritmética explícita;
el [cierre posterior](CIERRE_LEAN.md) demuestra esa obligación y la aplica.

Se conserva el nombre Ocelotas y el resultado escrito de la
[revisión anterior](REVISION_RACHAS.md). No se amplía el número de rachas
ni se atribuye a Lean el certificado Python.

## Enunciado y significado

Se importan las definiciones originales de [Ocelotas.lean](Ocelotas.lean):
`T(n)=n/2` si n es par, `(3n+1)/2` si es impar, sobre naturales; un paso
es un paso de este atajo. El resultado CST de interés tiene dominio n>=2.
`S k n` cuenta los pasos impares antes del índice k y `PrimerCruce n k`
exige coeficiente >=1 en todos los índices anteriores y <1 en k.
No hay ley probabilística ni hipótesis de distribución.

Las funciones `a,b : Nat → Nat` dan las longitudes de las rachas,
indexadas desde cero. Se definen

```text
ell_0=0, ell_(i+1)=ell_i+a_i+b_i; A_0=0, A_(i+1)=A_i+a_i.
Palabra n a b r:
  para cada i<r, a_i,b_i>=1;
  T^(ell_i+t)(n) es impar para t<a_i;
  T^(ell_i+a_i+t)(n) es par para t<b_i.
```

La palabra es consecutiva: no se omiten pasos ni se permite saltar rachas.
`cuenta_impares` prueba `S ell_i n=A_i` para i<=r. El enunciado central es:

```lean
theorem tiempo_diez (hR : RhinEntera) {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr10 : r ≤ 10)
    (hk : PrimerCruce n (tiempo a b r))
    (hf : n ≤ T^[tiempo a b r] n) :
    tiempo a b r < 131072
```

`hf` es la hipótesis de un posible fallo, que se eliminará al cerrar el
cálculo finito. `hR` es una hipótesis externa explícita, no una demostración
de Rhin ni un axioma global oculto. Que no aparezca en `#print axioms` no
la elimina del enunciado. Para n par el primer cruce y el descenso son
inmediatos; `Palabra` con r>0 describe el caso que empieza impar.

## De la órbita a la criba

Con x_i=T^ell_i(n), las identidades de tramos importadas dan

```text
2^a_i (T^(ell_i+a_i)(n)+1) = 3^a_i (x_i+1),
2^b_i x_(i+1) = T^(ell_i+a_i)(n).
```

`congruencia_racha` usa la coprimalidad de 2^a_i y 3^a_i para deducir
`2^a_i | x_i+1`. `cadena` prueba por inducción
`2^A_i (x_i+1) <= 3^A_i (n+1)`. Combinadas, dan
`2^A_(i+1) <= (n+1)3^A_i`, ahora sin postular esa desigualdad.

`criba_desde_trayectoria` aplica el núcleo de
[OcelotasRachas.lean](OcelotasRachas.lean): si n+1<2^m, entonces
`q=S ell_r n <= cota r m`, con
`cota 0 m=0` y `cota (i+1) m=(5m+8*cota i m-1)/5` en naturales.

## Término aditivo y Rhin

La identidad exacta de un bloque es

```text
2^ell_(i+1) x_(i+1) + 2^(ell_i+a_i)
  = 3^a_i 2^ell_i (x_i+1).
```

En cada comienzo de racha anterior al primer cruce,
`2^ell_i <= 3^A_i`. De la identidad, por inducción, resulta
`2^ell_i x_i <= 3^A_i (n+i)`, estricta para i>0.
Así se formaliza el control aditivo sin tener que representar una suma
de fracciones ni restas negativas.

Para k=ell_r, q=A_r, P=3^q y Delta=2^k-P, `fallo_producto` deduce
`Delta*n < r*P`. `ventana_cruce` demuestra `2^k <= 2*P`, incluso en el
borde k=1. Aplicando `RhinEntera`, `fallo_rhin` concluye **n < r*k^14**.
La ventana estricta para k>=2 también queda probada.

## Cota del tiempo sin logaritmos reales

Sea t=Nat.log 2 k, el piso del logaritmo binario entero. Entonces
`2^t <= k < 2^(t+1)`. Para r<=10, se toma m=4+14(t+1). La cota anterior da

```text
n+1 <= 10*k^14 < 16*(2^(t+1))^14 = 2^m.
q <= cota r m <= cota 10 m <= 182*m.
```

`cota_diez_lineal` prueba la última comparación para **todo m natural**,
no mediante un muestreo. Como q>0 y `3^q<4^q`, la ventana del primer
cruce obliga a k<=2q. Por tanto

```text
2^t <= k <= 364*(4+14*(t+1)).
```

`cola_diez`, ya certificado en la tanda anterior, contradice esto para
todo t>=17. Resulta k<2^17=131072. Esta variante formal de la derivación
anterior evita introducir `log2(M)`, números reales o redondeos.

## Interfaz con el cálculo finito

Sin usar Rhin, `criba_fallo` demuestra: para cualquier R>=r, si
`(R+1)P <= 2^m Delta`, un fallo requiere **q<=cota R m**.
`cota_semilla` demuestra **n<=(R*P-1)/Delta**, con división natural.
Son exactamente las condiciones que usa el certificado existente.

La [continuación](FINITO_LEAN.md) certifica el descenso para n<=11214 y
el ensamblaje; el [cierre](CIERRE_LEAN.md) certifica y aplica la criba
que obliga a esa cota de n.
La [interfaz del contador](CONTADOR_LEAN.md) demuestra la extracción de
`Palabra` desde el número de rachas de la órbita. No se afirma existencia
universal del primer cruce ni Collatz.

## Validación y reproducción

Lean 4.32.2; los tres módulos compilan con código 0. Los teoremas
principales imprimen únicamente subconjuntos de `propext`, `Classical.choice`
y `Quot.sound`, sin `sorryAx`. No se usa `sorry`, `admit` ni evaluación
nativa como sustituto del núcleo. Hay ejemplos decididos en el núcleo
para n=3 y n=39, y rechazo del comienzo par n=2.

[comprobar_rachas_lean.py](comprobar_rachas_lean.py) recompila las dependencias
locales en un directorio temporal, registra sus huellas y falla ante errores
o dependencias no admitidas. [Salida Lean](lean_trayectorias.txt).

El [cotejo independiente](verificar_trayectorias.py) compone coeficiente y
término aditivo con `Fraction`, extrae las rachas del mapa clásico agrupado
y comprueba las fórmulas e índices: **1999 semillas, 1764 bloques**, sin
fallos. Incluye n=2,3,7,39,2000, rechazo de n<2 y agotamiento del tope.
Es un cotejo finito de la interpretación, separado de las pruebas
universales y sin importar los otros verificadores.
[Salida del cotejo](cotejo_trayectorias.json).

Desde la raíz:

```text
python -B -X utf8 depuracion/cst20260930/comprobar_rachas_lean.py --salida depuracion/cst20260930/lean_trayectorias.txt
python -B -X utf8 depuracion/cst20260930/verificar_trayectorias.py --hasta 2000 --max-pasos 10000 --salida depuracion/cst20260930/cotejo_trayectorias.json
```

El registro de afirmaciones se actualiza sin añadir otra afirmación:
el resultado de diez rachas conserva su alcance y pasa a tener formalizada
toda la reducción del tiempo. Generador y controles: código 0, 246
afirmaciones ([evidencia](registro_trayectorias.txt)). Se preservan las salidas históricas y
`respuestas.db`; no hay publicación ni cambios en el repositorio compañero.
