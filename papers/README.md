# Artículos: Gao, Garner y Wu

27-09-2026. **Escritos, compilados y revisados; no enviados ni publicados.**
El usuario los pidió el 26-09 «como si fueran para arXiv», con nombres
completos y fechas, bien explicados y revisados antes. No se envía nada sin
su autorización.

| | Artículo | Archivo | Resultado principal (Lean) |
|---|---|---|---|
| I | *Consecutive integers coalesce with density one under the Collatz map: a formally verified proof of a conjecture of Gao* | [articulo_I_gao.tex](articulo_I_gao.tex), 15 págs. | `GaoEnunciado.conjetura_gao`, `GaoLiteral.conjetura_gao_literal` |
| II | *Arbitrarily long runs of consecutive integers with the same Collatz height* | [articulo_II_garner.tex](articulo_II_garner.tex), 8 págs. | `GarnerEnunciado.conjetura_garner` |
| III | *On two conjectures of Wu on consecutive integers of the same height in the Collatz problem* | [articulo_III_wu.tex](articulo_III_wu.tex), 6 págs. | `WuEnunciado.conjetura_wu_dos`, `conjetura_wu_uno` |

Los PDF se regeneran desde los `.tex`. En inglés, clase `amsart`, con la
bibliografía dentro. El II y el III citan al I; conviene leerlos en ese
orden.

- **I.** Gao (1993): `d̄_k → 1`, `d(x) → 1` y la forma de Lagarias
  (densidad 1). Contiene la cadena de pares, el transporte a clases, un
  resumen de la absorción casi segura (Martas) con cada enunciado y su
  nombre Lean, y el puente con prueba completa.
- **II.** Garner (1985), conjetura (2): para todo L hay L+1 consecutivos,
  tan grandes como se quiera, con la misma altura y el mismo `σ∞`. La
  prueba está completa y es elemental una vez dado el I.
- **III.** Wu (1992): `lim L = ∞` (conjetura 2), y `lim d(M) = 1` equivale
  a que los que llegan a 1 tengan densidad 1 (conjetura 1, abierta). Trae
  la tabla de Wu extendida hasta N = 26.

## Compilar

Con Tectonic 0.17.0 (portátil, de su GitHub oficial; el 27-09 se usó la copia
bajada el 26-09 a la carpeta temporal):

```
tectonic -X compile articulo_I_gao.tex
```

Los tres compilan sin avisos. Los símbolos de Lean (ℕ, →, 𝓝…) se mapean con
`newunicodechar`, y los nombres largos se cortan con `xurl`. Hay una rama
para pdfLaTeX (`\ifPDFTeX`), **sin probar**.

## Lo que falta, y es del autor

Hecho el 27-09, con los datos del usuario: autor «Omar Javier Said Duran,
Independent Researcher, omarsaid24@gmail.com» en los tres; sección *Use of
AI tools* (Claude Opus 5.5 en los resultados, Opus 5 y Fable 5 antes; en el
III, además, la IA de CNKI), sin agradecimientos vacíos; y Wu cotejado con la
IA de CNKI, que cita literal las dos conjeturas y la racha de 176
([nota](revision20260927/cnki_wu_20260927.md)). El impreso de Wu no se ha
visto, y el III lo dice. PDF recompilados el 27-09 por la tarde.

1. **Revisión humana** de los enunciados Lean ([gaopendientes.md](../gaopendientes.md))
   y lectura de los tres textos.
2. **Destino y formato.** El 27-09 el usuario descartó ccchallenge.org
   (tarda más de un año y no da revisión por pares). El plan pasa a ser un
   DOI en Zenodo y una revista *overlay*; se decide al retomar. Candidatas
   de Episciences que aceptan depósitos de Zenodo: *Discrete Mathematics &
   Theoretical Computer Science* y *Annals of Formalized Mathematics*. Falta
   armar el paquete (PDF, fuentes, los `.lean` y la evidencia) y poner su
   DOI donde dice `[TO CONFIRM: permanent archive and DOI]`.

## Revisión

[revision20260927/REVISION.md](revision20260927/REVISION.md) recoge la
revisión adversarial del 27-09. Cubre el Lean y los enunciados contra Gao
(PDF), Lagarias, zbMATH y Elia–Tucker. Incluye el cálculo independiente,
con las tablas 2 y 3 de Gao enteras, las rachas de Garner por otra ruta y
Wu hasta N = 26, además de la novedad, los nueve errores corregidos en los
borradores y los controles automáticos de los textos.

## OEIS

Enviadas el 27-09 con autorización del usuario; las tres en *proposed*
([oeis/](oeis/LEEME.md)):

- A400486: Gao, la tabla 3 en cuentas;
- A400487: Wu, la cuenta K;
- la revisión #31 de A078441: Garner.

No citan los artículos. Las líneas que los citarán esperan al DOI.

## Requisitos de arXiv (leídos el 26-09, por si se usa)

- Se sube el fuente TeX; un PDF generado desde TeX no se acepta.
- El resumen tiene como máximo 1920 caracteres, sin la palabra «Abstract».
- El primer envío a math.NT pide *endorsement*.
- Una IA no puede ser autora. El uso importante de IA se declara.
- El código Lean va en `anc/`.
- Rechazan afirmaciones exageradas; no más de tres envíos por día.

## Historia

El plan del 26-09 (formato, contenidos, pendientes y el primer orden de las
OEIS, con Wu primero) se conserva literal en [plan_20260926.md](plan_20260926.md).
