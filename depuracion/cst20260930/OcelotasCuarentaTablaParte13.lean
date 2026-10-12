import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasCuarentaTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_63 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 40)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 1882012007945416 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 2365627332311699) : n < 68719476737 := by
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
  by_cases hsmall : n < 68719476737
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 40038948149027473)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 137438953474
    · exact OcelotasPesos.pieza_cadena (m := 38) (nsup := 137438953474) (qmin := 1882012007945416)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 274877906950
    · exact OcelotasPesos.pieza_cadena (m := 39) (nsup := 274877906950) (qmin := 1882012007945416)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 549755813902
    · exact OcelotasPesos.pieza_cadena (m := 40) (nsup := 549755813902) (qmin := 1882012007945416)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 1099511627806
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1099511627806) (qmin := 1882012007945416)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 2199023255614
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2199023255614) (qmin := 1882012007945416)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 4398046511230
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4398046511230) (qmin := 1882012007945416)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 8796093022462
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 8796093022462) (qmin := 1882012007945416)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 17592186044926
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 17592186044926) (qmin := 1882012007945416)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 35184372089854
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 35184372089854) (qmin := 1882012007945416)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 70368744179710
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 70368744179710) (qmin := 1882012007945416)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 140737488359422
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 140737488359422) (qmin := 1882012007945416)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 281474976718846
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 281474976718846) (qmin := 1882012007945416)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 562949953437694
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 562949953437694) (qmin := 1882012007945416)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 1125899906875390
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1125899906875390) (qmin := 1882012007945416)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 2251799813750782
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 2251799813750782) (qmin := 1882012007945416)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp15 : n ≤ 4503599627501566
    · exact OcelotasPesos.pieza_cadena (m := 53) (nsup := 4503599627501566) (qmin := 1882012007945416)
        hn0 hw hr hrR hp15 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp16 : n ≤ 9007199255003134
    · exact OcelotasPesos.pieza_cadena (m := 54) (nsup := 9007199255003134) (qmin := 1882012007945416)
        hn0 hw hr hrR hp16 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp17 : n ≤ 18014398510006270
    · exact OcelotasPesos.pieza_cadena (m := 55) (nsup := 18014398510006270) (qmin := 1882012007945416)
        hn0 hw hr hrR hp17 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp18 : n ≤ 36028797020012542
    · exact OcelotasPesos.pieza_cadena (m := 56) (nsup := 36028797020012542) (qmin := 1882012007945416)
        hn0 hw hr hrR hp18 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 56) (h0 := 30) (ninf := 36028797020012543)
        (nsup := 40038948149027472) (qmin := 1882012007945416) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

end OcelotasCuarentaTabla

#print axioms OcelotasCuarentaTabla.fila_63
