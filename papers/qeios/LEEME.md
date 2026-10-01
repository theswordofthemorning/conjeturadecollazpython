# Artículo I (Gao) en Qeios

29-09-2026. AFM rechazó el artículo I (#19502) sin dar motivos. El usuario
pidió entonces «olvida a AFM, publica solo el artículo de Gao» en Qeios.
Garner y Wu no se envían: dependen de Gao, y en Wu falta cotejar el impreso.

## Estado

**Enviado el 29-09-2026, hacia las 17:20 (hora local), desde la cuenta del
usuario ya abierta en Chrome.** Qeios contestó: *"We've received your
article. It will be online on Qeios within 1 business day."* El número de
envío es **5962** (`/article-submission-confirm/5962`). Todavía no hay
enlace público ni DOI de Qeios; anotarlos aquí cuando aparezcan.

**Comprobado el 01-10-2026** (sesión del usuario en Chrome, sólo lectura): el
perfil ([108558](https://www.qeios.com/profile/108558)) dice «You haven't
posted any Publication yet»; sin notificaciones ni borradores; la búsqueda
«Collatz» no lo encuentra; `/article-submission-confirm/5962` da 400. El
plazo de «1 business day» ya pasó: sigue en revisión interna o hubo
respuesta por correo. Mirar el correo antes de escribir a info@qeios.com.
Ese día se rellenó el perfil (campo *Mathematics* y biografía de 125
caracteres); textos completos en [../perfil/PRESENTACION.md](../perfil/PRESENTACION.md).

**Abandonado el 01-10.** El correo del 30-09 pedía doctorado y publicaciones
revisadas; el usuario: «Qeios no va a publicar, olvídate de ellos». La
[respuesta](RESPUESTA_20261001.md) quedó sin enviar. Ese mismo día el
artículo se envió al *Journal of Automated Reasoning*, y la carta y el
formulario declaran este envío como preprint sin publicar
([../jar/LEEME.md](../jar/LEEME.md)).

**Retiro pedido el 01-10, a las 19:01**, con permiso del usuario («sí, está
bien, retíranos de Qeios»). Fue una respuesta desde su Gmail a info@qeios.com,
en el mismo hilo «Your recent submission»; figura en «Enviados». Se
desconocía otra vía: el perfil no muestra el envío. Texto literal:

> Dear Qeios Team,
>
> Thank you for your message. I have decided to withdraw my submission no. 5962, "Consecutive integers coalesce with density one under the Collatz map: a formally verified proof of a conjecture of Gao". Please do not publish it, and please let me know once it has been withdrawn.
>
> Best regards,
> Omar Javier Said Duran

No se contestó a la pregunta sobre credenciales ni se tocó la cuenta, cuyo
perfil está vacío. Falta la confirmación de Qeios: anotarla aquí cuando
llegue.

| Campo | Valor enviado |
|---|---|
| Manuscrito | [`papers/articulo_I_gao.tex`](../articulo_I_gao.tex) (LaTeX; huella abajo) |
| Suplementario | [said-duran-2026-gao-coalescence-density-one-v2.pdf](said-duran-2026-gao-coalescence-density-one-v2.pdf) |
| Autor | Omar Javier Said Duran, Independent Researcher, omarsaid24@gmail.com |
| Conflictos de interés | «The author declares no competing interests.» |
| Financiación | «This work received no specific funding.» |
| Preferencia | **Keep as preprint** (se puede enviar a una revista cuando se quiera) |
| Servicios Pro | ninguno: sin corrección gramatical, sin portada ni vídeo, sin redes |

Nota enviada a Qeios, literal:

> The manuscript is a single LaTeX file (amsart, bibliography included). It
> uses Unicode characters through newunicodechar and was compiled with XeTeX
> (Tectonic 0.17.0); the supplementary PDF is the reference rendering. The
> Lean 4 formal development is archived at doi:10.5281/zenodo.23003500;
> version 1 of this paper is doi:10.5281/zenodo.23003524. The paper does not
> claim anything about the 3x+1 conjecture itself. Reviewers in number
> theory (Collatz problem, arithmetic dynamics), probability (Markov chains)
> and formal verification (Lean/Mathlib) would be the most useful; Section
> 6.4 lists the three specific checks we ask for. AI assistance is declared
> in the section "Use of AI tools".

## Versión 2 del artículo

Cambios respecto de la versión 1 (Zenodo, commit `306b78b`); la demostración
no cambia:

1. Primera frase del resumen: el artículo no trata la conjetura 3x+1, sino
   la frecuencia con que se encuentran dos trayectorias consecutivas.
2. Sección 6.4, *What we ask reviewers to check*: tres veredictos separados
   (los enunciados Lean dicen lo que dicen los Teoremas A y B; la prueba no
   tiene `sorry`, axiomas propios ni hipótesis escondidas; el texto es fiel
   al desarrollo formal).
3. Fecha «29 September 2026 (version 2)» y, en *Formal verification*, el
   DOI de la versión 1 y la lista de estos cambios.

Compilado con Tectonic 0.17.0 (bajado de nuevo al scratchpad): 16 páginas,
sin avisos. `revisar_tex.py`, `nombres_lean.py` y `codigo_lean.py`: OK
(resumen de 1790 caracteres).

| Archivo | SHA-256 |
|---|---|
| `articulo_I_gao.tex` enviado | `45f7225f44e7869c5d0953346128207318c59eaee7118a8b38632ffe2948b79e` |
| PDF v2 (el suplementario) | `d2ed2bf9429d555a8aa1df9b3251d698d222ded96b35f98242a4deda8c8b018b` |

## Cómo funciona Qeios (comprobado el 29-09)

- [Planes](https://www.qeios.com/plans): el gratuito incluye *"Reviewer
  Recruitment Service on your first paper"* y *"Revise your papers once"*.
  Pro: US$24,99 al mes, revisiones ilimitadas, 30 días de prueba.
- El reclutamiento no compra revisiones: una IA de Qeios invita a
  investigadores, que aceptan o no.
- [Política](https://www.qeios.com/publishing-policy): «peer-approved» exige
  al menos 4 revisiones con medias de 3/5 o más en calidad general, claridad
  e impacto, y 2,5 o más en novedad. La IA se admite si se declara.
- Críticas: sin editor, revisores elegidos por IA, informes a veces breves
  ([telescoper](https://telescoper.blog/2024/12/15/qeios-and-the-nature-of-a-journal/),
  [Auclair](https://pierreauclair.org/blog/qeios.html)).

## Reglas para lo que sigue

- **No pasar a «Version of Record»**: contaría como publicación y cerraría
  INTEGERS u otra revista.
- **Una sola revisión gratuita**: no gastarla en erratas. Cuando lleguen
  informes con fondo, activar la prueba de Pro, corregir y cancelar.
- Leer cada informe por su contenido, no por su nota. Preparar las
  respuestas y **pedir autorización al usuario antes de publicarlas**.
- Garner y Wu, sólo después de que Gao reciba revisiones.

## Complementos

- **Zulip de Lean**: autorizado por el usuario el 29-09. Sin sesión en
  Chrome; el usuario debe entrar o crear la cuenta. Borrador en
  [ZULIP_borrador.md](ZULIP_borrador.md).
- **Palomar** ([anuncio de Tao, 18-08-2026](https://terrytao.wordpress.com/2026/08/18/palomar-a-registry-of-lean-verified-mathematics/),
  [instrucciones](https://palomar-registry.org/how-to-submit)): registro de
  matemáticas verificadas en Lean, respaldado por el Lean FRO, que admite
  pruebas hechas con IA. Su herramienta Comparator comprueba mecánicamente
  que la solución prueba exactamente el `Challenge.lean`. No es revisión por
  pares. Exige un repositorio público en GitHub, cabecera `module` en cada
  fichero, `Challenge.lean` de a lo sumo 1000 líneas que sólo importe
  Mathlib, `comparator.json` y `formalization.yaml`. Requiere adaptar los 30
  módulos; no se ha empezado.
