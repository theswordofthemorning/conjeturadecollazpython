import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasSetentaYSietePrefijos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasSetentaYSieteTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_16 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
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
  exact pequeno_por_cota (s := 101274) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_17 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
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
  exact pequeno_por_cota (s := 107443) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_18 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
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
  exact pequeno_por_cota (s := 114413) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_19 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
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
  exact pequeno_por_cota (s := 122349) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_20 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
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
  exact pequeno_por_cota (s := 131468) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_21 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
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
  exact pequeno_por_cota (s := 142055) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_22 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
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
  exact pequeno_por_cota (s := 154498) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_23 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
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
  exact pequeno_por_cota (s := 169330) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_24 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
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
  exact pequeno_por_cota (s := 187311) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_25 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
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
  exact pequeno_por_cota (s := 209566) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_26 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
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
  exact pequeno_por_cota (s := 237821) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_27 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
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
  exact pequeno_por_cota (s := 274883) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_28 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
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
  exact pequeno_por_cota (s := 325630) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_29 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
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
  exact pequeno_por_cota (s := 399355) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_30 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
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
  exact pequeno_por_cota (s := 516235) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_31 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr77 : r ≤ 77)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 77)
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
  exact pequeno_por_cota (s := 729839) hw hr hr77 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

end OcelotasSetentaYSieteTabla

#print axioms OcelotasSetentaYSieteTabla.fila_16
#print axioms OcelotasSetentaYSieteTabla.fila_17
#print axioms OcelotasSetentaYSieteTabla.fila_18
#print axioms OcelotasSetentaYSieteTabla.fila_19
#print axioms OcelotasSetentaYSieteTabla.fila_20
#print axioms OcelotasSetentaYSieteTabla.fila_21
#print axioms OcelotasSetentaYSieteTabla.fila_22
#print axioms OcelotasSetentaYSieteTabla.fila_23
#print axioms OcelotasSetentaYSieteTabla.fila_24
#print axioms OcelotasSetentaYSieteTabla.fila_25
#print axioms OcelotasSetentaYSieteTabla.fila_26
#print axioms OcelotasSetentaYSieteTabla.fila_27
#print axioms OcelotasSetentaYSieteTabla.fila_28
#print axioms OcelotasSetentaYSieteTabla.fila_29
#print axioms OcelotasSetentaYSieteTabla.fila_30
#print axioms OcelotasSetentaYSieteTabla.fila_31
