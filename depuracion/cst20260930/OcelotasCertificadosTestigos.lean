import OcelotasPrefijosTestigos

/-! # Certificados de prefijos que proporcionan el motivo de cada hoja

El árbol sólo propone dónde cortar y qué exponente B utilizar.
El verificador comprueba cada condición con enteros exactos. La aceptación
implica la del verificador binario, para el mismo estado y combustible.
-/

namespace OcelotasCertificadosTestigos

open Ocelotas OcelotasContador OcelotasPrefijosTestigos
open OcelotasResiduos (numerador)
open OcelotasCribaPrefijosBinarios (incremento)

inductive Testigo where
  | vacio
  | descenso
  | exceso
  | criba (B : ℕ)
  | rama (izquierda derecha : Testigo)

def verificar (limite qmin R : ℕ) :
    ℕ → ℕ → ℕ → ℕ → ℕ → ℕ → Bool → ℕ → Testigo → Bool
  | _, _, _, _, _, _, _, 0, _ => false
  | r, m, a, c, q, s, anterior, combustible + 1, testigo =>
    match testigo with
    | .vacio => decide (limite < r)
    | .descenso => decide (a < m ∧ c < r)
    | .exceso => decide (m ≤ a ∧ R < s)
    | .criba B => decide (m ≤ a ∧ anterior = false ∧
        (a * ((limite - r) / m) + c + 1) ^ 256 ≤ 2 ^ B ∧
        q + OcelotasPrefijosAfinados.cota B (R - s) < qmin)
    | .rama izquierda derecha => decide (m ≤ a) &&
        (verificar limite qmin R r (2 * m) (numerador a c) (T c)
          (q + c % 2) (s + incremento c anterior) (decide (c % 2 = 1))
          combustible izquierda &&
        verificar limite qmin R (r + m) (2 * m) (numerador a (a + c)) (T (a + c))
          (q + (a + c) % 2) (s + incremento (a + c) anterior)
          (decide ((a + c) % 2 = 1)) combustible derecha)

theorem verificar_correcto (limite qmin R combustible : ℕ) :
    ∀ testigo r m a c q s anterior,
    verificar limite qmin R r m a c q s anterior combustible testigo = true →
    OcelotasCribaPrefijosBinarios.comprobar limite qmin R r m a c q s anterior combustible = true := by
  induction combustible with
  | zero => intros; contradiction
  | succ combustible ih =>
    intro testigo r m a c q s anterior h
    cases testigo with
    | vacio => exact acepta_vacio (of_decide_eq_true h)
    | descenso =>
      have hh : a < m ∧ c < r := of_decide_eq_true h
      exact acepta_descenso hh.1 hh.2
    | exceso =>
      have hh : m ≤ a ∧ R < s := of_decide_eq_true h
      exact acepta_exceso hh.1 hh.2
    | criba B =>
      have hh : m ≤ a ∧ anterior = false ∧
          (a * ((limite - r) / m) + c + 1) ^ 256 ≤ 2 ^ B ∧
          q + OcelotasPrefijosAfinados.cota B (R - s) < qmin := of_decide_eq_true h
      exact acepta_criba hh.1 hh.2.1 hh.2.2.1 hh.2.2.2
    | rama izquierda derecha =>
      simp only [verificar, Bool.and_eq_true] at h
      exact acepta_rama (of_decide_eq_true h.1)
        (ih _ _ _ _ _ _ _ _ h.2.1) (ih _ _ _ _ _ _ _ _ h.2.2)

theorem descenso {inicio limite qmin R combustible : ℕ} {testigo : Testigo}
    (hc : verificar limite qmin R inicio 1 1 inicio 0 0 false combustible testigo = true)
    {n k : ℕ} (hinicio : inicio ≤ n) (hn : n ≤ limite)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ R) (hq : qmin ≤ S k n) : T^[k] n < n :=
  OcelotasCribaPrefijosBinarios.certificado_descenso
    (verificar_correcto limite qmin R combustible testigo inicio 1 1 inicio 0 0 false hc)
    hinicio hn hk hr hq

end OcelotasCertificadosTestigos

#print axioms OcelotasCertificadosTestigos.verificar_correcto
#print axioms OcelotasCertificadosTestigos.descenso
