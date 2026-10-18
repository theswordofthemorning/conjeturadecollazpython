import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasCuarentaYSieteTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_58 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 47)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 326267455807135 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 378716745326851) : n < 1200000000001 := by
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
  by_cases hsmall : n < 1200000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 11125563927653457)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 2400000000002
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2400000000002) (qmin := 326267455807135)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 4800000000006
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4800000000006) (qmin := 326267455807135)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 9600000000014
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 9600000000014) (qmin := 326267455807135)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 19200000000030
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 19200000000030) (qmin := 326267455807135)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 38400000000062
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 38400000000062) (qmin := 326267455807135)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 76800000000126
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 76800000000126) (qmin := 326267455807135)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 153600000000254
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 153600000000254) (qmin := 326267455807135)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 307200000000510
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 307200000000510) (qmin := 326267455807135)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 614400000001022
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 614400000001022) (qmin := 326267455807135)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 1228800000002046
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1228800000002046) (qmin := 326267455807135)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 2457600000004094
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 2457600000004094) (qmin := 326267455807135)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 4915200000008190
    · exact OcelotasPesos.pieza_cadena (m := 53) (nsup := 4915200000008190) (qmin := 326267455807135)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 9830400000016382
    · exact OcelotasPesos.pieza_cadena (m := 54) (nsup := 9830400000016382) (qmin := 326267455807135)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 54) (h0 := 32) (ninf := 9830400000016383)
        (nsup := 11125563927653456) (qmin := 326267455807135) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

theorem fila_59 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 47)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 378716745326851 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 431166034846567) : n < 1200000000001 := by
  have hU : (277914199695368154228734468384559923799 / 100000000000000000000000000000000000000000000000000000 : ℝ) ≤ (600251839738223 : ℝ) * log 2 - 378716745326851 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 600251839738223) (Q := 378716745326851) (p := 83130157078217) (v := 52449289519716)
    (c := (277914199695368154228734468384559923799 / 100000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 378716745326851 + 52449289519716) hk.2
  by_cases hsmall : n < 1200000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 16911694347218821)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 2400000000002
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2400000000002) (qmin := 378716745326851)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 4800000000006
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4800000000006) (qmin := 378716745326851)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 9600000000014
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 9600000000014) (qmin := 378716745326851)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 19200000000030
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 19200000000030) (qmin := 378716745326851)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 38400000000062
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 38400000000062) (qmin := 378716745326851)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 76800000000126
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 76800000000126) (qmin := 378716745326851)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 153600000000254
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 153600000000254) (qmin := 378716745326851)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 307200000000510
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 307200000000510) (qmin := 378716745326851)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 614400000001022
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 614400000001022) (qmin := 378716745326851)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 1228800000002046
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1228800000002046) (qmin := 378716745326851)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 2457600000004094
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 2457600000004094) (qmin := 378716745326851)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 4915200000008190
    · exact OcelotasPesos.pieza_cadena (m := 53) (nsup := 4915200000008190) (qmin := 378716745326851)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 9830400000016382
    · exact OcelotasPesos.pieza_cadena (m := 54) (nsup := 9830400000016382) (qmin := 378716745326851)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 54) (nsup := 16911694347218820) (qmin := 378716745326851)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

end OcelotasCuarentaYSieteTabla

#print axioms OcelotasCuarentaYSieteTabla.fila_58
#print axioms OcelotasCuarentaYSieteTabla.fila_59
