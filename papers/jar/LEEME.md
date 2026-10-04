# Artículo I (Gao) en el *Journal of Automated Reasoning*

01-10-2026. El usuario: «Qeios no va a publicar, olvídate de ellos […]
tendríamos que ir por Journal of Automated […] avanzar por un camino
seguro». Después fijó como objetivo de la sesión «publica Gao en la revista
acordada […] envía la publicación». Por qué JAR y no otra:
[../revistas/LEEME.md](../revistas/LEEME.md).

## Estado

**Enviado el 01-10-2026, hacia las 18:50 (hora local), por SNAPP de
Springer Nature.** ID de envío `6ea1db0a-7bc0-4dc2-bccb-586cf326943a`,
versión v.1.0, tipo *Research*, revisión *single anonymous*. Al enviar, la
página dijo: *"Your submission is now at our Technical Check stage"*. Los
avisos llegarán a omarsaid24@gmail.com. Seguimiento:
<https://submission.springernature.com/submission-details/6ea1db0a-7bc0-4dc2-bccb-586cf326943a>.

Cómo se hizo:
- **Acceso:** la cuenta de Springer Nature la abrió el usuario; Claude
  rellenó el formulario.
- **Avería:** a las 18:31 SNAPP dio 503 y luego 401. El usuario volvió a
  entrar y los datos de autor se escribieron de nuevo.
- **Casillas de aceptación:** el usuario marcó los términos y la política
  del modelo híbrido. La de políticas de autoría la marcó Claude cuando el
  usuario dijo «lo de la policy velo tú también».
- **Research Square («In Review»):** «No». El usuario dijo «lo del preprint
  velo tú», y ya existe el preprint en Zenodo.

| Campo | Valor enviado |
|---|---|
| Manuscrito | `articulo_I_gao_jar_latex.zip`. SNAPP lo compiló con pdfTeX 1.40.29: 16 páginas, solo avisos de `newunicodechar` por redefinir → ¬ ⟨ ⟩ · |
| Archivo relacionado | `articulo_I_gao_jar.pdf` (nuestra versión XeTeX) |
| Carta | `cover_letter.pdf` |
| Resumen | texto plano con superíndices Unicode (Cᵏ, 2ᵗ, log₂) |
| Autor | Omar Javier Said Duran, omarsaid24@gmail.com, «Independent Researcher, Calama, Chile», autor de correspondencia |
| Contribuciones | «O.J.S.D. is the sole author. O.J.S.D. directed the work and is responsible for the formalization, the numerical checks and the manuscript text, which were produced with the assistance of large language models as documented in Section 6.4 of the manuscript. The language models are not authors.» |
| Conflictos de interés | No |
| Publicación previa | **Sí, «Preprints only»**: Zenodo; Qeios como preprint sin publicar; Garner y Wu en AFM, que citan el resultado sin volver a demostrarlo |
| Material de terceros | No |
| Datos | Sí: Zenodo 23003500, GitHub `gao-palomar` y A398792 |
| Financiación | No |
| Agradecimientos | vacío |

La fila «Publicación previa» quedó inexacta: AFM había rechazado Garner y
Wu el 28-09, y estas notas no lo recogieron hasta el 04-10
([correos](../CORREOS_20261004.md)). No afecta al I; si la revista pregunta,
aclararlo.

Si hace falta escribir a la oficina editorial, la página de seguimiento da
el correo dharaniprakash.devaraj@springernature.com. **No escribir sin
autorización del usuario.**

El campo de institución autocompleta desde un registro: hay que pulsar
Escape antes de guardar, o se cuela «Independent Dance, London».

## Archivos

| Archivo | Uso | SHA-256 |
|---|---|---|
| [articulo_I_gao_jar.tex](articulo_I_gao_jar.tex) | fuente LaTeX, un solo archivo | `5b250989da63a1d8764e6c06c77bef4e0f5862fe3582d924764539ce93ea2c98` |
| [articulo_I_gao_jar_latex.zip](articulo_I_gao_jar_latex.zip) | lo que se subió como manuscrito (sólo el `.tex`) | `569a667d625e9b0efcbf268676052eb427b1fe86a14d4b371b3cbc6724fba980` |
| [articulo_I_gao_jar.pdf](articulo_I_gao_jar.pdf) | PDF compilado con Tectonic, 16 páginas, subido como *related file* | `19c64b861181ecdf72c7a35f635de987de85d3de26a8b2a5d2241bfde35fb19a` |
| [cover_letter.tex](cover_letter.tex) / [cover_letter.pdf](cover_letter.pdf) | carta al editor (la subida es el PDF) | `13386b4d…` (PDF) |
| [cover_letter.txt](cover_letter.txt) | la misma carta en texto plano | |
| [resumen_texto.txt](resumen_texto.txt) | resumen en texto plano (245 palabras); en el formulario se usaron superíndices Unicode | |

El original enviado a Qeios, [../articulo_I_gao.tex](../articulo_I_gao.tex),
no se tocó (sigue con `45f7225f…`).

## Cambios respecto de la versión 2

La matemática (secciones 2 a 5) no cambia.

1. Resumen de 304 a 244 palabras (JAR pide entre 150 y 250): fuera los
   ingredientes técnicos de detalle y la frase sobre la lentitud; dentro una
   frase sobre la ayuda de modelos de lenguaje.
2. Palabras clave de 7 a 6 (JAR: de 4 a 6), sin «3x+1 problem». En la MSC,
   68V20 pasa a primaria.
3. Dirección «Independent researcher, Calama, Chile», fecha 1 October 2026,
   sin la nota de la versión 2. Comentarios del encabezado en inglés.
4. Subsecciones de la introducción numeradas (JAR: sistema decimal).
5. La sección 6 pasa a llamarse «Methods: formalization, checks and use of
   AI tools», porque JAR exige documentar el uso de LLM en los métodos.
   - 6.4, *Use of AI tools*: el texto que antes iba al final, más el
     entorno agéntico y los controles.
   - 6.1 añade cifras de los 26 módulos (6067 líneas, 374 teoremas y lemas,
     142 definiciones) y dice que no se usa la teoría de la medida de
     Mathlib.
   - 6.1 también corrige qué guarda `evidencia_gao_lean.json`: hashes y
     axiomas sólo de los módulos finales, y `leanchecker` de los 30.
6. «Statements and Declarations» antes de la bibliografía: financiación,
   intereses, contribuciones, disponibilidad de datos y código, y preprint.
7. DOI como `https://doi.org/…`. Los 11 de revistas se comprobaron en
   Crossref el 01-10 y los 4 de Zenodo resuelven.

## Comprobaciones del 01-10

- Tectonic 0.17.0: 16 páginas. Único aviso: `Overfull \vbox` de 1,45 pt al
  cortar la página 1, invisible.
- `revisar_tex.py`, `nombres_lean.py` (65 nombres) y `codigo_lean.py` (11
  declaraciones literales) dan OK. Se corrieron sobre este archivo con un
  envoltorio en el scratchpad, sin modificar los scripts.
- Los 26 módulos no cambiaron desde el 27-09. Los hashes de la evidencia
  coinciden en cuanto se normalizan los saltos de línea CRLF de Windows.
- Las cifras de modelos (Opus 5.5 en la cadena de Gao; Fable 5 y Opus 5
  antes) salen de los `Co-Authored-By` del historial.

## Pendiente

- Esperar el correo de la revisión técnica y, después, el del editor. Leer
  cada informe por su contenido y preparar las respuestas, pero **no
  contestar sin autorización del usuario**. Al 04-10 sólo habían llegado los
  acuses del 01-10: Springer a las 18:50 y Research Square a las 18:53. Ver
  el estado en SNAPP exige entrar con la cuenta de Google del usuario.
- Qeios 5962: la carta y el formulario lo declaran como preprint sin
  publicar. Con permiso del usuario, el retiro se pidió el 01-10 a las 19:01,
  después del envío a JAR, y Qeios lo confirmó el 02-10
  ([../qeios/LEEME.md](../qeios/LEEME.md)). Si la revista pregunta, decir
  que nunca llegó a publicarse y que se retiró.
- Garner y Wu (#19503 y #19504): AFM los rechazó el 28-09, así que están
  libres. Adónde enviarlos lo decide el usuario.
