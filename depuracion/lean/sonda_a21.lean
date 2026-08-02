#check @Nat.decidableBallLT
example : ∀ r, r < 5 → r + 1 < 7 := by decide
example : (∀ r, r < 4 → (r % 2 = 0 ↔ (r = 0 ∨ r = 2))) := by decide
