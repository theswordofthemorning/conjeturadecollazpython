import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasVeinticuatroPrefijosBajo
import OcelotasVeinticuatroPrefijosAlto

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasVeinticuatroTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_15 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 3631 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 4296) : n < 4912741 := by
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
  exact pequeno_por_cota (s := 29852) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_16 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 4296 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 4961) : n < 4912741 := by
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
  exact pequeno_por_cota (s := 31566) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_17 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 4961 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 5626) : n < 4912741 := by
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
  exact pequeno_por_cota (s := 33489) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_18 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 5626 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 6291) : n < 4912741 := by
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
  exact pequeno_por_cota (s := 35661) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_19 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 6291 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 6956) : n < 4912741 := by
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
  exact pequeno_por_cota (s := 38135) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_20 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 6956 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 7621) : n < 4912741 := by
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
  exact pequeno_por_cota (s := 40977) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_21 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 7621 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 8286) : n < 4912741 := by
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
  exact pequeno_por_cota (s := 44277) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_22 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 8286 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 8951) : n < 4912741 := by
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
  exact pequeno_por_cota (s := 48156) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_23 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 8951 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 9616) : n < 4912741 := by
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
  exact pequeno_por_cota (s := 52778) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_24 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 9616 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 10281) : n < 4912741 := by
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
  exact pequeno_por_cota (s := 58383) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_25 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 10281 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 10946) : n < 4912741 := by
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
  exact pequeno_por_cota (s := 65320) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_26 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 10946 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 11611) : n < 4912741 := by
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
  exact pequeno_por_cota (s := 74126) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_27 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 11611 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 12276) : n < 4912741 := by
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
  exact pequeno_por_cota (s := 85678) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_28 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 12276 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 12941) : n < 4912741 := by
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
  exact pequeno_por_cota (s := 101495) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_29 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr24 : r ≤ 24)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 24)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 12941 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 13606) : n < 4912741 := by
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
  exact pequeno_por_cota (s := 124475) hw hr hr24 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

end OcelotasVeinticuatroTabla

#print axioms OcelotasVeinticuatroTabla.fila_15
#print axioms OcelotasVeinticuatroTabla.fila_16
#print axioms OcelotasVeinticuatroTabla.fila_17
#print axioms OcelotasVeinticuatroTabla.fila_18
#print axioms OcelotasVeinticuatroTabla.fila_19
#print axioms OcelotasVeinticuatroTabla.fila_20
#print axioms OcelotasVeinticuatroTabla.fila_21
#print axioms OcelotasVeinticuatroTabla.fila_22
#print axioms OcelotasVeinticuatroTabla.fila_23
#print axioms OcelotasVeinticuatroTabla.fila_24
#print axioms OcelotasVeinticuatroTabla.fila_25
#print axioms OcelotasVeinticuatroTabla.fila_26
#print axioms OcelotasVeinticuatroTabla.fila_27
#print axioms OcelotasVeinticuatroTabla.fila_28
#print axioms OcelotasVeinticuatroTabla.fila_29
