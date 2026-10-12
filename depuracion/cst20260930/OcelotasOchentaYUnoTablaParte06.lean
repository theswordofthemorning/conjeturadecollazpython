import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasOchentaYUnoTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_97 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 7941964418702608664581 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 15678296618531818732906) : n < 28000000000000000001 := by
  have hU : (33427719754824915510818778876757 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (12587715785705330118969 : ℝ) * log 2 - 7941964418702608664581 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (12261796429850908150604 : ℝ) * log 2 - 7736332199829210068325 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 12587715785705330118969) (Q := 7941964418702608664581) (p := 12261796429850908150604) (v := 7736332199829210068325)
    (c := (33427719754824915510818778876757 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 7941964418702608664581 + 7736332199829210068325) hk.2
  by_cases hsmall : n < 28000000000000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 1211569329198838947161995)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 56000000000000000002
    · exact OcelotasPesos.pieza_cadena (m := 66) (nsup := 56000000000000000002) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 112000000000000000006
    · exact OcelotasPesos.pieza_cadena (m := 67) (nsup := 112000000000000000006) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 224000000000000000014
    · exact OcelotasPesos.pieza_cadena (m := 68) (nsup := 224000000000000000014) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 448000000000000000030
    · exact OcelotasPesos.pieza_cadena (m := 69) (nsup := 448000000000000000030) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 896000000000000000062
    · exact OcelotasPesos.pieza_cadena (m := 70) (nsup := 896000000000000000062) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 1792000000000000000126
    · exact OcelotasPesos.pieza_cadena (m := 71) (nsup := 1792000000000000000126) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 3584000000000000000254
    · exact OcelotasPesos.pieza_cadena (m := 72) (nsup := 3584000000000000000254) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 7168000000000000000510
    · exact OcelotasPesos.pieza_cadena (m := 73) (nsup := 7168000000000000000510) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 14336000000000000001022
    · exact OcelotasPesos.pieza_cadena (m := 74) (nsup := 14336000000000000001022) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 28672000000000000002046
    · exact OcelotasPesos.pieza_cadena (m := 75) (nsup := 28672000000000000002046) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 57344000000000000004094
    · exact OcelotasPesos.pieza_cadena (m := 76) (nsup := 57344000000000000004094) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 114688000000000000008190
    · exact OcelotasPesos.pieza_cadena (m := 77) (nsup := 114688000000000000008190) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 229376000000000000016382
    · exact OcelotasPesos.pieza_cadena (m := 78) (nsup := 229376000000000000016382) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 458752000000000000032766
    · exact OcelotasPesos.pieza_cadena (m := 79) (nsup := 458752000000000000032766) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 917504000000000000065534
    · exact OcelotasPesos.pieza_cadena (m := 80) (nsup := 917504000000000000065534) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 81) (h0 := 41) (ninf := 917504000000000000065535)
        (nsup := 1211569329198838947161994) (qmin := 7941964418702608664581) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

theorem fila_98 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 15678296618531818732906 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 23414628818361028801231) : n < 28000000000000000001 := by
  have hU : (4470332677373715791616779571903 / 100000000000000000000000000000000000000000000000000000 : ℝ) ≤ (24849512215556238269573 : ℝ) * log 2 - 15678296618531818732906 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (12261796429850908150604 : ℝ) * log 2 - 7736332199829210068325 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 24849512215556238269573) (Q := 15678296618531818732906) (p := 12261796429850908150604) (v := 7736332199829210068325)
    (c := (4470332677373715791616779571903 / 100000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 15678296618531818732906 + 7736332199829210068325) hk.2
  by_cases hsmall : n < 28000000000000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 1811945683818476869122099)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 56000000000000000002
    · exact OcelotasPesos.pieza_cadena (m := 66) (nsup := 56000000000000000002) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 112000000000000000006
    · exact OcelotasPesos.pieza_cadena (m := 67) (nsup := 112000000000000000006) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 224000000000000000014
    · exact OcelotasPesos.pieza_cadena (m := 68) (nsup := 224000000000000000014) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 448000000000000000030
    · exact OcelotasPesos.pieza_cadena (m := 69) (nsup := 448000000000000000030) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 896000000000000000062
    · exact OcelotasPesos.pieza_cadena (m := 70) (nsup := 896000000000000000062) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 1792000000000000000126
    · exact OcelotasPesos.pieza_cadena (m := 71) (nsup := 1792000000000000000126) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 3584000000000000000254
    · exact OcelotasPesos.pieza_cadena (m := 72) (nsup := 3584000000000000000254) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 7168000000000000000510
    · exact OcelotasPesos.pieza_cadena (m := 73) (nsup := 7168000000000000000510) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 14336000000000000001022
    · exact OcelotasPesos.pieza_cadena (m := 74) (nsup := 14336000000000000001022) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 28672000000000000002046
    · exact OcelotasPesos.pieza_cadena (m := 75) (nsup := 28672000000000000002046) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 57344000000000000004094
    · exact OcelotasPesos.pieza_cadena (m := 76) (nsup := 57344000000000000004094) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 114688000000000000008190
    · exact OcelotasPesos.pieza_cadena (m := 77) (nsup := 114688000000000000008190) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 229376000000000000016382
    · exact OcelotasPesos.pieza_cadena (m := 78) (nsup := 229376000000000000016382) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 458752000000000000032766
    · exact OcelotasPesos.pieza_cadena (m := 79) (nsup := 458752000000000000032766) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 917504000000000000065534
    · exact OcelotasPesos.pieza_cadena (m := 80) (nsup := 917504000000000000065534) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 81) (nsup := 1811945683818476869122098) (qmin := 15678296618531818732906)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

end OcelotasOchentaYUnoTabla

#print axioms OcelotasOchentaYUnoTabla.fila_97
#print axioms OcelotasOchentaYUnoTabla.fila_98
