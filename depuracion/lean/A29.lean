/-
  A29 — "n ≡ 2^k − 1 (mod 2^k) sube k veces seguidas;
         n ≡ 0     (mod 2^k) baja k veces seguidas"

  MAPA: el ATAJO  T(n) = n/2 si n par, (3n+1)/2 si n impar.
  ("sube k veces SEGUIDAS" solo tiene sentido en el atajo: en el mapa clasico
   cada 3n+1 va seguido de una division, asi que nunca hay dos subidas seguidas.
   La version del mapa clasico del mismo enunciado es "k pasos impares seguidos",
   que aqui es el teorema sube_impar.)

  Lo demostrado, para todo k, todo j < k y todo m >= 1 (sin Mathlib):
    forma_sube :  T^j(2^k·m − 1) = 2^(k−j)·3^j·m − 1        (identidad exacta)
    sube       :  T^j(2^k·m − 1) < T^(j+1)(2^k·m − 1)       (k subidas seguidas)
    sube_impar :  T^j(2^k·m − 1) es impar                    (k pasos impares)
    forma_baja :  T^j(2^k·m)     = 2^(k−j)·m
    baja       :  T^(j+1)(2^k·m) < T^j(2^k·m)               (k bajadas seguidas)
  y las versiones literales por clase de resto:
    sube_residuo : n % 2^k = 2^k − 1  →  j < k  →  T^j(n) < T^(j+1)(n)
    baja_residuo : n % 2^k = 0  →  n ≥ 1  →  j < k  →  T^(j+1)(n) < T^j(n)

  BORDE que obliga a la hipotesis n ≥ 1 en baja_residuo: n = 0 esta en la
  clase 0 (mod 2^k) y NO baja (T(0) = 0). Ver borde_cero.
-/

set_option maxRecDepth 40000

-- El mapa del atajo, escrito desde cero
def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3*n+1)/2

-- Titer j n = T^j(n)
def Titer : Nat → Nat → Nat
  | 0,   n => n
  | k+1, n => Titer k (T n)

theorem dos_pos (d : Nat) : 0 < 2^d := by
  induction d with
  | zero => decide
  | succ d ih => rw [Nat.pow_succ]; omega

theorem tres_pos (j : Nat) : 0 < 3^j := by
  induction j with
  | zero => decide
  | succ j ih => rw [Nat.pow_succ]; omega

-- Un paso impar: T(2^(c+1)·m − 1) = 2^c·(3m) − 1
theorem paso_sube (c m : Nat) (hm : 1 ≤ m) :
    T (2^(c+1)*m - 1) = 2^c*(3*m) - 1 := by
  have h2 : 0 < 2^c := dos_pos c
  have ht : 0 < 2^c*m := Nat.mul_pos h2 hm
  have h : 2^(c+1)*m = 2*(2^c*m) := by
    rw [Nat.pow_succ, Nat.mul_assoc (2^c) 2 m, Nat.mul_left_comm (2^c) 2 m]
  rw [h]
  have hpar : ¬ ((2*(2^c*m) - 1) % 2 = 0) := by omega
  unfold T
  rw [if_neg hpar]
  have h3 : 2^c*(3*m) = 3*(2^c*m) := by rw [Nat.mul_left_comm (2^c) 3 m]
  rw [h3]
  omega

-- Un paso par: T(2^(c+1)·m) = 2^c·m
theorem paso_baja (c m : Nat) : T (2^(c+1)*m) = 2^c*m := by
  have h : 2^(c+1)*m = 2*(2^c*m) := by
    rw [Nat.pow_succ, Nat.mul_assoc (2^c) 2 m, Nat.mul_left_comm (2^c) 2 m]
  rw [h]
  have hpar : (2*(2^c*m)) % 2 = 0 := by omega
  unfold T
  rw [if_pos hpar]
  omega

-- LA IDENTIDAD DE SUBIDA: T^j(2^(j+d)·m − 1) = 2^d·(3^j·m) − 1
theorem forma_sube (j : Nat) : ∀ d m : Nat, 1 ≤ m →
    Titer j (2^(j+d)*m - 1) = 2^d*(3^j*m) - 1 := by
  induction j with
  | zero =>
    intro d m hm
    show 2^(0+d)*m - 1 = 2^d*(3^0*m) - 1
    rw [Nat.zero_add, Nat.pow_zero, Nat.one_mul]
  | succ j ih =>
    intro d m hm
    show Titer j (T (2^(j+1+d)*m - 1)) = 2^d*(3^(j+1)*m) - 1
    have he : j+1+d = (j+d)+1 := by omega
    rw [he, paso_sube (j+d) m hm, ih d (3*m) (by omega)]
    rw [Nat.pow_succ, Nat.mul_assoc (3^j) 3 m]

-- LA IDENTIDAD DE BAJADA: T^j(2^(j+d)·m) = 2^d·m
theorem forma_baja (j : Nat) : ∀ d m : Nat,
    Titer j (2^(j+d)*m) = 2^d*m := by
  induction j with
  | zero =>
    intro d m
    show 2^(0+d)*m = 2^d*m
    rw [Nat.zero_add]
  | succ j ih =>
    intro d m
    show Titer j (T (2^(j+1+d)*m)) = 2^d*m
    have he : j+1+d = (j+d)+1 := by omega
    rw [he, paso_baja (j+d) m]
    exact ih d m

-- SUBE k VECES SEGUIDAS (forma parametrica: n = 2^k·m − 1, m ≥ 1)
theorem sube (k m j : Nat) (hm : 1 ≤ m) (hj : j < k) :
    Titer j (2^k*m - 1) < Titer (j+1) (2^k*m - 1) := by
  have hd : ∃ d, k = j + (1 + d) := ⟨k - (j+1), by omega⟩
  cases hd with
  | intro d hk =>
    rw [hk]
    have e1 := forma_sube j (1+d) m hm
    have he : j + (1+d) = j+1+d := by omega
    rw [e1, he, forma_sube (j+1) d m hm]
    have h1 : 2^(1+d)*(3^j*m) = 2*(2^d*(3^j*m)) := by
      rw [Nat.add_comm 1 d, Nat.pow_succ,
          Nat.mul_assoc (2^d) 2 (3^j*m), Nat.mul_left_comm (2^d) 2 (3^j*m)]
    have h2 : 2^d*(3^(j+1)*m) = 3*(2^d*(3^j*m)) := by
      rw [Nat.pow_succ, Nat.mul_comm (3^j) 3,
          Nat.mul_assoc 3 (3^j) m, Nat.mul_left_comm (2^d) 3 (3^j*m)]
    have hW : 0 < 2^d*(3^j*m) :=
      Nat.mul_pos (dos_pos d) (Nat.mul_pos (tres_pos j) hm)
    rw [h1, h2]
    omega

-- LOS k PASOS SON IMPARES (la version del mapa clasico / vector de paridad)
theorem sube_impar (k m j : Nat) (hm : 1 ≤ m) (hj : j < k) :
    (Titer j (2^k*m - 1)) % 2 = 1 := by
  have hd : ∃ d, k = j + (1 + d) := ⟨k - (j+1), by omega⟩
  cases hd with
  | intro d hk =>
    rw [hk, forma_sube j (1+d) m hm]
    have h1 : 2^(1+d)*(3^j*m) = 2*(2^d*(3^j*m)) := by
      rw [Nat.add_comm 1 d, Nat.pow_succ,
          Nat.mul_assoc (2^d) 2 (3^j*m), Nat.mul_left_comm (2^d) 2 (3^j*m)]
    have hW : 0 < 2^d*(3^j*m) :=
      Nat.mul_pos (dos_pos d) (Nat.mul_pos (tres_pos j) hm)
    rw [h1]
    omega

-- BAJA k VECES SEGUIDAS (forma parametrica: n = 2^k·m, m ≥ 1)
theorem baja (k m j : Nat) (hm : 1 ≤ m) (hj : j < k) :
    Titer (j+1) (2^k*m) < Titer j (2^k*m) := by
  have hd : ∃ d, k = j + (1 + d) := ⟨k - (j+1), by omega⟩
  cases hd with
  | intro d hk =>
    rw [hk]
    have e1 := forma_baja j (1+d) m
    have he : j + (1+d) = j+1+d := by omega
    rw [e1, he, forma_baja (j+1) d m]
    have h1 : 2^(1+d)*m = 2*(2^d*m) := by
      rw [Nat.add_comm 1 d, Nat.pow_succ,
          Nat.mul_assoc (2^d) 2 m, Nat.mul_left_comm (2^d) 2 m]
    have hW : 0 < 2^d*m := Nat.mul_pos (dos_pos d) hm
    rw [h1]
    omega

-- EL ENUNCIADO LITERAL, POR CLASE DE RESTO -------------------------------

-- n ≡ 2^k − 1 (mod 2^k)  →  sube k veces seguidas
theorem sube_residuo (k n j : Nat) (h : n % 2^k = 2^k - 1) (hj : j < k) :
    Titer j n < Titer (j+1) n := by
  have hP : 0 < 2^k := dos_pos k
  have hdm : 2^k * (n / 2^k) + n % 2^k = n := Nat.div_add_mod n (2^k)
  have hms : 2^k * (n / 2^k + 1) = 2^k * (n / 2^k) + 2^k := by
    rw [Nat.mul_add, Nat.mul_one]
  have hn : n = 2^k * (n / 2^k + 1) - 1 := by omega
  rw [hn]
  exact sube k (n / 2^k + 1) j (Nat.succ_le_succ (Nat.zero_le _)) hj

-- lo mismo, con los pasos impares
theorem sube_residuo_impar (k n j : Nat) (h : n % 2^k = 2^k - 1) (hj : j < k) :
    (Titer j n) % 2 = 1 := by
  have hP : 0 < 2^k := dos_pos k
  have hdm : 2^k * (n / 2^k) + n % 2^k = n := Nat.div_add_mod n (2^k)
  have hms : 2^k * (n / 2^k + 1) = 2^k * (n / 2^k) + 2^k := by
    rw [Nat.mul_add, Nat.mul_one]
  have hn : n = 2^k * (n / 2^k + 1) - 1 := by omega
  rw [hn]
  exact sube_impar k (n / 2^k + 1) j (Nat.succ_le_succ (Nat.zero_le _)) hj

-- n ≡ 0 (mod 2^k), n ≥ 1  →  baja k veces seguidas
-- (la hipotesis n ≥ 1 es NECESARIA: ver borde_cero)
theorem baja_residuo (k n j : Nat) (h : n % 2^k = 0) (hn1 : 1 ≤ n) (hj : j < k) :
    Titer (j+1) n < Titer j n := by
  have hP : 0 < 2^k := dos_pos k
  have hdm : 2^k * (n / 2^k) + n % 2^k = n := Nat.div_add_mod n (2^k)
  have hq : 1 ≤ n / 2^k := by
    cases hq0 : n / 2^k with
    | zero =>
      exfalso
      rw [hq0, Nat.mul_zero] at hdm
      omega
    | succ q => omega
  have hn : n = 2^k * (n / 2^k) := by omega
  rw [hn]
  exact baja k (n / 2^k) j hq hj

-- CASOS CONOCIDOS, COMPROBADOS POR EL NUCLEO (by decide, no #eval) --------

-- k = 3: 7 ≡ 7 (mod 8): 7 → 11 → 17 → 26, tres subidas, tres impares
theorem caso_7 : Titer 0 7 = 7 ∧ Titer 1 7 = 11 ∧ Titer 2 7 = 17 ∧
    Titer 3 7 = 26 := by decide
theorem caso_7_sube : Titer 0 7 < Titer 1 7 ∧ Titer 1 7 < Titer 2 7 ∧
    Titer 2 7 < Titer 3 7 ∧ 7 % 2 = 1 ∧ 11 % 2 = 1 ∧ 17 % 2 = 1 := by decide

-- k = 5: 31 ≡ 31 (mod 32): 31 → 47 → 71 → 107 → 161 → 242, cinco subidas
theorem caso_31 : Titer 1 31 = 47 ∧ Titer 2 31 = 71 ∧ Titer 3 31 = 107 ∧
    Titer 4 31 = 161 ∧ Titer 5 31 = 242 := by decide

-- k = 3: 8 ≡ 0 (mod 8): 8 → 4 → 2 → 1, tres bajadas
theorem caso_8 : Titer 1 8 = 4 ∧ Titer 2 8 = 2 ∧ Titer 3 8 = 1 := by decide

-- EL BORDE: 0 ≡ 0 (mod 2^k) y NO baja — por eso baja_residuo pide n ≥ 1
theorem borde_cero : ¬ (Titer 1 0 < Titer 0 0) := by decide

-- El teorema general aplicado al caso concreto (enlace teorema ↔ caso)
theorem enlace_sube : Titer 2 7 < Titer 3 7 :=
  sube_residuo 3 7 2 (by decide) (by decide)
theorem enlace_baja : Titer 3 8 < Titer 2 8 :=
  baja_residuo 3 8 2 (by decide) (by decide) (by decide)

-- CONTROL FINAL -----------------------------------------------------------
#print axioms forma_sube
#print axioms forma_baja
#print axioms sube
#print axioms sube_impar
#print axioms baja
#print axioms sube_residuo
#print axioms sube_residuo_impar
#print axioms baja_residuo
#print axioms caso_7
#print axioms caso_7_sube
#print axioms caso_31
#print axioms caso_8
#print axioms borde_cero
#print axioms enlace_sube
#print axioms enlace_baja
