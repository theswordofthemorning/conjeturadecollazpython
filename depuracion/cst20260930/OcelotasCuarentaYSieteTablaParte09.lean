import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasCuarentaYSieteTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_56 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 47)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 221368876767703 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 273818166287419) : n < 1200000000001 := by
  have hU : (1778807721848820780977804944158939054633 / 250000000000000000000000000000000000000000000000000000 : ℝ) ≤ (350861368503572 : ℝ) * log 2 - 221368876767703 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 350861368503572) (Q := 221368876767703) (p := 83130157078217) (v := 52449289519716)
    (c := (1778807721848820780977804944158939054633 / 250000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 221368876767703 + 52449289519716) hk.2
  by_cases hsmall : n < 1200000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 6605548118369717)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 2400000000002
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2400000000002) (qmin := 221368876767703)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 4800000000006
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4800000000006) (qmin := 221368876767703)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 9600000000014
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 9600000000014) (qmin := 221368876767703)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 19200000000030
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 19200000000030) (qmin := 221368876767703)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 38400000000062
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 38400000000062) (qmin := 221368876767703)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 76800000000126
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 76800000000126) (qmin := 221368876767703)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 153600000000254
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 153600000000254) (qmin := 221368876767703)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 307200000000510
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 307200000000510) (qmin := 221368876767703)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 614400000001022
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 614400000001022) (qmin := 221368876767703)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 1228800000002046
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1228800000002046) (qmin := 221368876767703)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 2457600000004094
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 2457600000004094) (qmin := 221368876767703)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 4915200000008190
    · exact OcelotasPesos.pieza_cadena (m := 53) (nsup := 4915200000008190) (qmin := 221368876767703)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 53) (h0 := 1) (ninf := 4915200000008191)
        (nsup := 6605548118369716) (qmin := 221368876767703) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

theorem fila_57 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 47)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 273818166287419 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 326267455807135) : n < 1200000000001 := by
  have hU : (2834933961957374631684964039519518612509 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (433991525581789 : ℝ) * log 2 - 273818166287419 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 433991525581789) (Q := 273818166287419) (p := 83130157078217) (v := 52449289519716)
    (c := (2834933961957374631684964039519518612509 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 273818166287419 + 52449289519716) hk.2
  by_cases hsmall : n < 1200000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 8289434715359109)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 2400000000002
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2400000000002) (qmin := 273818166287419)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 4800000000006
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4800000000006) (qmin := 273818166287419)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 9600000000014
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 9600000000014) (qmin := 273818166287419)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 19200000000030
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 19200000000030) (qmin := 273818166287419)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 38400000000062
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 38400000000062) (qmin := 273818166287419)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 76800000000126
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 76800000000126) (qmin := 273818166287419)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 153600000000254
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 153600000000254) (qmin := 273818166287419)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 307200000000510
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 307200000000510) (qmin := 273818166287419)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 614400000001022
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 614400000001022) (qmin := 273818166287419)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 1228800000002046
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1228800000002046) (qmin := 273818166287419)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 2457600000004094
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 2457600000004094) (qmin := 273818166287419)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 4915200000008190
    · exact OcelotasPesos.pieza_cadena (m := 53) (nsup := 4915200000008190) (qmin := 273818166287419)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 53) (nsup := 8289434715359108) (qmin := 273818166287419)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

end OcelotasCuarentaYSieteTabla

#print axioms OcelotasCuarentaYSieteTabla.fila_56
#print axioms OcelotasCuarentaYSieteTabla.fila_57
