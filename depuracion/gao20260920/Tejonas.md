# Tejonas: transporte a pares reales y conjetura de Gao

25-09-2026. **Demostrado en Lean** ([Tejonas.lean](formal/Tejonas.lean), 8
consultas de axiomas, sólo `propext`, `Classical.choice`, `Quot.sound`;
`lake build GaoCore GaoFormal` completo). **Pendiente de revisión humana y
de cotejo con el artículo primario de Gao.**

## Enunciado final

Con `f(n)=n/2` si n es par y `3n+1` si es impar (A006370) y

    G = { n : existe k<=floor(log2 n) con f^k(n)=f^k(n+1) },

el teorema `TejonasGao.gao` dice: para todo eps>0 existe N0 tal que, para
todo N>=N0, `#(G ∩ [0,N)) >= (1-eps) N`. Como el cardinal no supera N, G
tiene **densidad natural 1**. La forma estándar, como límite, está aislada para
revisión en [GaoEnunciado.lean](formal/GaoEnunciado.lean):
`Tendsto (fun N => #(G ∩ [0,N))/N) atTop (𝓝 1)`, con `f` y G escritos de
nuevo sin depender de nombres internos. Es la conjetura de Gao (1993) tal como la
resume Lagarias y como la enuncia la propuesta OEIS del laboratorio.
No afirma que las trayectorias lleguen a 1.

## Piezas

1. **Pares reales.** `Par` guarda dos enteros y sus conteos impares bajo el
   mapa atajo `Tm`. El estado canónico toma como ancla el de menos pasos
   impares (o el menor si empatan): `k=|P-Q|`, `c=otro-3^k*ancla`.
   `canon_paso`: para **todo** par entero, el estado canónico del siguiente
   par es `paso` del estado actual con la paridad del ancla como bit. Casos:
   nivel 0 (`canon_paso_cero`), niveles altos y bajada a 0 con fusión en
   `c=1` (`canon_paso_alto`), y el resto por simetría (`gira`).
2. **Clases residuales.** Una representación afín `(3^p m+a, 3^q m+b)` tiene
   estado independiente de m (`canon_rep`); partir m por su bit bajo da un
   paso afín (`paso_rep`) y los dos hijos reciben bits opuestos (`bit_rep`).
3. **Transporte.** `suma_rep`/`transporte`: para toda f,
   `sum_{n<2^t} f(estado del par (n,n+1) en t) = 2^t E[f(cadena en t)]`.
   Con f=fusión: los n<2^t que fusionan hasta t son `2^t P(sigma<=t)`.
4. **Periodicidad.** `iter_rep`, `canon_modulo`: el estado en t depende sólo
   de `n mod 2^t`.
5. **Mapa clásico.** `iter_collatz`: tras t pasos del atajo cada miembro es
   `f^(t+P)`. `fusion_clasica`: fusión en t da `f^k(n)=f^k(n+1)` con
   `k=t+P<=2t`.
6. **Densidad.** `conteo_bloques` cuenta por bloques de `2^t`. Se elige t con
   `P(sigma<=t)>=1-eps/2` ([Martas](Martas.md)); para `n>=4^t`, `2t<=log2 n`.
   Los n<4^t son finitos: `#G∩[0,N)>=(N/2^t-1)|S_t|-4^t>=(1-eps)N` para N
   grande (`gao`).

## Cadena completa de dependencias

EF, VH, Hormigas, H3, C1 y el protocolo guardado (sesiones del 20-09)
→ [Lagartijas](Lagartijas.md) (pocas entradas, CF_F) → [Martas](Martas.md)
(límite) → Tejonas (transporte y densidad). Todo compila junto; `#print
axioms TejonasGao.gao` recorre todas las dependencias y no muestra `sorryAx`.
`leanchecker` vuelve a pasar por el núcleo los 24 módulos propios, desde
`cadena_completa` hasta `GaoEnunciado`, todos con código 0.
[Compilación, hashes, axiomas y leanchecker](evidencia_gao_lean.json).

## Contrastes

[verificar_lagartijas_pares.py](verificar_lagartijas_pares.py), 262.144
pares `(n,n+1)` con `n` en `[2^18,2^19)`: estado real igual a la cadena en
todos los instantes, biyección de clases, fusiones exactas hasta t=18,
periodicidad módulo `2^18` y encuentro clásico en `k<=2t` para los 103.358
pares fusionados, sin fallos. La densidad observada de G es 0,364 en `2^20`
y 0,374 en `2^22`: creciente y lejos de 1. El teorema es asintótico y su
ritmo es pésimo ([Cigarras](../gao20260924/Cigarras.md)); esas cifras no lo
contradicen ni lo confirman.

## Qué revisar antes de afirmarlo fuera

- El enunciado de Lean coincide literalmente con el de Lagarias, con C el
  mapa clásico. El original de Gao (1993), leído el 25-09, no coincide
  literalmente: conjetura `d̄_k -> 1` con una coalescencia más exigente
  ([ficha](ficha_gao_lagarias.md)). Esa forma quedó formalizada el 26-09 en
  [Hienas](Hienas.md) (`GaoLiteral.conjetura_gao_literal`).
- Una lectura humana de los enunciados Lean (`collatz`, `gao_encuentro`,
  `gao`): Lean certifica el enunciado, no su interpretación.
- No enviar a OEIS ni publicar sin autorización del usuario.
