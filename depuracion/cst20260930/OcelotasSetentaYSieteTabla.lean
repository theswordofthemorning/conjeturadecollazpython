import OcelotasSetentaYSieteTablaParte01
import OcelotasSetentaYSieteTablaParte02
import OcelotasSetentaYSieteTablaParte03
import OcelotasSetentaYSieteTablaParte04
import OcelotasSetentaYSieteTablaParte05
import OcelotasSetentaYSieteTablaParte06
import OcelotasSetentaYSieteTablaParte07

namespace OcelotasSetentaYSieteTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem pequeno_de_tabla {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hq : S (tiempo a b r) n < 4857481135601629720741) : n < 28000000000000000001 := by
  have hpos := impares_pos hw hr
  by_cases h0 : S (tiempo a b r) n < 3
  · exact fila_0 hw hr hr77 _hcontador hk hf (by omega) h0
  by_cases h1 : S (tiempo a b r) n < 5
  · exact fila_1 hw hr hr77 _hcontador hk hf (by omega) h1
  by_cases h2 : S (tiempo a b r) n < 17
  · exact fila_2 hw hr hr77 _hcontador hk hf (by omega) h2
  by_cases h3 : S (tiempo a b r) n < 29
  · exact fila_3 hw hr hr77 _hcontador hk hf (by omega) h3
  by_cases h4 : S (tiempo a b r) n < 41
  · exact fila_4 hw hr hr77 _hcontador hk hf (by omega) h4
  by_cases h5 : S (tiempo a b r) n < 94
  · exact fila_5 hw hr hr77 _hcontador hk hf (by omega) h5
  by_cases h6 : S (tiempo a b r) n < 147
  · exact fila_6 hw hr hr77 _hcontador hk hf (by omega) h6
  by_cases h7 : S (tiempo a b r) n < 200
  · exact fila_7 hw hr hr77 _hcontador hk hf (by omega) h7
  by_cases h8 : S (tiempo a b r) n < 253
  · exact fila_8 hw hr hr77 _hcontador hk hf (by omega) h8
  by_cases h9 : S (tiempo a b r) n < 306
  · exact fila_9 hw hr hr77 _hcontador hk hf (by omega) h9
  by_cases h10 : S (tiempo a b r) n < 971
  · exact fila_10 hw hr hr77 _hcontador hk hf (by omega) h10
  by_cases h11 : S (tiempo a b r) n < 1636
  · exact fila_11 hw hr hr77 _hcontador hk hf (by omega) h11
  by_cases h12 : S (tiempo a b r) n < 2301
  · exact fila_12 hw hr hr77 _hcontador hk hf (by omega) h12
  by_cases h13 : S (tiempo a b r) n < 2966
  · exact fila_13 hw hr hr77 _hcontador hk hf (by omega) h13
  by_cases h14 : S (tiempo a b r) n < 3631
  · exact fila_14 hw hr hr77 _hcontador hk hf (by omega) h14
  by_cases h15 : S (tiempo a b r) n < 4296
  · exact fila_15 hw hr hr77 _hcontador hk hf (by omega) h15
  by_cases h16 : S (tiempo a b r) n < 4961
  · exact fila_16 hw hr hr77 _hcontador hk hf (by omega) h16
  by_cases h17 : S (tiempo a b r) n < 5626
  · exact fila_17 hw hr hr77 _hcontador hk hf (by omega) h17
  by_cases h18 : S (tiempo a b r) n < 6291
  · exact fila_18 hw hr hr77 _hcontador hk hf (by omega) h18
  by_cases h19 : S (tiempo a b r) n < 6956
  · exact fila_19 hw hr hr77 _hcontador hk hf (by omega) h19
  by_cases h20 : S (tiempo a b r) n < 7621
  · exact fila_20 hw hr hr77 _hcontador hk hf (by omega) h20
  by_cases h21 : S (tiempo a b r) n < 8286
  · exact fila_21 hw hr hr77 _hcontador hk hf (by omega) h21
  by_cases h22 : S (tiempo a b r) n < 8951
  · exact fila_22 hw hr hr77 _hcontador hk hf (by omega) h22
  by_cases h23 : S (tiempo a b r) n < 9616
  · exact fila_23 hw hr hr77 _hcontador hk hf (by omega) h23
  by_cases h24 : S (tiempo a b r) n < 10281
  · exact fila_24 hw hr hr77 _hcontador hk hf (by omega) h24
  by_cases h25 : S (tiempo a b r) n < 10946
  · exact fila_25 hw hr hr77 _hcontador hk hf (by omega) h25
  by_cases h26 : S (tiempo a b r) n < 11611
  · exact fila_26 hw hr hr77 _hcontador hk hf (by omega) h26
  by_cases h27 : S (tiempo a b r) n < 12276
  · exact fila_27 hw hr hr77 _hcontador hk hf (by omega) h27
  by_cases h28 : S (tiempo a b r) n < 12941
  · exact fila_28 hw hr hr77 _hcontador hk hf (by omega) h28
  by_cases h29 : S (tiempo a b r) n < 13606
  · exact fila_29 hw hr hr77 _hcontador hk hf (by omega) h29
  by_cases h30 : S (tiempo a b r) n < 14271
  · exact fila_30 hw hr hr77 _hcontador hk hf (by omega) h30
  by_cases h31 : S (tiempo a b r) n < 14936
  · exact fila_31 hw hr hr77 _hcontador hk hf (by omega) h31
  by_cases h32 : S (tiempo a b r) n < 15601
  · exact fila_32 hw hr hr77 _hcontador hk hf (by omega) h32
  by_cases h33 : S (tiempo a b r) n < 47468
  · exact fila_33 hw hr hr77 _hcontador hk hf (by omega) h33
  by_cases h34 : S (tiempo a b r) n < 79335
  · exact fila_34 hw hr hr77 _hcontador hk hf (by omega) h34
  by_cases h35 : S (tiempo a b r) n < 190537
  · exact fila_35 hw hr hr77 _hcontador hk hf (by omega) h35
  by_cases h36 : S (tiempo a b r) n < 10781274
  · exact fila_36 hw hr hr77 _hcontador hk hf (by omega) h36
  by_cases h37 : S (tiempo a b r) n < 64497107
  · exact fila_37 hw hr hr77 _hcontador hk hf (by omega) h37
  by_cases h38 : S (tiempo a b r) n < 118212940
  · exact fila_38 hw hr hr77 _hcontador hk hf (by omega) h38
  by_cases h39 : S (tiempo a b r) n < 171928773
  · exact fila_39 hw hr hr77 _hcontador hk hf (by omega) h39
  by_cases h40 : S (tiempo a b r) n < 397573379
  · exact fila_40 hw hr hr77 _hcontador hk hf (by omega) h40
  by_cases h41 : S (tiempo a b r) n < 6586818670
  · exact fila_41 hw hr hr77 _hcontador hk hf (by omega) h41
  by_cases h42 : S (tiempo a b r) n < 72057431991
  · exact fila_42 hw hr hr77 _hcontador hk hf (by omega) h42
  by_cases h43 : S (tiempo a b r) n < 137528045312
  · exact fila_43 hw hr hr77 _hcontador hk hf (by omega) h43
  by_cases h44 : S (tiempo a b r) n < 890638885193
  · exact fila_44 hw hr hr77 _hcontador hk hf (by omega) h44
  by_cases h45 : S (tiempo a b r) n < 1643749725074
  · exact fila_45 hw hr hr77 _hcontador hk hf (by omega) h45
  by_cases h46 : S (tiempo a b r) n < 2396860564955
  · exact fila_46 hw hr hr77 _hcontador hk hf (by omega) h46
  by_cases h47 : S (tiempo a b r) n < 3149971404836
  · exact fila_47 hw hr hr77 _hcontador hk hf (by omega) h47
  by_cases h48 : S (tiempo a b r) n < 3903082244717
  · exact fila_48 hw hr hr77 _hcontador hk hf (by omega) h48
  by_cases h49 : S (tiempo a b r) n < 4656193084598
  · exact fila_49 hw hr hr77 _hcontador hk hf (by omega) h49
  by_cases h50 : S (tiempo a b r) n < 5409303924479
  · exact fila_50 hw hr hr77 _hcontador hk hf (by omega) h50
  by_cases h51 : S (tiempo a b r) n < 11571718688839
  · exact fila_51 hw hr hr77 _hcontador hk hf (by omega) h51
  by_cases h52 : S (tiempo a b r) n < 64021008208555
  · exact fila_52 hw hr hr77 _hcontador hk hf (by omega) h52
  by_cases h53 : S (tiempo a b r) n < 116470297728271
  · exact fila_53 hw hr hr77 _hcontador hk hf (by omega) h53
  by_cases h54 : S (tiempo a b r) n < 168919587247987
  · exact fila_54 hw hr hr77 _hcontador hk hf (by omega) h54
  by_cases h55 : S (tiempo a b r) n < 221368876767703
  · exact fila_55 hw hr hr77 _hcontador hk hf (by omega) h55
  by_cases h56 : S (tiempo a b r) n < 273818166287419
  · exact fila_56 hw hr hr77 _hcontador hk hf (by omega) h56
  by_cases h57 : S (tiempo a b r) n < 326267455807135
  · exact fila_57 hw hr hr77 _hcontador hk hf (by omega) h57
  by_cases h58 : S (tiempo a b r) n < 378716745326851
  · exact fila_58 hw hr hr77 _hcontador hk hf (by omega) h58
  by_cases h59 : S (tiempo a b r) n < 431166034846567
  · exact fila_59 hw hr hr77 _hcontador hk hf (by omega) h59
  by_cases h60 : S (tiempo a b r) n < 914781359212850
  · exact fila_60 hw hr hr77 _hcontador hk hf (by omega) h60
  by_cases h61 : S (tiempo a b r) n < 1398396683579133
  · exact fila_61 hw hr hr77 _hcontador hk hf (by omega) h61
  by_cases h62 : S (tiempo a b r) n < 1882012007945416
  · exact fila_62 hw hr hr77 _hcontador hk hf (by omega) h62
  by_cases h63 : S (tiempo a b r) n < 2365627332311699
  · exact fila_63 hw hr hr77 _hcontador hk hf (by omega) h63
  by_cases h64 : S (tiempo a b r) n < 2849242656677982
  · exact fila_64 hw hr hr77 _hcontador hk hf (by omega) h64
  by_cases h65 : S (tiempo a b r) n < 3332857981044265
  · exact fila_65 hw hr hr77 _hcontador hk hf (by omega) h65
  by_cases h66 : S (tiempo a b r) n < 3816473305410548
  · exact fila_66 hw hr hr77 _hcontador hk hf (by omega) h66
  by_cases h67 : S (tiempo a b r) n < 4300088629776831
  · exact fila_67 hw hr hr77 _hcontador hk hf (by omega) h67
  by_cases h68 : S (tiempo a b r) n < 4783703954143114
  · exact fila_68 hw hr hr77 _hcontador hk hf (by omega) h68
  by_cases h69 : S (tiempo a b r) n < 5267319278509397
  · exact fila_69 hw hr hr77 _hcontador hk hf (by omega) h69
  by_cases h70 : S (tiempo a b r) n < 5750934602875680
  · exact fila_70 hw hr hr77 _hcontador hk hf (by omega) h70
  by_cases h71 : S (tiempo a b r) n < 11985484530117643
  · exact fila_71 hw hr hr77 _hcontador hk hf (by omega) h71
  by_cases h72 : S (tiempo a b r) n < 18220034457359606
  · exact fila_72 hw hr hr77 _hcontador hk hf (by omega) h72
  by_cases h73 : S (tiempo a b r) n < 24454584384601569
  · exact fila_73 hw hr hr77 _hcontador hk hf (by omega) h73
  by_cases h74 : S (tiempo a b r) n < 30689134311843532
  · exact fila_74 hw hr hr77 _hcontador hk hf (by omega) h74
  by_cases h75 : S (tiempo a b r) n < 36923684239085495
  · exact fila_75 hw hr hr77 _hcontador hk hf (by omega) h75
  by_cases h76 : S (tiempo a b r) n < 43158234166327458
  · exact fila_76 hw hr hr77 _hcontador hk hf (by omega) h76
  by_cases h77 : S (tiempo a b r) n < 49392784093569421
  · exact fila_77 hw hr hr77 _hcontador hk hf (by omega) h77
  by_cases h78 : S (tiempo a b r) n < 55627334020811384
  · exact fila_78 hw hr hr77 _hcontador hk hf (by omega) h78
  by_cases h79 : S (tiempo a b r) n < 61861883948053347
  · exact fila_79 hw hr hr77 _hcontador hk hf (by omega) h79
  by_cases h80 : S (tiempo a b r) n < 68096433875295310
  · exact fila_80 hw hr hr77 _hcontador hk hf (by omega) h80
  by_cases h81 : S (tiempo a b r) n < 74330983802537273
  · exact fila_81 hw hr hr77 _hcontador hk hf (by omega) h81
  by_cases h82 : S (tiempo a b r) n < 80565533729779236
  · exact fila_82 hw hr hr77 _hcontador hk hf (by omega) h82
  by_cases h83 : S (tiempo a b r) n < 86800083657021199
  · exact fila_83 hw hr hr77 _hcontador hk hf (by omega) h83
  by_cases h84 : S (tiempo a b r) n < 93034633584263162
  · exact fila_84 hw hr hr77 _hcontador hk hf (by omega) h84
  by_cases h85 : S (tiempo a b r) n < 99269183511505125
  · exact fila_85 hw hr hr77 _hcontador hk hf (by omega) h85
  by_cases h86 : S (tiempo a b r) n < 105503733438747088
  · exact fila_86 hw hr hr77 _hcontador hk hf (by omega) h86
  by_cases h87 : S (tiempo a b r) n < 111738283365989051
  · exact fila_87 hw hr hr77 _hcontador hk hf (by omega) h87
  by_cases h88 : S (tiempo a b r) n < 117972833293231014
  · exact fila_88 hw hr hr77 _hcontador hk hf (by omega) h88
  by_cases h89 : S (tiempo a b r) n < 124207383220472977
  · exact fila_89 hw hr hr77 _hcontador hk hf (by omega) h89
  by_cases h90 : S (tiempo a b r) n < 130441933147714940
  · exact fila_90 hw hr hr77 _hcontador hk hf (by omega) h90
  by_cases h91 : S (tiempo a b r) n < 397560349370386783
  · exact fila_91 hw hr hr77 _hcontador hk hf (by omega) h91
  by_cases h92 : S (tiempo a b r) n < 4640282259296926456
  · exact fila_92 hw hr hr77 _hcontador hk hf (by omega) h92
  by_cases h93 : S (tiempo a b r) n < 27444133206411171953
  · exact fila_93 hw hr hr77 _hcontador hk hf (by omega) h93
  by_cases h94 : S (tiempo a b r) n < 77692117359936589403
  · exact fila_94 hw hr hr77 _hcontador hk hf (by omega) h94
  by_cases h95 : S (tiempo a b r) n < 205632218873398596256
  · exact fila_95 hw hr hr77 _hcontador hk hf (by omega) h95
  exact fila_96 hw hr hr77 _hcontador hk hf (by omega) hq

end OcelotasSetentaYSieteTabla

#print axioms OcelotasSetentaYSieteTabla.pequeno_de_tabla
