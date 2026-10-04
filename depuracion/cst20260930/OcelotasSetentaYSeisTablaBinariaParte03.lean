import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasSetentaYSeisPrefijosBinarios

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasSetentaYSeisTablaBinaria
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_32 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 14936 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 15601) : n < 28000000000000000001 := by
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
  exact pequeno_por_cota (s := 1228806) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_33 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 15601 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 47468) : n < 28000000000000000001 := by
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
  exact pequeno_por_cota (s := 4177067) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_34 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 47468 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 79335) : n < 28000000000000000001 := by
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
  exact pequeno_por_cota (s := 6953560) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_35 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 79335 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 190537) : n < 28000000000000000001 := by
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
  exact pequeno_por_cota (s := 20738280) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_36 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 190537 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 10781274) : n < 28000000000000000001 := by
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
  exact pequeno_por_cota (s := 1178157528) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_37 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 10781274 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 64497107) : n < 28000000000000000001 := by
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
  exact pequeno_por_cota (s := 6225944721) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_38 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 64497107 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 118212940) : n < 28000000000000000001 := by
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
  exact pequeno_por_cota (s := 8701233395) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_39 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 118212940 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 171928773) : n < 28000000000000000001 := by
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
  exact pequeno_por_cota (s := 14443712632) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_40 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 171928773 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 397573379) : n < 28000000000000000001 := by
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
  exact pequeno_por_cota (s := 42476700655) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_41 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 397573379 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 6586818670) : n < 28000000000000000001 := by
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
  exact pequeno_por_cota (s := 718041337509) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_42 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 6586818670 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 72057431991) : n < 28000000000000000001 := by
  have hU : (5061562660338676422022995203616590884713137 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (10439860591 : ℝ) * log 2 - 6586818670 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (103768467013 : ℝ) * log 2 - 65470613321 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 10439860591) (Q := 6586818670) (p := 103768467013) (v := 65470613321)
    (c := (5061562660338676422022995203616590884713137 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 6586818670 + 65470613321) hk.2
  exact pequeno_por_cota (s := 7507562891153) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_43 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 72057431991 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 137528045312) : n < 28000000000000000001 := by
  have hU : (1377722523942393164305913008656833942928121 / 250000000000000000000000000000000000000000000000000000 : ℝ) ≤ (114208327604 : ℝ) * log 2 - 72057431991 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (103768467013 : ℝ) * log 2 - 65470613321 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 114208327604) (Q := 72057431991) (p := 103768467013) (v := 65470613321)
    (c := (1377722523942393164305913008656833942928121 / 250000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 72057431991 + 65470613321) hk.2
  exact pequeno_por_cota (s := 13790875644271) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_44 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 137528045312 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 890638885193) : n < 28000000000000000001 := by
  have hU : (449327435430896235200656831010744886999347 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (217976794617 : ℝ) * log 2 - 137528045312 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1193652440098 : ℝ) * log 2 - 753110839881 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 217976794617) (Q := 137528045312) (p := 1193652440098) (v := 753110839881)
    (c := (449327435430896235200656831010744886999347 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 137528045312 + 753110839881) hk.2
  exact pequeno_por_cota (s := 84570843005745) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_45 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 890638885193 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 1643749725074) : n < 28000000000000000001 := by
  have hU : (389847000131487317792771799761546323139187 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (1411629234715 : ℝ) * log 2 - 890638885193 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1193652440098 : ℝ) * log 2 - 753110839881 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 1411629234715) (Q := 890638885193) (p := 1193652440098) (v := 753110839881)
    (c := (389847000131487317792771799761546323139187 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 890638885193 + 753110839881) hk.2
  exact pequeno_por_cota (s := 97474137256882) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_46 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 1643749725074 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 2396860564955) : n < 28000000000000000001 := by
  have hU : (330366564832078400384886768512347759279027 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (2605281674813 : ℝ) * log 2 - 1643749725074 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1193652440098 : ℝ) * log 2 - 753110839881 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 2605281674813) (Q := 1643749725074) (p := 1193652440098) (v := 753110839881)
    (c := (330366564832078400384886768512347759279027 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 1643749725074 + 753110839881) hk.2
  exact pequeno_por_cota (s := 115023746483895) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_47 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 2396860564955 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 3149971404836) : n < 28000000000000000001 := by
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
  exact pequeno_por_cota (s := 140280346083269) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

end OcelotasSetentaYSeisTablaBinaria

#print axioms OcelotasSetentaYSeisTablaBinaria.fila_32
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_33
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_34
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_35
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_36
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_37
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_38
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_39
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_40
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_41
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_42
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_43
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_44
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_45
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_46
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_47
