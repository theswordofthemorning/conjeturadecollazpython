import OcelotasPrefijosAfinados

/-! # Ocelotas: cota del logaritmo mediante ocho bisecciones

Primero se acota log2(s), cuyo argumento tiene unas 67 cifras binarias
en la ventana de 76. Después se busca un exponente para s^256 en un
intervalo de anchura 256. Cada bisección conserva una cota superior;
incluso un combustible insuficiente produce una cota válida.
-/

namespace OcelotasPrefijosBinarios

open Real Ocelotas OcelotasTrayectorias OcelotasContador

def buscar (x : ℕ) : ℕ → ℕ → ℕ → ℕ
  | _, superior, 0 => superior
  | inferior, superior, combustible + 1 =>
    let medio := (inferior + superior) / 2
    if x ≤ 2 ^ medio then buscar x inferior medio combustible
    else buscar x medio superior combustible

theorem buscar_cota (x combustible inferior superior : ℕ)
    (h : x ≤ 2 ^ superior) :
    x ≤ 2 ^ buscar x inferior superior combustible := by
  induction combustible generalizing inferior superior with
  | zero => exact h
  | succ combustible ih =>
    simp only [buscar]
    split
    next hm => exact ih _ _ hm
    next hm => exact ih _ _ h

def exponente (s : ℕ) : ℕ :=
  if s ≤ 1 then 0
  else
    let inferior := 256 * s.log2
    if s ^ 256 ≤ 2 ^ inferior then inferior
    else buscar (s ^ 256) inferior (inferior + 256) 8

theorem potencia_exponente (s : ℕ) : s ^ 256 ≤ 2 ^ exponente s := by
  by_cases hs : s ≤ 1
  · rcases (show s = 0 ∨ s = 1 by omega) with hz | hu
    · simp [hz, exponente]
    · simp [hu, exponente]
  · simp only [exponente, if_neg hs]
    split
    next hinf => exact hinf
    next hinf =>
      apply buscar_cota
      have hc : s ≤ 2 ^ (s.log2 + 1) := Nat.le_of_lt Nat.lt_log2_self
      have hp := Nat.pow_le_pow_left hc 256
      have he : (s.log2 + 1) * 256 = 256 * s.log2 + 256 := by omega
      simpa only [← pow_mul, he] using hp

theorem criba_despues_corte {n k i R maximo : ℕ}
    (hk : PrimerCruce n k) (hi : i < k)
    (hcorte : i = 0 ∨ T^[i - 1] n % 2 = 0) (hr : rachas n k ≤ R)
    (hvalor : T^[i] n ≤ maximo) :
    S k n ≤ S i n + OcelotasPrefijosAfinados.cota
      (exponente (maximo + 1)) (R - rachas n i) := by
  have hbeta := OcelotasTreceBase.beta_de_potencia (by omega : 0 < maximo + 1)
    (potencia_exponente (maximo + 1))
  have hc := OcelotasPrefijosAfinados.criba_real_despues_corte hk hi hcorte hr
    (by omega : 0 < maximo + 1) (by omega : T^[i] n + 1 ≤ maximo + 1)
    (by norm_num : (1 : ℝ) ≤ 1585 / 1000)
    (by positivity : (0 : ℝ) ≤ (exponente (maximo + 1) : ℝ) / 256)
    OcelotasTreceBase.alfa_valida hbeta
  simpa only [OcelotasPrefijosAfinados.cota_real] using hc

end OcelotasPrefijosBinarios

#print axioms OcelotasPrefijosBinarios.buscar_cota
#print axioms OcelotasPrefijosBinarios.potencia_exponente
#print axioms OcelotasPrefijosBinarios.criba_despues_corte
