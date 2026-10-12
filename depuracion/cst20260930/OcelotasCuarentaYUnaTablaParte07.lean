import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasCuarentaYUnaTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_51 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 41)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 5409303924479 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 11571718688839) : n < 200000000001 := by
  have hU : (32964388335033813345461612266354939978227 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (8573543875303 : ℝ) * log 2 - 5409303924479 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9767196315401 : ℝ) * log 2 - 6162414764360 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 8573543875303) (Q := 5409303924479) (p := 9767196315401) (v := 6162414764360)
    (c := (32964388335033813345461612266354939978227 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 5409303924479 + 6162414764360) hk.2
  by_cases hsmall : n < 200000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 621883221118745)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 400000000002
    · exact OcelotasPesos.pieza_cadena (m := 39) (nsup := 400000000002) (qmin := 5409303924479)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 800000000006
    · exact OcelotasPesos.pieza_cadena (m := 40) (nsup := 800000000006) (qmin := 5409303924479)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 1600000000014
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1600000000014) (qmin := 5409303924479)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 3200000000030
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 3200000000030) (qmin := 5409303924479)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 6400000000062
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 6400000000062) (qmin := 5409303924479)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 12800000000126
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 12800000000126) (qmin := 5409303924479)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 25600000000254
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 25600000000254) (qmin := 5409303924479)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 51200000000510
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 51200000000510) (qmin := 5409303924479)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 102400000001022
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 102400000001022) (qmin := 5409303924479)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 204800000002046
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 204800000002046) (qmin := 5409303924479)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 409600000004094
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 409600000004094) (qmin := 5409303924479)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 50) (h0 := 9) (ninf := 409600000004095)
        (nsup := 621883221118744) (qmin := 5409303924479) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

theorem fila_52 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 41)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 11571718688839 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 64021008208555) : n < 200000000001 := by
  have hU : (3224170685329354641519096641755658048147 / 250000000000000000000000000000000000000000000000000000 : ℝ) ≤ (18340740190704 : ℝ) * log 2 - 11571718688839 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 18340740190704) (Q := 11571718688839) (p := 83130157078217) (v := 52449289519716)
    (c := (3224170685329354641519096641755658048147 / 250000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 11571718688839 + 52449289519716) hk.2
  by_cases hsmall : n < 200000000001
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 3179112088153282)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 400000000002
    · exact OcelotasPesos.pieza_cadena (m := 39) (nsup := 400000000002) (qmin := 11571718688839)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 800000000006
    · exact OcelotasPesos.pieza_cadena (m := 40) (nsup := 800000000006) (qmin := 11571718688839)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 1600000000014
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1600000000014) (qmin := 11571718688839)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 3200000000030
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 3200000000030) (qmin := 11571718688839)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 6400000000062
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 6400000000062) (qmin := 11571718688839)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 12800000000126
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 12800000000126) (qmin := 11571718688839)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 25600000000254
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 25600000000254) (qmin := 11571718688839)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 51200000000510
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 51200000000510) (qmin := 11571718688839)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 102400000001022
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 102400000001022) (qmin := 11571718688839)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 204800000002046
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 204800000002046) (qmin := 11571718688839)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 409600000004094
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 409600000004094) (qmin := 11571718688839)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 819200000008190
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 819200000008190) (qmin := 11571718688839)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 1638400000016382
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1638400000016382) (qmin := 11571718688839)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 3179112088153281) (qmin := 11571718688839)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

end OcelotasCuarentaYUnaTabla

#print axioms OcelotasCuarentaYUnaTabla.fila_51
#print axioms OcelotasCuarentaYUnaTabla.fila_52
