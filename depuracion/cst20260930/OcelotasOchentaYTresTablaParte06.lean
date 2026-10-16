import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasOchentaYTresTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_98 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 83)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 15678296618531818732906 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 23414628818361028801231) : n < 46645791847966786688 := by
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
  by_cases hsmall : n < 46645791847966786688
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 1856685083418933088112768)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 93291583695933573376
    · exact OcelotasPesos.pieza_cadena (m := 67) (nsup := 93291583695933573376) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 186583167391867146754
    · exact OcelotasPesos.pieza_cadena (m := 68) (nsup := 186583167391867146754) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 373166334783734293510
    · exact OcelotasPesos.pieza_cadena (m := 69) (nsup := 373166334783734293510) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 746332669567468587022
    · exact OcelotasPesos.pieza_cadena (m := 70) (nsup := 746332669567468587022) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 1492665339134937174046
    · exact OcelotasPesos.pieza_cadena (m := 71) (nsup := 1492665339134937174046) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 2985330678269874348094
    · exact OcelotasPesos.pieza_cadena (m := 72) (nsup := 2985330678269874348094) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 5970661356539748696190
    · exact OcelotasPesos.pieza_cadena (m := 73) (nsup := 5970661356539748696190) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 11941322713079497392382
    · exact OcelotasPesos.pieza_cadena (m := 74) (nsup := 11941322713079497392382) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 23882645426158994784766
    · exact OcelotasPesos.pieza_cadena (m := 75) (nsup := 23882645426158994784766) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 47765290852317989569534
    · exact OcelotasPesos.pieza_cadena (m := 76) (nsup := 47765290852317989569534) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 95530581704635979139070
    · exact OcelotasPesos.pieza_cadena (m := 77) (nsup := 95530581704635979139070) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 191061163409271958278142
    · exact OcelotasPesos.pieza_cadena (m := 78) (nsup := 191061163409271958278142) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 382122326818543916556286
    · exact OcelotasPesos.pieza_cadena (m := 79) (nsup := 382122326818543916556286) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 764244653637087833112574
    · exact OcelotasPesos.pieza_cadena (m := 80) (nsup := 764244653637087833112574) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 1528489307274175666225150
    · exact OcelotasPesos.pieza_cadena (m := 81) (nsup := 1528489307274175666225150) (qmin := 15678296618531818732906)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 81) (h0 := 19) (ninf := 1528489307274175666225151)
        (nsup := 1856685083418933088112767) (qmin := 15678296618531818732906) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

theorem fila_99 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 83)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 23414628818361028801231 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 31150961018190238869556) : n < 46645791847966786688 := by
  have hU : (11275607018912242405349016842273 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (37111308645407146420177 : ℝ) * log 2 - 23414628818361028801231 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (12261796429850908150604 : ℝ) * log 2 - 7736332199829210068325 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 37111308645407146420177) (Q := 23414628818361028801231) (p := 12261796429850908150604) (v := 7736332199829210068325)
    (c := (11275607018912242405349016842273 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 23414628818361028801231 + 7736332199829210068325) hk.2
  by_cases hsmall : n < 46645791847966786688
  · exact hsmall
  · exfalso
    have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 3680511384477418955903336)
      hw hr hrR hk hf (by norm_num) hLambda (by norm_num)
    have hn0 : 0 < n := by omega
    by_cases hp0 : n ≤ 93291583695933573376
    · exact OcelotasPesos.pieza_cadena (m := 67) (nsup := 93291583695933573376) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp0 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp1 : n ≤ 186583167391867146754
    · exact OcelotasPesos.pieza_cadena (m := 68) (nsup := 186583167391867146754) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp1 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp2 : n ≤ 373166334783734293510
    · exact OcelotasPesos.pieza_cadena (m := 69) (nsup := 373166334783734293510) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp2 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp3 : n ≤ 746332669567468587022
    · exact OcelotasPesos.pieza_cadena (m := 70) (nsup := 746332669567468587022) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp3 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp4 : n ≤ 1492665339134937174046
    · exact OcelotasPesos.pieza_cadena (m := 71) (nsup := 1492665339134937174046) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp4 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp5 : n ≤ 2985330678269874348094
    · exact OcelotasPesos.pieza_cadena (m := 72) (nsup := 2985330678269874348094) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp5 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp6 : n ≤ 5970661356539748696190
    · exact OcelotasPesos.pieza_cadena (m := 73) (nsup := 5970661356539748696190) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp6 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp7 : n ≤ 11941322713079497392382
    · exact OcelotasPesos.pieza_cadena (m := 74) (nsup := 11941322713079497392382) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp7 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp8 : n ≤ 23882645426158994784766
    · exact OcelotasPesos.pieza_cadena (m := 75) (nsup := 23882645426158994784766) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp8 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp9 : n ≤ 47765290852317989569534
    · exact OcelotasPesos.pieza_cadena (m := 76) (nsup := 47765290852317989569534) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp9 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp10 : n ≤ 95530581704635979139070
    · exact OcelotasPesos.pieza_cadena (m := 77) (nsup := 95530581704635979139070) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp10 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp11 : n ≤ 191061163409271958278142
    · exact OcelotasPesos.pieza_cadena (m := 78) (nsup := 191061163409271958278142) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp11 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp12 : n ≤ 382122326818543916556286
    · exact OcelotasPesos.pieza_cadena (m := 79) (nsup := 382122326818543916556286) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp12 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp13 : n ≤ 764244653637087833112574
    · exact OcelotasPesos.pieza_cadena (m := 80) (nsup := 764244653637087833112574) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp13 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp14 : n ≤ 1528489307274175666225150
    · exact OcelotasPesos.pieza_cadena (m := 81) (nsup := 1528489307274175666225150) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp14 (by norm_num) (by norm_num) (by decide +kernel) hqa
    by_cases hp15 : n ≤ 3056978614548351332450302
    · exact OcelotasPesos.pieza_cadena (m := 82) (nsup := 3056978614548351332450302) (qmin := 23414628818361028801231)
        hn0 hw hr hrR hp15 (by norm_num) (by norm_num) (by decide +kernel) hqa
    exact OcelotasPesos.pieza_imposible (m := 82) (h0 := 24) (ninf := 3056978614548351332450303)
        (nsup := 3680511384477418955903335) (qmin := 23414628818361028801231) hn0 hw hr hrR hk hf (by norm_num) hLambda
        (by omega) (by omega) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (fun _ => by decide +kernel) hqa

end OcelotasOchentaYTresTabla

#print axioms OcelotasOchentaYTresTabla.fila_98
#print axioms OcelotasOchentaYTresTabla.fila_99
