# Estado para continuar — 26-09-2026

**Demostradas en Lean: la conjetura de Gao (1993), también en su forma
literal, y de ella la conjetura de Garner (1985) sobre rachas.**

- **Forma de Lagarias.** `GaoEnunciado.conjetura_gao`
  ([Tejonas](depuracion/gao20260920/Tejonas.md)): con f el mapa clásico
  (`n/2` o `3n+1`), el conjunto de n tales que `f^k(n)=f^k(n+1)` para algún
  `k<=log2 n` tiene densidad natural 1.
- **Forma de Gao (1993).** `GaoLiteral.conjetura_gao_literal`
  ([Hienas](depuracion/gao20260920/Hienas.md)): `d̄_k -> 1`, con su
  coalescencia exigente (mismas divisiones por 2, sin pasar por 1), y
  además `d(x) -> 1`.
- **Garner (1985).** `GarnerEnunciado.conjetura_garner`
  ([Alpacas](depuracion/garner20260926/Alpacas.md)): para cada L hay L+1
  consecutivos, tan grandes como se quiera, con la misma altura y el mismo
  tiempo total de parada.

`#print axioms` sólo muestra `propext`, `Classical.choice` y `Quot.sound`.
**Pendiente de revisión humana.** Salvo en las rachas construidas, no
afirma nada sobre la llegada a 1.

## Objeto y ley

`T(x)=x/2` o `(3x+1)/2`. Cadena absorbente con bits iid justos (paridad
del ancla), estado `{v,3^k*v+c}`; sigma es la fusión. Tejonas demuestra que
la proporción `a(t)/2^t` de clases módulo `2^t` fusionadas hasta t es
`P(sigma<=t)`.

## Cadena demostrada (todo en `depuracion/gao20260920/formal`)

1. Ingredientes del 20-09: C1, H3, VH, Hormigas, EF y protocolo guardado.
2. [Lagartijas](depuracion/gao20260920/Lagartijas.md): pocas entradas
   admisibles antes de h; de ahí CF_F.
3. [Martas](depuracion/gao20260920/Martas.md): `P(sigma>h)->0`. El ritmo es
   pésimo: `J_F*p_m>1` sólo desde m=802923 ([Cigarras](depuracion/gao20260924/Cigarras.md)).
4. [Tejonas](depuracion/gao20260920/Tejonas.md): transporte exacto de pares
   reales a clases; mapa clásico con `k<=2t`; densidad por bloques.
5. [Hienas](depuracion/gao20260920/Hienas.md): un encuentro en `<=log2 n`
   pasos ya es coalescencia de Gao; de ahí `d̄_k -> 1` y `d(x) -> 1`.
6. [Alpacas](depuracion/garner20260926/Alpacas.md): por cota de unión, L
   pares fusionados seguidos; valor común `3^a·u+A` con `3∤A`; como 2 es
   raíz primitiva módulo `3^a`, u con `3^a·u+A=2^m`.

## Primera obligación al retomar

Lista completa y criterios de cierre: [gaopendientes.md](gaopendientes.md).

1. **Revisión humana de los enunciados.** Leer
   [GaoEnunciado.lean](depuracion/gao20260920/formal/GaoEnunciado.lean),
   líneas 11–20; [Hienas.lean](depuracion/gao20260920/formal/Hienas.lean),
   líneas 34–76, y [GarnerEnunciado.lean](depuracion/gao20260920/formal/GarnerEnunciado.lean),
   líneas 11–27. Lean certifica el enunciado, no su lectura. Hay tres apoyos:
   - las definiciones reproducen la tabla 3 de Gao;
   - Hienas escribe de nuevo la forma de Lagarias sin importar nada del
     proyecto;
   - los `#guard` de Garner reproducen las rachas 943–949, 7083–7099 y
     57346–57370 de Gao.
2. **Bibliografía a fondo.** No se halló prueba publicada de ninguna de las
   dos ([ficha](depuracion/gao20260920/ficha_gao_lagarias.md),
   [Alpacas](depuracion/garner20260926/Alpacas.md#novedad)). Faltan zbMATH,
   MathSciNet, Scholar y el texto de Garner (1985).
3. **Redacción autocontenida para revisión externa.** Con autorización del
   usuario. ccchallenge.org acepta formalizaciones en Lean, pide declarar el
   uso de IA y las audita otra persona.

**No anunciar, no enviar a OEIS ni contactar a nadie sin autorización.**

- **OEIS.** La propuesta del 24-09 la envía el usuario. Conviene corregir
  dos frases sobre el original de Gao, y no añadir «proved» sin revisión.
- **Siguiente ruta:** la elige el usuario. Candidatas en
  [gaopendientes.md](gaopendientes.md), punto 6: el corolario
  `A398792(t)/2^t -> 1`, un ritmo útil, y Garner (1) con alturas en `ℕ∪{∞}`.
  Garner (1) con alturas finitas sigue abierta.

La ruta antigua (P1–P3, L-A, L-B) queda superada, no demostrada; sus nodos
siguen pendientes en el registro.

## Evidencia y conservación

Lean 4.32.2 y Mathlib fijado. El 26-09 se recompiló todo desde cero (1610
tareas, 175 consultas de axiomas estándar). Tras Alpacas, `leanchecker` da
código 0 en los 28 módulos propios, y `leanchecker --fresh GarnerEnunciado`,
que repasa además Mathlib, sale con código 0.
[Compilación, hashes y axiomas](depuracion/gao20260920/evidencia_gao_lean.json),
con hashes en LF. `formal/.lake/build_respaldo_20260920`, fuera de Git, se
puede borrar. `.lake/` se reconstruye con `lake exe cache get` ([README](depuracion/gao20260920/formal/README.md)).

Contrastes independientes:

- [cadena reimplementada](depuracion/gao20260920/verificar_lagartijas.py) y
  [262.144 pares reales](depuracion/gao20260920/verificar_lagartijas_pares.py);
- [verificar_hienas.py](depuracion/gao20260920/verificar_hienas.py): los 21
  valores de la tabla 3 de Gao y 0 fallos del puente en `n<2^24`;
- [verificar_alpacas.py](depuracion/garner20260926/verificar_alpacas.py):
  rachas construidas de L+1 para `L<=22`, con altura `t+a+m` y `σ∞=t+m`
  iterando de verdad, y la tabla 1 de Gao entera.

Son controles finitos; el certificado universal es Lean.

Registro 2026-09-26: 234 afirmaciones; Lagartijas, CF_F, Martas, Tejonas,
`gao_densidad`, `hienas` y `alpacas_garner` demostradas. Fuente versionada `depuracion/coherencia20260913/registro.json`
y generador `guardarafirmaciones.py`. No reconstruir conversaciones ni
alterar históricos. zootheorem permanece intacto.
