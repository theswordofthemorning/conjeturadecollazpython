import OcelotasTrayectorias

/-! # Ocelotas: cota racional del tiempo a partir de los pasos impares

La ventana del primer cruce y 3^v <= 2^u implican v*k <= u*q+v.
No se usa LMN ni una cota del número de rachas.
-/

namespace OcelotasTiempoRacional

open Ocelotas OcelotasTrayectorias

theorem tiempo_racional {k q u v : ℕ} (hbase : 3 ^ v ≤ 2 ^ u)
    (hvent : 2 ^ k ≤ 2 * 3 ^ q) : v * k ≤ u * q + v := by
  have hpow : 2 ^ (v * k) ≤ 2 ^ (u * q + v) := by
    calc
      2 ^ (v * k) = (2 ^ k) ^ v := by rw [Nat.mul_comm v k, pow_mul]
      _ ≤ (2 * 3 ^ q) ^ v := Nat.pow_le_pow_left hvent v
      _ = 2 ^ v * (3 ^ v) ^ q := by rw [mul_pow, ← pow_mul, Nat.mul_comm q v, pow_mul]
      _ ≤ 2 ^ v * (2 ^ u) ^ q := Nat.mul_le_mul_left _ (Nat.pow_le_pow_left hbase q)
      _ = 2 ^ (u * q + v) := by rw [← pow_mul, ← pow_add, Nat.add_comm]
  exact (Nat.pow_le_pow_iff_right (by decide : 1 < 2)).1 hpow

theorem tiempo_ocho_quintos {k q : ℕ} (hvent : 2 ^ k ≤ 2 * 3 ^ q) :
    5 * k ≤ 8 * q + 5 := tiempo_racional (by norm_num : 3 ^ 5 ≤ 2 ^ 8) hvent

theorem tiempo_del_cruce {n k : ℕ} (hk : PrimerCruce n k) :
    5 * k ≤ 8 * S k n + 5 := tiempo_ocho_quintos (ventana_cruce hk).2

end OcelotasTiempoRacional

#print axioms OcelotasTiempoRacional.tiempo_racional
#print axioms OcelotasTiempoRacional.tiempo_ocho_quintos
#print axioms OcelotasTiempoRacional.tiempo_del_cruce
