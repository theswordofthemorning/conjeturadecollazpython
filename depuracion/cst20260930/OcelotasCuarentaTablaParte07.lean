import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasCuarentaTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_51 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 40)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 5409303924479 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 11571718688839) : n < 68719476737 := by
  have hU : (32964388335033813345461612266354939978227 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (8573543875303 : ℝ) * log 2 - 5409303924479 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9767196315401 : ℝ) * log 2 - 6162414764360 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 8573543875303) (Q := 5409303924479) (p := 9767196315401) (v := 6162414764360)
    (c := (32964388335033813345461612266354939978227 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 5409303924479 + 6162414764360) hk.2
  by_cases hsmall : n < 68719476737
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 606715337676825)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 137438953474
    · exact OcelotasPesos.pieza_cadena (m := 38) (nsup := 137438953474) (qmin := 5409303924479)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 274877906950
    · exact OcelotasPesos.pieza_cadena (m := 39) (nsup := 274877906950) (qmin := 5409303924479)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 549755813902
    · exact OcelotasPesos.pieza_cadena (m := 40) (nsup := 549755813902) (qmin := 5409303924479)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 1099511627806
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1099511627806) (qmin := 5409303924479)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 2199023255614
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2199023255614) (qmin := 5409303924479)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 4398046511230
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4398046511230) (qmin := 5409303924479)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 8796093022462
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 8796093022462) (qmin := 5409303924479)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 17592186044926
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 17592186044926) (qmin := 5409303924479)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 35184372089854
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 35184372089854) (qmin := 5409303924479)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 70368744179710
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 70368744179710) (qmin := 5409303924479)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 140737488359422
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 140737488359422) (qmin := 5409303924479)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 281474976718846
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 281474976718846) (qmin := 5409303924479)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 562949953437694
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 562949953437694) (qmin := 5409303924479)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 50) (h0 := 33) (ninf := 562949953437695)
        (nsup := 606715337676824) (qmin := 5409303924479) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

theorem fila_52 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 40)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 11571718688839 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 64021008208555) : n < 68719476737 := by
  have hU : (3224170685329354641519096641755658048147 / 250000000000000000000000000000000000000000000000000000 : ℝ) ≤ (18340740190704 : ℝ) * log 2 - 11571718688839 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 18340740190704) (Q := 11571718688839) (p := 83130157078217) (v := 52449289519716)
    (c := (3224170685329354641519096641755658048147 / 250000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 11571718688839 + 52449289519716) hk.2
  by_cases hsmall : n < 68719476737
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 3101572768930031)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 137438953474
    · exact OcelotasPesos.pieza_cadena (m := 38) (nsup := 137438953474) (qmin := 11571718688839)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 274877906950
    · exact OcelotasPesos.pieza_cadena (m := 39) (nsup := 274877906950) (qmin := 11571718688839)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 549755813902
    · exact OcelotasPesos.pieza_cadena (m := 40) (nsup := 549755813902) (qmin := 11571718688839)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 1099511627806
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1099511627806) (qmin := 11571718688839)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 2199023255614
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2199023255614) (qmin := 11571718688839)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 4398046511230
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4398046511230) (qmin := 11571718688839)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 8796093022462
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 8796093022462) (qmin := 11571718688839)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 17592186044926
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 17592186044926) (qmin := 11571718688839)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 35184372089854
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 35184372089854) (qmin := 11571718688839)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 70368744179710
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 70368744179710) (qmin := 11571718688839)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 140737488359422
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 140737488359422) (qmin := 11571718688839)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 281474976718846
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 281474976718846) (qmin := 11571718688839)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 562949953437694
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 562949953437694) (qmin := 11571718688839)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 1125899906875390
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1125899906875390) (qmin := 11571718688839)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 2251799813750782
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 2251799813750782) (qmin := 11571718688839)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 52) (h0 := 4) (ninf := 2251799813750783)
        (nsup := 3101572768930030) (qmin := 11571718688839) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

end OcelotasCuarentaTabla

#print axioms OcelotasCuarentaTabla.fila_51
#print axioms OcelotasCuarentaTabla.fila_52
