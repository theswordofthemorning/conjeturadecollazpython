import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasOchentaYTresTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_92 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 83)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 397560349370386783 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 4640282259296926456) : n < 46645791847966786688 := by
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
  by_cases hsmall : n < 46645791847966786688
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 547180720141386120468)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 93291583695933573376
    · exact OcelotasPesos.pieza_imposible (m := 73) (h0 := 6) (ninf := 46645791847966786688)
        (nsup := 93291583695933573376) (qmin := 397560349370386783) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp0 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    by_cases hp1 : n ≤ 186583167391867146754
    · exact OcelotasPesos.pieza_imposible (m := 71) (h0 := 8) (ninf := 93291583695933573377)
        (nsup := 186583167391867146754) (qmin := 397560349370386783) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp1 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    by_cases hp2 : n ≤ 373166334783734293510
    · exact OcelotasPesos.pieza_imposible (m := 71) (h0 := 18) (ninf := 186583167391867146755)
        (nsup := 373166334783734293510) (qmin := 397560349370386783) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp2 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 70) (h0 := 33) (ninf := 373166334783734293511)
        (nsup := 547180720141386120467) (qmin := 397560349370386783) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

theorem fila_93 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 83)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 4640282259296926456 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 27444133206411171953) : n < 46645791847966786688 := by
  have hU : (2696849012780161512710306135246327 / 100000000000000000000000000000000000000000000000000000 : ℝ) ≤ (7354673373747273033 : ℝ) * log 2 - 4640282259296926456 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (36143248623210700400 : ℝ) * log 2 - 22803850947114245497 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 7354673373747273033) (Q := 4640282259296926456) (p := 36143248623210700400) (v := 22803850947114245497)
    (c := (2696849012780161512710306135246327 / 100000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 4640282259296926456 + 22803850947114245497) hk.2
  by_cases hsmall : n < 46645791847966786688
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 3077665809493573378609)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 93291583695933573376
    · exact OcelotasPesos.pieza_cadena (m := 67) (nsup := 93291583695933573376) (qmin := 4640282259296926456)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 186583167391867146754
    · exact OcelotasPesos.pieza_cadena (m := 68) (nsup := 186583167391867146754) (qmin := 4640282259296926456)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 373166334783734293510
    · exact OcelotasPesos.pieza_cadena (m := 69) (nsup := 373166334783734293510) (qmin := 4640282259296926456)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 746332669567468587022
    · exact OcelotasPesos.pieza_imposible (m := 73) (h0 := 3) (ninf := 373166334783734293511)
        (nsup := 746332669567468587022) (qmin := 4640282259296926456) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp3 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    by_cases hp4 : n ≤ 1492665339134937174046
    · exact OcelotasPesos.pieza_imposible (m := 73) (h0 := 8) (ninf := 746332669567468587023)
        (nsup := 1492665339134937174046) (qmin := 4640282259296926456) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp4 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    by_cases hp5 : n ≤ 2985330678269874348094
    · exact OcelotasPesos.pieza_imposible (m := 73) (h0 := 20) (ninf := 1492665339134937174047)
        (nsup := 2985330678269874348094) (qmin := 4640282259296926456) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) hp5 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 72) (h0 := 75) (ninf := 2985330678269874348095)
        (nsup := 3077665809493573378608) (qmin := 4640282259296926456) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

end OcelotasOchentaYTresTabla

#print axioms OcelotasOchentaYTresTabla.fila_92
#print axioms OcelotasOchentaYTresTabla.fila_93
