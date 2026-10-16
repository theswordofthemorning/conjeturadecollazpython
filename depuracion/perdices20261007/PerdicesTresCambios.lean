import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith

/-! Cierres lineales bajo cotas orbitales escritas en TRES_CAMBIOS.md.
Los testigos de la relajación no son semillas ni órbitas de Collatz.
-/

namespace PerdicesTresCambios

set_option exponentiation.threshold 8000

def CotasABAB (a b c d ell vin vf : ℕ) : Prop :=
  vin = a+2 ∧ a+2 ≤ ell ∧
  51*b+34 ≤ 17*ell+10*a ∧
  17*c+34 ≤ 17*ell+10*a+3*b ∧
  17*(3*d+vf) ≤ 17*ell+10*a+3*b+10*c

def CotasBABA (a b c d ell vin vf : ℕ) : Prop :=
  vin = 3*a+2 ∧
  17*b+34 ≤ 17*ell+3*a ∧
  51*c ≤ 17*ell+3*a+10*b ∧
  17*(d+vf) ≤ 17*ell+3*a+10*b+3*c

theorem presupuesto_abab {a b c d ell vin vf : ℕ}
    (h : CotasABAB a b c d ell vin vf) :
    a+3*b+c+3*d+13*vf ≤ 13*vin+26*ell := by
  rcases h with ⟨hin, he, hb, hc, hv⟩
  omega

theorem presupuesto_baba {a b c d ell vin vf : ℕ}
    (h : CotasBABA a b c d ell vin vf) :
    3*a+b+3*c+d+13*vf ≤ 13*vin+26*ell := by
  rcases h with ⟨hin, hb, hc, hv⟩
  omega

theorem presupuesto_hasta_dos {L vin vf ell : ℕ}
    (h : 7*L+17*vf ≤ 17*vin+34*ell) :
    L+13*vf ≤ 13*vin+26*ell := by
  omega

def CotasBABAB (a b c d e ell vin vf : ℕ) : Prop :=
  1 ≤ a ∧ 1 ≤ b ∧ 1 ≤ c ∧ 1 ≤ d ∧ 1 ≤ e ∧
  vin = 3*a+2 ∧ vin ≤ ell ∧
  17*b+34 ≤ 17*ell+3*a ∧
  51*c+34 ≤ 17*ell+3*a+10*b ∧
  17*d+34 ≤ 17*ell+3*a+10*b+3*c ∧
  17*(3*e+vf) ≤ 17*ell+3*a+10*b+3*c+10*d

theorem testigo_tres :
    CotasABAB 997 527 1670 1 1000 999 2600 ∧
    17*999+34*1000 < 7*(997+3*527+1670+3)+17*2600 := by
  norm_num [CotasABAB]

theorem testigo_cuatro :
    CotasBABAB 1 998 527 1670 1 1000 5 2600 ∧
    5+2*1000 < 2600 := by
  norm_num [CotasBABAB]

theorem no_cierre_cuatro_con_cotas :
    ¬ (∀ a b c d e ell vin vf : ℕ,
      CotasBABAB a b c d e ell vin vf → vf ≤ vin+2*ell) := by
  intro h
  have ht := h 1 998 527 1670 1 1000 5 2600 testigo_cuatro.1
  norm_num at ht

theorem balance_testigo_cuatro :
    (3+998+3*527+1670+3 : ℕ)+2600 =
      5+(998+3*527+1670+(2603-2)) := by
  norm_num

set_option maxRecDepth 30000 in
theorem encajes_exactos_testigo_cuatro :
    (2 : ℕ)^(3+1000) ≤ 3^2*2^1000 ∧
    (2 : ℕ)^(1001+1583) ≤ 3^1000*2^1000 ∧
    (2 : ℕ)^(2582+1672) ≤ 3^2054*2^1000 ∧
    (2 : ℕ)^(4252+2603) ≤ 3^3724*2^1000 := by
  decide

end PerdicesTresCambios

#print axioms PerdicesTresCambios.presupuesto_abab
#print axioms PerdicesTresCambios.presupuesto_baba
#print axioms PerdicesTresCambios.presupuesto_hasta_dos
#print axioms PerdicesTresCambios.testigo_tres
#print axioms PerdicesTresCambios.testigo_cuatro
#print axioms PerdicesTresCambios.no_cierre_cuatro_con_cotas
#print axioms PerdicesTresCambios.balance_testigo_cuatro
#print axioms PerdicesTresCambios.encajes_exactos_testigo_cuatro
