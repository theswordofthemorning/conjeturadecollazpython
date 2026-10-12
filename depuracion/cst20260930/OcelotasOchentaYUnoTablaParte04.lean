import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasOchentaYUnoTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_93 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 4640282259296926456 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 27444133206411171953) : n < 28000000000000000001 := by
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
  by_cases hsmall : n < 28000000000000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 3003505187578065586353)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 56000000000000000002
    · exact OcelotasPesos.pieza_cadena (m := 66) (nsup := 56000000000000000002) (qmin := 4640282259296926456)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 112000000000000000006
    · exact OcelotasPesos.pieza_cadena (m := 67) (nsup := 112000000000000000006) (qmin := 4640282259296926456)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 224000000000000000014
    · exact OcelotasPesos.pieza_cadena (m := 68) (nsup := 224000000000000000014) (qmin := 4640282259296926456)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 448000000000000000030
    · exact OcelotasPesos.pieza_cadena (m := 69) (nsup := 448000000000000000030) (qmin := 4640282259296926456)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 896000000000000000062
    · exact OcelotasPesos.pieza_cadena (m := 70) (nsup := 896000000000000000062) (qmin := 4640282259296926456)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 1792000000000000000126
    · exact OcelotasPesos.pieza_cadena (m := 71) (nsup := 1792000000000000000126) (qmin := 4640282259296926456)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 72) (nsup := 3003505187578065586352) (qmin := 4640282259296926456)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

theorem fila_94 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 27444133206411171953 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 77692117359936589403) : n < 28000000000000000001 := by
  have hU : (5062154870978150492839768211073613 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (43497921996957973433 : ℝ) * log 2 - 27444133206411171953 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (79641170620168673833 : ℝ) * log 2 - 50247984153525417450 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 43497921996957973433) (Q := 27444133206411171953) (p := 79641170620168673833) (v := 50247984153525417450)
    (c := (5062154870978150492839768211073613 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 27444133206411171953 + 50247984153525417450) hk.2
  by_cases hsmall : n < 28000000000000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 8000545426255254523322)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 56000000000000000002
    · exact OcelotasPesos.pieza_cadena (m := 66) (nsup := 56000000000000000002) (qmin := 27444133206411171953)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 112000000000000000006
    · exact OcelotasPesos.pieza_cadena (m := 67) (nsup := 112000000000000000006) (qmin := 27444133206411171953)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 224000000000000000014
    · exact OcelotasPesos.pieza_cadena (m := 68) (nsup := 224000000000000000014) (qmin := 27444133206411171953)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 448000000000000000030
    · exact OcelotasPesos.pieza_cadena (m := 69) (nsup := 448000000000000000030) (qmin := 27444133206411171953)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 896000000000000000062
    · exact OcelotasPesos.pieza_cadena (m := 70) (nsup := 896000000000000000062) (qmin := 27444133206411171953)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 1792000000000000000126
    · exact OcelotasPesos.pieza_cadena (m := 71) (nsup := 1792000000000000000126) (qmin := 27444133206411171953)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 3584000000000000000254
    · exact OcelotasPesos.pieza_cadena (m := 72) (nsup := 3584000000000000000254) (qmin := 27444133206411171953)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 7168000000000000000510
    · exact OcelotasPesos.pieza_cadena (m := 73) (nsup := 7168000000000000000510) (qmin := 27444133206411171953)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 73) (h0 := 25) (ninf := 7168000000000000000511)
        (nsup := 8000545426255254523321) (qmin := 27444133206411171953) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

end OcelotasOchentaYUnoTabla

#print axioms OcelotasOchentaYUnoTabla.fila_93
#print axioms OcelotasOchentaYUnoTabla.fila_94
