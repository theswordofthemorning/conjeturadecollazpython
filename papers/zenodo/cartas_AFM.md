# Cartas para el envío a Annals of Formalized Mathematics

Preparadas y **enviadas el 27-09-2026** (21:17–21:28 EDT), en el campo
*Comment* del formulario de Episciences, una por artículo. Se enviaron con
un cambio: las cartas II y III citan además los números de envío anteriores
(«submitted to AFM as #19502», «#19502 and #19503»). Envíos: #19502 (I),
#19503 (II) y #19504 (III). En la lista de editores se marcaron Kontorovich
y Gouëzel.

Editor sugerido: **Alex Kontorovich**, del comité editorial de AFM. Escribió
con Lagarias sobre modelos estocásticos del problema 3x+1 (*The Ultimate
Challenge*, 2010) y trabaja con Lean. Alternativa: **Sébastien Gouëzel**
(probabilidad y sistemas dinámicos, colaborador de Mathlib).

Datos del formulario: Repository = Zenodo; Version = 1; Document identifier:

| Artículo | Identificador |
|---|---|
| I (Gao) | `10.5281/zenodo.23003524` |
| II (Garner) | `10.5281/zenodo.23003526` |
| III (Wu) | `10.5281/zenodo.23003528` |

Software que se enlaza en la segunda fase: `10.5281/zenodo.23003500`.

---

## Artículo I

Dear Editors,

I submit the manuscript "Consecutive integers coalesce with density one
under the Collatz map: a formally verified proof of a conjecture of Gao"
(Zenodo, doi:10.5281/zenodo.23003524).

Gao (Discrete Math. 112, 1993) introduced the coalescence of consecutive
integers n and n+1 under the Collatz map, proved that his normalized count
d̄_k is nondecreasing, computed d̄_24 ≈ 0.389 and conjectured that d̄_k → 1.
Lagarias's annotated bibliography (entry 68) records the conjecture in the
form "the set of n with C^k(n) = C^k(n+1) for some k ≤ log_2 n has natural
density one". The paper proves both forms, and also that Gao's proportion
d(x) tends to 1. I have not found a proof of either form in the literature.

The whole proof is formalized in Lean 4 with Mathlib. The artifact
(doi:10.5281/zenodo.23003500, Apache License 2.0) builds with
`lake build GaoCore GaoFormal`; the final theorems
GaoEnunciado.conjetura_gao and GaoLiteral.conjetura_gao_literal depend only
on propext, Classical.choice and Quot.sound, and leanchecker replays all 30
modules. The statements a referee has to audit are short and
self-contained, and Section 6 of the paper explains what the formalization
certifies and what it does not. The results concern coalescence only: they
say nothing about the 3x+1 conjecture itself.

This is the first of three related submissions. The two companion papers
deduce from this result Garner's conjecture (1985) on arbitrarily long runs
of consecutive integers of the same height (doi:10.5281/zenodo.23003526) and
the second conjecture of Wu (1992) (doi:10.5281/zenodo.23003528); the three
papers share the same artifact. If the editors prefer, they can be merged
into a single article.

I would suggest Alex Kontorovich as handling editor, given his work on
stochastic models for the 3x+1 problem; Sébastien Gouëzel would also be well
placed for the probabilistic part of the argument.

The formalization and the first draft of the text were produced with
extensive assistance from AI models of Anthropic's Claude family, as
declared in the paper; every result is checked by the Lean kernel. I have no
conflict of interest and no funding to declare, and the manuscript has not
been submitted elsewhere.

Sincerely,
Omar Javier Said Duran
Independent Researcher, ORCID 0009-0009-1418-2558

---

## Artículo II

Dear Editors,

I submit "Arbitrarily long runs of consecutive integers with the same
Collatz height" (Zenodo, doi:10.5281/zenodo.23003526), the second of three
related submissions.

Garner (Discrete Math. 55, 1985) conjectured that there are arbitrarily long
runs of consecutive integers with the same Collatz height; Gao (1993)
recalled the conjecture with the same height and the same total stopping
time, and attributed it also to Penning. The paper proves this stronger
form: for all L and N there is n ≥ N such that n, …, n+L have the same
height and the same total stopping time. In particular, every term of the
OEIS sequence A078441 exists. The proof combines the main theorem of the
companion paper on Gao's conjecture (doi:10.5281/zenodo.23003524) with
Terras's formula and the fact that 2 is a primitive root modulo every power
of 3.

The result is formalized in Lean 4 with Mathlib
(GarnerEnunciado.conjetura_garner, in the artifact
doi:10.5281/zenodo.23003500), using only the standard axioms. The statement
uses Gao's definitions of height and total stopping time and fits in a few
lines.

Since this paper depends on the first one, it may be convenient to handle
both together; the papers can also be merged if the editors prefer. The
use of AI tools is declared in the paper, and every result is checked by the
Lean kernel. I have no conflict of interest and no funding to declare, and
the manuscript has not been submitted elsewhere.

Sincerely,
Omar Javier Said Duran
Independent Researcher, ORCID 0009-0009-1418-2558

---

## Artículo III

Dear Editors,

I submit "On two conjectures of Wu on consecutive integers of the same
height in the Collatz problem" (Zenodo, doi:10.5281/zenodo.23003528), the
third of three related submissions.

Wu (J. Huazhong Univ. Sci. Tech. 20, 1992) proposed two conjectures on
consecutive integers of the same height. The paper proves the second, that
the longest run of equal height in [1, M) tends to infinity, and shows that
the first, that the proportion of integers lying in runs tends to 1, is
equivalent to the statement that the integers reaching 1 have natural
density one, which is open. Both results are formalized in Lean 4
(WuEnunciado.conjetura_wu_dos and WuEnunciado.conjetura_wu_uno, in the
artifact doi:10.5281/zenodo.23003500).

The paper states one caveat openly: I could not obtain the printed article
of Wu, and the two conjectures were read through the AI reading assistant of
the CNKI database, which quotes them from the full text. The English
abstract (zbMATH, Lagarias's bibliography) confirms that two conjectures are
proposed, and the figures quoted by the assistant agree with my
computations.

This paper depends on the two companion papers; it may be convenient to
handle the three together, or to merge them if the editors prefer. The use
of AI tools is declared in the paper, and every result is checked by the
Lean kernel. I have no conflict of interest and no funding to declare, and
the manuscript has not been submitted elsewhere.

Sincerely,
Omar Javier Said Duran
Independent Researcher, ORCID 0009-0009-1418-2558
