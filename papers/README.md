# Artículos: Gao, Garner y Wu

27-09-2026. **Publicados en Zenodo y enviados a *Annals of Formalized
Mathematics*.** Detalle en [zenodo/LEEME.md](zenodo/LEEME.md).

28-09-2026. **AFM rechazó los tres sin dar motivos**, con tres correos a
las 17:39 (hora de Chile). Hasta el 04-10 estas notas decían que sólo había
rechazado el I y que el II y el III esperaban
([correos](CORREOS_20261004.md)).

29-09-2026. **El I, en versión 2, se envió a Qeios como preprint** (envío
5962): [qeios/LEEME.md](qeios/LEEME.md).

01-10-2026. **Se envió el I, adaptado a la revista, al *Journal of
Automated Reasoning*** (Springer). Envío `6ea1db0a…` en SNAPP, en revisión
técnica: [jar/LEEME.md](jar/LEEME.md). Qeios queda descartado; el retiro
del 5962 se pidió ese día a las 19:01 y Qeios lo confirmó el 02-10. Por qué
JAR: [revistas/LEEME.md](revistas/LEEME.md).

04-10-2026. JAR no ha escrito desde el acuse del 01-10. El II y el III
están libres; adónde enviarlos lo decide el autor.

| | Zenodo | AFM |
|---|---|---|
| Artefacto Lean | 10.5281/zenodo.23003500 | — |
| Artículo I | 10.5281/zenodo.23003524 | #19502, rechazado el 28-09 |
| Artículo II | 10.5281/zenodo.23003526 | #19503, rechazado el 28-09 |
| Artículo III | 10.5281/zenodo.23003528 | #19504, rechazado el 28-09 |

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
   (tarda más de un año y no da revisión por pares). El plan es un DOI en
   Zenodo y una revista *overlay* de Episciences. El 27-09 por la tarde se
   revisaron cuatro candidatas.

   **Qué repositorio admite cada una**

   | Revista | Repositorios |
   |---|---|
   | *Annals of Formalized Mathematics* (AFM) | Zenodo, arXiv o HAL |
   | DMTCS (actualizado el 24-09) | arXiv o HAL |
   | *Hardy-Ramanujan Journal* | arXiv o HAL |
   | *Communications in Mathematics* | arXiv |

   **Por qué se recomienda AFM**
   - Es la única de las cuatro que acepta Zenodo.
   - Exige un artefacto formal y admite lo obtenido con IA si hay prueba
     formal.
   - Acepta en unos 10 meses, según la mediana de sus 8 artículos.
   - Pide que el código sea abierto y accesible a los árbitros.

   **Hecho el 27-09 por la noche.** El usuario eligió Zenodo + AFM y pidió
   «envía los papers».
   - El paquete está armado y probado.
   - Los DOI ya figuran en los tres artículos.
   - Los cuatro registros están publicados en Zenodo, y los tres artículos
     enviados a AFM (#19502–#19504).

   Detalle, huellas y cartas: [zenodo/](zenodo/LEEME.md).
3. **Para la respuesta a los árbitros** (27-09):
   - citar Pandas en la pregunta de Gao (I y II);
   - citar Nashida (2026) en Wu 1 y en Garner (1) (II y III);
   - citar Novgorodtsev (2026b) y Kolpakov et al. (2026) como trabajos
     afines (I).

   Detalle en la [ruta transversal](../depuracion/transversal20260927/LEEME.md).
4. **ORCID sin obras.** El 04-10 el registro público
   (0009-0009-1418-2558) no mostraba nada, y los artículos y la carta a JAR
   lo enlazan. Falta añadir los cuatro DOI de Zenodo; es un cambio en la
   cuenta del autor.

## Revisión

[revision20260927/REVISION.md](revision20260927/REVISION.md) recoge la
revisión adversarial del 27-09. Cubre el Lean y los enunciados contra Gao
(PDF), Lagarias, zbMATH y Elia–Tucker. Incluye el cálculo independiente,
con las tablas 2 y 3 de Gao enteras, las rachas de Garner por otra ruta y
Wu hasta N = 26, además de la novedad, los nueve errores corregidos en los
borradores y los controles automáticos de los textos.

## OEIS

Enviadas el 27-09 con autorización del usuario ([oeis/](oeis/LEEME.md)):

- A400486: Gao, la tabla 3 en cuentas; aprobada el 04-10;
- A400487: Wu, la cuenta K; en *proposed*;
- la revisión #31 de A078441: Garner; aprobada el 30-09.

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
