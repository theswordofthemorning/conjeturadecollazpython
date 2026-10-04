import OcelotasPrefijos
import OcelotasPrefijosBinarios
import OcelotasResiduos
import OcelotasSueloContador

/-! # Ocelotas: verificador por residuos con suelo 4095

La aceptación excluye un fallo con q>=qmin y a lo sumo R rachas.
El estado conserva el prefijo real, su número de impares y sus rachas.
Sólo se reinicia la criba después de una entrada par o en el prefijo vacío.
El suelo se exige a la semilla inicial. El primer cruce lo conserva en el prefijo.
Conserva los verificadores anteriores como implementaciones independientes.
-/

namespace OcelotasCribaPrefijosSuelo

open Ocelotas OcelotasRachas OcelotasTrayectorias OcelotasContador
  OcelotasFinito OcelotasResiduos OcelotasPrefijos

def incremento (x : ℕ) (anterior : Bool) : ℕ :=
  if x % 2 = 1 ∧ anterior = false then 1 else 0

def comprobar (limite qmin R : ℕ) :
    ℕ → ℕ → ℕ → ℕ → ℕ → ℕ → Bool → ℕ → Bool
  | _, _, _, _, _, _, _, 0 => false
  | r, m, a, c, q, s, anterior, combustible + 1 =>
    if limite < r then true
    else if a < m then decide (c < r)
    else if R < s then true
    else if anterior = false ∧
        512 ≤ OcelotasPrefijosBinarios.exponente (a * ((limite - r) / m) + c + 1) ∧
        q + OcelotasSueloNumerica.cota
          (OcelotasPrefijosBinarios.exponente (a * ((limite - r) / m) + c + 1)) (R - s) < qmin
      then true
    else
      comprobar limite qmin R r (2 * m) (numerador a c) (T c)
        (q + c % 2) (s + incremento c anterior) (decide (c % 2 = 1)) combustible &&
      comprobar limite qmin R (r + m) (2 * m) (numerador a (a + c)) (T (a + c))
        (q + (a + c) % 2) (s + incremento (a + c) anterior)
        (decide ((a + c) % 2 = 1)) combustible

theorem comprobar_correcto (limite qmin R combustible : ℕ) :
    ∀ n k i r m a c q s anterior t,
    4095 ≤ n → PrimerCruce n k → n ≤ T^[k] n → rachas n k ≤ R → qmin ≤ S k n →
    n ≤ limite → i ≤ k → n = r + m * t → T^[i] n = a * t + c →
    3 ^ S i n = a → 2 ^ i = m → S i n = q → rachas n i = s →
    (anterior = false ↔ i = 0 ∨ T^[i - 1] n % 2 = 0) →
    comprobar limite qmin R r m a c q s anterior combustible = true → False := by
  induction combustible with
  | zero => simp [comprobar]
  | succ combustible ih =>
    intro n k i r m a c q s anterior t hsuelo hk hf hr hqmin hn hi hncl hx ha hm hq hs hprev hc
    simp only [comprobar] at hc
    split at hc
    next hvacio => omega
    next hvacio =>
      split at hc
      next hcruce =>
        have hdesc : c < r := of_decide_eq_true hc
        have he : i = k := by
          by_contra hne
          have hp := pre_cruce hk (by omega : i < k)
          rw [ha, hm] at hp
          omega
        rw [← he, hx, hncl] at hf
        nlinarith
      next hantes =>
        have hki : i < k := by
          by_contra hne
          have he : i = k := by omega
          have hp := hk.2
          rw [← he, ha, hm] at hp
          omega
        split at hc
        next hdemasiadas =>
          have hmono := rachas_monotonas n hi
          rw [hs] at hmono
          omega
        next hsR =>
          split at hc
          next hcriba =>
            have hmpos : 0 < m := by rw [← hm]; positivity
            have ht : t ≤ (limite - r) / m := by
              apply (Nat.le_div_iff_mul_le hmpos).2
              have hsub : limite - r + r = limite := Nat.sub_add_cancel (by omega)
              nlinarith
            have hmax : T^[i] n ≤ a * ((limite - r) / m) + c := by
              rw [hx]
              exact Nat.add_le_add_right (Nat.mul_le_mul_left a ht) c
            have hbound := OcelotasSueloContador.criba_desde_potencia
              hk hki hsuelo (hprev.mp hcriba.1) hr hmax hcriba.2.1
              (OcelotasPrefijosBinarios.potencia_exponente _)
            rw [hq, hs] at hbound
            omega
          next hnoc =>
            simp only [Bool.and_eq_true] at hc
            have hm' : 2 ^ (i + 1) = 2 * m := by rw [pow_succ, hm]; omega
            have rama (b : ℕ) (hb : t % 2 = b)
                (hacepta : comprobar limite qmin R (r + m * b) (2 * m)
                  (numerador a (a * b + c)) (T (a * b + c))
                  (q + (a * b + c) % 2) (s + incremento (a * b + c) anterior)
                  (decide ((a * b + c) % 2 = 1)) combustible = true) : False := by
              have hte : t = 2 * (t / 2) + b := by omega
              have hn' : n = (r + m * b) + (2 * m) * (t / 2) := by
                calc
                  n = r + m * t := hncl
                  _ = _ := by
                    conv_lhs => rw [hte]
                    ring
              have hx' : T^[i + 1] n = numerador a (a * b + c) * (t / 2) + T (a * b + c) := by
                rw [Function.iterate_succ_apply', hx]
                conv_lhs => rw [hte]
                have he : a * (2 * (t / 2) + b) + c =
                    a * (2 * (t / 2)) + (a * b + c) := by ring
                rw [he, paso_afin]
              have hmod : (T^[i] n) % 2 = (a * b + c) % 2 := by
                rw [hx, hte]
                have he : a * (2 * (t / 2) + b) + c =
                    2 * (a * (t / 2)) + (a * b + c) := by ring
                rw [he]
                omega
              have ha' : 3 ^ S (i + 1) n = numerador a (a * b + c) := by
                rw [numerador_siguiente, hmod, ha]
                rfl
              have hq' : S (i + 1) n = q + (a * b + c) % 2 := by
                rw [S_add]
                simp only [S, Nat.add_zero, hq, hmod]
              have hs' : rachas n (i + 1) = s + incremento (a * b + c) anterior := by
                simp only [rachas, hs, hmod, incremento, ← hprev]
              have hp' : (decide ((a * b + c) % 2 = 1) = false ↔
                  i + 1 = 0 ∨ T^[i + 1 - 1] n % 2 = 0) := by
                simp only [Nat.add_sub_cancel, show i + 1 ≠ 0 by omega, false_or, hmod]
                by_cases hxpar : (a * b + c) % 2 = 0
                · simp [hxpar]
                · have hxi : (a * b + c) % 2 = 1 := by omega
                  simp [hxi]
              exact ih n k (i + 1) (r + m * b) (2 * m)
                (numerador a (a * b + c)) (T (a * b + c))
                (q + (a * b + c) % 2) (s + incremento (a * b + c) anterior)
                (decide ((a * b + c) % 2 = 1)) (t / 2)
                hsuelo hk hf hr hqmin hn (by omega) hn' hx' ha' hm' hq' hs' hp' hacepta
            by_cases htpar : t % 2 = 0
            · apply rama 0 htpar
              simpa only [Nat.mul_zero, Nat.add_zero, Nat.zero_add] using hc.1
            · apply rama 1 (by omega)
              simpa only [Nat.mul_one] using hc.2

theorem certificado_descenso {inicio limite qmin R combustible : ℕ}
    (hsuelo : 4095 ≤ inicio)
    (hc : comprobar limite qmin R inicio 1 1 inicio 0 0 false combustible = true)
    {n k : ℕ} (hinicio : inicio ≤ n) (hn : n ≤ limite)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ R) (hq : qmin ≤ S k n) : T^[k] n < n := by
  by_contra hf
  exact comprobar_correcto limite qmin R combustible n k 0 inicio 1 1 inicio 0 0 false
    (n - inicio) (by omega) hk (by omega) hr hq hn (by omega) (by omega) (by simp; omega)
    (by simp [S]) (by simp) (by simp [S]) (by simp [rachas]) (by simp) hc

end OcelotasCribaPrefijosSuelo

#print axioms OcelotasCribaPrefijosSuelo.comprobar_correcto
#print axioms OcelotasCribaPrefijosSuelo.certificado_descenso
