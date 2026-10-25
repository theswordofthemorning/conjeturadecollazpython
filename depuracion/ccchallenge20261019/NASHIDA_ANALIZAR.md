# Nashida: lectura estratégica y auditoría pendiente

**Actualización 25-10-2026:** se revisaron estratégicamente los seis trabajos,
sus hipótesis y su relación con nuestras rutas. Los commits remotos siguen
coincidiendo con los de la tabla. El [balance global](../balance20261025/BALANCE.md)
no identifica un puente universal aplicable y precisa el alcance de las
barreras; en particular, corrige extrapolaciones demasiado amplias del plan
del 19-10. No se recompilaron los proyectos externos ni se completó una
auditoría de todas sus pruebas. Esa revisión sigue pendiente.

Se conserva a continuación la nota del 20-10 como registro de lo descargado
y comprobado entonces; su frase «todavía no está analizado» describe esa fecha.

## Nota original — 20-10-2026

Hay que analizar a fondo el trabajo de Hiroyuki Nashida: sus repositorios
de GitHub y sus artículos de Zenodo. Podría traer avances de este año que
sirvan a la ruta: barreras de YAH, el piloto G y la escalera G_Ak/G_Bk.
Todavía no está analizado; abajo queda lo que ya se bajó y se comprobó.

Ojo: Nashida declara que todo el código se escribió con Claude y que ningún
matemático ha revisado las pruebas. La parte III responde a una revisión
externa de su r3.

## Material, fuera del repo

En este PC, en `C:\Users\Home\Desktop\nashida\` (clones completos) y
`C:\Users\Home\Desktop\nashida\pdf\` (PDF de Zenodo). Para rehacerlo en
otro equipo:

| Repo (github.com/harappa/…) | Commit | Revisión | Zenodo (concepto → versión) | MD5 del PDF |
|---|---|---|---|---|
| collatz-termination-certificate-dichotomy (parte I) | a138adb | r3 | 23081447 → 23081448 | a2b4b134f299bd45d550ed580ced4b50 |
| collatz-matrix-interpretation-barriers (parte II) | 8e7d6da | r3 | 23081491 → 23081492 | 427c2017e3f3d897a2358dd2622215ec |
| collatz-arctic-interpretation-barriers (parte III) | de961be | r5 | 23147025 → 23397105 | 397443be6c96f4e7c1a52e5d807f5ed7 |
| collatz-terras-bound-improvement | 84de3b5 | r7 | 22986641 → 23019994 | 15459ce0ab03905a820b6f57b2867c2c |
| collatz-fixed-barrier-power-saving | 976fffb | r8 | 22986670 → 22986671 | a20e2cf1123471ec20c5e6aa7047eeab |
| collatz-generalized-natural-density | a390df8 | r5 | 22986677 → 22986678 | 8370db324a2446f870ecb3e2845fab27 |

Los PDF se bajan con
`https://zenodo.org/api/records/<versión>/files/<repo>-<revisión>.pdf/content`.
Quedan fuera tres repos de harappa que no tratan de Collatz: `jan`,
`harappa.github.io` y `nk-punctuated-band`.

## Ya comprobado (20-10)

- Manifiestos SHA-256: I, II y Terras coinciden. Fallan sólo `.gitignore`
  (III) y README (fixed-barrier y natural-density), tal como los subió el
  autor; no hay ningún `.lean` afectado.
- Comprobadores en Python 3.14: los dos de la parte II (`check_theorem83`,
  `check_ws_direct`) y los ocho de la III dan `ALL OK`, incluida la
  regeneración byte a byte de sus 12 certificados.
- En la III, `sorry` y `native_decide` sólo aparecen en comentarios. Su
  registro da los tres axiomas estándar en 217 teoremas. **No se compiló
  Lean aquí:** usa Lean 4.34.1 y Mathlib v4.34.1, y `leanchecker --fresh`
  tarda unos 40 a 55 min por módulo.
- La parte I ya se analizó el 19-10: [clasificacion.txt](clasificacion.txt)
  y [PLAN.md](PLAN.md).

## Primeras observaciones, por confirmar al analizar

- Nuestro `peldano5_completo` es el H de YAH (`collatz-T-5or7mod8`), pero
  con `b0 b0 $ -> t0 $` cambiado por `f R -> a0 R`, más la regla
  `L t t R -> L f f f R`. Las barreras de la III (ártica para T, H y R_H;
  natural sólo para T) **no cubren nuestro sistema**.
- No cubren tampoco: las interpretaciones tropicales, las naturales sobre H,
  los órdenes lexicográficos, las core matrices de Thiemann y otros, ni las
  cadenas donde otra técnica actúa primero (AProVE). Nuestras UNSAT de YAH
  siguen siendo datos, no teoremas.
- El método de la III (autómatas que leen los dígitos binarios a lo largo
  de la órbita, más el lema de simulación 5.6 en Lean) podría servir de
  plantilla para una barrera de G. Sería un resultado nuevo, no algo que
  ellos prueben.
- La parte II prueba en Lean siete debilitamientos de las conjeturas 4.11
  a 4.14 con certificados escalonados. Para G_Ak/G_Bk el clasificador dio
  enredo, así que ese tipo de certificado no les sirve (por la parte I,
  que no está en Lean).

## Qué analizar

1. Leer el PDF de la III: secciones 5 a 7 (el método), 8.2 (sistemas
   transformados) y 15 (los problemas abiertos Q1 a Q9). Cotejarlo con
   [INFORME_YAH.md](../judas20261016/escalera/yah/INFORME_YAH.md).
2. Decidir si su barrera se adapta a `peldano5_completo`, G_A2 y G_B4: qué
   hipótesis se cumplen y cuáles faltan. Una etiqueta no basta.
3. Leer los tres artículos de septiembre (Terras, densidad sobre N0,
   densidad natural generalizada) y buscar lo que toque a la ruta y a las
   afirmaciones del repo.
4. Si algo se usa como base, compilar su Lean con `leanchecker` en el
   Victus o en WSL, nunca durante una carrera.
