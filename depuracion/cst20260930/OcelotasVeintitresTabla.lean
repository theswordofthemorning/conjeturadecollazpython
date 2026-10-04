import OcelotasVeintitresTablaParte01
import OcelotasVeintitresTablaParte02
import OcelotasVeintitresTablaParte03

namespace OcelotasVeintitresTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem pequeno_de_tabla {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr23 : r ≤ 23)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 23)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hq : S (tiempo a b r) n < 19362882631) : n < 4912741 := by
  have hpos := impares_pos hw hr
  by_cases h0 : S (tiempo a b r) n < 3
  · exact fila_0 hw hr hr23 _hcontador hk hf (by omega) h0
  by_cases h1 : S (tiempo a b r) n < 5
  · exact fila_1 hw hr hr23 _hcontador hk hf (by omega) h1
  by_cases h2 : S (tiempo a b r) n < 17
  · exact fila_2 hw hr hr23 _hcontador hk hf (by omega) h2
  by_cases h3 : S (tiempo a b r) n < 29
  · exact fila_3 hw hr hr23 _hcontador hk hf (by omega) h3
  by_cases h4 : S (tiempo a b r) n < 41
  · exact fila_4 hw hr hr23 _hcontador hk hf (by omega) h4
  by_cases h5 : S (tiempo a b r) n < 94
  · exact fila_5 hw hr hr23 _hcontador hk hf (by omega) h5
  by_cases h6 : S (tiempo a b r) n < 147
  · exact fila_6 hw hr hr23 _hcontador hk hf (by omega) h6
  by_cases h7 : S (tiempo a b r) n < 200
  · exact fila_7 hw hr hr23 _hcontador hk hf (by omega) h7
  by_cases h8 : S (tiempo a b r) n < 253
  · exact fila_8 hw hr hr23 _hcontador hk hf (by omega) h8
  by_cases h9 : S (tiempo a b r) n < 306
  · exact fila_9 hw hr hr23 _hcontador hk hf (by omega) h9
  by_cases h10 : S (tiempo a b r) n < 971
  · exact fila_10 hw hr hr23 _hcontador hk hf (by omega) h10
  by_cases h11 : S (tiempo a b r) n < 1636
  · exact fila_11 hw hr hr23 _hcontador hk hf (by omega) h11
  by_cases h12 : S (tiempo a b r) n < 2301
  · exact fila_12 hw hr hr23 _hcontador hk hf (by omega) h12
  by_cases h13 : S (tiempo a b r) n < 2966
  · exact fila_13 hw hr hr23 _hcontador hk hf (by omega) h13
  by_cases h14 : S (tiempo a b r) n < 3631
  · exact fila_14 hw hr hr23 _hcontador hk hf (by omega) h14
  by_cases h15 : S (tiempo a b r) n < 4296
  · exact fila_15 hw hr hr23 _hcontador hk hf (by omega) h15
  by_cases h16 : S (tiempo a b r) n < 4961
  · exact fila_16 hw hr hr23 _hcontador hk hf (by omega) h16
  by_cases h17 : S (tiempo a b r) n < 5626
  · exact fila_17 hw hr hr23 _hcontador hk hf (by omega) h17
  by_cases h18 : S (tiempo a b r) n < 6291
  · exact fila_18 hw hr hr23 _hcontador hk hf (by omega) h18
  by_cases h19 : S (tiempo a b r) n < 6956
  · exact fila_19 hw hr hr23 _hcontador hk hf (by omega) h19
  by_cases h20 : S (tiempo a b r) n < 7621
  · exact fila_20 hw hr hr23 _hcontador hk hf (by omega) h20
  by_cases h21 : S (tiempo a b r) n < 8286
  · exact fila_21 hw hr hr23 _hcontador hk hf (by omega) h21
  by_cases h22 : S (tiempo a b r) n < 8951
  · exact fila_22 hw hr hr23 _hcontador hk hf (by omega) h22
  by_cases h23 : S (tiempo a b r) n < 9616
  · exact fila_23 hw hr hr23 _hcontador hk hf (by omega) h23
  by_cases h24 : S (tiempo a b r) n < 10281
  · exact fila_24 hw hr hr23 _hcontador hk hf (by omega) h24
  by_cases h25 : S (tiempo a b r) n < 10946
  · exact fila_25 hw hr hr23 _hcontador hk hf (by omega) h25
  by_cases h26 : S (tiempo a b r) n < 11611
  · exact fila_26 hw hr hr23 _hcontador hk hf (by omega) h26
  by_cases h27 : S (tiempo a b r) n < 12276
  · exact fila_27 hw hr hr23 _hcontador hk hf (by omega) h27
  by_cases h28 : S (tiempo a b r) n < 12941
  · exact fila_28 hw hr hr23 _hcontador hk hf (by omega) h28
  by_cases h29 : S (tiempo a b r) n < 13606
  · exact fila_29 hw hr hr23 _hcontador hk hf (by omega) h29
  by_cases h30 : S (tiempo a b r) n < 14271
  · exact fila_30 hw hr hr23 _hcontador hk hf (by omega) h30
  by_cases h31 : S (tiempo a b r) n < 14936
  · exact fila_31 hw hr hr23 _hcontador hk hf (by omega) h31
  by_cases h32 : S (tiempo a b r) n < 15601
  · exact fila_32 hw hr hr23 _hcontador hk hf (by omega) h32
  by_cases h33 : S (tiempo a b r) n < 47468
  · exact fila_33 hw hr hr23 _hcontador hk hf (by omega) h33
  by_cases h34 : S (tiempo a b r) n < 79335
  · exact fila_34 hw hr hr23 _hcontador hk hf (by omega) h34
  by_cases h35 : S (tiempo a b r) n < 190537
  · exact fila_35 hw hr hr23 _hcontador hk hf (by omega) h35
  by_cases h36 : S (tiempo a b r) n < 10781274
  · exact fila_36 hw hr hr23 _hcontador hk hf (by omega) h36
  by_cases h37 : S (tiempo a b r) n < 64497107
  · exact fila_37 hw hr hr23 _hcontador hk hf (by omega) h37
  by_cases h38 : S (tiempo a b r) n < 118212940
  · exact fila_38 hw hr hr23 _hcontador hk hf (by omega) h38
  by_cases h39 : S (tiempo a b r) n < 171928773
  · exact fila_39 hw hr hr23 _hcontador hk hf (by omega) h39
  by_cases h40 : S (tiempo a b r) n < 397573379
  · exact fila_40 hw hr hr23 _hcontador hk hf (by omega) h40
  by_cases h41 : S (tiempo a b r) n < 6586818670
  · exact fila_41 hw hr hr23 _hcontador hk hf (by omega) h41
  exact fila_42 hw hr hr23 _hcontador hk hf (by omega) hq

end OcelotasVeintitresTabla

#print axioms OcelotasVeintitresTabla.pequeno_de_tabla
