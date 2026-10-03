import OcelotasNumerica
import OcelotasVeintePrefijos

/-! # Ocelotas: tabla de veinte rachas

Generada por generar_veinte_lean.py. Todas las obligaciones se certifican en Lean.
-/

namespace OcelotasVeinteTabla

open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_0 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 1 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 3) : n < 4912741 := by
  have hU : (28768207245178092727 / 100000000000000000000 : ℝ) ≤ (2 : ℝ) * log 2 - 1 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (3 : ℝ) * log 2 - 2 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 2) (Q := 1) (p := 3) (v := 2)
    (c := (28768207245178092727 / 100000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 1 + 2) hk.2
  exact pequeno_por_cota (s := 70) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_1 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 3 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 5) : n < 4912741 := by
  have hU : (2654672449928085507 / 15625000000000000000 : ℝ) ≤ (5 : ℝ) * log 2 - 3 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (3 : ℝ) * log 2 - 2 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 5) (Q := 3) (p := 3) (v := 2)
    (c := (2654672449928085507 / 15625000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 3 + 2) hk.2
  exact pequeno_por_cota (s := 118) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_2 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 5 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 17) : n < 4912741 := by
  have hU : (26058000569507008813 / 500000000000000000000 : ℝ) ≤ (8 : ℝ) * log 2 - 5 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (19 : ℝ) * log 2 - 12 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 8) (Q := 5) (p := 19) (v := 12)
    (c := (26058000569507008813 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 5 + 12) hk.2
  exact pequeno_por_cota (s := 384) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_3 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 17 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 29) : n < 4912741 := by
  have hU : (4820620970082324757 / 125000000000000000000 : ℝ) ≤ (27 : ℝ) * log 2 - 17 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (19 : ℝ) * log 2 - 12 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 27) (Q := 17) (p := 19) (v := 12)
    (c := (4820620970082324757 / 125000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 17 + 12) hk.2
  exact pequeno_por_cota (s := 519) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_4 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 29 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 41) : n < 4912741 := by
  have hU : (12506967191151589243 / 500000000000000000000 : ℝ) ≤ (46 : ℝ) * log 2 - 29 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (19 : ℝ) * log 2 - 12 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 46) (Q := 29) (p := 19) (v := 12)
    (c := (12506967191151589243 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 29 + 12) hk.2
  exact pequeno_por_cota (s := 800) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_5 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 41 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 94) : n < 4912741 := by
  have hU : (2865725250986939729 / 250000000000000000000 : ℝ) ≤ (65 : ℝ) * log 2 - 41 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (84 : ℝ) * log 2 - 53 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 65) (Q := 41) (p := 84) (v := 53)
    (c := (2865725250986939729 / 250000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 41 + 53) hk.2
  exact pequeno_por_cota (s := 1745) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_6 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 94 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 147) : n < 4912741 := by
  have hU : (4687384314770049131 / 500000000000000000000 : ℝ) ≤ (149 : ℝ) * log 2 - 94 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (84 : ℝ) * log 2 - 53 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 149) (Q := 94) (p := 84) (v := 53)
    (c := (4687384314770049131 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 94 + 53) hk.2
  exact pequeno_por_cota (s := 2134) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_7 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 147 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 200) : n < 4912741 := by
  have hU : (910829531891554701 / 125000000000000000000 : ℝ) ≤ (233 : ℝ) * log 2 - 147 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (84 : ℝ) * log 2 - 53 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 233) (Q := 147) (p := 84) (v := 53)
    (c := (910829531891554701 / 125000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 147 + 53) hk.2
  exact pequeno_por_cota (s := 2745) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_8 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 200 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 253) : n < 4912741 := by
  have hU : (2599251940362388477 / 500000000000000000000 : ℝ) ≤ (317 : ℝ) * log 2 - 200 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (84 : ℝ) * log 2 - 53 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 317) (Q := 200) (p := 84) (v := 53)
    (c := (2599251940362388477 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 200 + 53) hk.2
  exact pequeno_por_cota (s := 3848) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_9 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 253 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 306) : n < 4912741 := by
  have hU : (31103715063171163 / 10000000000000000000 : ℝ) ≤ (401 : ℝ) * log 2 - 253 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (84 : ℝ) * log 2 - 53 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 401) (Q := 253) (p := 84) (v := 53)
    (c := (31103715063171163 / 10000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 253 + 53) hk.2
  exact pequeno_por_cota (s := 6431) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_10 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 306 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 971) : n < 4912741 := by
  have hU : (511119565954727823 / 500000000000000000000 : ℝ) ≤ (485 : ℝ) * log 2 - 306 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 485) (Q := 306) (p := 1054) (v := 665)
    (c := (511119565954727823 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 306 + 665) hk.2
  exact pequeno_por_cota (s := 19565) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_11 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 971 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 1636) : n < 4912741 := by
  have hU : (244646255330176571 / 250000000000000000000 : ℝ) ≤ (1539 : ℝ) * log 2 - 971 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 1539) (Q := 971) (p := 1054) (v := 665)
    (c := (244646255330176571 / 250000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 971 + 665) hk.2
  exact pequeno_por_cota (s := 20438) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_12 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 1636 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 2301) : n < 4912741 := by
  have hU : (467465455365978461 / 500000000000000000000 : ℝ) ≤ (2593 : ℝ) * log 2 - 1636 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 2593) (Q := 1636) (p := 1054) (v := 665)
    (c := (467465455365978461 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 1636 + 665) hk.2
  exact pequeno_por_cota (s := 21392) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_13 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 2301 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 2966) : n < 4912741 := by
  have hU : (22281920003580189 / 25000000000000000000 : ℝ) ≤ (3647 : ℝ) * log 2 - 2301 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 3647) (Q := 2301) (p := 1054) (v := 665)
    (c := (22281920003580189 / 25000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 2301 + 665) hk.2
  exact pequeno_por_cota (s := 22440) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_14 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 2966 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 3631) : n < 4912741 := by
  have hU : (423811344777229099 / 500000000000000000000 : ℝ) ≤ (4701 : ℝ) * log 2 - 2966 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 4701) (Q := 2966) (p := 1054) (v := 665)
    (c := (423811344777229099 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 2966 + 665) hk.2
  exact pequeno_por_cota (s := 23596) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_15 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 3631 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 4296) : n < 4912741 := by
  have hU : (200992144741427209 / 250000000000000000000 : ℝ) ≤ (5755 : ℝ) * log 2 - 3631 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 5755) (Q := 3631) (p := 1054) (v := 665)
    (c := (200992144741427209 / 250000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 3631 + 665) hk.2
  exact pequeno_por_cota (s := 24877) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_16 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 4296 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 4961) : n < 4912741 := by
  have hU : (380157234188479737 / 500000000000000000000 : ℝ) ≤ (6809 : ℝ) * log 2 - 4296 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 6809) (Q := 4296) (p := 1054) (v := 665)
    (c := (380157234188479737 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 4296 + 665) hk.2
  exact pequeno_por_cota (s := 26305) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_17 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 4961 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 5626) : n < 4912741 := by
  have hU : (11197818090440783 / 15625000000000000000 : ℝ) ≤ (7863 : ℝ) * log 2 - 4961 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 7863) (Q := 4961) (p := 1054) (v := 665)
    (c := (11197818090440783 / 15625000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 4961 + 665) hk.2
  exact pequeno_por_cota (s := 27908) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_18 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 5626 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 6291) : n < 4912741 := by
  have hU : (2692024988797843 / 4000000000000000000 : ℝ) ≤ (8917 : ℝ) * log 2 - 5626 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 8917) (Q := 5626) (p := 1054) (v := 665)
    (c := (2692024988797843 / 4000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 5626 + 665) hk.2
  exact pequeno_por_cota (s := 29718) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_19 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 6291 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 6956) : n < 4912741 := by
  have hU : (157338034152677847 / 250000000000000000000 : ℝ) ≤ (9971 : ℝ) * log 2 - 6291 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 9971) (Q := 6291) (p := 1054) (v := 665)
    (c := (157338034152677847 / 250000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 6291 + 665) hk.2
  exact pequeno_por_cota (s := 31779) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_20 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 6956 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 7621) : n < 4912741 := by
  have hU : (292849013010981013 / 500000000000000000000 : ℝ) ≤ (11025 : ℝ) * log 2 - 6956 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 11025) (Q := 6956) (p := 1054) (v := 665)
    (c := (292849013010981013 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 6956 + 665) hk.2
  exact pequeno_por_cota (s := 34148) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_21 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 7621 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 8286) : n < 4912741 := by
  have hU : (67755489429151583 / 125000000000000000000 : ℝ) ≤ (12079 : ℝ) * log 2 - 7621 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 12079) (Q := 7621) (p := 1054) (v := 665)
    (c := (67755489429151583 / 125000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 7621 + 665) hk.2
  exact pequeno_por_cota (s := 36898) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_22 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 8286 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 8951) : n < 4912741 := by
  have hU : (249194902422231651 / 500000000000000000000 : ℝ) ≤ (13133 : ℝ) * log 2 - 8286 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 13133) (Q := 8286) (p := 1054) (v := 665)
    (c := (249194902422231651 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 8286 + 665) hk.2
  exact pequeno_por_cota (s := 40130) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_23 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 8951 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 9616) : n < 4912741 := by
  have hU : (22736784712785697 / 50000000000000000000 : ℝ) ≤ (14187 : ℝ) * log 2 - 8951 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 14187) (Q := 8951) (p := 1054) (v := 665)
    (c := (22736784712785697 / 50000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 8951 + 665) hk.2
  exact pequeno_por_cota (s := 43982) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_24 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 9616 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 10281) : n < 4912741 := by
  have hU : (205540791833482289 / 500000000000000000000 : ℝ) ≤ (15241 : ℝ) * log 2 - 9616 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 15241) (Q := 9616) (p := 1054) (v := 665)
    (c := (205540791833482289 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 9616 + 665) hk.2
  exact pequeno_por_cota (s := 48653) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_25 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 10281 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 10946) : n < 4912741 := by
  have hU : (22964217067388451 / 62500000000000000000 : ℝ) ≤ (16295 : ℝ) * log 2 - 10281 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 16295) (Q := 10281) (p := 1054) (v := 665)
    (c := (22964217067388451 / 62500000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 10281 + 665) hk.2
  exact pequeno_por_cota (s := 54433) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_26 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 10946 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 11611) : n < 4912741 := by
  have hU : (161886681244732927 / 500000000000000000000 : ℝ) ≤ (17349 : ℝ) * log 2 - 10946 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 17349) (Q := 10946) (p := 1054) (v := 665)
    (c := (161886681244732927 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 10946 + 665) hk.2
  exact pequeno_por_cota (s := 61772) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_27 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 11611 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 12276) : n < 4912741 := by
  have hU : (70029812975179123 / 250000000000000000000 : ℝ) ≤ (18403 : ℝ) * log 2 - 11611 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 18403) (Q := 11611) (p := 1054) (v := 665)
    (c := (70029812975179123 / 250000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 11611 + 665) hk.2
  exact pequeno_por_cota (s := 71399) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_28 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 12276 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 12941) : n < 4912741 := by
  have hU : (23646514131196713 / 100000000000000000000 : ℝ) ≤ (19457 : ℝ) * log 2 - 12276 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 19457) (Q := 12276) (p := 1054) (v := 665)
    (c := (23646514131196713 / 100000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 12276 + 665) hk.2
  exact pequeno_por_cota (s := 84580) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_29 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 12941 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 13606) : n < 4912741 := by
  have hU : (24101378840402221 / 125000000000000000000 : ℝ) ≤ (20511 : ℝ) * log 2 - 12941 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 20511) (Q := 12941) (p := 1054) (v := 665)
    (c := (24101378840402221 / 125000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 12941 + 665) hk.2
  exact pequeno_por_cota (s := 103729) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_30 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 13606 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 14271) : n < 4912741 := by
  have hU : (74578460067234203 / 500000000000000000000 : ℝ) ≤ (21565 : ℝ) * log 2 - 13606 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 21565) (Q := 13606) (p := 1054) (v := 665)
    (c := (74578460067234203 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 13606 + 665) hk.2
  exact pequeno_por_cota (s := 134087) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_31 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 14271 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 14936) : n < 4912741 := by
  have hU : (26375702386429761 / 250000000000000000000 : ℝ) ≤ (22619 : ℝ) * log 2 - 14271 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 22619) (Q := 14271) (p := 1054) (v := 665)
    (c := (26375702386429761 / 250000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 14271 + 665) hk.2
  exact pequeno_por_cota (s := 189569) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_32 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 14936 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 15601) : n < 4912741 := by
  have hU : (30924349478484841 / 500000000000000000000 : ℝ) ≤ (23673 : ℝ) * log 2 - 14936 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 23673) (Q := 14936) (p := 1054) (v := 665)
    (c := (30924349478484841 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 14936 + 665) hk.2
  exact pequeno_por_cota (s := 323370) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_33 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 15601 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 47468) : n < 4912741 := by
  have hU : (113716177301377 / 6250000000000000000 : ℝ) ≤ (24727 : ℝ) * log 2 - 15601 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (50508 : ℝ) * log 2 - 31867 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 24727) (Q := 15601) (p := 50508) (v := 31867)
    (c := (113716177301377 / 6250000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 15601 + 31867) hk.2
  exact pequeno_por_cota (s := 1099228) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_34 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 47468 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 79335) : n < 4912741 := by
  have hU : (5464827257955799 / 500000000000000000000 : ℝ) ≤ (75235 : ℝ) * log 2 - 47468 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (50508 : ℝ) * log 2 - 31867 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 75235) (Q := 47468) (p := 50508) (v := 31867)
    (c := (5464827257955799 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 47468 + 31867) hk.2
  exact pequeno_por_cota (s := 1829885) hw hr hr20 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_35 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 79335 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 190537) : n < 4912741 := by
  have hU : (916180165900719 / 250000000000000000000 : ℝ) ≤ (125743 : ℝ) * log 2 - 79335 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (176251 : ℝ) * log 2 - 111202 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 125743) (Q := 79335) (p := 176251) (v := 111202)
    (c := (916180165900719 / 250000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 79335 + 111202) hk.2
  by_cases hsmall : n < 4912741
  · exact hsmall
  · have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 5457442)
      hw hr hr20 hk hf (by norm_num) hLambda (by norm_num)
    have hd := OcelotasVeintePrefijos.descenso_bajo
      (by omega : 4912741 ≤ n) (by omega : n ≤ 5457441) hk _hcontador hqa
    omega

theorem fila_36 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 190537 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 10781274) : n < 4912741 := by
  have hU : (6450747489703 / 100000000000000000000 : ℝ) ≤ (301994 : ℝ) * log 2 - 190537 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (16785921 : ℝ) * log 2 - 10590737 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 301994) (Q := 190537) (p := 16785921) (v := 10590737)
    (c := (6450747489703 / 100000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 190537 + 10590737) hk.2
  by_cases hsmall : n < 4912741
  · exact hsmall
  · have hns := OcelotasAfinadaTrayectorias.semilla_de_cota (s := 310041589)
      hw hr hr20 hk hf (by norm_num) hLambda (by norm_num)
    have hd := OcelotasVeintePrefijos.descenso_alto
      (by omega : 4912741 ≤ n) (by omega : n ≤ 310041588) hk _hcontador hqa
    omega

theorem fila_37 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 10781274 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 64497107) : n < 4912741 := by
  have hU : (6102702763917 / 500000000000000000000 : ℝ) ≤ (17087915 : ℝ) * log 2 - 10781274 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (85137581 : ℝ) * log 2 - 53715833 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 17087915) (Q := 10781274) (p := 85137581) (v := 53715833)
    (c := (6102702763917 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 10781274 + 53715833) hk.2
  have hpot : (1638618230 : ℕ) ^ 256 ≤ 2 ^ 7837 := by decide +kernel
  have hcriba : OcelotasAfinada.cota (1585 / 1000) (7837 / 256) 20 < 10781274 := by
    norm_num [OcelotasAfinada.cota]
  exact False.elim (imposible_por_criba (s := 1638618230) (B := 7837) hw hr hr20 hk hf
    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)

theorem fila_38 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 64497107 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 118212940) : n < 4912741 := by
  have hU : (4362479134987 / 500000000000000000000 : ℝ) ≤ (102225496 : ℝ) * log 2 - 64497107 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (85137581 : ℝ) * log 2 - 53715833 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 102225496) (Q := 64497107) (p := 85137581) (v := 53715833)
    (c := (4362479134987 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 64497107 + 53715833) hk.2
  have hpot : (2292274574 : ℕ) ^ 256 ≤ 2 ^ 7961 := by decide +kernel
  have hcriba : OcelotasAfinada.cota (1585 / 1000) (7961 / 256) 20 < 64497107 := by
    norm_num [OcelotasAfinada.cota]
  exact False.elim (imposible_por_criba (s := 2292274574) (B := 7961) hw hr hr20 hk hf
    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)

theorem fila_39 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 118212940 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 171928773) : n < 4912741 := by
  have hU : (2622255506057 / 500000000000000000000 : ℝ) ≤ (187363077 : ℝ) * log 2 - 118212940 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (85137581 : ℝ) * log 2 - 53715833 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 187363077) (Q := 118212940) (p := 85137581) (v := 53715833)
    (c := (2622255506057 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 118212940 + 53715833) hk.2
  have hpot : (3813510918 : ℕ) ^ 256 ≤ 2 ^ 8149 := by decide +kernel
  have hcriba : OcelotasAfinada.cota (1585 / 1000) (8149 / 256) 20 < 118212940 := by
    norm_num [OcelotasAfinada.cota]
  exact False.elim (imposible_por_criba (s := 3813510918) (B := 8149) hw hr hr20 hk hf
    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)

theorem fila_40 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 171928773 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 397573379) : n < 4912741 := by
  have hU : (882031877127 / 500000000000000000000 : ℝ) ≤ (272500658 : ℝ) * log 2 - 171928773 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (357638239 : ℝ) * log 2 - 225644606 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 272500658) (Q := 171928773) (p := 357638239) (v := 225644606)
    (c := (882031877127 / 500000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 171928773 + 225644606) hk.2
  have hpot : (11337458724 : ℕ) ^ 256 ≤ 2 ^ 8551 := by decide +kernel
  have hcriba : OcelotasAfinada.cota (1585 / 1000) (8551 / 256) 20 < 171928773 := by
    norm_num [OcelotasAfinada.cota]
  exact False.elim (imposible_por_criba (s := 11337458724) (B := 8551) hw hr hr20 hk hf
    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)

theorem fila_41 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 397573379 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 4598951775) : n < 4912741 := by
  have hU : (5960031331 / 125000000000000000000 : ℝ) ≤ (630138897 : ℝ) * log 2 - 397573379 * log 3 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (6659027209 : ℝ) * log 2 - 4201378396 * log 3 < 0 := by
    have h2 := log_dos_cotas; have h3 := log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 630138897) (Q := 397573379) (p := 6659027209) (v := 4201378396)
    (c := (5960031331 / 125000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 397573379 + 4201378396) hk.2
  have hpot : (419460882194 : ℕ) ^ 256 ≤ 2 ^ 9885 := by decide +kernel
  have hcriba : OcelotasAfinada.cota (1585 / 1000) (9885 / 256) 20 < 397573379 := by
    norm_num [OcelotasAfinada.cota]
  exact False.elim (imposible_por_criba (s := 419460882194) (B := 9885) hw hr hr20 hk hf
    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)

theorem pequeno_de_tabla {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr20 : r ≤ 20)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 20)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hq : S (tiempo a b r) n < 4598951775) : n < 4912741 := by
  have hpos := impares_pos hw hr
  by_cases h0 : S (tiempo a b r) n < 3
  · exact fila_0 hw hr hr20 _hcontador hk hf (by omega) h0
  by_cases h1 : S (tiempo a b r) n < 5
  · exact fila_1 hw hr hr20 _hcontador hk hf (by omega) h1
  by_cases h2 : S (tiempo a b r) n < 17
  · exact fila_2 hw hr hr20 _hcontador hk hf (by omega) h2
  by_cases h3 : S (tiempo a b r) n < 29
  · exact fila_3 hw hr hr20 _hcontador hk hf (by omega) h3
  by_cases h4 : S (tiempo a b r) n < 41
  · exact fila_4 hw hr hr20 _hcontador hk hf (by omega) h4
  by_cases h5 : S (tiempo a b r) n < 94
  · exact fila_5 hw hr hr20 _hcontador hk hf (by omega) h5
  by_cases h6 : S (tiempo a b r) n < 147
  · exact fila_6 hw hr hr20 _hcontador hk hf (by omega) h6
  by_cases h7 : S (tiempo a b r) n < 200
  · exact fila_7 hw hr hr20 _hcontador hk hf (by omega) h7
  by_cases h8 : S (tiempo a b r) n < 253
  · exact fila_8 hw hr hr20 _hcontador hk hf (by omega) h8
  by_cases h9 : S (tiempo a b r) n < 306
  · exact fila_9 hw hr hr20 _hcontador hk hf (by omega) h9
  by_cases h10 : S (tiempo a b r) n < 971
  · exact fila_10 hw hr hr20 _hcontador hk hf (by omega) h10
  by_cases h11 : S (tiempo a b r) n < 1636
  · exact fila_11 hw hr hr20 _hcontador hk hf (by omega) h11
  by_cases h12 : S (tiempo a b r) n < 2301
  · exact fila_12 hw hr hr20 _hcontador hk hf (by omega) h12
  by_cases h13 : S (tiempo a b r) n < 2966
  · exact fila_13 hw hr hr20 _hcontador hk hf (by omega) h13
  by_cases h14 : S (tiempo a b r) n < 3631
  · exact fila_14 hw hr hr20 _hcontador hk hf (by omega) h14
  by_cases h15 : S (tiempo a b r) n < 4296
  · exact fila_15 hw hr hr20 _hcontador hk hf (by omega) h15
  by_cases h16 : S (tiempo a b r) n < 4961
  · exact fila_16 hw hr hr20 _hcontador hk hf (by omega) h16
  by_cases h17 : S (tiempo a b r) n < 5626
  · exact fila_17 hw hr hr20 _hcontador hk hf (by omega) h17
  by_cases h18 : S (tiempo a b r) n < 6291
  · exact fila_18 hw hr hr20 _hcontador hk hf (by omega) h18
  by_cases h19 : S (tiempo a b r) n < 6956
  · exact fila_19 hw hr hr20 _hcontador hk hf (by omega) h19
  by_cases h20 : S (tiempo a b r) n < 7621
  · exact fila_20 hw hr hr20 _hcontador hk hf (by omega) h20
  by_cases h21 : S (tiempo a b r) n < 8286
  · exact fila_21 hw hr hr20 _hcontador hk hf (by omega) h21
  by_cases h22 : S (tiempo a b r) n < 8951
  · exact fila_22 hw hr hr20 _hcontador hk hf (by omega) h22
  by_cases h23 : S (tiempo a b r) n < 9616
  · exact fila_23 hw hr hr20 _hcontador hk hf (by omega) h23
  by_cases h24 : S (tiempo a b r) n < 10281
  · exact fila_24 hw hr hr20 _hcontador hk hf (by omega) h24
  by_cases h25 : S (tiempo a b r) n < 10946
  · exact fila_25 hw hr hr20 _hcontador hk hf (by omega) h25
  by_cases h26 : S (tiempo a b r) n < 11611
  · exact fila_26 hw hr hr20 _hcontador hk hf (by omega) h26
  by_cases h27 : S (tiempo a b r) n < 12276
  · exact fila_27 hw hr hr20 _hcontador hk hf (by omega) h27
  by_cases h28 : S (tiempo a b r) n < 12941
  · exact fila_28 hw hr hr20 _hcontador hk hf (by omega) h28
  by_cases h29 : S (tiempo a b r) n < 13606
  · exact fila_29 hw hr hr20 _hcontador hk hf (by omega) h29
  by_cases h30 : S (tiempo a b r) n < 14271
  · exact fila_30 hw hr hr20 _hcontador hk hf (by omega) h30
  by_cases h31 : S (tiempo a b r) n < 14936
  · exact fila_31 hw hr hr20 _hcontador hk hf (by omega) h31
  by_cases h32 : S (tiempo a b r) n < 15601
  · exact fila_32 hw hr hr20 _hcontador hk hf (by omega) h32
  by_cases h33 : S (tiempo a b r) n < 47468
  · exact fila_33 hw hr hr20 _hcontador hk hf (by omega) h33
  by_cases h34 : S (tiempo a b r) n < 79335
  · exact fila_34 hw hr hr20 _hcontador hk hf (by omega) h34
  by_cases h35 : S (tiempo a b r) n < 190537
  · exact fila_35 hw hr hr20 _hcontador hk hf (by omega) h35
  by_cases h36 : S (tiempo a b r) n < 10781274
  · exact fila_36 hw hr hr20 _hcontador hk hf (by omega) h36
  by_cases h37 : S (tiempo a b r) n < 64497107
  · exact fila_37 hw hr hr20 _hcontador hk hf (by omega) h37
  by_cases h38 : S (tiempo a b r) n < 118212940
  · exact fila_38 hw hr hr20 _hcontador hk hf (by omega) h38
  by_cases h39 : S (tiempo a b r) n < 171928773
  · exact fila_39 hw hr hr20 _hcontador hk hf (by omega) h39
  by_cases h40 : S (tiempo a b r) n < 397573379
  · exact fila_40 hw hr hr20 _hcontador hk hf (by omega) h40
  exact fila_41 hw hr hr20 _hcontador hk hf (by omega) hq

end OcelotasVeinteTabla

#print axioms OcelotasVeinteTabla.pequeno_de_tabla
