import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasOchentaYUnoTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_91 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 130441933147714940 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 397560349370386783) : n < 28000000000000000001 := by
  have hU : (896635541085219531098081459479562729 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (206745572560704147 : ℝ) * log 2 - 130441933147714940 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (423372672964960618 : ℝ) * log 2 - 267118416222671843 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 206745572560704147) (Q := 130441933147714940) (p := 423372672964960618) (v := 267118416222671843)
    (c := (896635541085219531098081459479562729 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 130441933147714940 + 267118416222671843) hk.2
  by_cases hsmall : n < 28000000000000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 45168854171207486663)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    exact OcelotasPesos.pieza_imposible (m := 67) (h0 := 36) (ninf := 28000000000000000001)
        (nsup := 45168854171207486662) (qmin := 130441933147714940) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

theorem fila_92 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 397560349370386783 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 4640282259296926456) : n < 28000000000000000001 := by
  have hU : (75843315512426694888469415846316197 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (630118245525664765 : ℝ) * log 2 - 397560349370386783 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (6724555128221608268 : ℝ) * log 2 - 4242721909926539673 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 630118245525664765) (Q := 397560349370386783) (p := 6724555128221608268) (v := 4242721909926539673)
    (c := (75843315512426694888469415846316197 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 397560349370386783 + 4242721909926539673) hk.2
  by_cases hsmall : n < 28000000000000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 533995642547617780216)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 56000000000000000002
    · exact OcelotasPesos.pieza_imposible (m := 74) (h0 := 4) (ninf := 28000000000000000001)
        (nsup := 56000000000000000002) (qmin := 397560349370386783) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp0 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    by_cases hp1 : n ≤ 112000000000000000006
    · exact OcelotasPesos.pieza_imposible (m := 71) (h0 := 4) (ninf := 56000000000000000003)
        (nsup := 112000000000000000006) (qmin := 397560349370386783) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp1 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    by_cases hp2 : n ≤ 224000000000000000014
    · exact OcelotasPesos.pieza_imposible (m := 71) (h0 := 10) (ninf := 112000000000000000007)
        (nsup := 224000000000000000014) (qmin := 397560349370386783) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp2 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    by_cases hp3 : n ≤ 448000000000000000030
    · exact OcelotasPesos.pieza_imposible (m := 70) (h0 := 5) (ninf := 224000000000000000015)
        (nsup := 448000000000000000030) (qmin := 397560349370386783) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp3 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 70) (h0 := 57) (ninf := 448000000000000000031)
        (nsup := 533995642547617780215) (qmin := 397560349370386783) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

end OcelotasOchentaYUnoTabla

#print axioms OcelotasOchentaYUnoTabla.fila_91
#print axioms OcelotasOchentaYUnoTabla.fila_92
