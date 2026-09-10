/- GACELAS: masa armonica de la cadena entera y certificados finitos.
   No formaliza probabilidad, limites de condicionamientos ni P2. -/
namespace Gacelas

def masa : Nat -> Int -> Int -> Int
  | 0, k, _ => k-1
  | n+1, k, c => if k <= 1 then 0 else
      if c % 2 = 0 then
        masa n k (c/2) + masa n k ((3*c+1-3^k.toNat)/2)
      else
        masa n (k+1) ((3*c+1)/2) +
        masa n (k-1) ((c-3^(k-1).toNat)/2)

theorem masa_armonica (n : Nat) (k c : Int) (hk : 1 <= k) :
    masa n k c = 2^n*(k-1) := by
  induction n generalizing k c with
  | zero => simp [masa]
  | succ n ih =>
    by_cases h : k <= 1
    · have he : k = 1 := by omega
      simp [masa, he]
    · have hu : 1 <= k+1 := by omega
      have hd : 1 <= k-1 := by omega
      rw [masa, if_neg h]
      split
      · rw [ih k _ hk, ih k _ hk, Int.pow_succ]
        grind
      · rw [ih (k+1) _ hu, ih (k-1) _ hd, Int.pow_succ]
        grind

theorem pesos_mixtos (k : Int) (hk : 2 <= k) :
    0 <= k /\ 0 <= k-2 /\ 0 < 2*(k-1) /\
    k+(k-2) = 2*(k-1) := by omega

theorem certificado_balota (m : Int) :
    (2*m+1)^2*(4*m+5) - (2*m+2)^2*(4*m+1) = 1 := by grind

theorem certificado_raiz : (3 : Rat) < (7/4)^2 := by grind

theorem certificado_exponencial :
    (15/16 : Rat)/(31/32) = 30/31 /\
    (30/31 : Rat) < (61/62)^2 := by grind

theorem cola_monotona (t : Int) (ht : 29 <= t) :
    61^2*(2*t+5) <= 62^2*(2*t+3) := by grind

set_option maxRecDepth 10000 in
set_option exponentiation.threshold 4096 in
theorem cola_inicial :
    4*62^2*61^2048*(2*1024+3) <= (62 : Nat)^2048 := by decide

def vivos : Nat -> Int -> Int -> Nat
  | 0, k, _ => if k <= 1 then 0 else 1
  | n+1, k, c => if k <= 1 then 0 else
      if c % 2 = 0 then
        vivos n k (c/2) + vivos n k ((3*c+1-3^k.toNat)/2)
      else
        vivos n (k+1) ((3*c+1)/2) +
        vivos n (k-1) ((c-3^(k-1).toNat)/2)

theorem sesgo_compartido :
    vivos 4 2 0 = 12 /\ vivos 3 2 0 = 8 /\ vivos 3 2 (-4) = 4 := by decide

#print axioms masa_armonica
#print axioms pesos_mixtos
#print axioms certificado_balota
#print axioms certificado_raiz
#print axioms certificado_exponencial
#print axioms cola_monotona
#print axioms cola_inicial
#print axioms sesgo_compartido
end Gacelas
