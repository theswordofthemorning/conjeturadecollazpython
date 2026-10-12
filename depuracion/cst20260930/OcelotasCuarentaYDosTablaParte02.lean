import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasCuarentaYDosTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_41 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 42)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 397573379 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 6586818670) : n < 300000000001 := by
  have hU : (10584348843168130862728224244493766369197653 / 100000000000000000000000000000000000000000000000000000 : ℝ) ≤ (630138897 : ℝ) * log 2 - 397573379 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9809721694 : ℝ) * log 2 - 6189245291 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 630138897) (Q := 397573379) (p := 9809721694) (v := 6189245291)
    (c := (10584348843168130862728224244493766369197653 / 100000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 397573379 + 6189245291) hk.2
  by_cases hsmall : n < 300000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 396812318097)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    exact OcelotasPesos.pieza_imposible (m := 40) (h0 := 25) (ninf := 300000000001)
        (nsup := 396812318096) (qmin := 397573379) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

theorem fila_42 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 42)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 6586818670 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 72057431991) : n < 300000000001 := by
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
  by_cases hsmall : n < 300000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 4148916334585)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 600000000002
    · exact OcelotasPesos.pieza_imposible (m := 50) (h0 := 3) (ninf := 300000000001)
        (nsup := 600000000002) (qmin := 6586818670) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp0 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    by_cases hp1 : n ≤ 1200000000006
    · exact OcelotasPesos.pieza_imposible (m := 44) (h0 := 3) (ninf := 600000000003)
        (nsup := 1200000000006) (qmin := 6586818670) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp1 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    by_cases hp2 : n ≤ 2400000000014
    · exact OcelotasPesos.pieza_imposible (m := 44) (h0 := 7) (ninf := 1200000000007)
        (nsup := 2400000000014) (qmin := 6586818670) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp2 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 43) (h0 := 8) (ninf := 2400000000015)
        (nsup := 4148916334584) (qmin := 6586818670) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

end OcelotasCuarentaYDosTabla

#print axioms OcelotasCuarentaYDosTabla.fila_41
#print axioms OcelotasCuarentaYDosTabla.fila_42
