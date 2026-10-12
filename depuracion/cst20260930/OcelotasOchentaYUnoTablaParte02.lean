import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasPesos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasOchentaYUnoTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_46 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 122591098226256) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_47 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 149509316220326) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_48 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 191574783010874) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_49 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 266578449720687) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_50 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 438099164536788) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_51 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 1228598558795569) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_52 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 6280684857083312) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_53 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 7073420494008825) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_54 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 8095177852834902) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_55 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 9461960397959197) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_56 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 11384029735913767) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_57 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 14286047062640167) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_58 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 19173844215743192) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_59 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 29145686002653712) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_60 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 60729699573306971) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_61 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 66274197769496406) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_62 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 72932815674608198) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_63 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 81078870001780632) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_64 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 91273435466757338) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_65 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 104400361366073484) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_66 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 121937367370565061) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_67 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 146555531553240392) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_68 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 183628668400561935) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_69 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 245809357551467250) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_70 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 371662379946113151) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_71 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 761594547892523681) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_72 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 800967673558701028) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_73 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 844633784664013528) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_74 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 893335483581622015) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_75 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 947997126871210736) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_76 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 1009784055590181228) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_77 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 1080186602970464662) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_78 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 1161141878149442546) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_79 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 1255214749618739360) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_80 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 1365874561747126163) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_81 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 1497932375175722431) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_82 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 1658258999367843381) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_83 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 1857019409308776816) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_84 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 2109915809302842553) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_85 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 2442552464574813754) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_86 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 2899702080210469346) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_87 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 3567373979711581329) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_88 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 4634490088557343512) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_89 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 6612501671847735836) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

theorem fila_90 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hrR : r ≤ 81)
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
  exact pequeno_por_cota (s := 11536164662347833458) hw hr hrR hk hf (by norm_num)
    hLambda (by norm_num) (by norm_num)

end OcelotasOchentaYUnoTabla

#print axioms OcelotasOchentaYUnoTabla.fila_46
#print axioms OcelotasOchentaYUnoTabla.fila_47
#print axioms OcelotasOchentaYUnoTabla.fila_48
#print axioms OcelotasOchentaYUnoTabla.fila_49
#print axioms OcelotasOchentaYUnoTabla.fila_50
#print axioms OcelotasOchentaYUnoTabla.fila_51
#print axioms OcelotasOchentaYUnoTabla.fila_52
#print axioms OcelotasOchentaYUnoTabla.fila_53
#print axioms OcelotasOchentaYUnoTabla.fila_54
#print axioms OcelotasOchentaYUnoTabla.fila_55
#print axioms OcelotasOchentaYUnoTabla.fila_56
#print axioms OcelotasOchentaYUnoTabla.fila_57
#print axioms OcelotasOchentaYUnoTabla.fila_58
#print axioms OcelotasOchentaYUnoTabla.fila_59
#print axioms OcelotasOchentaYUnoTabla.fila_60
#print axioms OcelotasOchentaYUnoTabla.fila_61
#print axioms OcelotasOchentaYUnoTabla.fila_62
#print axioms OcelotasOchentaYUnoTabla.fila_63
#print axioms OcelotasOchentaYUnoTabla.fila_64
#print axioms OcelotasOchentaYUnoTabla.fila_65
#print axioms OcelotasOchentaYUnoTabla.fila_66
#print axioms OcelotasOchentaYUnoTabla.fila_67
#print axioms OcelotasOchentaYUnoTabla.fila_68
#print axioms OcelotasOchentaYUnoTabla.fila_69
#print axioms OcelotasOchentaYUnoTabla.fila_70
#print axioms OcelotasOchentaYUnoTabla.fila_71
#print axioms OcelotasOchentaYUnoTabla.fila_72
#print axioms OcelotasOchentaYUnoTabla.fila_73
#print axioms OcelotasOchentaYUnoTabla.fila_74
#print axioms OcelotasOchentaYUnoTabla.fila_75
#print axioms OcelotasOchentaYUnoTabla.fila_76
#print axioms OcelotasOchentaYUnoTabla.fila_77
#print axioms OcelotasOchentaYUnoTabla.fila_78
#print axioms OcelotasOchentaYUnoTabla.fila_79
#print axioms OcelotasOchentaYUnoTabla.fila_80
#print axioms OcelotasOchentaYUnoTabla.fila_81
#print axioms OcelotasOchentaYUnoTabla.fila_82
#print axioms OcelotasOchentaYUnoTabla.fila_83
#print axioms OcelotasOchentaYUnoTabla.fila_84
#print axioms OcelotasOchentaYUnoTabla.fila_85
#print axioms OcelotasOchentaYUnoTabla.fila_86
#print axioms OcelotasOchentaYUnoTabla.fila_87
#print axioms OcelotasOchentaYUnoTabla.fila_88
#print axioms OcelotasOchentaYUnoTabla.fila_89
#print axioms OcelotasOchentaYUnoTabla.fila_90
