import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasOchentaYUnoTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_99 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 23414628818361028801231 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 31150961018190238869556) : n < 28000000000000000001 := by
  have hU : (11275607018912242405349016842273 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (37111308645407146420177 : ℝ) * log 2 - 23414628818361028801231 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (12261796429850908150604 : ℝ) * log 2 - 7736332199829210068325 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 37111308645407146420177) (Q := 23414628818361028801231) (p := 12261796429850908150604) (v := 7736332199829210068325)
    (c := (11275607018912242405349016842273 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 23414628818361028801231 + 7736332199829210068325) hk.2
  by_cases hsmall : n < 28000000000000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 3591824363164710065399641)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 56000000000000000002
    · exact OcelotasPesos.pieza_cadena (m := 66) (nsup := 56000000000000000002) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 112000000000000000006
    · exact OcelotasPesos.pieza_cadena (m := 67) (nsup := 112000000000000000006) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 224000000000000000014
    · exact OcelotasPesos.pieza_cadena (m := 68) (nsup := 224000000000000000014) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 448000000000000000030
    · exact OcelotasPesos.pieza_cadena (m := 69) (nsup := 448000000000000000030) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 896000000000000000062
    · exact OcelotasPesos.pieza_cadena (m := 70) (nsup := 896000000000000000062) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 1792000000000000000126
    · exact OcelotasPesos.pieza_cadena (m := 71) (nsup := 1792000000000000000126) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 3584000000000000000254
    · exact OcelotasPesos.pieza_cadena (m := 72) (nsup := 3584000000000000000254) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 7168000000000000000510
    · exact OcelotasPesos.pieza_cadena (m := 73) (nsup := 7168000000000000000510) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 14336000000000000001022
    · exact OcelotasPesos.pieza_cadena (m := 74) (nsup := 14336000000000000001022) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 28672000000000000002046
    · exact OcelotasPesos.pieza_cadena (m := 75) (nsup := 28672000000000000002046) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 57344000000000000004094
    · exact OcelotasPesos.pieza_cadena (m := 76) (nsup := 57344000000000000004094) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 114688000000000000008190
    · exact OcelotasPesos.pieza_cadena (m := 77) (nsup := 114688000000000000008190) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 229376000000000000016382
    · exact OcelotasPesos.pieza_cadena (m := 78) (nsup := 229376000000000000016382) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 458752000000000000032766
    · exact OcelotasPesos.pieza_cadena (m := 79) (nsup := 458752000000000000032766) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 917504000000000000065534
    · exact OcelotasPesos.pieza_cadena (m := 80) (nsup := 917504000000000000065534) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp15 : n ≤ 1835008000000000000131070
    · exact OcelotasPesos.pieza_cadena (m := 81) (nsup := 1835008000000000000131070) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp15 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 82) (nsup := 3591824363164710065399640) (qmin := 23414628818361028801231)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

theorem fila_100 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 31150961018190238869556 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 38887293218019448937881) : n < 28000000000000000001 := by
  have hU : (199550650955905852614135825031 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (49373105075258054570781 : ℝ) * log 2 - 31150961018190238869556 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (12261796429850908150604 : ℝ) * log 2 - 7736332199829210068325 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 49373105075258054570781) (Q := 31150961018190238869556) (p := 12261796429850908150604) (v := 7736332199829210068325)
    (c := (199550650955905852614135825031 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 31150961018190238869556 + 7736332199829210068325) hk.2
  by_cases hsmall : n < 28000000000000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 202955990401400250774443114)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 56000000000000000002
    · exact OcelotasPesos.pieza_cadena (m := 66) (nsup := 56000000000000000002) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 112000000000000000006
    · exact OcelotasPesos.pieza_cadena (m := 67) (nsup := 112000000000000000006) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 224000000000000000014
    · exact OcelotasPesos.pieza_cadena (m := 68) (nsup := 224000000000000000014) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 448000000000000000030
    · exact OcelotasPesos.pieza_cadena (m := 69) (nsup := 448000000000000000030) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 896000000000000000062
    · exact OcelotasPesos.pieza_cadena (m := 70) (nsup := 896000000000000000062) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 1792000000000000000126
    · exact OcelotasPesos.pieza_cadena (m := 71) (nsup := 1792000000000000000126) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 3584000000000000000254
    · exact OcelotasPesos.pieza_cadena (m := 72) (nsup := 3584000000000000000254) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 7168000000000000000510
    · exact OcelotasPesos.pieza_cadena (m := 73) (nsup := 7168000000000000000510) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 14336000000000000001022
    · exact OcelotasPesos.pieza_cadena (m := 74) (nsup := 14336000000000000001022) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 28672000000000000002046
    · exact OcelotasPesos.pieza_cadena (m := 75) (nsup := 28672000000000000002046) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 57344000000000000004094
    · exact OcelotasPesos.pieza_cadena (m := 76) (nsup := 57344000000000000004094) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 114688000000000000008190
    · exact OcelotasPesos.pieza_cadena (m := 77) (nsup := 114688000000000000008190) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 229376000000000000016382
    · exact OcelotasPesos.pieza_cadena (m := 78) (nsup := 229376000000000000016382) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 458752000000000000032766
    · exact OcelotasPesos.pieza_cadena (m := 79) (nsup := 458752000000000000032766) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 917504000000000000065534
    · exact OcelotasPesos.pieza_cadena (m := 80) (nsup := 917504000000000000065534) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp15 : n ≤ 1835008000000000000131070
    · exact OcelotasPesos.pieza_cadena (m := 81) (nsup := 1835008000000000000131070) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp15 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp16 : n ≤ 3670016000000000000262142
    · exact OcelotasPesos.pieza_cadena (m := 82) (nsup := 3670016000000000000262142) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp16 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp17 : n ≤ 7340032000000000000524286
    · exact OcelotasPesos.pieza_cadena (m := 83) (nsup := 7340032000000000000524286) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp17 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp18 : n ≤ 14680064000000000001048574
    · exact OcelotasPesos.pieza_cadena (m := 84) (nsup := 14680064000000000001048574) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp18 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp19 : n ≤ 29360128000000000002097150
    · exact OcelotasPesos.pieza_cadena (m := 85) (nsup := 29360128000000000002097150) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp19 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp20 : n ≤ 58720256000000000004194302
    · exact OcelotasPesos.pieza_cadena (m := 86) (nsup := 58720256000000000004194302) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp20 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp21 : n ≤ 117440512000000000008388606
    · exact OcelotasPesos.pieza_cadena (m := 87) (nsup := 117440512000000000008388606) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp21 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 88) (nsup := 202955990401400250774443113) (qmin := 31150961018190238869556)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

end OcelotasOchentaYUnoTabla

#print axioms OcelotasOchentaYUnoTabla.fila_99
#print axioms OcelotasOchentaYUnoTabla.fila_100
