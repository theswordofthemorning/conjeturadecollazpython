import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasCuarentaYUnaTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_57 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 41)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 273818166287419 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 326267455807135) : n < 200000000001 := by
  have hU : (2834933961957374631684964039519518612509 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (433991525581789 : ℝ) * log 2 - 273818166287419 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 433991525581789) (Q := 273818166287419) (p := 83130157078217) (v := 52449289519716)
    (c := (2834933961957374631684964039519518612509 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 273818166287419 + 52449289519716) hk.2
  by_cases hsmall : n < 200000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 7231209007015393)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 400000000002
    · exact OcelotasPesos.pieza_cadena (m := 39) (nsup := 400000000002) (qmin := 273818166287419)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 800000000006
    · exact OcelotasPesos.pieza_cadena (m := 40) (nsup := 800000000006) (qmin := 273818166287419)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 1600000000014
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1600000000014) (qmin := 273818166287419)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 3200000000030
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 3200000000030) (qmin := 273818166287419)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 6400000000062
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 6400000000062) (qmin := 273818166287419)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 12800000000126
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 12800000000126) (qmin := 273818166287419)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 25600000000254
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 25600000000254) (qmin := 273818166287419)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 51200000000510
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 51200000000510) (qmin := 273818166287419)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 102400000001022
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 102400000001022) (qmin := 273818166287419)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 204800000002046
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 204800000002046) (qmin := 273818166287419)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 409600000004094
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 409600000004094) (qmin := 273818166287419)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 819200000008190
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 819200000008190) (qmin := 273818166287419)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 1638400000016382
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1638400000016382) (qmin := 273818166287419)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 3276800000032766
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 3276800000032766) (qmin := 273818166287419)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 6553600000065534
    · exact OcelotasPesos.pieza_cadena (m := 53) (nsup := 6553600000065534) (qmin := 273818166287419)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 53) (h0 := 21) (ninf := 6553600000065535)
        (nsup := 7231209007015392) (qmin := 273818166287419) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

theorem fila_58 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 41)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 326267455807135 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 378716745326851) : n < 200000000001 := by
  have hU : (264031560027138462676789773840144889469 / 62500000000000000000000000000000000000000000000000000 : ℝ) ≤ (517121682660006 : ℝ) * log 2 - 326267455807135 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 517121682660006) (Q := 326267455807135) (p := 83130157078217) (v := 52449289519716)
    (c := (264031560027138462676789773840144889469 / 62500000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 326267455807135 + 52449289519716) hk.2
  by_cases hsmall : n < 200000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 9705279170931739)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 400000000002
    · exact OcelotasPesos.pieza_cadena (m := 39) (nsup := 400000000002) (qmin := 326267455807135)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 800000000006
    · exact OcelotasPesos.pieza_cadena (m := 40) (nsup := 800000000006) (qmin := 326267455807135)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 1600000000014
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1600000000014) (qmin := 326267455807135)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 3200000000030
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 3200000000030) (qmin := 326267455807135)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 6400000000062
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 6400000000062) (qmin := 326267455807135)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 12800000000126
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 12800000000126) (qmin := 326267455807135)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 25600000000254
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 25600000000254) (qmin := 326267455807135)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 51200000000510
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 51200000000510) (qmin := 326267455807135)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 102400000001022
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 102400000001022) (qmin := 326267455807135)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 204800000002046
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 204800000002046) (qmin := 326267455807135)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 409600000004094
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 409600000004094) (qmin := 326267455807135)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 819200000008190
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 819200000008190) (qmin := 326267455807135)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 1638400000016382
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1638400000016382) (qmin := 326267455807135)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 3276800000032766
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 3276800000032766) (qmin := 326267455807135)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 6553600000065534
    · exact OcelotasPesos.pieza_cadena (m := 53) (nsup := 6553600000065534) (qmin := 326267455807135)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 54) (h0 := 12) (ninf := 6553600000065535)
        (nsup := 9705279170931738) (qmin := 326267455807135) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

end OcelotasCuarentaYUnaTabla

#print axioms OcelotasCuarentaYUnaTabla.fila_57
#print axioms OcelotasCuarentaYUnaTabla.fila_58
