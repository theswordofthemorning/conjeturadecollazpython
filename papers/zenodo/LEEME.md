# Depósito en Zenodo y envío a AFM

27-09-2026, por la noche. El usuario pidió «envía los papers» con las
cuentas de ORCID, Zenodo y AFM ya activas. Ruta: Zenodo y después *Annals of
Formalized Mathematics* (AFM), la revista *overlay* de Episciences.

## Estado

**Publicados en Zenodo y enviados a AFM el 27-09-2026, entre las 21:17 y
las 21:28 EDT.** En AFM figuran como *Submitted*. En la hora del servidor
de Episciences es el 28-09, 03:17–03:28.

| Registro | DOI | Archivo | AFM |
|---|---|---|---|
| Artefacto Lean (software, Apache 2.0) | [10.5281/zenodo.23003500](https://doi.org/10.5281/zenodo.23003500) | `said-duran-collatz-lean-1.0.0.zip` | enlazado a los tres |
| Artículo I, Gao (preprint, CC BY 4.0) | [10.5281/zenodo.23003524](https://doi.org/10.5281/zenodo.23003524) | `said-duran-2026-gao-coalescence-density-one.pdf` | [#19502](https://afm.episciences.org/paper/view/id/19502) |
| Artículo II, Garner | [10.5281/zenodo.23003526](https://doi.org/10.5281/zenodo.23003526) | `said-duran-2026-garner-long-runs.pdf` | [#19503](https://afm.episciences.org/paper/view/id/19503) |
| Artículo III, Wu | [10.5281/zenodo.23003528](https://doi.org/10.5281/zenodo.23003528) | `said-duran-2026-wu-two-conjectures.pdf` | [#19504](https://afm.episciences.org/paper/view/id/19504) |

El DOI conceptual del artefacto (todas sus versiones) es 10.5281/zenodo.23003499.

Cómo se hizo:
- El artefacto se publicó primero.
- El clasificador de permisos del modo automático bloqueó la primera
  publicación de los artículos. Se publicaron cuando el usuario dijo
  «continua con las publicaciones».
- En AFM, cada envío llevó como editores sugeridos a Alex Kontorovich y
  Sébastien Gouëzel.
- La carta de [cartas_AFM.md](cartas_AFM.md) fue en el campo *Comment*,
  visible para editores y árbitros. Las cartas II y III citan además los
  números de envío anteriores.
- Episciences importó de Zenodo las relaciones: *is supplemented by* el
  software, y las referencias a los compañeros. No hizo falta enlazar el
  software a mano.

Si responden los editores: leer, preparar la respuesta y **pedir
autorización al usuario antes de contestar**, como con OEIS.

## Qué se hizo

1. **Artículos.** Tienen DOI en la bibliografía (el artefacto y los
   compañeros), ORCID como `\urladdr`, la fecha sin «Draft» y título y autor
   en los metadatos del PDF. Se quitó el `[TO CONFIRM: permanent archive and
   DOI]` del artículo I. Los controles `revisar_tex.py`, `nombres_lean.py` y
   `codigo_lean.py` dan OK.
2. **Artefacto.** Lo arma [armar_artefacto.py](armar_artefacto.py) con los
   fuentes de `HEAD` (`git show`) y la misma estructura de carpetas, para que
   `lakefile.lean` funcione sin cambios. Comprueba 13 SHA-256 contra
   `evidencia_gao_lean.json` y que `leanchecker` dio código 0 en los 30
   módulos. Añade:
   - [README_artefacto.md](README_artefacto.md) en inglés, con los teoremas,
     cómo compilar, los módulos, un glosario y los controles;
   - la licencia Apache 2.0, con el texto de la copia de Mathlib;
   - los programas de control (`checks/`) con sus salidas.
3. **Prueba de compilación del zip.** Se extrajo en una carpeta corta y
   `lake build GaoCore GaoFormal` dio «Build completed successfully (1615
   jobs)», con los paquetes de Mathlib enlazados por un *junction*. Hubo un
   solo aviso, por un lema obsoleto en `Tejonas.lean:654`. En la ruta larga
   del scratchpad falló la escritura de un `.olean` por el límite de 260
   caracteres de Windows; por eso el README lo advierte. Las carpetas de
   prueba se borraron, quitando antes los enlaces.
4. **Control nuevo.** `revision_wu.py` con `N_MAX = 24`
   ([salida](revision_wu_n24_salida.txt)): `K(2^N)` coincide hasta N = 24 y
   la pregunta de Gao no tiene contraejemplos para n < 2^24, como dicen los
   artículos I y II.
5. **Zenodo.** Borradores creados con la API del propio sitio, desde la
   sesión del usuario. Tienen el autor con ORCID, la afiliación, el resumen
   en texto plano, las palabras clave, la licencia y las relaciones: los
   artículos *is supplemented by* el software, el software *is supplement
   to* los artículos, y cada artículo *references* a los otros dos. Los MD5
   de los archivos subidos coinciden con los locales.

## Huellas

| Archivo | MD5 | SHA-256 |
|---|---|---|
| `said-duran-collatz-lean-1.0.0.zip` | `33df5cd80a7e8d805d5721df7b522c8d` | `a3c20737f2da4fc57a1dfcc9adbe7645d652a1668050b1f5fc6c37a905ebf9da` |
| `said-duran-2026-gao-coalescence-density-one.pdf` | `e419d8d9c16eb3d8a4c0d9c028c4f8da` | `ceb7d9ae27fdb037a0139cd25300b1680f741576e1e0a91f5b135d43771f7f7a` |
| `said-duran-2026-garner-long-runs.pdf` | `c8aa40af0628ad86c6b8ad0fa1be01dd` | `afe5636895c7e236b2aa452758271e44fbf82ab3152b360ece9ce760a7c91182` |
| `said-duran-2026-wu-two-conjectures.pdf` | `76acb2d64ac267aed40379534561d8a4` | `61c58e04f80fa37b53fe765467465cdcc20c85c7d314660805d8d4208b2694c9` |

[metadatos_base.json](metadatos_base.json) guarda los textos de las fichas.
