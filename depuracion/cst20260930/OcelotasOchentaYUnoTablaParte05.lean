import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasOchentaYUnoTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_95 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 77692117359936589403 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 205632218873398596256) : n < 28000000000000000001 := by
  have hU : (425554887258410978741943489247301 / 125000000000000000000000000000000000000000000000000000 : ℝ) ≤ (123139092617126647266 : ℝ) * log 2 - 77692117359936589403 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (202780263237295321099 : ℝ) * log 2 - 127940101513462006853 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 123139092617126647266) (Q := 77692117359936589403) (p := 202780263237295321099) (v := 127940101513462006853)
    (c := (425554887258410978741943489247301 / 125000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 77692117359936589403 + 127940101513462006853) hk.2
  by_cases hsmall : n < 28000000000000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 23792465562384120117837)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 56000000000000000002
    · exact OcelotasPesos.pieza_cadena (m := 66) (nsup := 56000000000000000002) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 112000000000000000006
    · exact OcelotasPesos.pieza_cadena (m := 67) (nsup := 112000000000000000006) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 224000000000000000014
    · exact OcelotasPesos.pieza_cadena (m := 68) (nsup := 224000000000000000014) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 448000000000000000030
    · exact OcelotasPesos.pieza_cadena (m := 69) (nsup := 448000000000000000030) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 896000000000000000062
    · exact OcelotasPesos.pieza_cadena (m := 70) (nsup := 896000000000000000062) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 1792000000000000000126
    · exact OcelotasPesos.pieza_cadena (m := 71) (nsup := 1792000000000000000126) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 3584000000000000000254
    · exact OcelotasPesos.pieza_cadena (m := 72) (nsup := 3584000000000000000254) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 7168000000000000000510
    · exact OcelotasPesos.pieza_cadena (m := 73) (nsup := 7168000000000000000510) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 14336000000000000001022
    · exact OcelotasPesos.pieza_cadena (m := 74) (nsup := 14336000000000000001022) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 75) (nsup := 23792465562384120117836) (qmin := 77692117359936589403)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

theorem fila_96 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 205632218873398596256 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 7941964418702608664581) : n < 28000000000000000001 := by
  have hU : (44503776122781252063553659893999 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (325919355854421968365 : ℝ) * log 2 - 205632218873398596256 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (12261796429850908150604 : ℝ) * log 2 - 7736332199829210068325 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 325919355854421968365) (Q := 205632218873398596256) (p := 12261796429850908150604) (v := 7736332199829210068325)
    (c := (44503776122781252063553659893999 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 205632218873398596256 + 7736332199829210068325) hk.2
  by_cases hsmall : n < 28000000000000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 910035136979494649169322)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 56000000000000000002
    · exact OcelotasPesos.pieza_cadena (m := 66) (nsup := 56000000000000000002) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 112000000000000000006
    · exact OcelotasPesos.pieza_cadena (m := 67) (nsup := 112000000000000000006) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 224000000000000000014
    · exact OcelotasPesos.pieza_cadena (m := 68) (nsup := 224000000000000000014) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 448000000000000000030
    · exact OcelotasPesos.pieza_cadena (m := 69) (nsup := 448000000000000000030) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 896000000000000000062
    · exact OcelotasPesos.pieza_cadena (m := 70) (nsup := 896000000000000000062) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 1792000000000000000126
    · exact OcelotasPesos.pieza_cadena (m := 71) (nsup := 1792000000000000000126) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 3584000000000000000254
    · exact OcelotasPesos.pieza_cadena (m := 72) (nsup := 3584000000000000000254) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 7168000000000000000510
    · exact OcelotasPesos.pieza_cadena (m := 73) (nsup := 7168000000000000000510) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 14336000000000000001022
    · exact OcelotasPesos.pieza_cadena (m := 74) (nsup := 14336000000000000001022) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 28672000000000000002046
    · exact OcelotasPesos.pieza_cadena (m := 75) (nsup := 28672000000000000002046) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 57344000000000000004094
    · exact OcelotasPesos.pieza_cadena (m := 76) (nsup := 57344000000000000004094) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 114688000000000000008190
    · exact OcelotasPesos.pieza_cadena (m := 77) (nsup := 114688000000000000008190) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 229376000000000000016382
    · exact OcelotasPesos.pieza_cadena (m := 78) (nsup := 229376000000000000016382) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 458752000000000000032766
    · exact OcelotasPesos.pieza_cadena (m := 79) (nsup := 458752000000000000032766) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 80) (nsup := 910035136979494649169321) (qmin := 205632218873398596256)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

end OcelotasOchentaYUnoTabla

#print axioms OcelotasOchentaYUnoTabla.fila_95
#print axioms OcelotasOchentaYUnoTabla.fila_96
