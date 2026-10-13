import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasCuarentaYSeisTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_62 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 46)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 1398396683579133 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 1882012007945416) : n < 700000000001 := by
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
  by_cases hsmall : n < 700000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 41418636062123175)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 1400000000002
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1400000000002) (qmin := 1398396683579133)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 2800000000006
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2800000000006) (qmin := 1398396683579133)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 5600000000014
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 5600000000014) (qmin := 1398396683579133)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 11200000000030
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 11200000000030) (qmin := 1398396683579133)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 22400000000062
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 22400000000062) (qmin := 1398396683579133)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 44800000000126
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 44800000000126) (qmin := 1398396683579133)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 89600000000254
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 89600000000254) (qmin := 1398396683579133)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 179200000000510
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 179200000000510) (qmin := 1398396683579133)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 358400000001022
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 358400000001022) (qmin := 1398396683579133)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 716800000002046
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 716800000002046) (qmin := 1398396683579133)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 1433600000004094
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1433600000004094) (qmin := 1398396683579133)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 2867200000008190
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 2867200000008190) (qmin := 1398396683579133)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 5734400000016382
    · exact OcelotasPesos.pieza_cadena (m := 53) (nsup := 5734400000016382) (qmin := 1398396683579133)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 11468800000032766
    · exact OcelotasPesos.pieza_cadena (m := 54) (nsup := 11468800000032766) (qmin := 1398396683579133)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 22937600000065534
    · exact OcelotasPesos.pieza_cadena (m := 55) (nsup := 22937600000065534) (qmin := 1398396683579133)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 56) (nsup := 41418636062123174) (qmin := 1398396683579133)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

theorem fila_63 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 46)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 1882012007945416 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 2365627332311699) : n < 700000000001 := by
  have hU : (499513621725494572680168426102681998681 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (2982918458500411 : ℝ) * log 2 - 1882012007945416 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (766512153894657 : ℝ) * log 2 - 483615324366283 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 2982918458500411) (Q := 1882012007945416) (p := 766512153894657) (v := 483615324366283)
    (c := (499513621725494572680168426102681998681 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 1882012007945416 + 483615324366283) hk.2
  by_cases hsmall : n < 700000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 46044790371381594)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 1400000000002
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1400000000002) (qmin := 1882012007945416)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 2800000000006
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2800000000006) (qmin := 1882012007945416)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 5600000000014
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 5600000000014) (qmin := 1882012007945416)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 11200000000030
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 11200000000030) (qmin := 1882012007945416)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 22400000000062
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 22400000000062) (qmin := 1882012007945416)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 44800000000126
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 44800000000126) (qmin := 1882012007945416)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 89600000000254
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 89600000000254) (qmin := 1882012007945416)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 179200000000510
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 179200000000510) (qmin := 1882012007945416)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 358400000001022
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 358400000001022) (qmin := 1882012007945416)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 716800000002046
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 716800000002046) (qmin := 1882012007945416)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 1433600000004094
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1433600000004094) (qmin := 1882012007945416)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 2867200000008190
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 2867200000008190) (qmin := 1882012007945416)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 5734400000016382
    · exact OcelotasPesos.pieza_cadena (m := 53) (nsup := 5734400000016382) (qmin := 1882012007945416)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 11468800000032766
    · exact OcelotasPesos.pieza_cadena (m := 54) (nsup := 11468800000032766) (qmin := 1882012007945416)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 22937600000065534
    · exact OcelotasPesos.pieza_cadena (m := 55) (nsup := 22937600000065534) (qmin := 1882012007945416)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp15 : n ≤ 45875200000131070
    · exact OcelotasPesos.pieza_cadena (m := 56) (nsup := 45875200000131070) (qmin := 1882012007945416)
        hn0 hw hr hrR hp15 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 56) (h0 := 45) (ninf := 45875200000131071)
        (nsup := 46044790371381593) (qmin := 1882012007945416) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

end OcelotasCuarentaYSeisTabla

#print axioms OcelotasCuarentaYSeisTabla.fila_62
#print axioms OcelotasCuarentaYSeisTabla.fila_63
