import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasCuarentaYSieteTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_44 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 47)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 137528045312 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 890638885193) : n < 1200000000001 := by
  have hU : (449327435430896235200656831010744886999347 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (217976794617 : ℝ) * log 2 - 137528045312 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1193652440098 : ℝ) * log 2 - 753110839881 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 217976794617) (Q := 137528045312) (p := 1193652440098) (v := 753110839881)
    (c := (449327435430896235200656831010744886999347 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 137528045312 + 753110839881) hk.2
  by_cases hsmall : n < 1200000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 52300389753553)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 2400000000002
    · exact OcelotasPesos.pieza_imposible (m := 51) (h0 := 1) (ninf := 1200000000001)
        (nsup := 2400000000002) (qmin := 137528045312) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp0 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    by_cases hp1 : n ≤ 4800000000006
    · exact OcelotasPesos.pieza_imposible (m := 48) (h0 := 1) (ninf := 2400000000003)
        (nsup := 4800000000006) (qmin := 137528045312) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp1 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    by_cases hp2 : n ≤ 9600000000014
    · exact OcelotasPesos.pieza_imposible (m := 47) (h0 := 1) (ninf := 4800000000007)
        (nsup := 9600000000014) (qmin := 137528045312) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp2 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    by_cases hp3 : n ≤ 19200000000030
    · exact OcelotasPesos.pieza_imposible (m := 47) (h0 := 2) (ninf := 9600000000015)
        (nsup := 19200000000030) (qmin := 137528045312) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp3 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    by_cases hp4 : n ≤ 38400000000062
    · exact OcelotasPesos.pieza_imposible (m := 47) (h0 := 6) (ninf := 19200000000031)
        (nsup := 38400000000062) (qmin := 137528045312) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp4 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 47) (h0 := 27) (ninf := 38400000000063)
        (nsup := 52300389753552) (qmin := 137528045312) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

theorem fila_45 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 47)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 890638885193 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 1643749725074) : n < 1200000000001 := by
  have hU : (389847000131487317792771799761546323139187 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (1411629234715 : ℝ) * log 2 - 890638885193 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1193652440098 : ℝ) * log 2 - 753110839881 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 1411629234715) (Q := 890638885193) (p := 1193652440098) (v := 753110839881)
    (c := (389847000131487317792771799761546323139187 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 890638885193 + 753110839881) hk.2
  by_cases hsmall : n < 1200000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 60280058566756)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 2400000000002
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2400000000002) (qmin := 890638885193)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 4800000000006
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4800000000006) (qmin := 890638885193)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 9600000000014
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 9600000000014) (qmin := 890638885193)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 19200000000030
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 19200000000030) (qmin := 890638885193)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 38400000000062
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 38400000000062) (qmin := 890638885193)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 60280058566755) (qmin := 890638885193)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

end OcelotasCuarentaYSieteTabla

#print axioms OcelotasCuarentaYSieteTabla.fila_44
#print axioms OcelotasCuarentaYSieteTabla.fila_45
