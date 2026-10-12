import OcelotasCuarentaYUnaTablaParte01
import OcelotasCuarentaYUnaTablaParte02
import OcelotasCuarentaYUnaTablaParte03
import OcelotasCuarentaYUnaTablaParte04
import OcelotasCuarentaYUnaTablaParte05
import OcelotasCuarentaYUnaTablaParte06
import OcelotasCuarentaYUnaTablaParte07
import OcelotasCuarentaYUnaTablaParte08
import OcelotasCuarentaYUnaTablaParte09
import OcelotasCuarentaYUnaTablaParte10
import OcelotasCuarentaYUnaTablaParte11
import OcelotasCuarentaYUnaTablaParte12
import OcelotasCuarentaYUnaTablaParte13

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasCuarentaYUnaTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem pequeno_de_tabla {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 41)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hq : S (tiempo a b r) n < 2365627332311699) : n < 200000000001 := by
  have hpos := impares_pos hw hr
  by_cases h0 : S (tiempo a b r) n < 3
  · exact fila_0 hw hr hrR hk hf (by omega) h0
  by_cases h1 : S (tiempo a b r) n < 5
  · exact fila_1 hw hr hrR hk hf (by omega) h1
  by_cases h2 : S (tiempo a b r) n < 17
  · exact fila_2 hw hr hrR hk hf (by omega) h2
  by_cases h3 : S (tiempo a b r) n < 29
  · exact fila_3 hw hr hrR hk hf (by omega) h3
  by_cases h4 : S (tiempo a b r) n < 41
  · exact fila_4 hw hr hrR hk hf (by omega) h4
  by_cases h5 : S (tiempo a b r) n < 94
  · exact fila_5 hw hr hrR hk hf (by omega) h5
  by_cases h6 : S (tiempo a b r) n < 147
  · exact fila_6 hw hr hrR hk hf (by omega) h6
  by_cases h7 : S (tiempo a b r) n < 200
  · exact fila_7 hw hr hrR hk hf (by omega) h7
  by_cases h8 : S (tiempo a b r) n < 253
  · exact fila_8 hw hr hrR hk hf (by omega) h8
  by_cases h9 : S (tiempo a b r) n < 306
  · exact fila_9 hw hr hrR hk hf (by omega) h9
  by_cases h10 : S (tiempo a b r) n < 971
  · exact fila_10 hw hr hrR hk hf (by omega) h10
  by_cases h11 : S (tiempo a b r) n < 1636
  · exact fila_11 hw hr hrR hk hf (by omega) h11
  by_cases h12 : S (tiempo a b r) n < 2301
  · exact fila_12 hw hr hrR hk hf (by omega) h12
  by_cases h13 : S (tiempo a b r) n < 2966
  · exact fila_13 hw hr hrR hk hf (by omega) h13
  by_cases h14 : S (tiempo a b r) n < 3631
  · exact fila_14 hw hr hrR hk hf (by omega) h14
  by_cases h15 : S (tiempo a b r) n < 4296
  · exact fila_15 hw hr hrR hk hf (by omega) h15
  by_cases h16 : S (tiempo a b r) n < 4961
  · exact fila_16 hw hr hrR hk hf (by omega) h16
  by_cases h17 : S (tiempo a b r) n < 5626
  · exact fila_17 hw hr hrR hk hf (by omega) h17
  by_cases h18 : S (tiempo a b r) n < 6291
  · exact fila_18 hw hr hrR hk hf (by omega) h18
  by_cases h19 : S (tiempo a b r) n < 6956
  · exact fila_19 hw hr hrR hk hf (by omega) h19
  by_cases h20 : S (tiempo a b r) n < 7621
  · exact fila_20 hw hr hrR hk hf (by omega) h20
  by_cases h21 : S (tiempo a b r) n < 8286
  · exact fila_21 hw hr hrR hk hf (by omega) h21
  by_cases h22 : S (tiempo a b r) n < 8951
  · exact fila_22 hw hr hrR hk hf (by omega) h22
  by_cases h23 : S (tiempo a b r) n < 9616
  · exact fila_23 hw hr hrR hk hf (by omega) h23
  by_cases h24 : S (tiempo a b r) n < 10281
  · exact fila_24 hw hr hrR hk hf (by omega) h24
  by_cases h25 : S (tiempo a b r) n < 10946
  · exact fila_25 hw hr hrR hk hf (by omega) h25
  by_cases h26 : S (tiempo a b r) n < 11611
  · exact fila_26 hw hr hrR hk hf (by omega) h26
  by_cases h27 : S (tiempo a b r) n < 12276
  · exact fila_27 hw hr hrR hk hf (by omega) h27
  by_cases h28 : S (tiempo a b r) n < 12941
  · exact fila_28 hw hr hrR hk hf (by omega) h28
  by_cases h29 : S (tiempo a b r) n < 13606
  · exact fila_29 hw hr hrR hk hf (by omega) h29
  by_cases h30 : S (tiempo a b r) n < 14271
  · exact fila_30 hw hr hrR hk hf (by omega) h30
  by_cases h31 : S (tiempo a b r) n < 14936
  · exact fila_31 hw hr hrR hk hf (by omega) h31
  by_cases h32 : S (tiempo a b r) n < 15601
  · exact fila_32 hw hr hrR hk hf (by omega) h32
  by_cases h33 : S (tiempo a b r) n < 47468
  · exact fila_33 hw hr hrR hk hf (by omega) h33
  by_cases h34 : S (tiempo a b r) n < 79335
  · exact fila_34 hw hr hrR hk hf (by omega) h34
  by_cases h35 : S (tiempo a b r) n < 190537
  · exact fila_35 hw hr hrR hk hf (by omega) h35
  by_cases h36 : S (tiempo a b r) n < 10781274
  · exact fila_36 hw hr hrR hk hf (by omega) h36
  by_cases h37 : S (tiempo a b r) n < 64497107
  · exact fila_37 hw hr hrR hk hf (by omega) h37
  by_cases h38 : S (tiempo a b r) n < 118212940
  · exact fila_38 hw hr hrR hk hf (by omega) h38
  by_cases h39 : S (tiempo a b r) n < 171928773
  · exact fila_39 hw hr hrR hk hf (by omega) h39
  by_cases h40 : S (tiempo a b r) n < 397573379
  · exact fila_40 hw hr hrR hk hf (by omega) h40
  by_cases h41 : S (tiempo a b r) n < 6586818670
  · exact fila_41 hw hr hrR hk hf (by omega) h41
  by_cases h42 : S (tiempo a b r) n < 72057431991
  · exact fila_42 hw hr hrR hk hf (by omega) h42
  by_cases h43 : S (tiempo a b r) n < 137528045312
  · exact fila_43 hw hr hrR hk hf (by omega) h43
  by_cases h44 : S (tiempo a b r) n < 890638885193
  · exact fila_44 hw hr hrR hk hf (by omega) h44
  by_cases h45 : S (tiempo a b r) n < 1643749725074
  · exact fila_45 hw hr hrR hk hf (by omega) h45
  by_cases h46 : S (tiempo a b r) n < 2396860564955
  · exact fila_46 hw hr hrR hk hf (by omega) h46
  by_cases h47 : S (tiempo a b r) n < 3149971404836
  · exact fila_47 hw hr hrR hk hf (by omega) h47
  by_cases h48 : S (tiempo a b r) n < 3903082244717
  · exact fila_48 hw hr hrR hk hf (by omega) h48
  by_cases h49 : S (tiempo a b r) n < 4656193084598
  · exact fila_49 hw hr hrR hk hf (by omega) h49
  by_cases h50 : S (tiempo a b r) n < 5409303924479
  · exact fila_50 hw hr hrR hk hf (by omega) h50
  by_cases h51 : S (tiempo a b r) n < 11571718688839
  · exact fila_51 hw hr hrR hk hf (by omega) h51
  by_cases h52 : S (tiempo a b r) n < 64021008208555
  · exact fila_52 hw hr hrR hk hf (by omega) h52
  by_cases h53 : S (tiempo a b r) n < 116470297728271
  · exact fila_53 hw hr hrR hk hf (by omega) h53
  by_cases h54 : S (tiempo a b r) n < 168919587247987
  · exact fila_54 hw hr hrR hk hf (by omega) h54
  by_cases h55 : S (tiempo a b r) n < 221368876767703
  · exact fila_55 hw hr hrR hk hf (by omega) h55
  by_cases h56 : S (tiempo a b r) n < 273818166287419
  · exact fila_56 hw hr hrR hk hf (by omega) h56
  by_cases h57 : S (tiempo a b r) n < 326267455807135
  · exact fila_57 hw hr hrR hk hf (by omega) h57
  by_cases h58 : S (tiempo a b r) n < 378716745326851
  · exact fila_58 hw hr hrR hk hf (by omega) h58
  by_cases h59 : S (tiempo a b r) n < 431166034846567
  · exact fila_59 hw hr hrR hk hf (by omega) h59
  by_cases h60 : S (tiempo a b r) n < 914781359212850
  · exact fila_60 hw hr hrR hk hf (by omega) h60
  by_cases h61 : S (tiempo a b r) n < 1398396683579133
  · exact fila_61 hw hr hrR hk hf (by omega) h61
  by_cases h62 : S (tiempo a b r) n < 1882012007945416
  · exact fila_62 hw hr hrR hk hf (by omega) h62
  exact fila_63 hw hr hrR hk hf (by omega) hq

end OcelotasCuarentaYUnaTabla

#print axioms OcelotasCuarentaYUnaTabla.pequeno_de_tabla
