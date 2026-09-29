# Gao en Palomar

29-09-2026. El usuario pidió «haz lo de Palomar». [Palomar](https://palomar-registry.org/)
es un registro de matemáticas verificadas en Lean, respaldado por el Lean FRO
y por ICARM, con Terence Tao en su consejo científico
([anuncio del 18-08-2026](https://terrytao.wordpress.com/2026/08/18/palomar-a-registry-of-lean-verified-mathematics/)).
Admite pruebas hechas con IA. **No es revisión por pares.** Cada envío pasa
dos filtros:

- uno mecánico: `lake comparator` comprueba que `Solution.lean` prueba
  exactamente lo que dice `Challenge.lean`, con los núcleos de Lean, NanoDa y
  con-ron;
- uno editorial hecho por un modelo de lenguaje. Rechaza, entre otras cosas,
  las «soluciones de problemas famosos» que no traen una comparación
  cuidadosa con la conjetura, un estado de la literatura y una declaración
  honesta de lo que falte.

## Repositorio

**https://github.com/theswordofthemorning/gao-palomar**, público, creado el
29-09 desde la sesión del usuario en Chrome. Está en
`Desktop/gao-palomar`, al lado de este proyecto. Primer commit: `953ca98`.

- Partió de la plantilla oficial
  [PalomarTemplate](https://github.com/PalomarRegistry/PalomarTemplate): CI,
  scripts, `docbuild/` y licencia Apache-2.0.
- Usa `leanprover/lean4:v4.35.0-rc2` con Mathlib `v4.35.0-rc2`, el mínimo
  que Palomar exige (`toolchains.json`). Nuestro desarrollo estaba en
  v4.32.2.
- `GaoCoalescence/` contiene los 26 módulos de la cadena de Gao, de
  `cadena_completa` y `rachas` a `GaoLiteral`, con el sistema de módulos:
  `module`, `public import` y `@[expose] public section`. Garner y Wu no
  están.
- `Challenge.lean`, de unas 100 líneas y en inglés, sólo importa Mathlib.
  Define `collatz`, `halvings`, `Coalesce`, `dbar` y `d`, y enuncia
  `GaoCoalescence.lagarias_form` y `GaoCoalescence.gao_form` con `sorry`.
- `Solution.lean` repite esas definiciones y prueba los dos teoremas a
  partir de `GaoEnunciado.conjetura_gao` y
  `GaoLiteral.conjetura_gao_literal`.
- `formalization.yaml` (v0.4) valida contra el esquema oficial sin errores.
  Declara el resultado como `original-proof`, con Gao y Lagarias como
  fuentes de contexto, los modelos Claude usados, `review: self-assessed` y
  las divergencias con el texto de Gao.

### Cambios del port (v4.32.2 → v4.35.0-rc2)

Sólo cuatro módulos necesitaron cambios en las pruebas; ningún enunciado
cambió.

| Módulo | Cambio |
|---|---|
| `Reloj` | `media_reloj`: el `simp` ya no reescribía con la hipótesis de inducción; se cierra con `congrArg`. `sin_progreso`: `promedio_fuera` se aplica con `rw` en los tres casos triviales. |
| `Lagartijas` | Importa `Mathlib.Algebra.Order.Ring.Pow` (`one_add_mul_le_pow` cambió de módulo). `activo_tamano`: `of_decide_eq_true` en vez de `simpa`. |
| `Tejonas` | `Finset.filter_card_add_filter_neg_card_eq_card` pasa a llamarse `Finset.card_filter_add_card_filter_not`. |
| `GaoLiteral` | `meta import GaoCoalescence.Hienas`, para que el `#guard` de la tabla 3 de Gao pueda evaluarse con el sistema de módulos. |

Quedan avisos por lemas obsoletos (`if_true`, `if_pos`…) que no impiden
compilar.

### Verificación local (Windows)

- `lake build`: «Build completed successfully (1635 jobs)». Los únicos
  `sorry` son los dos intencionados de `Challenge.lean`.
- `#print axioms` de `GaoCoalescence.lagarias_form` y
  `GaoCoalescence.gao_form`: `propext`, `Classical.choice`, `Quot.sound`.
- El `#guard` de `GaoLiteral` recalcula la tabla 3 de Gao para k = 4..12.
- `scripts/check-lean-sources.py`: OK.
- `lake comparator` necesita Linux y `bwrap`, así que no se ejecuta aquí;
  lo corre el CI de GitHub.

## Envío

**Enviado el 29-09-2026 a las 21:38:37 UTC**, con autorización expresa del
usuario («sí, autoriza y envía»):

- repositorio `theswordofthemorning/gao-palomar`;
- commit `c621ea46ed2cc34cddf7cbf8c065ca824f1495eb`;
- configuración `comparator.json`;
- relación: «I am a responsible author or maintainer of it»;
- una nota para la revisión automática, con lo que no se afirma (3x+1), la
  ayuda de IA, las divergencias con Gao, los DOI y el ORCID.

Se autorizó en GitHub la aplicación «Palomar Submissions» de PalomarRegistry,
con acceso sólo a datos públicos.

CI de GitHub en ese commit: compilación, `lake comparator`, metadatos,
licencia, enlace del README y documentación de la API en verde (lo último,
comprobado por el usuario en GitHub). El primer CI (`953ca98`) falló sólo porque
`verify-comparator.sh` perdió el permiso de ejecución al copiarse en Windows;
se corrigió en `a12a7eb`. Dependabot se quitó en `c621ea4`, y sus dos
propuestas se cerraron.

Palomar no manda correos. El enlace de estado es privado, porque permite
retirar el envío, y está en `papers/palomar/ENLACE_PRIVADO.txt`, excluido de
Git. Posibles resultados de la revisión: `neutral`, `revision_required` o
`rejected`. Sólo se hacen públicos si se completa el registro.

## Pendiente

1. Seguir el estado del envío; si pide revisión, corregir y enviar un commit
   nuevo.
2. Zulip: publicado el 29-09 a las 18:45 ([registro](../qeios/ZULIP_borrador.md)). Leer las
   respuestas y contestar sólo con autorización.
3. No consultar la API de GitHub sin autenticar en bucle: el cupo es de 60
   peticiones por hora y por IP, y el 29-09 se agotó.
