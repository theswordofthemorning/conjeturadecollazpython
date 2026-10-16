import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasOchentaYTresTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_100 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 83)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 31150961018190238869556 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 101189215254399926676993) : n < 46645791847966786688 := by
  have hU : (199550650955905852614135825031 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (49373105075258054570781 : ℝ) * log 2 - 31150961018190238869556 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (111008006580367017292166 : ℝ) * log 2 - 70038254236209687807437 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 49373105075258054570781) (Q := 31150961018190238869556) (p := 111008006580367017292166) (v := 70038254236209687807437)
    (c := (199550650955905852614135825031 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 31150961018190238869556 + 70038254236209687807437) hk.2
  by_cases hsmall : n < 46645791847966786688
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 207967249423657047089861462)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 93291583695933573376
    · exact OcelotasPesos.pieza_cadena (m := 67) (nsup := 93291583695933573376) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 186583167391867146754
    · exact OcelotasPesos.pieza_cadena (m := 68) (nsup := 186583167391867146754) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 373166334783734293510
    · exact OcelotasPesos.pieza_cadena (m := 69) (nsup := 373166334783734293510) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 746332669567468587022
    · exact OcelotasPesos.pieza_cadena (m := 70) (nsup := 746332669567468587022) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 1492665339134937174046
    · exact OcelotasPesos.pieza_cadena (m := 71) (nsup := 1492665339134937174046) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 2985330678269874348094
    · exact OcelotasPesos.pieza_cadena (m := 72) (nsup := 2985330678269874348094) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 5970661356539748696190
    · exact OcelotasPesos.pieza_cadena (m := 73) (nsup := 5970661356539748696190) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 11941322713079497392382
    · exact OcelotasPesos.pieza_cadena (m := 74) (nsup := 11941322713079497392382) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 23882645426158994784766
    · exact OcelotasPesos.pieza_cadena (m := 75) (nsup := 23882645426158994784766) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 47765290852317989569534
    · exact OcelotasPesos.pieza_cadena (m := 76) (nsup := 47765290852317989569534) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 95530581704635979139070
    · exact OcelotasPesos.pieza_cadena (m := 77) (nsup := 95530581704635979139070) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 191061163409271958278142
    · exact OcelotasPesos.pieza_cadena (m := 78) (nsup := 191061163409271958278142) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 382122326818543916556286
    · exact OcelotasPesos.pieza_cadena (m := 79) (nsup := 382122326818543916556286) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 764244653637087833112574
    · exact OcelotasPesos.pieza_cadena (m := 80) (nsup := 764244653637087833112574) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 1528489307274175666225150
    · exact OcelotasPesos.pieza_cadena (m := 81) (nsup := 1528489307274175666225150) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp15 : n ≤ 3056978614548351332450302
    · exact OcelotasPesos.pieza_cadena (m := 82) (nsup := 3056978614548351332450302) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp15 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp16 : n ≤ 6113957229096702664900606
    · exact OcelotasPesos.pieza_cadena (m := 83) (nsup := 6113957229096702664900606) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp16 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp17 : n ≤ 12227914458193405329801214
    · exact OcelotasPesos.pieza_cadena (m := 84) (nsup := 12227914458193405329801214) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp17 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp18 : n ≤ 24455828916386810659602430
    · exact OcelotasPesos.pieza_cadena (m := 85) (nsup := 24455828916386810659602430) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp18 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp19 : n ≤ 48911657832773621319204862
    · exact OcelotasPesos.pieza_cadena (m := 86) (nsup := 48911657832773621319204862) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp19 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp20 : n ≤ 97823315665547242638409726
    · exact OcelotasPesos.pieza_cadena (m := 87) (nsup := 97823315665547242638409726) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp20 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp21 : n ≤ 195646631331094485276819454
    · exact OcelotasPesos.pieza_cadena (m := 88) (nsup := 195646631331094485276819454) (qmin := 31150961018190238869556)
        hn0 hw hr hrR hp21 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 88) (h0 := 68) (ninf := 195646631331094485276819455)
        (nsup := 207967249423657047089861461) (qmin := 31150961018190238869556) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

end OcelotasOchentaYTresTabla

#print axioms OcelotasOchentaYTresTabla.fila_100
