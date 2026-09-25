# Estado para continuar — 25-09-2026

**La conjetura de Gao, en la forma que resume Lagarias, está demostrada
en Lean.** Teorema `TejonasGao.gao` ([Tejonas](depuracion/gao20260920/Tejonas.md)):
con f el mapa clásico (`n/2` o `3n+1`), el conjunto de n tales que
`f^k(n)=f^k(n+1)` para algún `k<=log2 n` tiene densidad natural 1.
`#print axioms` sólo muestra `propext`, `Classical.choice` y `Quot.sound`.
**Pendiente de revisión humana y de cotejo del artículo primario de Gao.**
No afirma nada sobre la llegada a 1.

## Objeto y ley

`T(x)=x/2` si es par, `(3x+1)/2` si es impar. Cadena original absorbente
con bits iid justos (paridad del ancla); estado `{v,3^k*v+c}`, sigma es la
fusión. `a(t)` cuenta clases módulo `2^t` que fusionan balanceadas hasta t,
y `phi=lim a(t)/2^t`. Tejonas demuestra que `a(t)/2^t=P(sigma<=t)`.

## Cadena demostrada (todo en `depuracion/gao20260920/formal`)

1. Ingredientes del 20-09: C1 (magnitud `<=66/h`), H3, VH, Hormigas, EF y
   protocolo guardado: `P(sigma>h)<=P(sigma>h y K_C(h)<1+j(W+2))+(1-p)^j`.
2. [Lagartijas](depuracion/gao20260920/Lagartijas.md): con `N=2^m`, `h=N^6`,
   `C=9h^4`, `P(sigma>h y K_C(h)<N)<=3/N+66/h+1/(4h^3)`; de ahí CF_F. La
   prueba usa un potencial por huecos entre entradas.
3. [Martas](depuracion/gao20260920/Martas.md): el lado derecho de CF_F tiende
   a cero, luego `P(sigma>h)->0`. El ritmo es pésimo: `J_F*p_m>1` sólo
   desde m=802923 ([Cigarras](depuracion/gao20260924/Cigarras.md)).
4. [Tejonas](depuracion/gao20260920/Tejonas.md): el estado canónico de todo
   par entero evoluciona por la cadena; transporte exacto a clases; paso al
   mapa clásico con `k<=2t`; densidad por bloques con `n>=4^t`.

## Primera obligación al retomar

Lista completa y criterios de cierre: [gaopendientes.md](gaopendientes.md).

1. **Revisión humana del enunciado**: [GaoEnunciado.lean](depuracion/gao20260920/formal/GaoEnunciado.lean),
   líneas 11–20 (`f`, `encuentro`, límite de densidad). Lean certifica el
   enunciado, no su lectura.
2. **Cotejo de Gao (1993)**, Discrete Math. 112, 261–267: el usuario dejó el
   PDF en local el 25-09, sin leer todavía; no se sube por derechos. El de
   Lagarias está hecho y coincide literalmente, con C el mapa clásico
   ([ficha](depuracion/gao20260920/ficha_gao_lagarias.md)). No se halló
   prueba publicada en una búsqueda breve.
3. Si ambas cosas salen bien, redactar la prueba para revisión externa.
   **No anunciar, no enviar a OEIS ni contactar a nadie sin autorización.**
   La propuesta OEIS del 24-09 sigue siendo correcta como texto histórico
   («Gao conjectured»); no añadirle que está demostrada sin revisión.

La ruta antigua (P1–P3, L-A, L-B, arranques polinómicos) queda superada,
no demostrada; sus nodos siguen pendientes en el registro. El P2 de
ventana constante para W sigue abierto y no hace falta.

## Evidencia y conservación

Lean 4.32.2 y Mathlib fijado; `lake build GaoCore GaoFormal` completo
(1609 tareas) y `leanchecker` repasa por el núcleo los 24 módulos propios,
todos con código 0. [Compilación, hashes y axiomas](depuracion/gao20260920/evidencia_gao_lean.json);
la de las piezas anteriores está en `evidencia_guardias_lean.json`. `.lake/`
se reconstruye con `lake exe cache get` ([README](depuracion/gao20260920/formal/README.md)).

Contrastes independientes: [cadena reimplementada](depuracion/gao20260920/verificar_lagartijas.py)
y [262.144 pares reales](depuracion/gao20260920/verificar_lagartijas_pares.py):
estado, biyección de clases, fusiones hasta t=18, periodicidad y encuentro
clásico, todo sin fallos. La densidad observada de G es 0,374 en `2^22`. Son
controles finitos; el certificado universal es Lean.

Registro 2026-09-25: 232 afirmaciones; Lagartijas, CF_F, Martas, Tejonas y
`gao_densidad` demostradas. Fuente versionada `depuracion/coherencia20260913/registro.json`
y generador `guardarafirmaciones.py`. No reconstruir conversaciones ni
alterar históricos. OEIS, 24-09: propuesta única lista, la envía el usuario
([texto](../zootheorem/drafts/PROPUESTA_ENCUENTRO_20260924.md)). zootheorem
permanece intacto.
