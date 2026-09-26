# Estado para continuar — 26-09-2026

**La conjetura de Gao está demostrada en Lean, también en su forma
literal.**

- **Forma de Lagarias.** `GaoEnunciado.conjetura_gao`
  ([Tejonas](depuracion/gao20260920/Tejonas.md)): con f el mapa clásico
  (`n/2` o `3n+1`), el conjunto de n tales que `f^k(n)=f^k(n+1)` para algún
  `k<=log2 n` tiene densidad natural 1.
- **Forma de Gao (1993).** `GaoLiteral.conjetura_gao_literal`
  ([Hienas](depuracion/gao20260920/Hienas.md)): `d̄_k -> 1`, con su
  coalescencia exigente (mismas divisiones por 2, sin pasar por 1), y
  además `d(x) -> 1`.

`#print axioms` sólo muestra `propext`, `Classical.choice` y `Quot.sound`.
**Pendiente de revisión humana.** No afirma nada sobre la llegada a 1.

## Objeto y ley

`T(x)=x/2` si es par, `(3x+1)/2` si es impar. Cadena original absorbente
con bits iid justos (paridad del ancla); estado `{v,3^k*v+c}`, sigma es la
fusión. `a(t)` cuenta clases módulo `2^t` que fusionan balanceadas hasta t,
y `phi=lim a(t)/2^t`. Tejonas demuestra que `a(t)/2^t=P(sigma<=t)`.

## Cadena demostrada (todo en `depuracion/gao20260920/formal`)

1. Ingredientes del 20-09: C1 (magnitud `<=66/h`), H3, VH, Hormigas, EF y
   protocolo guardado: `P(sigma>h)<=P(sigma>h y K_C(h)<1+j(W+2))+(1-p)^j`.
2. [Lagartijas](depuracion/gao20260920/Lagartijas.md): con `N=2^m`, `h=N^6`,
   `C=9h^4`, `P(sigma>h y K_C(h)<N)<=3/N+66/h+1/(4h^3)`; de ahí CF_F.
3. [Martas](depuracion/gao20260920/Martas.md): `P(sigma>h)->0`. El ritmo es
   pésimo: `J_F*p_m>1` sólo desde m=802923 ([Cigarras](depuracion/gao20260924/Cigarras.md)).
4. [Tejonas](depuracion/gao20260920/Tejonas.md): transporte exacto de pares
   reales a clases; mapa clásico con `k<=2t`; densidad por bloques.
5. [Hienas](depuracion/gao20260920/Hienas.md): un encuentro en `<=log2 n`
   pasos ya es coalescencia de Gao; de ahí `d̄_k -> 1` y `d(x) -> 1`.

## Primera obligación al retomar

Lista completa y criterios de cierre: [gaopendientes.md](gaopendientes.md).

1. **Revisión humana de los enunciados.** Leer
   [GaoEnunciado.lean](depuracion/gao20260920/formal/GaoEnunciado.lean),
   líneas 11–20, y [Hienas.lean](depuracion/gao20260920/formal/Hienas.lean),
   líneas 34–76. Lean certifica el enunciado, no su lectura. Para la lectura
   ya hay dos apoyos:
   - las definiciones reproducen la tabla 3 de Gao;
   - Hienas escribe de nuevo la forma de Lagarias sin importar nada del
     proyecto.
2. **Bibliografía a fondo.** No se halló prueba publicada: bibliografías de
   Lagarias, 9 citas de Gao y ccchallenge, donde Gao (1993) sigue sin
   formalizar ([ficha](depuracion/gao20260920/ficha_gao_lagarias.md)).
   Faltan zbMATH, MathSciNet y Scholar.
3. **Redacción autocontenida para revisión externa.** Con autorización del
   usuario. ccchallenge.org acepta formalizaciones en Lean, pide declarar el
   uso de IA y las audita otra persona.

**No anunciar, no enviar a OEIS ni contactar a nadie sin autorización.**

- **OEIS.** La propuesta del 24-09 la envía el usuario. Conviene corregir
  dos frases sobre el original de Gao, y no añadir «proved» sin revisión.
- **Siguiente ruta, elegida por el usuario el 26-09:** la conjetura de
  Garner (1985) de rachas arbitrariamente largas de la misma altura
  ([plan](depuracion/garner20260926/LEEME.md)). Parece salir de Martas más
  la elección de u que lleva a una potencia de 2. Un sondeo construyó
  rachas de 23. Primero, comprobar que no esté ya demostrada.

La ruta antigua (P1–P3, L-A, L-B, arranques polinómicos) queda superada,
no demostrada; sus nodos siguen pendientes en el registro. El P2 de
ventana constante para W sigue abierto y no hace falta.

## Evidencia y conservación

Lean 4.32.2 y Mathlib fijado. El 26-09 se recompiló todo desde cero: 1610
tareas y 175 consultas de axiomas, todas estándar. `leanchecker` da código
0 en los 26 módulos propios, y `leanchecker --fresh`, Mathlib incluido,
también. [Compilación, hashes y axiomas](depuracion/gao20260920/evidencia_gao_lean.json),
con hashes tomados en LF. La compilación del 20-09 quedó apartada en
`formal/.lake/build_respaldo_20260920`, fuera de Git, y se puede borrar.
`.lake/` se reconstruye con `lake exe cache get` ([README](depuracion/gao20260920/formal/README.md)).

Contrastes independientes:

- [cadena reimplementada](depuracion/gao20260920/verificar_lagartijas.py) y
  [262.144 pares reales](depuracion/gao20260920/verificar_lagartijas_pares.py),
  sin fallos;
- [verificar_hienas.py](depuracion/gao20260920/verificar_hienas.py): los 21
  valores de la tabla 3 de Gao y 0 fallos del puente en `n<2^24`.

La densidad observada de G es 0,382 en `2^24`. Son controles finitos; el
certificado universal es Lean.

Registro 2026-09-26: 233 afirmaciones; Lagartijas, CF_F, Martas, Tejonas,
`gao_densidad` y `hienas` demostradas. Fuente versionada `depuracion/coherencia20260913/registro.json`
y generador `guardarafirmaciones.py`. No reconstruir conversaciones ni
alterar históricos. zootheorem permanece intacto.
