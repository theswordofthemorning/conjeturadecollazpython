import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasOchentaYUnoTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_0 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 282) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_1 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 477) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_2 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 1555) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_3 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 2101) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_4 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 3239) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_5 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 7067) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_6 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 8641) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_7 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 11117) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_8 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 15582) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_9 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 26042) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_10 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 79238) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_11 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 82773) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_12 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 86638) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_13 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 90881) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_14 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 95562) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_15 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 100751) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_16 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 4296 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 4961) : n < 28000000000000000001 := by
  have hU : (380157234188793979988594776912430230489226223189347 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (6809 : ℝ) * log 2 - 4296 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 6809) (Q := 4296) (p := 1054) (v := 665)
    (c := (380157234188793979988594776912430230489226223189347 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 4296 + 665) hk.2
  exact pequeno_por_cota (s := 106535) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_17 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 4961 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 5626) : n < 28000000000000000001 := by
  have hU : (71666035778893588455065299233402145689911602703083 / 100000000000000000000000000000000000000000000000000000 : ℝ) ≤ (7863 : ℝ) * log 2 - 4961 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 7863) (Q := 4961) (p := 1054) (v := 665)
    (c := (71666035778893588455065299233402145689911602703083 / 100000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 4961 + 665) hk.2
  exact pequeno_por_cota (s := 113025) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_18 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 5626 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 6291) : n < 28000000000000000001 := by
  have hU : (336503123600141904562058215421591226409889803841483 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (8917 : ℝ) * log 2 - 5626 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 8917) (Q := 5626) (p := 1054) (v := 665)
    (c := (336503123600141904562058215421591226409889803841483 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 5626 + 665) hk.2
  exact pequeno_por_cota (s := 120356) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_19 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 6291 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 6956) : n < 28000000000000000001 := by
  have hU : (314676068305815866848789934676171724370221594167551 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (9971 : ℝ) * log 2 - 6291 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 9971) (Q := 6291) (p := 1054) (v := 665)
    (c := (314676068305815866848789934676171724370221594167551 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 6291 + 665) hk.2
  exact pequeno_por_cota (s := 128704) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_20 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 6956 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 7621) : n < 28000000000000000001 := by
  have hU : (292849013011489829135521653930752222330553384493619 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (11025 : ℝ) * log 2 - 6956 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 11025) (Q := 6956) (p := 1054) (v := 665)
    (c := (292849013011489829135521653930752222330553384493619 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 6956 + 665) hk.2
  exact pequeno_por_cota (s := 138297) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_21 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 7621 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 8286) : n < 28000000000000000001 := by
  have hU : (271021957717163791422253373185332720290885174819687 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (12079 : ℝ) * log 2 - 7621 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 12079) (Q := 7621) (p := 1054) (v := 665)
    (c := (271021957717163791422253373185332720290885174819687 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 7621 + 665) hk.2
  exact pequeno_por_cota (s := 149435) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_22 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 8286 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 8951) : n < 28000000000000000001 := by
  have hU : (49838980484567550741797018487982643650243393029151 / 100000000000000000000000000000000000000000000000000000 : ℝ) ≤ (13133 : ℝ) * log 2 - 8286 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 13133) (Q := 8286) (p := 1054) (v := 665)
    (c := (49838980484567550741797018487982643650243393029151 / 100000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 8286 + 665) hk.2
  exact pequeno_por_cota (s := 162524) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_23 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 8951 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 9616) : n < 28000000000000000001 := by
  have hU : (227367847128511715995716811694493716211548755471823 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (14187 : ℝ) * log 2 - 8951 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 14187) (Q := 8951) (p := 1054) (v := 665)
    (c := (227367847128511715995716811694493716211548755471823 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 8951 + 665) hk.2
  exact pequeno_por_cota (s := 178126) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_24 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 9616 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 10281) : n < 28000000000000000001 := by
  have hU : (205540791834185678282448530949074214171880545797891 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (15241 : ℝ) * log 2 - 9616 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 15241) (Q := 9616) (p := 1054) (v := 665)
    (c := (205540791834185678282448530949074214171880545797891 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 9616 + 665) hk.2
  exact pequeno_por_cota (s := 197042) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_25 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 10281 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 10946) : n < 28000000000000000001 := by
  have hU : (183713736539859640569180250203654712132212336123959 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (16295 : ℝ) * log 2 - 10281 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 16295) (Q := 10281) (p := 1054) (v := 665)
    (c := (183713736539859640569180250203654712132212336123959 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 10281 + 665) hk.2
  exact pequeno_por_cota (s := 220452) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_26 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 10946 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 11611) : n < 28000000000000000001 := by
  have hU : (161886681245533602855911969458235210092544126450027 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (17349 : ℝ) * log 2 - 10946 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 17349) (Q := 10946) (p := 1054) (v := 665)
    (c := (161886681245533602855911969458235210092544126450027 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 10946 + 665) hk.2
  exact pequeno_por_cota (s := 250175) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_27 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 11611 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 12276) : n < 28000000000000000001 := by
  have hU : (28011925190241513028528737742563141610575183355219 / 100000000000000000000000000000000000000000000000000000 : ℝ) ≤ (18403 : ℝ) * log 2 - 11611 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 18403) (Q := 11611) (p := 1054) (v := 665)
    (c := (28011925190241513028528737742563141610575183355219 / 100000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 11611 + 665) hk.2
  exact pequeno_por_cota (s := 289163) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_28 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 12276 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 12941) : n < 28000000000000000001 := by
  have hU : (118232570656881527429375407967396206013207707102163 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (19457 : ℝ) * log 2 - 12276 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 19457) (Q := 12276) (p := 1054) (v := 665)
    (c := (118232570656881527429375407967396206013207707102163 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 12276 + 665) hk.2
  exact pequeno_por_cota (s := 342546) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_29 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 12941 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 13606) : n < 28000000000000000001 := by
  have hU : (96405515362555489716107127221976703973539497428231 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (20511 : ℝ) * log 2 - 12941 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1054 : ℝ) * log 2 - 665 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 20511) (Q := 12941) (p := 1054) (v := 665)
    (c := (96405515362555489716107127221976703973539497428231 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 12941 + 665) hk.2
  exact pequeno_por_cota (s := 420101) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_30 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 13606 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 14271) : n < 28000000000000000001 := by
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
  exact pequeno_por_cota (s := 543053) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_31 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 14271 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 14936) : n < 28000000000000000001 := by
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
  exact pequeno_por_cota (s := 767753) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_32 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 1309648) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_33 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 4451874) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_34 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 7411031) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_35 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 22102640) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_36 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 1255667892) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_37 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 6635546348) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_38 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 9273682961) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_39 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 15393956884) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_40 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 45271220435) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_41 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 765280899187) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_42 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 8001481502413) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_43 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 14698170094552) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_44 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 90134714256123) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_45 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 103886909444834) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

end OcelotasOchentaYUnoTabla

#print axioms OcelotasOchentaYUnoTabla.fila_0
#print axioms OcelotasOchentaYUnoTabla.fila_1
#print axioms OcelotasOchentaYUnoTabla.fila_2
#print axioms OcelotasOchentaYUnoTabla.fila_3
#print axioms OcelotasOchentaYUnoTabla.fila_4
#print axioms OcelotasOchentaYUnoTabla.fila_5
#print axioms OcelotasOchentaYUnoTabla.fila_6
#print axioms OcelotasOchentaYUnoTabla.fila_7
#print axioms OcelotasOchentaYUnoTabla.fila_8
#print axioms OcelotasOchentaYUnoTabla.fila_9
#print axioms OcelotasOchentaYUnoTabla.fila_10
#print axioms OcelotasOchentaYUnoTabla.fila_11
#print axioms OcelotasOchentaYUnoTabla.fila_12
#print axioms OcelotasOchentaYUnoTabla.fila_13
#print axioms OcelotasOchentaYUnoTabla.fila_14
#print axioms OcelotasOchentaYUnoTabla.fila_15
#print axioms OcelotasOchentaYUnoTabla.fila_16
#print axioms OcelotasOchentaYUnoTabla.fila_17
#print axioms OcelotasOchentaYUnoTabla.fila_18
#print axioms OcelotasOchentaYUnoTabla.fila_19
#print axioms OcelotasOchentaYUnoTabla.fila_20
#print axioms OcelotasOchentaYUnoTabla.fila_21
#print axioms OcelotasOchentaYUnoTabla.fila_22
#print axioms OcelotasOchentaYUnoTabla.fila_23
#print axioms OcelotasOchentaYUnoTabla.fila_24
#print axioms OcelotasOchentaYUnoTabla.fila_25
#print axioms OcelotasOchentaYUnoTabla.fila_26
#print axioms OcelotasOchentaYUnoTabla.fila_27
#print axioms OcelotasOchentaYUnoTabla.fila_28
#print axioms OcelotasOchentaYUnoTabla.fila_29
#print axioms OcelotasOchentaYUnoTabla.fila_30
#print axioms OcelotasOchentaYUnoTabla.fila_31
#print axioms OcelotasOchentaYUnoTabla.fila_32
#print axioms OcelotasOchentaYUnoTabla.fila_33
#print axioms OcelotasOchentaYUnoTabla.fila_34
#print axioms OcelotasOchentaYUnoTabla.fila_35
#print axioms OcelotasOchentaYUnoTabla.fila_36
#print axioms OcelotasOchentaYUnoTabla.fila_37
#print axioms OcelotasOchentaYUnoTabla.fila_38
#print axioms OcelotasOchentaYUnoTabla.fila_39
#print axioms OcelotasOchentaYUnoTabla.fila_40
#print axioms OcelotasOchentaYUnoTabla.fila_41
#print axioms OcelotasOchentaYUnoTabla.fila_42
#print axioms OcelotasOchentaYUnoTabla.fila_43
#print axioms OcelotasOchentaYUnoTabla.fila_44
#print axioms OcelotasOchentaYUnoTabla.fila_45
