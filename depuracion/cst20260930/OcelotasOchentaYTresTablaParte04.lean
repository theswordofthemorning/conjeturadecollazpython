import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasOchentaYTresTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_94 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 83)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 27444133206411171953 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 77692117359936589403) : n < 46645791847966786688 := by
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
  by_cases hsmall : n < 46645791847966786688
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 8198089757767729943651)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 93291583695933573376
    · exact OcelotasPesos.pieza_cadena (m := 67) (nsup := 93291583695933573376) (qmin := 27444133206411171953)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 186583167391867146754
    · exact OcelotasPesos.pieza_cadena (m := 68) (nsup := 186583167391867146754) (qmin := 27444133206411171953)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 373166334783734293510
    · exact OcelotasPesos.pieza_cadena (m := 69) (nsup := 373166334783734293510) (qmin := 27444133206411171953)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 746332669567468587022
    · exact OcelotasPesos.pieza_cadena (m := 70) (nsup := 746332669567468587022) (qmin := 27444133206411171953)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 1492665339134937174046
    · exact OcelotasPesos.pieza_cadena (m := 71) (nsup := 1492665339134937174046) (qmin := 27444133206411171953)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 2985330678269874348094
    · exact OcelotasPesos.pieza_cadena (m := 72) (nsup := 2985330678269874348094) (qmin := 27444133206411171953)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 5970661356539748696190
    · exact OcelotasPesos.pieza_cadena (m := 73) (nsup := 5970661356539748696190) (qmin := 27444133206411171953)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_cadena (m := 73) (nsup := 8198089757767729943650) (qmin := 27444133206411171953)
        hn0 hw hr hrR (by omega) (by norm_num) (by norm_num) (by decide +kernel) hqa

theorem fila_95 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 83)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 77692117359936589403 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 205632218873398596256) : n < 46645791847966786688 := by
  have hU : (425554887258410978741943489247301 / 125000000000000000000000000000000000000000000000000000 : ℝ) ≤ (123139092617126647266 : ℝ) * log 2 - 77692117359936589403 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (202780263237295321099 : ℝ) * log 2 - 127940101513462006853 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 123139092617126647266) (Q := 77692117359936589403) (p := 202780263237295321099) (v := 127940101513462006853)
    (c := (425554887258410978741943489247301 / 125000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 77692117359936589403 + 127940101513462006853) hk.2
  by_cases hsmall : n < 46645791847966786688
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 24379933847875086046672)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 93291583695933573376
    · exact OcelotasPesos.pieza_cadena (m := 67) (nsup := 93291583695933573376) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 186583167391867146754
    · exact OcelotasPesos.pieza_cadena (m := 68) (nsup := 186583167391867146754) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 373166334783734293510
    · exact OcelotasPesos.pieza_cadena (m := 69) (nsup := 373166334783734293510) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 746332669567468587022
    · exact OcelotasPesos.pieza_cadena (m := 70) (nsup := 746332669567468587022) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 1492665339134937174046
    · exact OcelotasPesos.pieza_cadena (m := 71) (nsup := 1492665339134937174046) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 2985330678269874348094
    · exact OcelotasPesos.pieza_cadena (m := 72) (nsup := 2985330678269874348094) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 5970661356539748696190
    · exact OcelotasPesos.pieza_cadena (m := 73) (nsup := 5970661356539748696190) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 11941322713079497392382
    · exact OcelotasPesos.pieza_cadena (m := 74) (nsup := 11941322713079497392382) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 23882645426158994784766
    · exact OcelotasPesos.pieza_cadena (m := 75) (nsup := 23882645426158994784766) (qmin := 77692117359936589403)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 75) (h0 := 78) (ninf := 23882645426158994784767)
        (nsup := 24379933847875086046671) (qmin := 77692117359936589403) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

end OcelotasOchentaYTresTabla

#print axioms OcelotasOchentaYTresTabla.fila_94
#print axioms OcelotasOchentaYTresTabla.fila_95
