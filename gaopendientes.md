# Gao: lo hecho y lo pendiente

25-09-2026. Qué está demostrado, qué falta y cómo cerrarlo. El estado breve
está en [ESTADO_INVESTIGACION.md](ESTADO_INVESTIGACION.md); las pruebas, en
las notas enlazadas. Esta hoja no las repite.

## El resultado

Mapa clásico `f(n)=n/2` si n es par y `3n+1` si es impar (A006370), sobre los
naturales. Conjunto

    G = { m : f^k(m) = f^k(m+1) para algún k <= floor(log2 m) }.

Teorema `GaoEnunciado.conjetura_gao`: `#(G ∩ [0,N))/N -> 1`, es decir, G
tiene **densidad natural 1**. Es la conjetura de Gao (1993) **en la forma
que resume Lagarias**. El artículo original, leído el 25-09, la enuncia de
otro modo, más exigente (punto 2). No hay ley ni condicionamiento: el
teorema es determinista. La cadena con bits justos es sólo el vehículo, y
Tejonas la transporta de forma exacta a las clases módulo `2^t`. **No dice
nada de llegar a 1: no es la conjetura de Collatz.**

| Pieza | Qué da | Nota |
|---|---|---|
| Sesiones del 20-09 al 24-09 | EF, VH, Hormigas, H3, C1, protocolo guardado | [Guardias](depuracion/gao20260920/Guardias_finitas.md) |
| Lagartijas | pocas entradas; CF_F entera | [Lagartijas](depuracion/gao20260920/Lagartijas.md) |
| Martas | `P(sigma>h) -> 0` | [Martas](depuracion/gao20260920/Martas.md) |
| Tejonas | pares reales, mapa clásico, densidad | [Tejonas](depuracion/gao20260920/Tejonas.md) |
| GaoEnunciado | forma de límite, autocontenida | [GaoEnunciado.lean](depuracion/gao20260920/formal/GaoEnunciado.lean) |

## Lo ya comprobado

- **Formalización.** Lean 4.32.2 y Mathlib `905b95818eb3`. `lake build GaoCore
  GaoFormal` completo (1609 tareas). `#print axioms` sólo muestra `propext`,
  `Classical.choice` y `Quot.sound` en las 35 consultas de Lagartijas, Martas,
  Tejonas y GaoEnunciado. No hay `sorry`, `admit`, `native_decide`, `axiom`
  propios ni `extern`. `leanchecker` repasa por el núcleo los 24 módulos
  propios: los 24 terminan con código 0. El 25-09 los hashes de
  [la evidencia](depuracion/gao20260920/evidencia_gao_lean.json) coinciden con
  los archivos.
- **Conteo exacto.** [Pares reales](depuracion/gao20260920/verificar_lagartijas_pares.py):
  262.144 pares `(n,n+1)` con n en `[2^18,2^19)`.
  - El estado real coincide con la cadena en cada paso.
  - Las fusiones coinciden hasta t=18.
  - Periodicidad módulo `2^18`.
  - Encuentro clásico con `k<=2t` en los 103.358 pares fusionados.
  - Cero fallos.

  La [cadena reimplementada](depuracion/gao20260920/verificar_lagartijas.py)
  comprueba las desigualdades de Lagartijas con parámetros pequeños.
- **Cotejo del enunciado.** Coincide literalmente con el resumen de
  Lagarias, con C el mapa clásico. Con el original de Gao no coincide
  (punto 2; [ficha](depuracion/gao20260920/ficha_gao_lagarias.md)).
- **Coherencia numérica.** Las fusiones balanceadas hasta t son A398792(t),
  y `A398792(32)/2^32 = 0,4356…`. La densidad observada de G es 0,364 en
  `2^20` y 0,374 en `2^22`. El 0,389 de Gao es otra cantidad: `d̄_24`, de su
  tabla 3. Son mediciones finitas: ni confirman ni refutan un límite.

## Lo que falta, en orden

1. **Lectura humana del enunciado.** Basta leer las líneas 11–20 de
   [GaoEnunciado.lean](depuracion/gao20260920/formal/GaoEnunciado.lean).
   Lean certifica el enunciado, no su lectura. Comprobar:
   - `f` es el mapa clásico, con `f(0)=0`.
   - `Nat.log 2 m` es `floor(log2 m)` si m>=1, y 0 si m=0. Para k entero,
     `k<=log2 m` equivale a `k<=floor(log2 m)`.
   - `f^[k]` es la k-ésima iteración.
   - El filtro de `Finset.range N` son los `m<N` de G; el cociente por N
     tiende a 1. En Lean `x/0=0`, lo que no afecta al límite.
   - `open Classical in` sólo da la decidibilidad del filtro.
   - El teorema no tiene hipótesis, y `f = TejonasGao.collatz` se prueba por
     `rfl`.
2. **Forma literal de Gao.** El artículo se leyó el 25-09 y **no coincide
   literalmente** con lo demostrado
   ([ficha con las citas](depuracion/gao20260920/ficha_gao_lagarias.md)).
   Gao conjetura `d̄_k -> 1`, donde `d̄_k` es la proporción de los `n < 2^k`
   tales que n y n+1 coalescen en `<= k` iteraciones de C. Su coalescencia
   exige la misma imagen, el mismo número de divisiones por 2 y no pasar
   por 1. Pendiente:
   - Formalizar esa forma. La prueba parece cubrirla: la fusión da el mismo
     número de divisiones, y con `k <= log2 n` nadie pasa por 1. No está
     hecho.
   - Hasta entonces, decir «forma de Lagarias» y no «conjetura de Gao» a
     secas.
   - Actualizar la nota de `gao_densidad_uno` en el registro (cotejo hecho,
     no literal) y regenerar la base con el generador.
3. **Búsqueda bibliográfica a fondo.** Buscar quién cita a Gao (1993) en
   zbMATH, MathSciNet y Google Scholar. La búsqueda breve del 25-09 no halló
   ninguna prueba publicada, pero eso no basta para decir que es nueva.
4. **Redacción en prosa autocontenida.** Las notas usan el vocabulario del
   laboratorio y dependen de las sesiones desde el 20-09. Un revisor necesita
   en un solo texto:
   - las definiciones, la cadena y el potencial de Lagartijas;
   - el transporte y la densidad;
   - la relación con el enunciado original de Gao;
   - un mapa del código Lean.
5. **Revisión externa**, sólo con autorización del usuario.
6. **OEIS.** La propuesta del 24-09 (borrador en zootheorem, que no se toca
   desde aquí) dice que Gao «proved that its density is at least 0.389 (as
   summarized by Lagarias)» y que «Gao's conjecture is thus the statement
   that…».
   - Según el original, 0,389 es `d̄_24` calculado, y lo probado es que
     existe `lim d̄_k`.
   - La conjetura literal es `d̄_k -> 1`.

   Conviene ajustar esas dos frases antes de enviarla. Lo decide y lo hace
   el usuario. Las fichas de A398792 decían «They do not establish that lim
   A398792(n)/2^n = 1» ([nota del 24-09](depuracion/oeis20260924/LEEME.md)),
   y ese límite es justo lo que dan Tejonas y Martas. Cualquier edición,
   tras la revisión.
7. **Opcionales.**
   - Enunciar en Lean el corolario `A398792(t)/2^t -> 1`, que sale de
     `transporte` y `martas`.
   - Un ritmo útil. El de la prueba es pésimo: `J_F*p_m>1` sólo desde
     m=802923 ([Cigarras](depuracion/gao20260924/Cigarras.md)).
   - Cotejar si el resultado implica la conjetura de Garner (1985). Gao la
     resume así: la mayoría de los enteros tienen la misma altura que un
     vecino.
   - Decidir si `phi_uno` se cierra en el registro: sigue pendiente por sus
     aristas históricas, aunque `gao_densidad` ya da su contenido.

## Reglas vigentes

El repositorio es público: lo que se sube es visible, pero no es un anuncio.
**No anunciar, no enviar a OEIS ni a revistas y no contactar a nadie sin
autorización del usuario.** Los cambios de afirmaciones van al registro
versionado. No se reconstruyen conversaciones. El PDF de Gao no se sube.

## Reproducir

```
cd depuracion/gao20260920/formal     # primera vez: lake exe cache get (README)
lake build GaoCore GaoFormal
lake env lean GaoEnunciado.lean      # axiomas del teorema final
lake env leanchecker GaoEnunciado
cd ..
python -B -X utf8 evidencia_gao_lean.py            # todo, y reescribe la evidencia
python -B -X utf8 verificar_lagartijas_pares.py
python -B -X utf8 verificar_lagartijas.py
```

## Fuentes

- J. C. Lagarias, *The 3x+1 problem: An annotated bibliography (1963–1999)*,
  arXiv:math/0309224, pág. 28, entrada 68.
- G.-G. Gao, *On consecutive numbers of the same height in the Collatz
  problem*, Discrete Math. 112 (1993) 261–267, doi:10.1016/0012-365X(93)90240-T.
  Leído el 25-09, en el PDF que aportó el usuario.
- ccchallenge.org, que el 25-09 listaba Gao (1993) como «not formalized».
- arXiv:2603.11066 y arXiv:1511.09141: consultados el 25-09; no demuestran
  esta conjetura.
