# Artículo IV (Ocelotas) en *Research in Number Theory*

12-10-2026. El usuario: «publica en otra revista». Gao sigue en JAR
(01-10), así que se elige otro trabajo: el IV.

Por qué *Research in Number Theory* (Springer):
- aplica la misma norma de IA que JAR: el uso de LLM se documenta en métodos;
- admite autores sin afiliación;
- el acceso abierto es opcional, así que enviar no cuesta nada;
- encaja con la temática (11B83, 11J86).

Se descartó *Mathematics in Computer Science* porque exige su plantilla y
una lista de 10 a 20 revisores.

## Estado

**Sin enviar.** El manuscrito se actualizó el 12-10:
- 81 rachas con pesos y Rozier–Terracol;
- teorema nuevo de 42 rachas con censo propio hasta 3·10^11;
- secciones 8 (pesos) y 9 (censo);
- resumen de 222 palabras;
- «Statements and declarations».

Compila con Tectonic 0.17.0 (bajado de nuevo de su GitHub oficial al
scratchpad): 18 páginas, sin avisos salvo un `Overfull \vbox` de 2 pt.

Bloqueo: la «Data availability» cita el repositorio público
`theswordofthemorning/conjeturadecollazpython`, pero los ficheros de 81, 40,
41 y 42 rachas siguen sin commit. Antes de enviar hacen falta el commit y
el push, que requieren permiso del usuario, y después el hash del commit
en el .tex.

Ficheros: [cover_letter.tex](cover_letter.tex) y su PDF.

## 12-10, 20:10
- Commit ccedd6c empujado; el .tex cita `ccedd6cfd3ff` en Data availability y
  el PDF está recompilado (cambio local, sin commit).
- El asistente no puede operar Editorial Manager (www.editorialmanager.com/rntb):
  la extensión deniega el dominio y el inicio de sesión exige contraseña.
  El envío lo hace el usuario con articulo_IV_ocelotas.pdf, cover_letter.pdf
  y el .tex como fuente.

## 12-10, ~21:00: ENVIADO
- Enviado a Research in Number Theory por Editorial Manager (usuario OmarSaid;
  la cuenta la creó el usuario). Tipo «Research», editor solicitado
  A. V. Sutherland, sin revisores sugeridos ni vetados, sin financiación.
- Archivos: articulo_IV_ocelotas.pdf (Manuscript) y enlace «Link(s) to
  supporting data» a github.com/theswordofthemorning/conjeturadecollazpython/
  tree/ccedd6cfd3ff/depuracion/cst20260930. El formulario no tenía casilla
  para la carta de presentación; no se subió.
- Confirmación en pantalla: «Thank you for approving». El número de
  manuscrito llegará por correo a omarsaid24@gmail.com.
- El usuario escribió su contraseña en el chat: se le recomendó cambiarla.

## Para una eventual revisión (no tocar el .tex enviado)
El .tex queda como se envió (42 rachas con censo hasta 3·10^11). Si la revista
pide cambios, se pueden incorporar:
- **46 rachas** con censo propio hasta 7·10^11 (12-10, noche): certificado
  pesos_46.json (42 filas al censo, 22 por pesos, 244 piezas; cola
  A=4086654774, c=7, H=51); Lean `OcelotasCuarentaYSeis`, 19 módulos y 96
  consultas estándar. Cambia el resumen, el teorema D, la sección 9 (tres
  tramos más, de 1 h 55 min) y la línea 497.
- **Corolario de ciclos formalizado**: la prueba en papel de
  Corollary cor:cycles ya está en Lean (`OcelotasCiclos.ciclo_exige`, con
  instancias para 24, 42 y 81). Puede citarse en el párrafo del corolario y en
  la sección de formalización. Ver depuracion/cst20260930/CICLOS_CALIBRACION.md.
