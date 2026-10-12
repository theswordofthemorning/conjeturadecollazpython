import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasCuarentaYUnaTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_43 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 41)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 72057431991 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 137528045312) : n < 200000000001 := by
  have hU : (1377722523942393164305913008656833942928121 / 250000000000000000000000000000000000000000000000000000 : ℝ) ≤ (114208327604 : ℝ) * log 2 - 72057431991 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (103768467013 : ℝ) * log 2 - 65470613321 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 114208327604) (Q := 72057431991) (p := 103768467013) (v := 65470613321)
    (c := (1377722523942393164305913008656833942928121 / 250000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 72057431991 + 65470613321) hk.2
  by_cases hsmall : n < 200000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 7439814492304)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 400000000002
    · exact OcelotasPesos.pieza_cadena (m := 39) (nsup := 400000000002) (qmin := 72057431991)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 800000000006
    · exact OcelotasPesos.pieza_cadena (m := 40) (nsup := 800000000006) (qmin := 72057431991)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 1600000000014
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1600000000014) (qmin := 72057431991)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 3200000000030
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 3200000000030) (qmin := 72057431991)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 6400000000062
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 6400000000062) (qmin := 72057431991)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 43) (h0 := 3) (ninf := 6400000000063)
        (nsup := 7439814492303) (qmin := 72057431991) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

theorem fila_44 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 41)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 137528045312 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 890638885193) : n < 200000000001 := by
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
  by_cases hsmall : n < 200000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 45623744253099)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 400000000002
    · exact OcelotasPesos.pieza_cadena (m := 39) (nsup := 400000000002) (qmin := 137528045312)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 800000000006
    · exact OcelotasPesos.pieza_cadena (m := 40) (nsup := 800000000006) (qmin := 137528045312)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 1600000000014
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1600000000014) (qmin := 137528045312)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 3200000000030
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 3200000000030) (qmin := 137528045312)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 6400000000062
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 6400000000062) (qmin := 137528045312)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 12800000000126
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 12800000000126) (qmin := 137528045312)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 25600000000254
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 25600000000254) (qmin := 137528045312)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 45623744253098) (qmin := 137528045312)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

end OcelotasCuarentaYUnaTabla

#print axioms OcelotasCuarentaYUnaTabla.fila_43
#print axioms OcelotasCuarentaYUnaTabla.fila_44
