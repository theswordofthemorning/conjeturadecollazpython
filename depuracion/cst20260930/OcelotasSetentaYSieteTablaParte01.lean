import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasSetentaYSietePrefijos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasSetentaYSieteTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_0 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 1 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 3) : n < 28000000000000000001 := by
  have hU : (8990064764118153982475593937307107234484678465555033 / 31250000000000000000000000000000000000000000000000000 : ℝ) ≤ (2 : ℝ) * log 2 - 1 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (3 : ℝ) * log 2 - 2 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 2) (Q := 1) (p := 3) (v := 2)
    (c := (8990064764118153982475593937307107234484678465555033 / 31250000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 1 + 2) hk.2
  exact pequeno_por_cota (s := 268) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_1 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 3 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 5) : n < 28000000000000000001 := by
  have hU : (84949518397698736450212448261652863217514499166513957 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (5 : ℝ) * log 2 - 3 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (3 : ℝ) * log 2 - 2 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 5) (Q := 3) (p := 3) (v := 2)
    (c := (84949518397698736450212448261652863217514499166513957 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 3 + 2) hk.2
  exact pequeno_por_cota (s := 454) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_2 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 5 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 17) : n < 28000000000000000001 := by
  have hU : (13029000284753504590407696763196005341637071442073693 / 250000000000000000000000000000000000000000000000000000 : ℝ) ≤ (8 : ℝ) * log 2 - 5 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (19 : ℝ) * log 2 - 12 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 8) (Q := 5) (p := 19) (v := 12)
    (c := (13029000284753504590407696763196005341637071442073693 / 250000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 5 + 12) hk.2
  exact pequeno_por_cota (s := 1478) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_3 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 17 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 29) : n < 28000000000000000001 := by
  have hU : (19282483880329300273049125843915179515582072370075587 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (27 : ℝ) * log 2 - 17 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (19 : ℝ) * log 2 - 12 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 27) (Q := 17) (p := 19) (v := 12)
    (c := (19282483880329300273049125843915179515582072370075587 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 17 + 12) hk.2
  exact pequeno_por_cota (s := 1997) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_4 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 29 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 41) : n < 28000000000000000001 := by
  have hU : (3126741797787897841320714540359587086972500464000947 / 125000000000000000000000000000000000000000000000000000 : ℝ) ≤ (46 : ℝ) * log 2 - 29 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (19 : ℝ) * log 2 - 12 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 46) (Q := 29) (p := 19) (v := 12)
    (c := (3126741797787897841320714540359587086972500464000947 / 125000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 29 + 12) hk.2
  exact pequeno_por_cota (s := 3079) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_5 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 41 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 94) : n < 28000000000000000001 := by
  have hU : (5731450501973882457516590478961517180197931341931989 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (65 : ℝ) * log 2 - 41 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (84 : ℝ) * log 2 - 53 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 65) (Q := 41) (p := 84) (v := 53)
    (c := (5731450501973882457516590478961517180197931341931989 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 41 + 53) hk.2
  exact pequeno_por_cota (s := 6718) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_6 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 94 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 147) : n < 28000000000000000001 := by
  have hU : (4687384314770056007266913275446203192703792169792179 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (149 : ℝ) * log 2 - 94 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (84 : ℝ) * log 2 - 53 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 149) (Q := 94) (p := 84) (v := 53)
    (c := (4687384314770056007266913275446203192703792169792179 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 94 + 53) hk.2
  exact pequeno_por_cota (s := 8214) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_7 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 147 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 200) : n < 28000000000000000001 := by
  have hU : (3643318127566229557017236071930889205209652997652369 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (233 : ℝ) * log 2 - 147 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (84 : ℝ) * log 2 - 53 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 233) (Q := 147) (p := 84) (v := 53)
    (c := (3643318127566229557017236071930889205209652997652369 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 147 + 53) hk.2
  exact pequeno_por_cota (s := 10568) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_8 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 200 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 253) : n < 28000000000000000001 := by
  have hU : (2599251940362403106767558868415575217715513825512559 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (317 : ℝ) * log 2 - 200 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (84 : ℝ) * log 2 - 53 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 317) (Q := 200) (p := 84) (v := 53)
    (c := (2599251940362403106767558868415575217715513825512559 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 200 + 53) hk.2
  exact pequeno_por_cota (s := 14812) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_9 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 253 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 306) : n < 28000000000000000001 := by
  have hU : (1555185753158576656517881664900261230221374653372749 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (401 : ℝ) * log 2 - 253 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (84 : ℝ) * log 2 - 53 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 401) (Q := 253) (p := 84) (v := 53)
    (c := (1555185753158576656517881664900261230221374653372749 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 253 + 53) hk.2
  exact pequeno_por_cota (s := 24756) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_10 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 306 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 971) : n < 28000000000000000001 := by
  have hU : (511119565954750206268204461384947242727235481232939 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (485 : ℝ) * log 2 - 306 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 485) (Q := 306) (p := 1054) (v := 665)
    (c := (511119565954750206268204461384947242727235481232939 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 306 + 665) hk.2
  exact pequeno_por_cota (s := 75325) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_11 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 971 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 1636) : n < 28000000000000000001 := by
  have hU : (489292510660424168554936180639527740687567271559007 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (1539 : ℝ) * log 2 - 971 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 1539) (Q := 971) (p := 1054) (v := 665)
    (c := (489292510660424168554936180639527740687567271559007 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 971 + 665) hk.2
  exact pequeno_por_cota (s := 78686) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_12 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 1636 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 2301) : n < 28000000000000000001 := by
  have hU : (18698618214643925233666715995764329545915962475403 / 20000000000000000000000000000000000000000000000000000 : ℝ) ≤ (2593 : ℝ) * log 2 - 1636 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 2593) (Q := 1636) (p := 1054) (v := 665)
    (c := (18698618214643925233666715995764329545915962475403 / 20000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 1636 + 665) hk.2
  exact pequeno_por_cota (s := 82360) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_13 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 2301 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 2966) : n < 28000000000000000001 := by
  have hU : (445638400071772093128399619148688736608230852211143 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (3647 : ℝ) * log 2 - 2301 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 3647) (Q := 2301) (p := 1054) (v := 665)
    (c := (445638400071772093128399619148688736608230852211143 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 2301 + 665) hk.2
  exact pequeno_por_cota (s := 86393) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_14 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 2966 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 3631) : n < 28000000000000000001 := by
  have hU : (423811344777446055415131338403269234568562642537211 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (4701 : ℝ) * log 2 - 2966 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 4701) (Q := 2966) (p := 1054) (v := 665)
    (c := (423811344777446055415131338403269234568562642537211 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 2966 + 665) hk.2
  exact pequeno_por_cota (s := 90843) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_15 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 3631 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 4296) : n < 28000000000000000001 := by
  have hU : (401984289483120017701863057657849732528894432863279 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (5755 : ℝ) * log 2 - 3631 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 5755) (Q := 3631) (p := 1054) (v := 665)
    (c := (401984289483120017701863057657849732528894432863279 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 3631 + 665) hk.2
  exact pequeno_por_cota (s := 95775) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

end OcelotasSetentaYSieteTabla

#print axioms OcelotasSetentaYSieteTabla.fila_0
#print axioms OcelotasSetentaYSieteTabla.fila_1
#print axioms OcelotasSetentaYSieteTabla.fila_2
#print axioms OcelotasSetentaYSieteTabla.fila_3
#print axioms OcelotasSetentaYSieteTabla.fila_4
#print axioms OcelotasSetentaYSieteTabla.fila_5
#print axioms OcelotasSetentaYSieteTabla.fila_6
#print axioms OcelotasSetentaYSieteTabla.fila_7
#print axioms OcelotasSetentaYSieteTabla.fila_8
#print axioms OcelotasSetentaYSieteTabla.fila_9
#print axioms OcelotasSetentaYSieteTabla.fila_10
#print axioms OcelotasSetentaYSieteTabla.fila_11
#print axioms OcelotasSetentaYSieteTabla.fila_12
#print axioms OcelotasSetentaYSieteTabla.fila_13
#print axioms OcelotasSetentaYSieteTabla.fila_14
#print axioms OcelotasSetentaYSieteTabla.fila_15
