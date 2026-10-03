import OcelotasFinito

/-! # Ocelotas: verificador finito por clases de residuos

El estado (r,m,a,c) representa n=r+m*t y T^[i] n=a*t+c,
con m=2^i y a=3^(S i n). Las ramas separan t par e impar.
Cuando queda una sola semilla se usa el verificador individual anterior.
El combustible agotado rechaza. No se presupone el resultado del censo.
-/

namespace OcelotasResiduos

open Ocelotas OcelotasFinito

def numerador (a x : ℕ) : ℕ := if x % 2 = 0 then a else 3 * a

theorem paso_afin (a c u : ℕ) :
    T (a * (2 * u) + c) = numerador a c * u + T c := by
  have hmod : (a * (2 * u) + c) % 2 = c % 2 := by
    have he : a * (2 * u) + c = 2 * (a * u) + c := by ring
    rw [he]
    omega
  unfold T numerador
  rw [hmod]
  split
  · have he : a * (2 * u) + c = c + (a * u) * 2 := by ring
    rw [he]
    omega
  · have he : 3 * (a * (2 * u) + c) + 1 =
        (3 * c + 1) + (3 * a * u) * 2 := by ring
    rw [he]
    omega

def comprobar (limite : ℕ) : ℕ → ℕ → ℕ → ℕ → ℕ → Bool
  | _, _, _, _, 0 => false
  | r, m, a, c, combustible + 1 =>
    if limite < r then true
    else if a < m then decide (c < r)
    else if limite < r + m then OcelotasFinito.comprobar r c a m (combustible + 1)
    else
      comprobar limite r (2 * m) (numerador a c) (T c) combustible &&
        comprobar limite (r + m) (2 * m) (numerador a (a + c)) (T (a + c)) combustible

theorem comprobar_correcto (limite combustible : ℕ) : ∀ n i r m a c t,
    n ≤ limite → n = r + m * t → T^[i] n = a * t + c →
    3 ^ S i n = a → 2 ^ i = m →
    (∀ j, j < i → 1 ≤ j → 2 ^ j ≤ 3 ^ S j n) →
    comprobar limite r m a c combustible = true →
    ∃ k, i ≤ k ∧ k < i + combustible ∧ PrimerCruce n k ∧ T^[k] n < n := by
  induction combustible with
  | zero => simp [comprobar]
  | succ combustible ih =>
    intro n i r m a c t hn hncl hx ha hm hpref hc
    simp only [comprobar] at hc
    split at hc
    next hvacio => omega
    next hvacio =>
      split at hc
      next hcruce =>
        have hdesc : c < r := of_decide_eq_true hc
        refine ⟨i, le_rfl, by omega, ⟨hpref, ?_⟩, ?_⟩
        · simpa only [ha, hm] using hcruce
        · rw [hx, hncl]
          nlinarith
      next hantes =>
        have hpref' : ∀ j, j < i + 1 → 1 ≤ j → 2 ^ j ≤ 3 ^ S j n := by
          intro j hj hj1
          by_cases hji : j < i
          · exact hpref j hji hj1
          · have he : j = i := by omega
            subst j
            omega
        split at hc
        next hsola =>
          have hmpos : 0 < m := by rw [← hm]; positivity
          have ht : t = 0 := by
            by_contra h
            have : 1 ≤ t := by omega
            nlinarith
          have hnr : n = r := by simpa only [ht, Nat.mul_zero, Nat.add_zero] using hncl
          have hxc : T^[i] n = c := by simpa only [ht, Nat.mul_zero, Nat.zero_add] using hx
          have hc' : OcelotasFinito.comprobar n (T^[i] n)
              (3 ^ S i n) (2 ^ i) (combustible + 1) = true := by
            rw [hxc, ha, hm, hnr]
            exact hc
          exact OcelotasFinito.comprobar_correcto n (combustible + 1) i hpref hc'
        next hvarias =>
          simp only [Bool.and_eq_true] at hc
          have hdes : t = 2 * (t / 2) + t % 2 := by omega
          have hm' : 2 ^ (i + 1) = 2 * m := by rw [pow_succ, hm]; omega
          have rama (b : ℕ) (hb : t % 2 = b)
              (hacepta : comprobar limite (r + m * b) (2 * m)
                (numerador a (a * b + c)) (T (a * b + c)) combustible = true) :
              ∃ k, i ≤ k ∧ k < i + (combustible + 1) ∧
                PrimerCruce n k ∧ T^[k] n < n := by
            have hte : t = 2 * (t / 2) + b := by omega
            have hn' : n = (r + m * b) + (2 * m) * (t / 2) := by
              calc
                n = r + m * t := hncl
                _ = (r + m * b) + (2 * m) * (t / 2) := by
                  conv_lhs => rw [hte]
                  ring
            have hx' : T^[i + 1] n =
                numerador a (a * b + c) * (t / 2) + T (a * b + c) := by
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
            obtain ⟨k, hik, hkc, hk, hd⟩ := ih n (i + 1) (r + m * b) (2 * m)
              (numerador a (a * b + c)) (T (a * b + c)) (t / 2)
              hn hn' hx' ha' hm' hpref' hacepta
            exact ⟨k, by omega, by omega, hk, hd⟩
          by_cases htpar : t % 2 = 0
          · apply rama 0 htpar
            simpa only [Nat.mul_zero, Nat.add_zero, Nat.zero_add] using hc.1
          · apply rama 1 (by omega)
            simpa only [Nat.mul_one] using hc.2

def intervalo (limite combustible : ℕ) : Bool := comprobar limite 2 1 1 2 combustible

/-- Ensamblaje de dos bloques ya certificados, sin evaluar de nuevo sus árboles. -/
theorem acepta_rama {limite r m a c combustible : ℕ}
    (hr : r ≤ limite) (ha : m ≤ a) (hm : r + m ≤ limite)
    (h0 : comprobar limite r (2 * m) (numerador a c) (T c) combustible = true)
    (h1 : comprobar limite (r + m) (2 * m) (numerador a (a + c))
      (T (a + c)) combustible = true) :
    comprobar limite r m a c (combustible + 1) = true := by
  rw [comprobar, if_neg (by omega), if_neg (by omega), if_neg (by omega)]
  rw [h0, h1]
  rfl

theorem intervalo_correcto {limite combustible : ℕ}
    (hc : intervalo limite combustible = true) {n : ℕ}
    (hn : 2 ≤ n) (hmax : n ≤ limite) :
    ∃ k, k < combustible ∧ PrimerCruce n k ∧ T^[k] n < n := by
  have h := comprobar_correcto limite combustible n 0 2 1 1 2 (n - 2)
    hmax (by omega) (by simp; omega) (by simp [S]) (by simp) (by omega) hc
  obtain ⟨k, _, hkc, hk, hd⟩ := h
  exact ⟨k, by omega, hk, hd⟩

end OcelotasResiduos

#print axioms OcelotasResiduos.paso_afin
#print axioms OcelotasResiduos.comprobar_correcto
#print axioms OcelotasResiduos.intervalo_correcto
#print axioms OcelotasResiduos.acepta_rama
