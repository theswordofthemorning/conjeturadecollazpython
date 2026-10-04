import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasSetentaYSeisPrefijosBinarios

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasSetentaYSeisTablaBinaria
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_80 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 61861883948053347 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 68096433875295310) : n < 28000000000000000001 := by
  have hU : (29651331926260770413561606047995654619 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (98048766281628583 : ℝ) * log 2 - 61861883948053347 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 98048766281628583) (Q := 61861883948053347) (p := 9881527843552324) (v := 6234549927241963)
    (c := (29651331926260770413561606047995654619 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 61861883948053347 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 1281561317194834425) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_81 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 68096433875295310 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 74330983802537273) : n < 28000000000000000001 := by
  have hU : (27037268618517538515155831085403282629 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (107930294125180907 : ℝ) * log 2 - 68096433875295310 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 107930294125180907) (Q := 68096433875295310) (p := 9881527843552324) (v := 6234549927241963)
    (c := (27037268618517538515155831085403282629 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 68096433875295310 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 1405467413745122281) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_82 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 74330983802537273 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 80565533729779236) : n < 28000000000000000001 := by
  have hU : (24423205310774306616750056122810910639 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (117811821968733231 : ℝ) * log 2 - 74330983802537273 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 117811821968733231) (Q := 74330983802537273) (p := 9881527843552324) (v := 6234549927241963)
    (c := (24423205310774306616750056122810910639 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 74330983802537273 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 1555897332740198728) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_83 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 80565533729779236 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 86800083657021199) : n < 28000000000000000001 := by
  have hU : (21809142003031074718344281160218538649 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (127693349812285555 : ℝ) * log 2 - 80565533729779236 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 127693349812285555) (Q := 80565533729779236) (p := 9881527843552324) (v := 6234549927241963)
    (c := (21809142003031074718344281160218538649 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 80565533729779236 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 1742388581573667136) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_84 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 86800083657021199 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 93034633584263162) : n < 28000000000000000001 := by
  have hU : (19195078695287842819938506197626166659 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (137574877655837879 : ℝ) * log 2 - 86800083657021199 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 137574877655837879) (Q := 86800083657021199) (p := 9881527843552324) (v := 6234549927241963)
    (c := (19195078695287842819938506197626166659 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 86800083657021199 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 1979674092679210297) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_85 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 93034633584263162 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 99269183511505125) : n < 28000000000000000001 := by
  have hU : (16581015387544610921532731235033794669 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (147456405499390203 : ℝ) * log 2 - 93034633584263162 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 147456405499390203) (Q := 93034633584263162) (p := 9881527843552324) (v := 6234549927241963)
    (c := (16581015387544610921532731235033794669 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 93034633584263162 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 2291777621082541300) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_86 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 99269183511505125 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 105503733438747088) : n < 28000000000000000001 := by
  have hU : (13966952079801379023126956272441422679 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (157337933342942527 : ℝ) * log 2 - 99269183511505125 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 157337933342942527) (Q := 99269183511505125) (p := 9881527843552324) (v := 6234549927241963)
    (c := (13966952079801379023126956272441422679 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 99269183511505125 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 2720708124641921855) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_87 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 105503733438747088 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 111738283365989051) : n < 28000000000000000001 := by
  have hU : (11352888772058147124721181309849050689 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (167219461186494851 : ℝ) * log 2 - 105503733438747088 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 167219461186494851) (Q := 105503733438747088) (p := 9881527843552324) (v := 6234549927241963)
    (c := (11352888772058147124721181309849050689 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 105503733438747088 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 3347165709359014580) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_88 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 111738283365989051 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 117972833293231014) : n < 28000000000000000001 := by
  have hU : (8738825464314915226315406347256678699 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (177100989030047175 : ℝ) * log 2 - 111738283365989051 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 177100989030047175) (Q := 111738283365989051) (p := 9881527843552324) (v := 6234549927241963)
    (c := (8738825464314915226315406347256678699 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 111738283365989051 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 4348410453461211197) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_89 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 117972833293231014 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 124207383220472977) : n < 28000000000000000001 := by
  have hU : (6124762156571683327909631384664306709 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (186982516873599499 : ℝ) * log 2 - 117972833293231014 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 186982516873599499) (Q := 117972833293231014) (p := 9881527843552324) (v := 6234549927241963)
    (c := (6124762156571683327909631384664306709 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 117972833293231014 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 6204322556301579303) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_90 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 124207383220472977 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 130441933147714940) : n < 28000000000000000001 := by
  have hU : (3510698848828451429503856422071934719 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (196864044717151823 : ℝ) * log 2 - 124207383220472977 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 196864044717151823) (Q := 124207383220472977) (p := 9881527843552324) (v := 6234549927241963)
    (c := (3510698848828451429503856422071934719 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 124207383220472977 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 10824055732573275837) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_91 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 130441933147714940 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 397560349370386783) : n < 28000000000000000001 := by
  have hU : (896635541085219531098081459479562729 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (206745572560704147 : ℝ) * log 2 - 130441933147714940 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (423372672964960618 : ℝ) * log 2 - 267118416222671843 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 206745572560704147) (Q := 130441933147714940) (p := 423372672964960618) (v := 267118416222671843)
    (c := (896635541085219531098081459479562729 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 130441933147714940 + 267118416222671843) hk.2
  by_cases hsmall : n < 28000000000000000001
  · exact hsmall
  · have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 42380653296441592425)
      hw hr hr76 hk hf (by norm_num) hLambda (by norm_num)
    have hd := OcelotasSetentaYSeisPrefijosBinarios.descenso
      (by omega : 28000000000000000001 ≤ n) (by omega : n ≤ 42380653296441592424) hk _hcontador hqa
    omega

theorem fila_92 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 397560349370386783 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 4640282259296926456) : n < 28000000000000000001 := by
  have hU : (75843315512426694888469415846316197 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (630118245525664765 : ℝ) * log 2 - 397560349370386783 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (6724555128221608268 : ℝ) * log 2 - 4242721909926539673 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 630118245525664765) (Q := 397560349370386783) (p := 6724555128221608268) (v := 4242721909926539673)
    (c := (75843315512426694888469415846316197 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 397560349370386783 + 4242721909926539673) hk.2
  have hpot : (501032948563196929585 : ℕ) ^ 256 ≤ 2 ^ 17604 := by decide +kernel
  have hcriba : OcelotasAfinada.cota (1585 / 1000) (17604 / 256) 76 < 397560349370386783 := by
    norm_num [OcelotasAfinada.cota]
  exact False.elim (imposible_por_criba (s := 501032948563196929585) (B := 17604) hw hr hr76 hk hf
    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)

theorem fila_93 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 4640282259296926456 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 27444133206411171953) : n < 28000000000000000001 := by
  have hU : (2696849012780161512710306135246327 / 100000000000000000000000000000000000000000000000000000 : ℝ) ≤ (7354673373747273033 : ℝ) * log 2 - 4640282259296926456 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (36143248623210700400 : ℝ) * log 2 - 22803850947114245497 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 7354673373747273033) (Q := 4640282259296926456) (p := 36143248623210700400) (v := 22803850947114245497)
    (c := (2696849012780161512710306135246327 / 100000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 4640282259296926456 + 22803850947114245497) hk.2
  have hpot : (2818103632789296105714 : ℕ) ^ 256 ≤ 2 ^ 18242 := by decide +kernel
  have hcriba : OcelotasAfinada.cota (1585 / 1000) (18242 / 256) 76 < 4640282259296926456 := by
    norm_num [OcelotasAfinada.cota]
  exact False.elim (imposible_por_criba (s := 2818103632789296105714) (B := 18242) hw hr hr76 hk hf
    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)

theorem fila_94 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 27444133206411171953 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 77692117359936589403) : n < 28000000000000000001 := by
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
  have hpot : (7506684597474065972500 : ℕ) ^ 256 ≤ 2 ^ 18604 := by decide +kernel
  have hcriba : OcelotasAfinada.cota (1585 / 1000) (18604 / 256) 76 < 27444133206411171953 := by
    norm_num [OcelotasAfinada.cota]
  exact False.elim (imposible_por_criba (s := 7506684597474065972500) (B := 18604) hw hr hr76 hk hf
    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)

theorem fila_95 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 77692117359936589403 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 205632218873398596256) : n < 28000000000000000001 := by
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
  have hpot : (22323794848656705295748 : ℕ) ^ 256 ≤ 2 ^ 19006 := by decide +kernel
  have hcriba : OcelotasAfinada.cota (1585 / 1000) (19006 / 256) 76 < 77692117359936589403 := by
    norm_num [OcelotasAfinada.cota]
  exact False.elim (imposible_por_criba (s := 22323794848656705295748) (B := 19006) hw hr hr76 hk hf
    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)

end OcelotasSetentaYSeisTablaBinaria

#print axioms OcelotasSetentaYSeisTablaBinaria.fila_80
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_81
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_82
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_83
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_84
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_85
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_86
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_87
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_88
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_89
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_90
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_91
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_92
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_93
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_94
#print axioms OcelotasSetentaYSeisTablaBinaria.fila_95
