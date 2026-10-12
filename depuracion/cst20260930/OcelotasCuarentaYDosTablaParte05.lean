import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasCuarentaYDosTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_47 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 42)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 2396860564955 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 3149971404836) : n < 300000000001 := by
  have hU : (270886129532669482977001737263149195418867 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (3798934114911 : ℝ) * log 2 - 2396860564955 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1193652440098 : ℝ) * log 2 - 753110839881 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 3798934114911) (Q := 2396860564955) (p := 1193652440098) (v := 753110839881)
    (c := (270886129532669482977001737263149195418867 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 2396860564955 + 753110839881) hk.2
  by_cases hsmall : n < 300000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 77523349151281)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 600000000002
    · exact OcelotasPesos.pieza_cadena (m := 40) (nsup := 600000000002) (qmin := 2396860564955)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 1200000000006
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1200000000006) (qmin := 2396860564955)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 2400000000014
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2400000000014) (qmin := 2396860564955)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 4800000000030
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4800000000030) (qmin := 2396860564955)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 9600000000062
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 9600000000062) (qmin := 2396860564955)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 19200000000126
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 19200000000126) (qmin := 2396860564955)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 38400000000254
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 38400000000254) (qmin := 2396860564955)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 76800000000510
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 76800000000510) (qmin := 2396860564955)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 47) (h0 := 41) (ninf := 76800000000511)
        (nsup := 77523349151280) (qmin := 2396860564955) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

theorem fila_48 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 42)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 3149971404836 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 3903082244717) : n < 300000000001 := by
  have hU : (211405694233260565569116706013950631558707 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (4992586555009 : ℝ) * log 2 - 3149971404836 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1193652440098 : ℝ) * log 2 - 753110839881 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 4992586555009) (Q := 3149971404836) (p := 1193652440098) (v := 753110839881)
    (c := (211405694233260565569116706013950631558707 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 3149971404836 + 753110839881) hk.2
  by_cases hsmall : n < 300000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 99335072672305)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 600000000002
    · exact OcelotasPesos.pieza_cadena (m := 40) (nsup := 600000000002) (qmin := 3149971404836)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 1200000000006
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1200000000006) (qmin := 3149971404836)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 2400000000014
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2400000000014) (qmin := 3149971404836)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 4800000000030
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4800000000030) (qmin := 3149971404836)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 9600000000062
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 9600000000062) (qmin := 3149971404836)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 19200000000126
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 19200000000126) (qmin := 3149971404836)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 38400000000254
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 38400000000254) (qmin := 3149971404836)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 76800000000510
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 76800000000510) (qmin := 3149971404836)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 47) (h0 := 9) (ninf := 76800000000511)
        (nsup := 99335072672304) (qmin := 3149971404836) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

end OcelotasCuarentaYDosTabla

#print axioms OcelotasCuarentaYDosTabla.fila_47
#print axioms OcelotasCuarentaYDosTabla.fila_48
