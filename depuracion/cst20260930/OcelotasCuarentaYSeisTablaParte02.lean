import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasCuarentaYSeisTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_42 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 46)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 6586818670 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 72057431991) : n < 700000000001 := by
  have hU : (5061562660338676422022995203616590884713137 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (10439860591 : ℝ) * log 2 - 6586818670 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (103768467013 : ℝ) * log 2 - 65470613321 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 10439860591) (Q := 6586818670) (p := 103768467013) (v := 65470613321)
    (c := (5061562660338676422022995203616590884713137 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 6586818670 + 65470613321) hk.2
  by_cases hsmall : n < 700000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 4544051223593)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 1400000000002
    · exact OcelotasPesos.pieza_imposible (m := 50) (h0 := 7) (ninf := 700000000001)
        (nsup := 1400000000002) (qmin := 6586818670) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp0 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    by_cases hp1 : n ≤ 2800000000006
    · exact OcelotasPesos.pieza_imposible (m := 44) (h0 := 8) (ninf := 1400000000003)
        (nsup := 2800000000006) (qmin := 6586818670) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp1 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 43) (h0 := 9) (ninf := 2800000000007)
        (nsup := 4544051223592) (qmin := 6586818670) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

theorem fila_43 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 46)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 72057431991 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 137528045312) : n < 700000000001 := by
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
  by_cases hsmall : n < 700000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 8347108942585)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 1400000000002
    · exact OcelotasPesos.pieza_imposible (m := 45) (h0 := 2) (ninf := 700000000001)
        (nsup := 1400000000002) (qmin := 72057431991) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp0 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    by_cases hp1 : n ≤ 2800000000006
    · exact OcelotasPesos.pieza_imposible (m := 45) (h0 := 4) (ninf := 1400000000003)
        (nsup := 2800000000006) (qmin := 72057431991) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp1 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    by_cases hp2 : n ≤ 5600000000014
    · exact OcelotasPesos.pieza_imposible (m := 45) (h0 := 9) (ninf := 2800000000007)
        (nsup := 5600000000014) (qmin := 72057431991) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp2 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 44) (h0 := 17) (ninf := 5600000000015)
        (nsup := 8347108942584) (qmin := 72057431991) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

end OcelotasCuarentaYSeisTabla

#print axioms OcelotasCuarentaYSeisTabla.fila_42
#print axioms OcelotasCuarentaYSeisTabla.fila_43
