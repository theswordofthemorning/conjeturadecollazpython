# Borrador para el Zulip de Lean

29-09-2026. Autorizado por el usuario («si también puedes hablar a los de
Zulip, qué más da»). Su cuenta en Zulip: **ZeroSorry**; Zulip muestra su nombre
completo.

**Publicado el 29-09-2026 a las 18:45 (hora local)**, por orden del usuario
(«publica el mensaje en zulip»), en #Machine Learning for Theorem Proving,
tema «Gao's 1993 Collatz coalescence conjecture, formalized»: [mensaje](https://leanprover.zulipchat.com/#narrow/channel/219941-Machine-Learning-for-Theorem-Proving/topic/Gao.27s.201993.20Collatz.20coalescence.20conjecture.2C.20formalized/with/627912094).
El texto publicado es el de abajo, con dos cambios: el título se acortó (Zulip
admite 60 caracteres) y se añadió la línea «Its CI passes `lake comparator`, and
it has just been submitted to Palomar.»

**Borrado a los cinco minutos.** A las 18:50 la moderación borró el mensaje
y suspendió la cuenta un día. Las normas de la comunidad Lean no permiten
usar IA para escribir mensajes en Zulip ni en GitHub, ni siquiera en parte;
una nueva falta duplica la suspensión. El aviso llegó por correo y no quedó
registrado aquí hasta el 04-10 ([correos](../CORREOS_20261004.md)). **No volver a publicar
allí texto redactado ni traducido por IA**: si el usuario escribe, ha de ser
con sus propias palabras.

- Canal propuesto: **#Machine Learning for Theorem Proving**, donde se
  discuten las formalizaciones hechas con IA. Las dudas sobre el envío van
  al canal #Palomar.
- Cuándo: con el CI de `gao-palomar` en verde, para que el enlace lleve a un
  repositorio comprobado. Si Qeios ya lo publicó, añadir su enlace.
- Una sola publicación; responder a lo que digan sólo con autorización.

---

**Tema:** Gao's 1993 conjecture on Collatz coalescence, formalized: are the statements right?

Hi all. I'm an independent researcher. With extensive help from Claude (Anthropic), I built a Lean 4 + Mathlib development that claims to prove a conjecture of G.-G. Gao (Discrete Math. 112, 1993) on the Collatz map, in Gao's own form and in the form recorded in Lagarias's annotated bibliography (entry 68). It is **not** a claim about the 3x+1 conjecture: the trajectories of n and n+1 may meet without reaching 1.

Repository, prepared for Palomar (Lean v4.35.0-rc2): https://github.com/theswordofthemorning/gao-palomar

The part where expert eyes would help most is small: [`Challenge.lean`](https://github.com/theswordofthemorning/gao-palomar/blob/main/Challenge.lean), about 100 lines importing only Mathlib. The Lagarias form reads:

```lean
def collatz (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else 3 * n + 1

theorem lagarias_form :
    Tendsto (fun N : ℕ => (((Finset.range N).filter
      (fun m => ∃ k, k ≤ Nat.log 2 m ∧ collatz^[k] m = collatz^[k] (m + 1))).card : ℝ) / N)
      atTop (𝓝 1)
```

and `gao_form` states Gao's `d̄_k → 1` (and `d(x) → 1`) with his stricter notion of coalescence (same number of halvings, 1 never visited). Both depend only on `propext`, `Classical.choice` and `Quot.sound`.

Concretely:
1. Do these statements say what Gao conjectured, with no hidden triviality?
2. Would anyone be willing to try to break the development?

Paper (v1): https://doi.org/10.5281/zenodo.23003524. Negative answers are the most useful ones. Thanks!
