# Destinos revisados el 01-10-2026

Criterios del usuario: que acepte trabajo hecho con IA, que acepte autores
sin título ni afiliación, y sin costes. Todo comprobado en la página
oficial de cada revista ese día salvo donde se indica.

| Destino | IA | Sin afiliación | Coste | Veredicto |
|---|---|---|---|---|
| *INTEGERS* | **Prohibida** para «producing mathematics, computer code, bibliographic information, or other content»; hay que confirmarlo por escrito al enviar ([submit](https://math.colgate.edu/~integers/submit.html)) | no dice | gratis | **Muro** |
| *Qeios* | admitida si se declara | **no**: piden doctorado/MD y publicaciones revisadas (correo del 30-09) | gratis | **Muro** |
| arXiv | admitida | **no** en la práctica: desde el 21-01-2026 el autor nuevo necesita aval personal de alguien que ya publica en la categoría ([blog](https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/)) | gratis | Muro sin padrino |
| *Journal of Integer Sequences* | IA puede «propose proofs» con crédito explícito; **prohibido que un LLM escriba el texto inglés** ([JIS](https://cs.uwaterloo.ca/journals/JIS/)) | sin requisito | gratis | Posible si Omar escribe el texto |
| *Experimental Mathematics* (T&F) | código generado por IA sí, revisado; **prohibido el primer borrador del texto con IA**; traducción sí ([guía T&F](https://authorservices.taylorandfrancis.com/editorial-policies/using-ai-in-your-research-and-manuscript-preparations/)) | sin requisito | gratis por suscripción | Posible si Omar escribe el texto |
| *Journal of Automated Reasoning* (Springer) | **Admitida**: «Use of an LLM should be properly documented in the Methods section»; LLM no puede ser autor | **sí**: «For authors that are (temporarily) unaffiliated we will only capture their city and country» | gratis por suscripción (OA opcional, de pago) | **Recomendada para Gao** |
| *Research in Number Theory* / *Ramanujan J.* (Springer) | misma política Springer | sin requisito | gratis por suscripción (OA: 2990 €, opcional) | Plan B de Gao |

**Decisión del 01-10:** Gao va a JAR. **Enviado ese día hacia las 18:50**
([../jar/LEEME.md](../jar/LEEME.md)). Qeios queda descartado; el usuario:
«olvídate de ellos».

## Por qué JAR para Gao

- Es la única del grupo cuya norma acepta, sin condiciones extra, lo que ya
  hicimos: IA en la prueba, en el código y en el texto, declarada en una
  sección de métodos.
- Su ámbito incluye expresamente «formal proof assistants», «the use of
  artificial intelligence techniques to guide the search for a proof» y
  formalizaciones de matemática pura (publicó en 2025 la formalización del
  teorema de los números primos con término de error).
- Contempla autores sin afiliación en sus instrucciones.
- El artículo ya está escrito con el desarrollo Lean en el centro. Hay que
  rebautizar *Use of AI tools* como sección de métodos (o añadir una) y
  pasarlo a la plantilla de Springer.

## Muros que siguen en pie

- **Envío simultáneo: ya no existe.** Hasta el 04-10 estas notas daban a
  Garner (#19503) y Wu (#19504) por pendientes en AFM. En realidad AFM los
  había rechazado el 28-09, junto con Gao ([correos](../CORREOS_20261004.md)):
  los tres están libres.
- **Qeios 5962** era un preprint, no una revista, y no bloqueaba a
  Springer. Aun así se pidió su retiro el 01-10 a las 19:01, y Qeios lo
  confirmó el 02-10 ([qeios/LEEME.md](../qeios/LEEME.md)).
- **Texto escrito por IA.** JIS y Taylor & Francis lo prohíben. Para ellas
  Omar tendría que escribir el texto (en español; la traducción con IA la
  admite T&F, JIS no lo aclara).
- **Rechazo de mesa.** Ninguna exige título, pero un Collatz de autor
  independiente se mira con lupa. Lo que lo compensa es el artefacto Lean
  y la claridad sobre lo que no se demuestra.
