import OcelotasNumerica
import OcelotasLogaritmosPrecisos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasSetentaYCincoTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_96 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr75 : r ≤ 75)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 205632218873398596256 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 1361733414753853584389) : n < 28000000000000000001 := by
  have hU : (44503776122781252063553659893999 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (325919355854421968365 : ℝ) * log 2 - 205632218873398596256 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (1832377042509405162924 : ℝ) * log 2 - 1156101195880454988133 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 325919355854421968365) (Q := 205632218873398596256) (p := 1832377042509405162924) (v := 1156101195880454988133)
    (c := (44503776122781252063553659893999 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 205632218873398596256 + 1156101195880454988133) hk.2
  have hpot : (842625126832865415897521 : ℕ) ^ 256 ≤ 2 ^ 20347 := by decide +kernel
  have hcriba : OcelotasAfinada.cota (1585 / 1000) (20347 / 256) 75 < 205632218873398596256 := by
    norm_num [OcelotasAfinada.cota]
  exact False.elim (imposible_por_criba (s := 842625126832865415897521) (B := 20347) hw hr hr75 hk hf
    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)

end OcelotasSetentaYCincoTabla

#print axioms OcelotasSetentaYCincoTabla.fila_96
