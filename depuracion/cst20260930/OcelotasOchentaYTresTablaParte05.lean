import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasOchentaYTresTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_96 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 83)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 205632218873398596256 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 7941964418702608664581) : n < 46645791847966786688 := by
  have hU : (44503776122781252063553659893999 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (325919355854421968365 : ℝ) * log 2 - 205632218873398596256 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (12261796429850908150604 : ℝ) * log 2 - 7736332199829210068325 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 325919355854421968365) (Q := 205632218873398596256) (p := 12261796429850908150604) (v := 7736332199829210068325)
    (c := (44503776122781252063553659893999 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 205632218873398596256 + 7736332199829210068325) hk.2
  by_cases hsmall : n < 46645791847966786688
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 932505140361704393593256)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 93291583695933573376
    · exact OcelotasPesos.pieza_cadena (m := 67) (nsup := 93291583695933573376) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 186583167391867146754
    · exact OcelotasPesos.pieza_cadena (m := 68) (nsup := 186583167391867146754) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 373166334783734293510
    · exact OcelotasPesos.pieza_cadena (m := 69) (nsup := 373166334783734293510) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 746332669567468587022
    · exact OcelotasPesos.pieza_cadena (m := 70) (nsup := 746332669567468587022) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 1492665339134937174046
    · exact OcelotasPesos.pieza_cadena (m := 71) (nsup := 1492665339134937174046) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 2985330678269874348094
    · exact OcelotasPesos.pieza_cadena (m := 72) (nsup := 2985330678269874348094) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 5970661356539748696190
    · exact OcelotasPesos.pieza_cadena (m := 73) (nsup := 5970661356539748696190) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 11941322713079497392382
    · exact OcelotasPesos.pieza_cadena (m := 74) (nsup := 11941322713079497392382) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 23882645426158994784766
    · exact OcelotasPesos.pieza_cadena (m := 75) (nsup := 23882645426158994784766) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 47765290852317989569534
    · exact OcelotasPesos.pieza_cadena (m := 76) (nsup := 47765290852317989569534) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 95530581704635979139070
    · exact OcelotasPesos.pieza_cadena (m := 77) (nsup := 95530581704635979139070) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 191061163409271958278142
    · exact OcelotasPesos.pieza_cadena (m := 78) (nsup := 191061163409271958278142) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 382122326818543916556286
    · exact OcelotasPesos.pieza_cadena (m := 79) (nsup := 382122326818543916556286) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 764244653637087833112574
    · exact OcelotasPesos.pieza_cadena (m := 80) (nsup := 764244653637087833112574) (qmin := 205632218873398596256)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 80) (h0 := 17) (ninf := 764244653637087833112575)
        (nsup := 932505140361704393593255) (qmin := 205632218873398596256) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

theorem fila_97 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 83)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 7941964418702608664581 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 15678296618531818732906) : n < 46645791847966786688 := by
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
  by_cases hsmall : n < 46645791847966786688
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 1241484621277822624869699)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 93291583695933573376
    · exact OcelotasPesos.pieza_cadena (m := 67) (nsup := 93291583695933573376) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 186583167391867146754
    · exact OcelotasPesos.pieza_cadena (m := 68) (nsup := 186583167391867146754) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 373166334783734293510
    · exact OcelotasPesos.pieza_cadena (m := 69) (nsup := 373166334783734293510) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 746332669567468587022
    · exact OcelotasPesos.pieza_cadena (m := 70) (nsup := 746332669567468587022) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 1492665339134937174046
    · exact OcelotasPesos.pieza_cadena (m := 71) (nsup := 1492665339134937174046) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 2985330678269874348094
    · exact OcelotasPesos.pieza_cadena (m := 72) (nsup := 2985330678269874348094) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 5970661356539748696190
    · exact OcelotasPesos.pieza_cadena (m := 73) (nsup := 5970661356539748696190) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 11941322713079497392382
    · exact OcelotasPesos.pieza_cadena (m := 74) (nsup := 11941322713079497392382) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 23882645426158994784766
    · exact OcelotasPesos.pieza_cadena (m := 75) (nsup := 23882645426158994784766) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 47765290852317989569534
    · exact OcelotasPesos.pieza_cadena (m := 76) (nsup := 47765290852317989569534) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 95530581704635979139070
    · exact OcelotasPesos.pieza_cadena (m := 77) (nsup := 95530581704635979139070) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 191061163409271958278142
    · exact OcelotasPesos.pieza_cadena (m := 78) (nsup := 191061163409271958278142) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 382122326818543916556286
    · exact OcelotasPesos.pieza_cadena (m := 79) (nsup := 382122326818543916556286) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 764244653637087833112574
    · exact OcelotasPesos.pieza_cadena (m := 80) (nsup := 764244653637087833112574) (qmin := 7941964418702608664581)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 81) (h0 := 17) (ninf := 764244653637087833112575)
        (nsup := 1241484621277822624869698) (qmin := 7941964418702608664581) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

end OcelotasOchentaYTresTabla

#print axioms OcelotasOchentaYTresTabla.fila_96
#print axioms OcelotasOchentaYTresTabla.fila_97
