import OcelotasNumerica
import OcelotasLogaritmosPrecisos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasSetentaYCincoTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_64 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr75 : r ≤ 75)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 2365627332311699 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 2849242656677982) : n < 28000000000000000001 := by
  have hU : (221860828360900741641274535214381312081 / 250000000000000000000000000000000000000000000000000000 : ℝ) ≤ (3749430612395068 : ℝ) * log 2 - 2365627332311699 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (766512153894657 : ℝ) * log 2 - 483615324366283 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 3749430612395068) (Q := 2365627332311699) (p := 766512153894657) (v := 483615324366283)
    (c := (221860828360900741641274535214381312081 / 250000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 2365627332311699 + 483615324366283) hk.2
  exact pequeno_por_cota (s := 84512440246997536) hw hr hr75 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_65 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr75 : r ≤ 75)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 2849242656677982 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 3332857981044265) : n < 28000000000000000001 := by
  have hU : (387929691718108393884929714754843249643 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (4515942766289725 : ℝ) * log 2 - 2849242656677982 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (766512153894657 : ℝ) * log 2 - 483615324366283 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 4515942766289725) (Q := 2849242656677982) (p := 766512153894657) (v := 483615324366283)
    (c := (387929691718108393884929714754843249643 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 2849242656677982 + 483615324366283) hk.2
  exact pequeno_por_cota (s := 96667001264882855) hw hr hr75 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_66 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr75 : r ≤ 75)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 3332857981044265 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 3816473305410548) : n < 28000000000000000001 := by
  have hU : (83034431678603826121827589770230968781 / 125000000000000000000000000000000000000000000000000000 : ℝ) ≤ (5282454920184382 : ℝ) * log 2 - 3332857981044265 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (766512153894657 : ℝ) * log 2 - 483615324366283 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 5282454920184382) (Q := 3332857981044265) (p := 766512153894657) (v := 483615324366283)
    (c := (83034431678603826121827589770230968781 / 125000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 3332857981044265 + 483615324366283) hk.2
  exact pequeno_por_cota (s := 112904969787560242) hw hr hr75 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_67 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr75 : r ≤ 75)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 3816473305410548 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 4300088629776831) : n < 28000000000000000001 := by
  have hU : (55269152342144443017938200681400900121 / 100000000000000000000000000000000000000000000000000000 : ℝ) ≤ (6048967074079039 : ℝ) * log 2 - 3816473305410548 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (766512153894657 : ℝ) * log 2 - 483615324366283 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 6048967074079039) (Q := 3816473305410548) (p := 766512153894657) (v := 483615324366283)
    (c := (55269152342144443017938200681400900121 / 100000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 3816473305410548 + 483615324366283) hk.2
  exact pequeno_por_cota (s := 135699566253000363) hw hr hr75 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_68 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr75 : r ≤ 75)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 4300088629776831 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 4783703954143114) : n < 28000000000000000001 := by
  have hU : (110276898353514562846035823866542563043 / 250000000000000000000000000000000000000000000000000000 : ℝ) ≤ (6815479227973696 : ℝ) * log 2 - 4300088629776831 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (766512153894657 : ℝ) * log 2 - 483615324366283 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 6815479227973696) (Q := 4300088629776831) (p := 766512153894657) (v := 483615324366283)
    (c := (110276898353514562846035823866542563043 / 250000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 4300088629776831 + 483615324366283) hk.2
  exact pequeno_por_cota (s := 170026544815335125) hw hr hr75 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_69 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr75 : r ≤ 75)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 4783703954143114 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 5267319278509397) : n < 28000000000000000001 := by
  have hU : (164761831703336036294452292059165751567 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (7581991381868353 : ℝ) * log 2 - 4783703954143114 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (766512153894657 : ℝ) * log 2 - 483615324366283 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 7581991381868353) (Q := 4783703954143114) (p := 766512153894657) (v := 483615324366283)
    (c := (164761831703336036294452292059165751567 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 4783703954143114 + 483615324366283) hk.2
  exact pequeno_por_cota (s := 227601256992099306) hw hr hr75 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_70 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr75 : r ≤ 75)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 5267319278509397 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 5750934602875680) : n < 28000000000000000001 := by
  have hU : (13621233337455368362104117048155797131 / 62500000000000000000000000000000000000000000000000000 : ℝ) ≤ (8348503535763010 : ℝ) * log 2 - 5267319278509397 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (766512153894657 : ℝ) * log 2 - 483615324366283 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 8348503535763010) (Q := 5267319278509397) (p := 766512153894657) (v := 483615324366283)
    (c := (13621233337455368362104117048155797131 / 62500000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 5267319278509397 + 483615324366283) hk.2
  exact pequeno_por_cota (s := 344131833283438103) hw hr hr75 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_71 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr75 : r ≤ 75)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 5750934602875680 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 11985484530117643) : n < 28000000000000000001 := by
  have hU : (53177901695949857499213580711327002529 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (9115015689657667 : ℝ) * log 2 - 5750934602875680 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 9115015689657667) (Q := 5750934602875680) (p := 9881527843552324) (v := 6234549927241963)
    (c := (53177901695949857499213580711327002529 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 5750934602875680 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 705180136937521927) hw hr hr75 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_72 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr75 : r ≤ 75)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 11985484530117643 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 18220034457359606) : n < 28000000000000000001 := by
  have hU : (50563838388206625600807805748734630539 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (18996543533209991 : ℝ) * log 2 - 11985484530117643 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 18996543533209991) (Q := 11985484530117643) (p := 9881527843552324) (v := 6234549927241963)
    (c := (50563838388206625600807805748734630539 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 11985484530117643 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 741636734776575026) hw hr hr75 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_73 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr75 : r ≤ 75)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 18220034457359606 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 24454584384601569) : n < 28000000000000000001 := by
  have hU : (47949775080463393702402030786142258549 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (28878071376762315 : ℝ) * log 2 - 18220034457359606 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 28878071376762315) (Q := 18220034457359606) (p := 9881527843552324) (v := 6234549927241963)
    (c := (47949775080463393702402030786142258549 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 18220034457359606 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 782068319133345859) hw hr hr75 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_74 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr75 : r ≤ 75)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 24454584384601569 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 30689134311843532) : n < 28000000000000000001 := by
  have hU : (45335711772720161803996255823549886559 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (38759599220314639 : ℝ) * log 2 - 24454584384601569 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 38759599220314639) (Q := 24454584384601569) (p := 9881527843552324) (v := 6234549927241963)
    (c := (45335711772720161803996255823549886559 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 24454584384601569 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 827162484797798163) hw hr hr75 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_75 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr75 : r ≤ 75)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 30689134311843532 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 36923684239085495) : n < 28000000000000000001 := by
  have hU : (42721648464976929905590480860957514569 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (48641127063866963 : ℝ) * log 2 - 30689134311843532 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 48641127063866963) (Q := 30689134311843532) (p := 9881527843552324) (v := 6234549927241963)
    (c := (42721648464976929905590480860957514569 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 30689134311843532 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 877775117473343274) hw hr hr75 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_76 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr75 : r ≤ 75)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 36923684239085495 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 43158234166327458) : n < 28000000000000000001 := by
  have hU : (40107585157233698007184705898365142579 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (58522654907419287 : ℝ) * log 2 - 36923684239085495 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 58522654907419287) (Q := 36923684239085495) (p := 9881527843552324) (v := 6234549927241963)
    (c := (40107585157233698007184705898365142579 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 36923684239085495 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 934985236657575211) hw hr hr75 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_77 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr75 : r ≤ 75)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 43158234166327458 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 49392784093569421) : n < 28000000000000000001 := by
  have hU : (37493521849490466108778930935772770589 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (68404182750971611 : ℝ) * log 2 - 43158234166327458 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 68404182750971611) (Q := 43158234166327458) (p := 9881527843552324) (v := 6234549927241963)
    (c := (37493521849490466108778930935772770589 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 43158234166327458 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 1000172780528208020) hw hr hr75 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_78 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr75 : r ≤ 75)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 49392784093569421 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 55627334020811384) : n < 28000000000000000001 := by
  have hU : (34879458541747234210373155973180398599 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (78285710594523935 : ℝ) * log 2 - 49392784093569421 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 78285710594523935) (Q := 49392784093569421) (p := 9881527843552324) (v := 6234549927241963)
    (c := (34879458541747234210373155973180398599 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 49392784093569421 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 1075131368656891246) hw hr hr75 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_79 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr75 : r ≤ 75)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 55627334020811384 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 61861883948053347) : n < 28000000000000000001 := by
  have hU : (32265395234004002311967381010588026609 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (88167238438076259 : ℝ) * log 2 - 55627334020811384 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9881527843552324 : ℝ) * log 2 - 6234549927241963 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 88167238438076259) (Q := 55627334020811384) (p := 9881527843552324) (v := 6234549927241963)
    (c := (32265395234004002311967381010588026609 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 55627334020811384 + 6234549927241963) hk.2
  exact pequeno_por_cota (s := 1162235879276610518) hw hr hr75 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

end OcelotasSetentaYCincoTabla

#print axioms OcelotasSetentaYCincoTabla.fila_64
#print axioms OcelotasSetentaYCincoTabla.fila_65
#print axioms OcelotasSetentaYCincoTabla.fila_66
#print axioms OcelotasSetentaYCincoTabla.fila_67
#print axioms OcelotasSetentaYCincoTabla.fila_68
#print axioms OcelotasSetentaYCincoTabla.fila_69
#print axioms OcelotasSetentaYCincoTabla.fila_70
#print axioms OcelotasSetentaYCincoTabla.fila_71
#print axioms OcelotasSetentaYCincoTabla.fila_72
#print axioms OcelotasSetentaYCincoTabla.fila_73
#print axioms OcelotasSetentaYCincoTabla.fila_74
#print axioms OcelotasSetentaYCincoTabla.fila_75
#print axioms OcelotasSetentaYCincoTabla.fila_76
#print axioms OcelotasSetentaYCincoTabla.fila_77
#print axioms OcelotasSetentaYCincoTabla.fila_78
#print axioms OcelotasSetentaYCincoTabla.fila_79
