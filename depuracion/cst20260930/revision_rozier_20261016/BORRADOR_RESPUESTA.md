# Respuesta a Olivier Rozier — borrador sin enviar

**ENVIADO el 17-10-2026 a las 22:22**, a pedido del usuario, que dejó atrás
el plan B. Se envió en el mismo hilo, solo a olivier.rozier@gmail.com y sin
Terracol. El texto inglés de abajo salió tal cual, con un párrafo más, que
iba antes del enlace al código:

> Separately, and only in case it is of interest: earlier I wrote Lean proofs of three older conjectures on consecutive integers of the same height. They cover Gao's conjecture (1993) that n and n+1 coalesce for a set of density one, Garner's conjecture (1985) on arbitrarily long runs, and Wu's conjecture (1992) that the longest run below M tends to infinity. Wu's other conjecture, lim d(M) = 1, I could only reduce to the open statement that almost all integers reach 1. Since Garner measures heights with the shortcut map T, I have now also checked in Lean that the results hold for both T and the classical map. These are formal proofs that nobody has reviewed yet. I would be glad to send the three short preprints if you would like to see them.

El respaldo de ese párrafo es `depuracion/gao20260920/formal/AlturaT.lean`.

**Plan anterior:** [esperar a un avance considerable y un nuevo paper](PLAN_RESPUESTA.md).
Entonces se integrará su presentación con estas respuestas, de forma breve.
Este texto queda como base comprobada; no se envía ahora.

Responder al mismo hilo. Su cabecera `Reply-To` indica
`olivier.rozier@gmail.com`; su respuesta vino sin Terracol en copia.
Este documento no autoriza enviar ni añadir destinatarios.

El usuario autorizó commit y push de la extensión de 83, su auditoría y el
plan el 16-10. Al preparar el futuro envío, actualizar el texto y comprobar
los enlaces al código y al nuevo paper.

## Inglés

Dear Dr Rozier,

Thank you for your helpful reply, especially the pointer to Roosendaal's updated delay records. It led to a concrete improvement, which I checked before replying.

I have not contacted John Simons yet and do not have a confirmed current email address for him. Could you point me to his preferred contact address? Thank you for pointing out his investigation; I will keep the priority question open. I have also located his 2022 survey discussing m-nykels and am taking that antecedent into account.

You are right that Rhin gives a stronger bound. I originally chose LMN because I could check its original statement and conditions directly. I have now obtained Rhin's original and checked Proposition (7), p. 160: the exponent 13.3 applies for H ≥ 2, exactly matching the hypothesis of the conditional Lean version I added. With the same auxiliary estimates, the 83-run tail cutoff improves from 2^76 to 2^68. The present finite sieve nevertheless stops at 83 with either choice.

Following your suggestion, I used the confirmed record 46,645,791,847,966,786,687, with classical delay 2480. The weighted extension mentioned in my previous email improves from 81 to 83 runs. Its exact finite certificate and Lean proof have now passed the checks. I also formalized the bridge from a uniform delay bound on this interval to the CST statement, using our existing kernel-checked small-case certificate.

Regarding axioms: the external inputs are explicit theorem hypotheses. The final versions assume either LMN or Rhin, together with Roosendaal's coverage of the interval. Lean checks the deductions and finite certificates; it does not verify that external exhaustive computation or prove the transcendence estimate. The dependency audit reports only the standard Lean axioms.

The public code is at https://github.com/theswordofthemorning/conjeturadecollazpython/tree/main/depuracion/cst20260930. The checked 83-run extension and its audit log are ready to share.

Thank you again: your comments improved both the bound and the precision of the assumptions.

Best regards,
Omar Saïd

## Español, para revisar el contenido

Estimado Dr. Rozier:

Gracias por su respuesta y, en particular, por indicarme la actualización de
los récords de Roosendaal. Permitió una mejora concreta que he comprobado
antes de responder.

Todavía no he contactado a John Simons y no tengo confirmado su correo actual.
¿Podría indicarme su dirección de contacto preferida? Gracias por señalar que
investigó esta cuestión; mantendré abierta la cuestión de la prioridad. También he
localizado su artículo de 2022 sobre m-nykels y estoy teniendo en cuenta ese
antecedente.

Tiene razón en que Rhin proporciona una cota más fuerte. Elegí inicialmente
LMN porque pude cotejar directamente su enunciado original y sus condiciones.
Ahora he obtenido el original de Rhin y cotejado la proposición (7), p. 160:
el exponente 13,3 vale para H ≥ 2 y coincide exactamente con la hipótesis
de la versión condicional en Lean que añadí. Manteniendo las mismas estimaciones
auxiliares, el corte de la cola para 83 rachas mejora de 2^76 a 2^68. Aun así,
la criba finita actual se detiene en 83 con cualquiera de las dos herramientas.

Siguiendo su sugerencia, utilicé el récord confirmado
46.645.791.847.966.786.687, cuyo tiempo clásico es 2480. La extensión con pesos
que mencioné en el correo anterior mejora de 81 a 83 rachas. El certificado
finito exacto y la prueba Lean ya pasaron las comprobaciones. También formalicé
el paso de una cota uniforme del tiempo total en ese intervalo a CST,
utilizando nuestro certificado de casos pequeños ya comprobado por el núcleo.

Sobre los axiomas: los resultados externos entran como hipótesis explícitas
del teorema. Las versiones finales suponen LMN o Rhin, junto con la cobertura
del intervalo de Roosendaal. Lean comprueba las deducciones y los certificados
finitos; no verifica ese cálculo exhaustivo externo ni demuestra la cota de
trascendencia. La auditoría sólo encuentra los axiomas estándar de Lean.

El código público está en la dirección indicada. La extensión comprobada de
83 rachas y su registro de auditoría están listos para compartir.

Gracias de nuevo: sus comentarios mejoraron tanto la cota como la precisión
de las hipótesis.

Saludos cordiales,
Omar Saïd
