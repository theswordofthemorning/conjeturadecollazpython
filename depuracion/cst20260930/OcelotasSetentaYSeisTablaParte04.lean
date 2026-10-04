import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasSetentaYSeisPrefijos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasSetentaYSeisTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_48 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 3149971404836 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 3903082244717) : n < 28000000000000000001 := by
  have hU : (211405694233260565569116706013950631558707 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (4992586555009 : ℝ) * log 2 - 3149971404836 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1193652440098 : ℝ) * log 2 - 753110839881 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 4992586555009) (Q := 3149971404836) (p := 1193652440098) (v := 753110839881)
    (c := (211405694233260565569116706013950631558707 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 3149971404836 + 753110839881) hk.2
  exact pequeno_por_cota (s := 179749179121314) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_49 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 3903082244717 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 4656193084598) : n < 28000000000000000001 := by
  have hU : (151925258933851648161231674764752067698547 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (6186238995107 : ℝ) * log 2 - 3903082244717 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1193652440098 : ℝ) * log 2 - 753110839881 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 6186238995107) (Q := 3903082244717) (p := 1193652440098) (v := 753110839881)
    (c := (151925258933851648161231674764752067698547 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 3903082244717 + 753110839881) hk.2
  exact pequeno_por_cota (s := 250122989861385) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_50 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 4656193084598 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 5409303924479) : n < 28000000000000000001 := by
  have hU : (92444823634442730753346643515553503838387 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (7379891435205 : ℝ) * log 2 - 4656193084598 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1193652440098 : ℝ) * log 2 - 753110839881 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 7379891435205) (Q := 4656193084598) (p := 1193652440098) (v := 753110839881)
    (c := (92444823634442730753346643515553503838387 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 4656193084598 + 753110839881) hk.2
  exact pequeno_por_cota (s := 411056006232048) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_51 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 5409303924479 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 11571718688839) : n < 28000000000000000001 := by
  have hU : (32964388335033813345461612266354939978227 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (8573543875303 : ℝ) * log 2 - 5409303924479 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (9767196315401 : ℝ) * log 2 - 6162414764360 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 8573543875303) (Q := 5409303924479) (p := 9767196315401) (v := 6162414764360)
    (c := (32964388335033813345461612266354939978227 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 5409303924479 + 6162414764360) hk.2
  exact pequeno_por_cota (s := 1152759141585966) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_52 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 11571718688839 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 64021008208555) : n < 28000000000000000001 := by
  have hU : (3224170685329354641519096641755658048147 / 250000000000000000000000000000000000000000000000000000 : ℝ) ≤ (18340740190704 : ℝ) * log 2 - 11571718688839 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 18340740190704) (Q := 11571718688839) (p := 83130157078217) (v := 52449289519716)
    (c := (3224170685329354641519096641755658048147 / 250000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 11571718688839 + 52449289519716) hk.2
  exact pequeno_por_cota (s := 5892988260967058) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_53 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 64021008208555 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 116470297728271) : n < 28000000000000000001 := by
  have hU : (5725659888918442352767547434712956599537 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (101470897268921 : ℝ) * log 2 - 64021008208555 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 101470897268921) (Q := 64021008208555) (p := 83130157078217) (v := 52449289519716)
    (c := (5725659888918442352767547434712956599537 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 64021008208555 + 52449289519716) hk.2
  exact pequeno_por_cota (s := 6636789599316922) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_54 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 116470297728271 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 168919587247987) : n < 28000000000000000001 := by
  have hU : (250148920358908771124845079295729855139 / 25000000000000000000000000000000000000000000000000000 : ℝ) ≤ (184601054347138 : ℝ) * log 2 - 116470297728271 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 184601054347138) (Q := 116470297728271) (p := 83130157078217) (v := 52449289519716)
    (c := (250148920358908771124845079295729855139 / 25000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 116470297728271 + 52449289519716) hk.2
  exact pequeno_por_cota (s := 7595475516240155) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_55 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 168919587247987 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 221368876767703) : n < 28000000000000000001 := by
  have hU : (4280296925437908492226255737116237606023 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (267731211425355 : ℝ) * log 2 - 168919587247987 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 267731211425355) (Q := 168919587247987) (p := 83130157078217) (v := 52449289519716)
    (c := (4280296925437908492226255737116237606023 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 168919587247987 + 52449289519716) hk.2
  exact pequeno_por_cota (s := 8877888768455543) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_56 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 221368876767703 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 273818166287419) : n < 28000000000000000001 := by
  have hU : (1778807721848820780977804944158939054633 / 250000000000000000000000000000000000000000000000000000 : ℝ) ≤ (350861368503572 : ℝ) * log 2 - 221368876767703 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 350861368503572) (Q := 221368876767703) (p := 83130157078217) (v := 52449289519716)
    (c := (1778807721848820780977804944158939054633 / 250000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 221368876767703 + 52449289519716) hk.2
  exact pequeno_por_cota (s := 10681311850980819) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_57 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 273818166287419 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 326267455807135) : n < 28000000000000000001 := by
  have hU : (2834933961957374631684964039519518612509 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (433991525581789 : ℝ) * log 2 - 273818166287419 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 433991525581789) (Q := 273818166287419) (p := 83130157078217) (v := 52449289519716)
    (c := (2834933961957374631684964039519518612509 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 273818166287419 + 52449289519716) hk.2
  exact pequeno_por_cota (s := 13404192305687070) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_58 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 326267455807135 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 378716745326851) : n < 28000000000000000001 := by
  have hU : (264031560027138462676789773840144889469 / 62500000000000000000000000000000000000000000000000000 : ℝ) ≤ (517121682660006 : ℝ) * log 2 - 326267455807135 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 517121682660006) (Q := 326267455807135) (p := 83130157078217) (v := 52449289519716)
    (c := (264031560027138462676789773840144889469 / 62500000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 326267455807135 + 52449289519716) hk.2
  exact pequeno_por_cota (s := 17990273585141760) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_59 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 378716745326851 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 431166034846567) : n < 28000000000000000001 := by
  have hU : (277914199695368154228734468384559923799 / 100000000000000000000000000000000000000000000000000000 : ℝ) ≤ (600251839738223 : ℝ) * log 2 - 378716745326851 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (83130157078217 : ℝ) * log 2 - 52449289519716 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 600251839738223) (Q := 378716745326851) (p := 83130157078217) (v := 52449289519716)
    (c := (277914199695368154228734468384559923799 / 100000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 378716745326851 + 52449289519716) hk.2
  exact pequeno_por_cota (s := 27346569582736816) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_60 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 431166034846567 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 914781359212850) : n < 28000000000000000001 := by
  have hU : (333444758368286920436513246562220061119 / 250000000000000000000000000000000000000000000000000000 : ℝ) ≤ (683381996816440 : ℝ) * log 2 - 431166034846567 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (766512153894657 : ℝ) * log 2 - 483615324366283 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 683381996816440) (Q := 431166034846567) (p := 766512153894657) (v := 483615324366283)
    (c := (333444758368286920436513246562220061119 / 250000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 431166034846567 + 483615324366283) hk.2
  exact pequeno_por_cota (s := 56980952686065800) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_61 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 914781359212850 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 1398396683579133) : n < 28000000000000000001 := by
  have hU : (611097551732880751475407137450520747719 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (1449894150711097 : ℝ) * log 2 - 914781359212850 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (766512153894657 : ℝ) * log 2 - 483615324366283 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 1449894150711097) (Q := 914781359212850) (p := 766512153894657) (v := 483615324366283)
    (c := (611097551732880751475407137450520747719 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 914781359212850 + 483615324366283) hk.2
  exact pequeno_por_cota (s := 62183197907181813) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_62 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 1398396683579133 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 1882012007945416) : n < 28000000000000000001 := by
  have hU : (1388263966822969155194469454441503433 / 1250000000000000000000000000000000000000000000000000 : ℝ) ≤ (2216406304605754 : ℝ) * log 2 - 1398396683579133 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (766512153894657 : ℝ) * log 2 - 483615324366283 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 2216406304605754) (Q := 1398396683579133) (p := 766512153894657) (v := 483615324366283)
    (c := (1388263966822969155194469454441503433 / 1250000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 1398396683579133 + 483615324366283) hk.2
  exact pequeno_por_cota (s := 68430790015681766) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_63 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 1882012007945416 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 2365627332311699) : n < 28000000000000000001 := by
  have hU : (499513621725494572680168426102681998681 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (2982918458500411 : ℝ) * log 2 - 1882012007945416 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (766512153894657 : ℝ) * log 2 - 483615324366283 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 2982918458500411) (Q := 1882012007945416) (p := 766512153894657) (v := 483615324366283)
    (c := (499513621725494572680168426102681998681 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 1882012007945416 + 483615324366283) hk.2
  exact pequeno_por_cota (s := 76074001483152198) hw hr hr76 hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

end OcelotasSetentaYSeisTabla

#print axioms OcelotasSetentaYSeisTabla.fila_48
#print axioms OcelotasSetentaYSeisTabla.fila_49
#print axioms OcelotasSetentaYSeisTabla.fila_50
#print axioms OcelotasSetentaYSeisTabla.fila_51
#print axioms OcelotasSetentaYSeisTabla.fila_52
#print axioms OcelotasSetentaYSeisTabla.fila_53
#print axioms OcelotasSetentaYSeisTabla.fila_54
#print axioms OcelotasSetentaYSeisTabla.fila_55
#print axioms OcelotasSetentaYSeisTabla.fila_56
#print axioms OcelotasSetentaYSeisTabla.fila_57
#print axioms OcelotasSetentaYSeisTabla.fila_58
#print axioms OcelotasSetentaYSeisTabla.fila_59
#print axioms OcelotasSetentaYSeisTabla.fila_60
#print axioms OcelotasSetentaYSeisTabla.fila_61
#print axioms OcelotasSetentaYSeisTabla.fila_62
#print axioms OcelotasSetentaYSeisTabla.fila_63
