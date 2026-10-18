import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasCuarentaYSieteTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_60 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 47)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 431166034846567 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 914781359212850) : n < 1200000000001 := by
  have hU : (333444758368286920436513246562220061119 / 250000000000000000000000000000000000000000000000000000 : ℝ) ≤ (683381996816440 : ℝ) * log 2 - 431166034846567 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (766512153894657 : ℝ) * log 2 - 483615324366283 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 683381996816440) (Q := 431166034846567) (p := 766512153894657) (v := 483615324366283)
    (c := (333444758368286920436513246562220061119 / 250000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 431166034846567 + 483615324366283) hk.2
  by_cases hsmall : n < 1200000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 35238220740067008)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 2400000000002
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2400000000002) (qmin := 431166034846567)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 4800000000006
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4800000000006) (qmin := 431166034846567)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 9600000000014
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 9600000000014) (qmin := 431166034846567)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 19200000000030
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 19200000000030) (qmin := 431166034846567)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 38400000000062
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 38400000000062) (qmin := 431166034846567)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 76800000000126
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 76800000000126) (qmin := 431166034846567)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 153600000000254
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 153600000000254) (qmin := 431166034846567)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 307200000000510
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 307200000000510) (qmin := 431166034846567)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 614400000001022
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 614400000001022) (qmin := 431166034846567)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 1228800000002046
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1228800000002046) (qmin := 431166034846567)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 2457600000004094
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 2457600000004094) (qmin := 431166034846567)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 4915200000008190
    · exact OcelotasPesos.pieza_cadena (m := 53) (nsup := 4915200000008190) (qmin := 431166034846567)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 9830400000016382
    · exact OcelotasPesos.pieza_cadena (m := 54) (nsup := 9830400000016382) (qmin := 431166034846567)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 19660800000032766
    · exact OcelotasPesos.pieza_cadena (m := 55) (nsup := 19660800000032766) (qmin := 431166034846567)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 55) (nsup := 35238220740067007) (qmin := 431166034846567)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

theorem fila_61 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 47)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 914781359212850 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 1398396683579133) : n < 1200000000001 := by
  have hU : (611097551732880751475407137450520747719 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (1449894150711097 : ℝ) * log 2 - 914781359212850 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (766512153894657 : ℝ) * log 2 - 483615324366283 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 1449894150711097) (Q := 914781359212850) (p := 766512153894657) (v := 483615324366283)
    (c := (611097551732880751475407137450520747719 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 914781359212850 + 483615324366283) hk.2
  by_cases hsmall : n < 1200000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 38455398705757174)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 2400000000002
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2400000000002) (qmin := 914781359212850)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 4800000000006
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4800000000006) (qmin := 914781359212850)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 9600000000014
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 9600000000014) (qmin := 914781359212850)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 19200000000030
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 19200000000030) (qmin := 914781359212850)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 38400000000062
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 38400000000062) (qmin := 914781359212850)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 76800000000126
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 76800000000126) (qmin := 914781359212850)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 153600000000254
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 153600000000254) (qmin := 914781359212850)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 307200000000510
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 307200000000510) (qmin := 914781359212850)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 614400000001022
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 614400000001022) (qmin := 914781359212850)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 1228800000002046
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1228800000002046) (qmin := 914781359212850)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 2457600000004094
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 2457600000004094) (qmin := 914781359212850)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 4915200000008190
    · exact OcelotasPesos.pieza_cadena (m := 53) (nsup := 4915200000008190) (qmin := 914781359212850)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 9830400000016382
    · exact OcelotasPesos.pieza_cadena (m := 54) (nsup := 9830400000016382) (qmin := 914781359212850)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 19660800000032766
    · exact OcelotasPesos.pieza_cadena (m := 55) (nsup := 19660800000032766) (qmin := 914781359212850)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 56) (nsup := 38455398705757173) (qmin := 914781359212850)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

end OcelotasCuarentaYSieteTabla

#print axioms OcelotasCuarentaYSieteTabla.fila_60
#print axioms OcelotasCuarentaYSieteTabla.fila_61
