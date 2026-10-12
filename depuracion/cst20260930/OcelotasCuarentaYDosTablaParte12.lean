import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasCuarentaYDosTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_61 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 42)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 914781359212850 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 1398396683579133) : n < 300000000001 := by
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
  by_cases hsmall : n < 300000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 34364398843442581)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 600000000002
    · exact OcelotasPesos.pieza_cadena (m := 40) (nsup := 600000000002) (qmin := 914781359212850)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 1200000000006
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1200000000006) (qmin := 914781359212850)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 2400000000014
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2400000000014) (qmin := 914781359212850)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 4800000000030
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4800000000030) (qmin := 914781359212850)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 9600000000062
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 9600000000062) (qmin := 914781359212850)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 19200000000126
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 19200000000126) (qmin := 914781359212850)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 38400000000254
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 38400000000254) (qmin := 914781359212850)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 76800000000510
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 76800000000510) (qmin := 914781359212850)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 153600000001022
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 153600000001022) (qmin := 914781359212850)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 307200000002046
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 307200000002046) (qmin := 914781359212850)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 614400000004094
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 614400000004094) (qmin := 914781359212850)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 1228800000008190
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1228800000008190) (qmin := 914781359212850)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 2457600000016382
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 2457600000016382) (qmin := 914781359212850)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 4915200000032766
    · exact OcelotasPesos.pieza_cadena (m := 53) (nsup := 4915200000032766) (qmin := 914781359212850)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 9830400000065534
    · exact OcelotasPesos.pieza_cadena (m := 54) (nsup := 9830400000065534) (qmin := 914781359212850)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp15 : n ≤ 19660800000131070
    · exact OcelotasPesos.pieza_cadena (m := 55) (nsup := 19660800000131070) (qmin := 914781359212850)
        hn0 hw hr hrR hp15 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 55) (nsup := 34364398843442580) (qmin := 914781359212850)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

theorem fila_62 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 42)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 1398396683579133 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 1882012007945416) : n < 300000000001 := by
  have hU : (1388263966822969155194469454441503433 / 1250000000000000000000000000000000000000000000000000 : ℝ) ≤ (2216406304605754 : ℝ) * log 2 - 1398396683579133 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (766512153894657 : ℝ) * log 2 - 483615324366283 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 2216406304605754) (Q := 1398396683579133) (p := 766512153894657) (v := 483615324366283)
    (c := (1388263966822969155194469454441503433 / 1250000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 1398396683579133 + 483615324366283) hk.2
  by_cases hsmall : n < 300000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 37817015534982029)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 600000000002
    · exact OcelotasPesos.pieza_cadena (m := 40) (nsup := 600000000002) (qmin := 1398396683579133)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 1200000000006
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1200000000006) (qmin := 1398396683579133)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 2400000000014
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2400000000014) (qmin := 1398396683579133)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 4800000000030
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4800000000030) (qmin := 1398396683579133)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 9600000000062
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 9600000000062) (qmin := 1398396683579133)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 19200000000126
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 19200000000126) (qmin := 1398396683579133)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 38400000000254
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 38400000000254) (qmin := 1398396683579133)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 76800000000510
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 76800000000510) (qmin := 1398396683579133)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 153600000001022
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 153600000001022) (qmin := 1398396683579133)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 307200000002046
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 307200000002046) (qmin := 1398396683579133)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 614400000004094
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 614400000004094) (qmin := 1398396683579133)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 1228800000008190
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1228800000008190) (qmin := 1398396683579133)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 2457600000016382
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 2457600000016382) (qmin := 1398396683579133)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 4915200000032766
    · exact OcelotasPesos.pieza_cadena (m := 53) (nsup := 4915200000032766) (qmin := 1398396683579133)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 9830400000065534
    · exact OcelotasPesos.pieza_cadena (m := 54) (nsup := 9830400000065534) (qmin := 1398396683579133)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp15 : n ≤ 19660800000131070
    · exact OcelotasPesos.pieza_cadena (m := 55) (nsup := 19660800000131070) (qmin := 1398396683579133)
        hn0 hw hr hrR hp15 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 56) (nsup := 37817015534982028) (qmin := 1398396683579133)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

end OcelotasCuarentaYDosTabla

#print axioms OcelotasCuarentaYDosTabla.fila_61
#print axioms OcelotasCuarentaYDosTabla.fila_62
