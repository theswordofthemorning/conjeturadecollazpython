-- A7: "con la regla clasica dos pasos impares nunca van seguidos:
--      P(impar | impar) = 0 exacto"
-- Mapa CLASICO: n par -> n/2 ; n impar -> 3n+1
-- Escrito desde cero, sin mirar ningun fichero del repo.

set_option maxRecDepth 40000

-- ============ la definicion del mapa, escrita aqui mismo ============
def paso (n : Nat) : Nat :=
  if n % 2 = 0 then n / 2 else 3 * n + 1

-- trayectoria: tray n k = k-esimo iterado
def tray (n : Nat) : Nat -> Nat
  | 0 => n
  | k+1 => paso (tray n k)

-- ============ LA TRAMPA: comprobar que 'paso' es Collatz de verdad ============
-- casos concretos del mapa, decididos por el NUCLEO (no #eval):
theorem casos_mapa : paso 6 = 3 /\ paso 3 = 10 /\ paso 1 = 4 /\ paso 27 = 82 := by
  decide

-- trayectoria conocida del 7 (clasico, 16 pasos hasta el 1):
-- 7,22,11,34,17,52,26,13,40,20,10,5,16,8,4,2,1
theorem caso_7 : tray 7 16 = 1 := by decide

-- y un punto intermedio del 27: tras 10 pasos clasicos esta en 214
-- (27,82,41,124,62,31,94,47,142,71,214)
theorem caso_27 : tray 27 10 = 214 := by decide

-- ============ EL TEOREMA ============
-- si n es impar, su sucesor clasico 3n+1 es PAR. Para todo n : Nat.
theorem impar_luego_par (n : Nat) (h : n % 2 = 1) : paso n % 2 = 0 := by
  unfold paso
  split
  · -- rama n % 2 = 0: contradice h
    omega
  · -- rama impar: el objetivo es (3*n+1) % 2 = 0 con n % 2 = 1
    omega

-- forma "dos impares seguidos nunca": en cualquier posicion k de cualquier
-- trayectoria, si el valor es impar el siguiente es par.
theorem no_dos_impares_seguidos (n k : Nat) (h : tray n k % 2 = 1) :
    tray n (k+1) % 2 = 0 :=
  impar_luego_par (tray n k) h

-- forma negativa explicita del enunciado: P(impar | impar) = 0
theorem prohibicion (n : Nat) (h : n % 2 = 1) : paso n % 2 ≠ 1 := by
  have hp := impar_luego_par n h
  omega

-- ============ barrido finito extra, decidido por el nucleo ============
-- (bordes incluidos: n = 1 esta dentro; n = 0 es par y queda vacuo)
theorem barrido_2000 : ∀ n, n < 2000 → n % 2 = 1 → paso n % 2 = 0 := by
  decide

-- ============ control de axiomas ============
#print axioms casos_mapa
#print axioms caso_7
#print axioms caso_27
#print axioms impar_luego_par
#print axioms no_dos_impares_seguidos
#print axioms prohibicion
#print axioms barrido_2000
