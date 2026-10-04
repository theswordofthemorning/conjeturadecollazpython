import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasVeinticuatroPrefijosBajo
import OcelotasVeinticuatroPrefijosAlto

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasVeinticuatroTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_30 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 13606 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 14271) : n < 4912741 := by
  have hU : (74578460068229452002838846476557201933871287754299 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (21565 : ℝ) * log 2 - 13606 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 21565) (Q := 13606) (p := 1054) (v := 665)
    (c := (74578460068229452002838846476557201933871287754299 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 13606 + 665) hk.2
  exact pequeno_por_cota (s := 160905) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_31 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 14271 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 14936) : n < 4912741 := by
  have hU : (52751404773903414289570565731137699894203078080367 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (22619 : ℝ) * log 2 - 14271 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 22619) (Q := 14271) (p := 1054) (v := 665)
    (c := (52751404773903414289570565731137699894203078080367 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 14271 + 665) hk.2
  exact pequeno_por_cota (s := 227483) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_32 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 14936 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 15601) : n < 4912741 := by
  have hU : (6184869895915475315260456997143639570906973681287 / 100000000000000000000000000000000000000000000000000000 : ℝ) ≤ (23673 : ℝ) * log 2 - 14936 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 23673) (Q := 14936) (p := 1054) (v := 665)
    (c := (6184869895915475315260456997143639570906973681287 / 100000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 14936 + 665) hk.2
  exact pequeno_por_cota (s := 388044) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_33 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 15601 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 47468) : n < 4912741 := by
  have hU : (9097294185251338863034004240298695814866658732503 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (24727 : ℝ) * log 2 - 15601 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (50508 : ℝ) * log 2 - 31867 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 24727) (Q := 15601) (p := 50508) (v := 31867)
    (c := (9097294185251338863034004240298695814866658732503 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 15601 + 31867) hk.2
  exact pequeno_por_cota (s := 1319074) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_34 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 47468 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 79335) : n < 4912741 := by
  have hU : (5464827261427978875833731975476585404931766523577 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (75235 : ℝ) * log 2 - 47468 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (50508 : ℝ) * log 2 - 31867 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 75235) (Q := 47468) (p := 50508) (v := 31867)
    (c := (5464827261427978875833731975476585404931766523577 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 47468 + 31867) hk.2
  exact pequeno_por_cota (s := 2195861) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_35 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 79335 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 190537) : n < 4912741 := by
  have hU : (1832360337604618888633459710654474994996874314651 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (125743 : ℝ) * log 2 - 79335 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (176251 : ℝ) * log 2 - 111202 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 125743) (Q := 79335) (p := 176251) (v := 111202)
    (c := (1832360337604618888633459710654474994996874314651 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 79335 + 111202) hk.2
  by_cases hsmall : n < 4912741
  · exact hsmall
  · have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 6548931)
      hw hr hr24 hk hf (by norm_num) hLambda (by norm_num)
    have hd := OcelotasVeinticuatroPrefijosBajo.descenso
      (by omega : 4912741 ≤ n) (by omega : n ≤ 6548930) hk _hcontador hqa
    omega

theorem fila_36 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 190537 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 10781274) : n < 4912741 := by
  have hU : (4031718923234723758330894560854947507357052547 / 62500000000000000000000000000000000000000000000000000 : ℝ) ≤ (301994 : ℝ) * log 2 - 190537 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (16785921 : ℝ) * log 2 - 10590737 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 301994) (Q := 190537) (p := 16785921) (v := 10590737)
    (c := (4031718923234723758330894560854947507357052547 / 62500000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 190537 + 10590737) hk.2
  by_cases hsmall : n < 4912741
  · exact hsmall
  · have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 372049746)
      hw hr hr24 hk hf (by norm_num) hLambda (by norm_num)
    have hd := OcelotasVeinticuatroPrefijosAlto.descenso
      (by omega : 4912741 ≤ n) (by omega : n ≤ 372049745) hk _hcontador hqa
    omega

theorem fila_37 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 10781274 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 64497107) : n < 4912741 := by
  have hU : (6103491390415145165428209095381068357941646781 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (17087915 : ℝ) * log 2 - 10781274 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (85137581 : ℝ) * log 2 - 53715833 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 17087915) (Q := 10781274) (p := 85137581) (v := 53715833)
    (c := (6103491390415145165428209095381068357941646781 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 10781274 + 53715833) hk.2
  have hpot : (1966087807 : ℕ) ^ 256 ≤ 2 ^ 7904 := by decide +kernel
  have hcriba : OcelotasAfinada.cota (1585 / 1000) (7904 / 256) 24 < 10781274 := by
    norm_num [OcelotasAfinada.cota]
  exact False.elim (imposible_por_criba (s := 1966087807) (B := 7904) hw hr hr24 hk hf
    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)

theorem fila_38 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 64497107 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 118212940) : n < 4912741 := by
  have hU : (436719695661308092592209808544683008879346031 / 50000000000000000000000000000000000000000000000000000 : ℝ) ≤ (102225496 : ℝ) * log 2 - 64497107 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (85137581 : ℝ) * log 2 - 53715833 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 102225496) (Q := 64497107) (p := 85137581) (v := 53715833)
    (c := (436719695661308092592209808544683008879346031 / 50000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 64497107 + 53715833) hk.2
  have hpot : (2747757915 : ℕ) ^ 256 ≤ 2 ^ 8028 := by decide +kernel
  have hcriba : OcelotasAfinada.cota (1585 / 1000) (8028 / 256) 24 < 64497107 := by
    norm_num [OcelotasAfinada.cota]
  exact False.elim (imposible_por_criba (s := 2747757915) (B := 8028) hw hr hr24 hk hf
    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)

theorem fila_39 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 118212940 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 171928773) : n < 4912741 := by
  have hU : (2630902522811016686415987075512591819645273839 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (187363077 : ℝ) * log 2 - 118212940 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (85137581 : ℝ) * log 2 - 53715833 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 187363077) (Q := 118212940) (p := 85137581) (v := 53715833)
    (c := (2630902522811016686415987075512591819645273839 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 118212940 + 53715833) hk.2
  have hpot : (4561172410 : ℕ) ^ 256 ≤ 2 ^ 8215 := by decide +kernel
  have hcriba : OcelotasAfinada.cota (1585 / 1000) (8215 / 256) 24 < 118212940 := by
    norm_num [OcelotasAfinada.cota]
  exact False.elim (imposible_por_criba (s := 4561172410) (B := 8215) hw hr hr24 hk hf
    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)

theorem fila_40 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 171928773 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 397573379) : n < 4912741 := by
  have hU : (111826011126119055863734508197294193812135921 / 62500000000000000000000000000000000000000000000000000 : ℝ) ≤ (272500658 : ℝ) * log 2 - 171928773 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (357638239 : ℝ) * log 2 - 225644606 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 272500658) (Q := 171928773) (p := 357638239) (v := 225644606)
    (c := (111826011126119055863734508197294193812135921 / 62500000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 171928773 + 225644606) hk.2
  have hpot : (13413694944 : ℕ) ^ 256 ≤ 2 ^ 8613 := by decide +kernel
  have hcriba : OcelotasAfinada.cota (1585 / 1000) (8613 / 256) 24 < 171928773 := by
    norm_num [OcelotasAfinada.cota]
  exact False.elim (imposible_por_criba (s := 13413694944) (B := 8613) hw hr hr24 hk hf
    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)

theorem fila_41 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 397573379 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 6586818670) : n < 4912741 := by
  have hU : (10584348843168130862728224244493766369197653 / 100000000000000000000000000000000000000000000000000000 : ℝ) ≤ (630138897 : ℝ) * log 2 - 397573379 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9809721694 : ℝ) * log 2 - 6189245291 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 630138897) (Q := 397573379) (p := 9809721694) (v := 6189245291)
    (c := (10584348843168130862728224244493766369197653 / 100000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 397573379 + 6189245291) hk.2
  have hpot : (226749896056 : ℕ) ^ 256 ≤ 2 ^ 9657 := by decide +kernel
  have hcriba : OcelotasAfinada.cota (1585 / 1000) (9657 / 256) 24 < 397573379 := by
    norm_num [OcelotasAfinada.cota]
  exact False.elim (imposible_por_criba (s := 226749896056) (B := 9657) hw hr hr24 hk hf
    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)

theorem fila_42 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 6586818670 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 39123338641) : n < 4912741 := by
  have hU : (5061562660338676422022995203616590884713137 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (10439860591 : ℝ) * log 2 - 6586818670 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (51569164058 : ℝ) * log 2 - 32536519971 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 10439860591) (Q := 6586818670) (p := 51569164058) (v := 32536519971)
    (c := (5061562660338676422022995203616590884713137 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 6586818670 + 32536519971) hk.2
  have hpot : (2370809334049 : ℕ) ^ 256 ≤ 2 ^ 10524 := by decide +kernel
  have hcriba : OcelotasAfinada.cota (1585 / 1000) (10524 / 256) 24 < 6586818670 := by
    norm_num [OcelotasAfinada.cota]
  exact False.elim (imposible_por_criba (s := 2370809334049) (B := 10524) hw hr hr24 hk hf
    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)

end OcelotasVeinticuatroTabla

#print axioms OcelotasVeinticuatroTabla.fila_30
#print axioms OcelotasVeinticuatroTabla.fila_31
#print axioms OcelotasVeinticuatroTabla.fila_32
#print axioms OcelotasVeinticuatroTabla.fila_33
#print axioms OcelotasVeinticuatroTabla.fila_34
#print axioms OcelotasVeinticuatroTabla.fila_35
#print axioms OcelotasVeinticuatroTabla.fila_36
#print axioms OcelotasVeinticuatroTabla.fila_37
#print axioms OcelotasVeinticuatroTabla.fila_38
#print axioms OcelotasVeinticuatroTabla.fila_39
#print axioms OcelotasVeinticuatroTabla.fila_40
#print axioms OcelotasVeinticuatroTabla.fila_41
#print axioms OcelotasVeinticuatroTabla.fila_42
