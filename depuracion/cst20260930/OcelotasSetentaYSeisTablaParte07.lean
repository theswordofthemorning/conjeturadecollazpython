import OcelotasNumerica
import OcelotasLogaritmosPrecisos
import OcelotasSetentaYSeisPrefijos

/-! Tabla generada; Lean comprueba todas las obligaciones. -/
namespace OcelotasSetentaYSeisTabla
open Real Ocelotas OcelotasTrayectorias OcelotasLMN OcelotasNumerica

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fila_96 {n r : ℕ} {a b : ℕ → ℕ}
    (hw : Palabra n a b r) (hr : 0 < r) (hr76 : r ≤ 76)
    (_hcontador : OcelotasContador.rachas n (tiempo a b r) ≤ 76)
    (hk : PrimerCruce n (tiempo a b r)) (hf : n ≤ T^[tiempo a b r] n)
    (hqa : 205632218873398596256 ≤ S (tiempo a b r) n)
    (hqb : S (tiempo a b r) n < 2389894509120846565669) : n < 28000000000000000001 := by
  have hU : (44503776122781252063553659893999 / 500000000000000000000000000000000000000000000000000000 : ℝ) ≤ (325919355854421968365 : ℝ) * log 2 - 205632218873398596256 * log 3 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.1, h3.2]
  have hV : (3461973821781515004749 : ℝ) * log 2 - 2184262290247447969413 * log 3 < 0 := by
    have h2 := OcelotasLogaritmosPrecisos.log_dos_cotas
    have h3 := OcelotasLogaritmosPrecisos.log_tres_cotas
    linarith [h2.2, h3.1]
  have hLambda := OcelotasTreceBase.lambda_de_pareja (P := 325919355854421968365) (Q := 205632218873398596256) (p := 3461973821781515004749) (v := 2184262290247447969413)
    (c := (44503776122781252063553659893999 / 500000000000000000000000000000000000000000000000000000 : ℝ)) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by simpa using hU) (by simpa using hV)
    (by omega : 0 < S (tiempo a b r) n)
    (by exact_mod_cast hqb : (S (tiempo a b r) n : ℤ) < 205632218873398596256 + 2184262290247447969413) hk.2
  have hpot : (853860128523970288109488 : ℕ) ^ 256 ≤ 2 ^ 20352 := by decide +kernel
  have hcriba : OcelotasAfinada.cota (1585 / 1000) (20352 / 256) 76 < 205632218873398596256 := by
    norm_num [OcelotasAfinada.cota]
  exact False.elim (imposible_por_criba (s := 853860128523970288109488) (B := 20352) hw hr hr76 hk hf
    (by norm_num) hLambda (by norm_num) hpot hcriba hqa)

end OcelotasSetentaYSeisTabla

#print axioms OcelotasSetentaYSeisTabla.fila_96
