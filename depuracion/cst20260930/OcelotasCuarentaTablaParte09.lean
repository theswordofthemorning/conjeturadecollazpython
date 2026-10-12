import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasCuarentaTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_55 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 40)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 168919587247987 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 221368876767703) : n < 68719476737 := by
  have hU : (4280296925437908492226255737116237606023 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (267731211425355 : ℝ) * log 2 - 168919587247987 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 267731211425355) (Q := 168919587247987) (p := 83130157078217) (v := 52449289519716)
    (c := (4280296925437908492226255737116237606023 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 168919587247987 + 52449289519716) hk.2
  by_cases hsmall : n < 68719476737
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 4672573036029234)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 137438953474
    · exact OcelotasPesos.pieza_cadena (m := 38) (nsup := 137438953474) (qmin := 168919587247987)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 274877906950
    · exact OcelotasPesos.pieza_cadena (m := 39) (nsup := 274877906950) (qmin := 168919587247987)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 549755813902
    · exact OcelotasPesos.pieza_cadena (m := 40) (nsup := 549755813902) (qmin := 168919587247987)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 1099511627806
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1099511627806) (qmin := 168919587247987)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 2199023255614
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2199023255614) (qmin := 168919587247987)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 4398046511230
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4398046511230) (qmin := 168919587247987)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 8796093022462
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 8796093022462) (qmin := 168919587247987)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 17592186044926
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 17592186044926) (qmin := 168919587247987)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 35184372089854
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 35184372089854) (qmin := 168919587247987)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 70368744179710
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 70368744179710) (qmin := 168919587247987)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 140737488359422
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 140737488359422) (qmin := 168919587247987)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 281474976718846
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 281474976718846) (qmin := 168919587247987)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 562949953437694
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 562949953437694) (qmin := 168919587247987)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 1125899906875390
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1125899906875390) (qmin := 168919587247987)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 2251799813750782
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 2251799813750782) (qmin := 168919587247987)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp15 : n ≤ 4503599627501566
    · exact OcelotasPesos.pieza_cadena (m := 53) (nsup := 4503599627501566) (qmin := 168919587247987)
        hn0 hw hr hrR hp15 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 53) (h0 := 36) (ninf := 4503599627501567)
        (nsup := 4672573036029233) (qmin := 168919587247987) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

theorem fila_56 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 40)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 221368876767703 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 273818166287419) : n < 68719476737 := by
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
  by_cases hsmall : n < 68719476737
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 5621743079463589)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 137438953474
    · exact OcelotasPesos.pieza_cadena (m := 38) (nsup := 137438953474) (qmin := 221368876767703)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 274877906950
    · exact OcelotasPesos.pieza_cadena (m := 39) (nsup := 274877906950) (qmin := 221368876767703)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 549755813902
    · exact OcelotasPesos.pieza_cadena (m := 40) (nsup := 549755813902) (qmin := 221368876767703)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 1099511627806
    · exact OcelotasPesos.pieza_cadena (m := 41) (nsup := 1099511627806) (qmin := 221368876767703)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 2199023255614
    · exact OcelotasPesos.pieza_cadena (m := 42) (nsup := 2199023255614) (qmin := 221368876767703)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 4398046511230
    · exact OcelotasPesos.pieza_cadena (m := 43) (nsup := 4398046511230) (qmin := 221368876767703)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 8796093022462
    · exact OcelotasPesos.pieza_cadena (m := 44) (nsup := 8796093022462) (qmin := 221368876767703)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 17592186044926
    · exact OcelotasPesos.pieza_cadena (m := 45) (nsup := 17592186044926) (qmin := 221368876767703)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 35184372089854
    · exact OcelotasPesos.pieza_cadena (m := 46) (nsup := 35184372089854) (qmin := 221368876767703)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 70368744179710
    · exact OcelotasPesos.pieza_cadena (m := 47) (nsup := 70368744179710) (qmin := 221368876767703)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 140737488359422
    · exact OcelotasPesos.pieza_cadena (m := 48) (nsup := 140737488359422) (qmin := 221368876767703)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 281474976718846
    · exact OcelotasPesos.pieza_cadena (m := 49) (nsup := 281474976718846) (qmin := 221368876767703)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 562949953437694
    · exact OcelotasPesos.pieza_cadena (m := 50) (nsup := 562949953437694) (qmin := 221368876767703)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 1125899906875390
    · exact OcelotasPesos.pieza_cadena (m := 51) (nsup := 1125899906875390) (qmin := 221368876767703)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 2251799813750782
    · exact OcelotasPesos.pieza_cadena (m := 52) (nsup := 2251799813750782) (qmin := 221368876767703)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp15 : n ≤ 4503599627501566
    · exact OcelotasPesos.pieza_cadena (m := 53) (nsup := 4503599627501566) (qmin := 221368876767703)
        hn0 hw hr hrR hp15 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 53) (h0 := 18) (ninf := 4503599627501567)
        (nsup := 5621743079463588) (qmin := 221368876767703) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

end OcelotasCuarentaTabla

#print axioms OcelotasCuarentaTabla.fila_55
#print axioms OcelotasCuarentaTabla.fila_56
