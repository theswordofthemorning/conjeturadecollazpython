import OcelotasTiempoRacional

/-! # Ocelotas: cota racional inferior del tiempo de cruce -/

namespace OcelotasVentanaRacional

theorem tiempo_inferior {k q u v : ℕ} (hv : 0 < v) (hbase : 2 ^ u ≤ 3 ^ v)
    (hcruce : 3 ^ q < 2 ^ k) : u * q < v * k := by
  have hpow : 2 ^ (u * q) < 2 ^ (v * k) := by
    calc
      2 ^ (u * q) = (2 ^ u) ^ q := by rw [pow_mul]
      _ ≤ (3 ^ v) ^ q := Nat.pow_le_pow_left hbase q
      _ = (3 ^ q) ^ v := by rw [← pow_mul, Nat.mul_comm v q, pow_mul]
      _ < (2 ^ k) ^ v := Nat.pow_lt_pow_left hcruce (by omega)
      _ = 2 ^ (v * k) := by rw [← pow_mul, Nat.mul_comm k v]
  exact (Nat.pow_lt_pow_iff_right (by decide : 1 < 2)).1 hpow

theorem tiempo_tres_medios {k q : ℕ} (hcruce : 3 ^ q < 2 ^ k) :
    3 * q < 2 * k := tiempo_inferior (by decide) (by norm_num : 2 ^ 3 ≤ 3 ^ 2) hcruce

end OcelotasVentanaRacional

#print axioms OcelotasVentanaRacional.tiempo_inferior
#print axioms OcelotasVentanaRacional.tiempo_tres_medios
