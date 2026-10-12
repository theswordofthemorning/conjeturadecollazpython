import PerdicesCancelaciones

/-! # Perdices: repeticiones, representantes y complejidad de la palabra.

Dos instantes de una misma órbita cuyas `m` paridades siguientes coinciden tienen
valores congruentes módulo `2^m` (`CasaRetrato.misma_paridad_congruentes`). Si los
valores son distintos, el mayor alcanza `2^m`. Con `x_t+1 <= (3/2)^(S_t) (n+1)`,
eso acota cada repetición temprana y obliga a toda órbita inyectiva a tener más
de `m+1` factores distintos de largo `m`. No se supone ninguna ley aleatoria.
-/

namespace PerdicesComplejidad

open Ocelotas CasaPlano CasaRetrato

/-- Factor de paridades de largo `m` que empieza en el instante `t` de la órbita de `n`. -/
def factor (n m t : ℕ) : Fin m → ℕ := fun k => T^[t + k] n % 2

/-- Un paso: `x+1` se multiplica por `3/2` si `x` es impar y no crece si es par. -/
theorem paso_uno (x : ℕ) : 2 ^ (x % 2) * (T x + 1) ≤ 3 ^ (x % 2) * (x + 1) := by
  unfold T
  rcases Nat.mod_two_eq_zero_or_one x with h | h
  · rw [if_pos h, h]
    omega
  · rw [if_neg (by omega), h]
    omega

/-- `x_k+1 <= (3/2)^(S_k) (n+1)`, en forma entera. -/
theorem cota_impares (k n : ℕ) : 2 ^ S k n * (T^[k] n + 1) ≤ 3 ^ S k n * (n + 1) := by
  induction k generalizing n with
  | zero => simp [S]
  | succ k ih =>
    have h1 := ih (T n)
    have h2 := paso_uno n
    rw [S, iterT_succ, pow_add, pow_add]
    calc 2 ^ (n % 2) * 2 ^ S k (T n) * (T^[k] (T n) + 1)
        = 2 ^ (n % 2) * (2 ^ S k (T n) * (T^[k] (T n) + 1)) := by ring
      _ ≤ 2 ^ (n % 2) * (3 ^ S k (T n) * (T n + 1)) := Nat.mul_le_mul_left _ h1
      _ = 3 ^ S k (T n) * (2 ^ (n % 2) * (T n + 1)) := by ring
      _ ≤ 3 ^ S k (T n) * (3 ^ (n % 2) * (n + 1)) := Nat.mul_le_mul_left _ h2
      _ = 3 ^ (n % 2) * 3 ^ S k (T n) * (n + 1) := by ring

/-- Dos naturales distintos y congruentes módulo `2^m` distan al menos `2^m`. -/
theorem separacion {a b m : ℕ} (hc : a % 2 ^ m = b % 2 ^ m) (hab : a < b) :
    2 ^ m ≤ b - a := by
  have hd : 2 ^ m ∣ b - a := (Nat.modEq_iff_dvd' hab.le).mp hc
  exact Nat.le_of_dvd (by omega) hd

/-- Misma paridad en `m` pasos desde `y` y desde `z`: congruencia módulo `2^m`. -/
theorem repeticion_congruente {y z m : ℕ}
    (hp : ∀ i, i < m → T^[i] y % 2 = T^[i] z % 2) : y % 2 ^ m = z % 2 ^ m :=
  misma_paridad_congruentes m y z hp

/-- Ley local. Si las `m` paridades que siguen a `y` y a `z = T^[d] y` coinciden y
`z ≠ y`, entonces `2^(m+s) < 3^s (y+1)`, con `s = S d y` impares entre ambos. -/
theorem ley_local {y d m : ℕ} (hne : T^[d] y ≠ y)
    (hp : ∀ i, i < m → T^[i] y % 2 = T^[i] (T^[d] y) % 2) :
    2 ^ (m + S d y) < 3 ^ S d y * (y + 1) := by
  have hc := repeticion_congruente hp
  have hcota := cota_impares d y
  have h23 : 2 ^ S d y ≤ 3 ^ S d y := Nat.pow_le_pow_left (by decide) _
  have h3 : 0 < 3 ^ S d y := by positivity
  rw [pow_add]
  rcases lt_or_gt_of_ne hne with h | h
  · -- el valor posterior es menor: `2^m <= y - z <= y`
    have hs := separacion hc.symm h
    have hm : 2 ^ m ≤ y := le_trans hs (Nat.sub_le _ _)
    calc 2 ^ m * 2 ^ S d y ≤ y * 3 ^ S d y := Nat.mul_le_mul hm h23
      _ < 3 ^ S d y * (y + 1) := by nlinarith
  · -- el valor posterior es mayor: `2^m <= z - y < z+1`
    have hs := separacion hc h
    have hm : 2 ^ m < T^[d] y + 1 := by omega
    calc 2 ^ m * 2 ^ S d y < (T^[d] y + 1) * 2 ^ S d y :=
          Nat.mul_lt_mul_of_pos_right hm (by positivity)
      _ = 2 ^ S d y * (T^[d] y + 1) := by ring
      _ ≤ 3 ^ S d y * (y + 1) := hcota

/-- Ley global: la misma repetición, medida desde la semilla `n`. -/
theorem ley_global {n i d m : ℕ} (hne : T^[i + d] n ≠ T^[i] n)
    (hp : ∀ k, k < m → T^[i + k] n % 2 = T^[i + d + k] n % 2) :
    2 ^ (m + S (i + d) n) < 3 ^ S (i + d) n * (n + 1) := by
  set y := T^[i] n with hy
  have hz : T^[i + d] n = T^[d] y := by
    rw [hy, ← Function.iterate_add_apply, Nat.add_comm d i]
  have hloc : 2 ^ (m + S d y) < 3 ^ S d y * (y + 1) := by
    apply ley_local (by rwa [← hz])
    intro k hk
    have h := hp k hk
    have e1 : T^[i + k] n = T^[k] y := by
      rw [hy, ← Function.iterate_add_apply, Nat.add_comm k i]
    have e2 : T^[i + d + k] n = T^[k] (T^[d] y) := by
      rw [← hz, ← Function.iterate_add_apply, Nat.add_comm k (i + d)]
    rwa [e1, e2] at h
  have hini := cota_impares i n
  rw [← hy] at hini
  rw [S_add, ← hy]
  have hpos : 0 < 2 ^ S i n := by positivity
  calc 2 ^ (m + (S i n + S d y)) = 2 ^ (m + S d y) * 2 ^ S i n := by
        rw [← pow_add]; congr 1; omega
    _ < 3 ^ S d y * (y + 1) * 2 ^ S i n := Nat.mul_lt_mul_of_pos_right hloc hpos
    _ = 3 ^ S d y * (2 ^ S i n * (y + 1)) := by ring
    _ ≤ 3 ^ S d y * (3 ^ S i n * (n + 1)) := Nat.mul_le_mul_left _ hini
    _ = 3 ^ (S i n + S d y) * (n + 1) := by rw [pow_add]; ring

/-- Un tramo expansivo no cierra un ciclo natural: sin hipótesis de inyectividad. -/
theorem tramo_expansivo_no_cierra {y d : ℕ} (hy : 1 ≤ y) (hd : 1 ≤ d)
    (hexp : 2 ^ d ≤ 3 ^ S d y) : T^[d] y ≠ y := by
  intro hc
  have := ciclo_cruza hy hd hc
  omega

/-- Ley expansiva: si el tramo entre las dos apariciones es expansivo, la cota local
vale para todo natural `y >= 1`, sin suponer que su órbita sea inyectiva. -/
theorem ley_expansiva {y d m : ℕ} (hy : 1 ≤ y) (hd : 1 ≤ d)
    (hexp : 2 ^ d ≤ 3 ^ S d y)
    (hp : ∀ i, i < m → T^[i] y % 2 = T^[i] (T^[d] y) % 2) :
    2 ^ (m + S d y) < 3 ^ S d y * (y + 1) :=
  ley_local (tramo_expansivo_no_cierra hy hd hexp) hp

/-- Representantes: todo natural `n >= 1` que realiza una repetición de largo `m` con
segunda aparición en `j = i+d`, separada por un tramo expansivo, cumple
`2^(m + S_j) < 3^(S_j) (n+1)`. No se supone inyectividad. -/
theorem representante_crece {n i d m : ℕ} (hn : 1 ≤ n) (hd : 1 ≤ d)
    (hexp : 2 ^ d ≤ 3 ^ S d (T^[i] n))
    (hp : ∀ k, k < m → T^[i + k] n % 2 = T^[i + d + k] n % 2) :
    2 ^ (m + S (i + d) n) < 3 ^ S (i + d) n * (n + 1) := by
  apply ley_global _ hp
  have hz : T^[i + d] n = T^[d] (T^[i] n) := by
    rw [← Function.iterate_add_apply, Nat.add_comm d i]
  rw [hz]
  exact tramo_expansivo_no_cierra (iter_pos hn i) hd hexp

/-- En una órbita inyectiva, dos instantes con valores menores que `2^m` y el mismo
factor de largo `m` coinciden. -/
theorem factores_distintos {n m t t' : ℕ} (hi : Function.Injective (fun j => T^[j] n))
    (ht : T^[t] n < 2 ^ m) (ht' : T^[t'] n < 2 ^ m)
    (hf : factor n m t = factor n m t') : t = t' := by
  have hp : ∀ k, k < m → T^[k] (T^[t] n) % 2 = T^[k] (T^[t'] n) % 2 := by
    intro k hk
    have h := congrFun hf ⟨k, hk⟩
    simp only [factor] at h
    rwa [show t + k = k + t by omega, show t' + k = k + t' by omega,
      Function.iterate_add_apply, Function.iterate_add_apply] at h
  have hc := repeticion_congruente hp
  rw [Nat.mod_eq_of_lt ht, Nat.mod_eq_of_lt ht'] at hc
  exact hi hc

/-- Cota de complejidad: entre los `K` primeros instantes, hay al menos tantos factores
distintos de largo `m` como valores de la órbita menores que `2^m`. -/
theorem complejidad_cota {n : ℕ} (hi : Function.Injective (fun j => T^[j] n)) (m K : ℕ) :
    ((Finset.range K).filter (fun t => T^[t] n < 2 ^ m)).card ≤
      ((Finset.range K).image (factor n m)).card := by
  rw [← Finset.card_image_of_injOn (f := factor n m)]
  · exact Finset.card_le_card (Finset.image_subset_image (Finset.filter_subset _ _))
  · intro t ht t' ht' h
    simp only [Finset.coe_filter, Set.mem_setOf_eq] at ht ht'
    exact factores_distintos hi ht.2 ht'.2 h

/-- Antes de `K` pasos la órbita sigue bajo `2^m` si `3^K (n+1) <= 2^(m+K)`. -/
theorem bajo_umbral {n m K t : ℕ} (ht : t ≤ K) (h : 3 ^ K * (n + 1) ≤ 2 ^ (m + K)) :
    T^[t] n < 2 ^ m := by
  have hc := cota_impares t n
  have hs : S t n ≤ t := PerdicesEstela.S_le_pasos t n
  set s := S t n
  have hsK : s ≤ K := le_trans hs ht
  obtain ⟨r, hr⟩ : ∃ r, K = s + r := ⟨K - s, by omega⟩
  have h23 : 2 ^ r ≤ 3 ^ r := Nat.pow_le_pow_left (by decide) _
  have key : 2 ^ K * (T^[t] n + 1) ≤ 2 ^ (m + K) := by
    calc 2 ^ K * (T^[t] n + 1) = 2 ^ r * (2 ^ s * (T^[t] n + 1)) := by
          rw [hr, pow_add]; ring
      _ ≤ 3 ^ r * (3 ^ s * (n + 1)) := Nat.mul_le_mul h23 hc
      _ = 3 ^ K * (n + 1) := by rw [hr, pow_add]; ring
      _ ≤ 2 ^ (m + K) := h
  have hK : 0 < 2 ^ K := by positivity
  have key2 : 2 ^ K * (T^[t] n + 1) ≤ 2 ^ K * 2 ^ m := by
    rw [← pow_add, Nat.add_comm K m]
    exact key
  have : T^[t] n + 1 ≤ 2 ^ m := Nat.le_of_mul_le_mul_left key2 hK
  omega

/-- Si `3^K (n+1) <= 2^(m+K)`, los factores de largo `m` en los instantes `0..K` de una
órbita inyectiva son todos distintos. -/
theorem factores_iniciales {n m K : ℕ} (hi : Function.Injective (fun j => T^[j] n))
    (h : 3 ^ K * (n + 1) ≤ 2 ^ (m + K)) :
    ((Finset.range (K + 1)).image (factor n m)).card = K + 1 := by
  apply le_antisymm
  · exact (Finset.card_image_le).trans (by simp)
  · have hf : (Finset.range (K + 1)).filter (fun t => T^[t] n < 2 ^ m) =
        Finset.range (K + 1) := by
      apply Finset.filter_true_of_mem
      intro t ht
      exact bajo_umbral (by simp at ht; omega) h
    have := complejidad_cota hi m (K + 1)
    rw [hf] at this
    simpa using this

/-- Bernoulli entero: `3^m (3+m) <= 3*4^m`. -/
theorem bernoulli_cuatro_tercios (m : ℕ) : 3 ^ m * (3 + m) ≤ 3 * 4 ^ m := by
  induction m with
  | zero => simp
  | succ m ih =>
    rw [pow_succ, pow_succ]
    nlinarith [ih, Nat.zero_le (3 ^ m)]

/-- Umbral explícito: para `m >= 5(n+1)` se cumple `3^(m+1) (n+1) <= 2^(2m+1)`. -/
theorem umbral_explicito {n m : ℕ} (hm : 5 * (n + 1) ≤ m) :
    3 ^ (m + 1) * (n + 1) ≤ 2 ^ (m + (m + 1)) := by
  have hb := bernoulli_cuatro_tercios m
  have h4 : 2 ^ (m + (m + 1)) = 2 * 4 ^ m := by
    rw [show m + (m + 1) = 2 * m + 1 by omega, pow_succ, pow_mul]; norm_num; ring
  rw [h4, pow_succ]
  have h3 : 0 < 3 ^ m := by positivity
  nlinarith [hb, h3]

/-- Ninguna órbita inyectiva tiene palabra de complejidad mínima: para `m >= 5(n+1)`,
sus `m+2` primeros factores de largo `m` son distintos. Una palabra sturmiana tiene
exactamente `m+1` factores de cada largo `m`. -/
theorem mas_que_sturmiana {n m : ℕ} (hi : Function.Injective (fun j => T^[j] n))
    (hm : 5 * (n + 1) ≤ m) :
    ((Finset.range (m + 2)).image (factor n m)).card = m + 2 :=
  factores_iniciales hi (umbral_explicito hm)

/-- Forma de cota superior: si a lo sumo `m+1` factores distintos de largo `m` aparecen
en los instantes `0..m+1`, para algún `m >= 5(n+1)`, la órbita de `n` no es inyectiva. -/
theorem no_inyectiva_si_pocos_factores {n m : ℕ} (hm : 5 * (n + 1) ≤ m)
    (hpocos : ((Finset.range (m + 2)).image (factor n m)).card ≤ m + 1) :
    ¬ Function.Injective (fun j => T^[j] n) := by
  intro hi
  have := mas_que_sturmiana hi hm
  omega

end PerdicesComplejidad

#print axioms PerdicesComplejidad.paso_uno
#print axioms PerdicesComplejidad.cota_impares
#print axioms PerdicesComplejidad.separacion
#print axioms PerdicesComplejidad.repeticion_congruente
#print axioms PerdicesComplejidad.ley_local
#print axioms PerdicesComplejidad.ley_global
#print axioms PerdicesComplejidad.tramo_expansivo_no_cierra
#print axioms PerdicesComplejidad.ley_expansiva
#print axioms PerdicesComplejidad.representante_crece
#print axioms PerdicesComplejidad.factores_distintos
#print axioms PerdicesComplejidad.complejidad_cota
#print axioms PerdicesComplejidad.bajo_umbral
#print axioms PerdicesComplejidad.factores_iniciales
#print axioms PerdicesComplejidad.bernoulli_cuatro_tercios
#print axioms PerdicesComplejidad.umbral_explicito
#print axioms PerdicesComplejidad.mas_que_sturmiana
#print axioms PerdicesComplejidad.no_inyectiva_si_pocos_factores
