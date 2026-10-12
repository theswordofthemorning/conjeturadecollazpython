import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasCuarentaTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_53 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 40)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 64021008208555 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 116470297728271) : n < 68719476737 := by
  have hU : (5725659888918442352767547434712956599537 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (101470897268921 : ℝ) * log 2 - 64021008208555 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 101470897268921) (Q := 64021008208555) (p := 83130157078217) (v := 52449289519716)
    (c := (5725659888918442352767547434712956599537 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 64021008208555 + 52449289519716) hk.2
  by_cases hsmall : n < 68719476737
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 3493047157535222)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 137438953474
    · exact OcelotasPesos.pieza_cadena (m := 38) (nsup := 137438953474) (qmin := 64021008208555)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 274877906950
    · exact OcelotasPesos.pieza_cadena (m := 39) (nsup := 274877906950) (qmin := 64021008208555)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 549755813902
    · exact OcelotasPesos.pieza_cadena (m := 40) (nsup := 549755813902) (qmin := 64021008208555)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 1099511627806
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1099511627806) (qmin := 64021008208555)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 2199023255614
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2199023255614) (qmin := 64021008208555)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 4398046511230
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4398046511230) (qmin := 64021008208555)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 8796093022462
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 8796093022462) (qmin := 64021008208555)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 17592186044926
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 17592186044926) (qmin := 64021008208555)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 35184372089854
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 35184372089854) (qmin := 64021008208555)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 70368744179710
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 70368744179710) (qmin := 64021008208555)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 140737488359422
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 140737488359422) (qmin := 64021008208555)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 281474976718846
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 281474976718846) (qmin := 64021008208555)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 562949953437694
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 562949953437694) (qmin := 64021008208555)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 1125899906875390
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1125899906875390) (qmin := 64021008208555)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 2251799813750782
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 2251799813750782) (qmin := 64021008208555)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 3493047157535221) (qmin := 64021008208555)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

theorem fila_54 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 40)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 116470297728271 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 168919587247987) : n < 68719476737 := by
  have hU : (250148920358908771124845079295729855139 / 25000000000000000000000000000000000000000000000000000 : ℝ) ≤ (184601054347138 : ℝ) * log 2 - 116470297728271 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 184601054347138) (Q := 116470297728271) (p := 83130157078217) (v := 52449289519716)
    (c := (250148920358908771124845079295729855139 / 25000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 116470297728271 + 52449289519716) hk.2
  by_cases hsmall : n < 68719476737
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 3997618692757977)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 137438953474
    · exact OcelotasPesos.pieza_cadena (m := 38) (nsup := 137438953474) (qmin := 116470297728271)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 274877906950
    · exact OcelotasPesos.pieza_cadena (m := 39) (nsup := 274877906950) (qmin := 116470297728271)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 549755813902
    · exact OcelotasPesos.pieza_cadena (m := 40) (nsup := 549755813902) (qmin := 116470297728271)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 1099511627806
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1099511627806) (qmin := 116470297728271)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 2199023255614
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2199023255614) (qmin := 116470297728271)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 4398046511230
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4398046511230) (qmin := 116470297728271)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 8796093022462
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 8796093022462) (qmin := 116470297728271)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 17592186044926
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 17592186044926) (qmin := 116470297728271)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 35184372089854
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 35184372089854) (qmin := 116470297728271)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 70368744179710
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 70368744179710) (qmin := 116470297728271)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 140737488359422
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 140737488359422) (qmin := 116470297728271)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 281474976718846
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 281474976718846) (qmin := 116470297728271)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 562949953437694
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 562949953437694) (qmin := 116470297728271)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 1125899906875390
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1125899906875390) (qmin := 116470297728271)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 2251799813750782
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 2251799813750782) (qmin := 116470297728271)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 3997618692757976) (qmin := 116470297728271)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

end OcelotasCuarentaTabla

#print axioms OcelotasCuarentaTabla.fila_53
#print axioms OcelotasCuarentaTabla.fila_54
