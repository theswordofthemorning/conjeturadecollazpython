import Tejonas

/- Alpacas: rachas arbitrariamente largas de enteros consecutivos con la misma altura
   y el mismo tiempo total de parada (Garner 1985; Gao 1993, pág. 262).

   Idea: por Martas casi todos los residuos r módulo 2^t tienen el par (r,r+1)
   fusionado por clases hasta t; una cota de unión da L residuos consecutivos así.
   Entonces los 2^t·u+r+i comparten, tras t pasos del atajo, el valor 3^a·u+A con
   el mismo a. Como 3 no divide a A y 2 es raíz primitiva módulo 3^a, se elige u
   con 3^a·u+A = 2^m: todos llegan a 1 a la vez, con las mismas mitades. -/

namespace AlpacasGarner

open TejonasGao CadenaCompletaGao

/-! ## Cada miembro del par por separado -/

theorem iter_succ (t : ℕ) (s : Par) : iter (t+1) s=paso_par (iter t s) := by
  simp only [iter,Function.iterate_succ_apply']

theorem iter_succ' (t : ℕ) (s : Par) : iter (t+1) s=iter t (paso_par s) := by
  simp only [iter,Function.iterate_succ_apply]

/-- La primera componente y su conteo de impares sólo dependen de la primera componente. -/
theorem iter_x (t : ℕ) : ∀ s : Par,
    (iter t s).x=(iter t ⟨s.x,s.x,s.p,s.p⟩).x ∧ (iter t s).p=(iter t ⟨s.x,s.x,s.p,s.p⟩).p := by
  induction t with
  | zero => intro s; simp [iter]
  | succ t ih =>
    intro s
    rw [iter_succ',iter_succ']
    obtain ⟨h1,h2⟩ := ih (paso_par s)
    obtain ⟨h3,h4⟩ := ih (paso_par ⟨s.x,s.x,s.p,s.p⟩)
    constructor
    · rw [h1,h3]; rfl
    · rw [h2,h4]; rfl

theorem iter_gira (t : ℕ) : ∀ s : Par, iter t (gira s)=gira (iter t s) := by
  induction t with
  | zero => intro s; rfl
  | succ t ih =>
    intro s
    rw [iter_succ',iter_succ']
    have e : paso_par (gira s)=gira (paso_par s) := rfl
    rw [e,ih]

/-- Valor tras t pasos del atajo desde x. -/
def sx (t : ℕ) (x : ℤ) : ℤ := (iter t ⟨x,x,0,0⟩).x

/-- Pasos impares entre los t primeros pasos del atajo desde x. -/
def sp (t : ℕ) (x : ℤ) : ℕ := (iter t ⟨x,x,0,0⟩).p

theorem par_x (t : ℕ) (x y : ℤ) : (iter t ⟨x,y,0,0⟩).x=sx t x ∧ (iter t ⟨x,y,0,0⟩).p=sp t x :=
  iter_x t ⟨x,y,0,0⟩

theorem par_y (t : ℕ) (x y : ℤ) : (iter t ⟨x,y,0,0⟩).y=sx t y ∧ (iter t ⟨x,y,0,0⟩).q=sp t y := by
  have h := iter_x t ⟨y,x,0,0⟩
  have g := iter_gira t ⟨x,y,0,0⟩
  have e : gira ⟨x,y,0,0⟩=(⟨y,x,0,0⟩ : Par) := rfl
  rw [e] at g
  rw [g] at h
  exact h

theorem sx_succ (t : ℕ) (x : ℤ) : sx (t+1) x=Tm (sx t x) := by
  unfold sx; rw [iter_succ]; rfl

theorem sp_succ (t : ℕ) (x : ℤ) : sp (t+1) x=sp t x+imp (sx t x) := by
  unfold sp sx; rw [iter_succ]; rfl

/-- Un par fusionado por clases: mismo valor y mismo conteo de impares. -/
theorem fusion_sx (t : ℕ) (x y : ℤ) (h : canon (iter t ⟨x,y,0,0⟩)=.fusion) :
    sx t x=sx t y ∧ sp t x=sp t y := by
  have hf : (iter t ⟨x,y,0,0⟩).p=(iter t ⟨x,y,0,0⟩).q ∧
      (iter t ⟨x,y,0,0⟩).x=(iter t ⟨x,y,0,0⟩).y := by
    by_contra hne
    unfold canon at h
    rw [if_neg hne] at h
    split at h <;> simp at h
  obtain ⟨hx,hp⟩ := par_x t x y
  obtain ⟨hy,hq⟩ := par_y t x y
  exact ⟨by rw [← hx,← hy]; exact hf.2,by rw [← hp,← hq]; exact hf.1⟩

/-! ## Del atajo al mapa clásico, con las mitades -/

/-- Pasos pares (divisiones por 2) entre los h primeros pasos clásicos desde n. -/
def pares (n h : ℕ) : ℕ := ((Finset.range h).filter (fun k => collatz^[k] n%2=0)).card

theorem pares_succ (n h : ℕ) :
    pares n (h+1)=pares n h+(if collatz^[h] n%2=0 then 1 else 0) := by
  unfold pares
  rw [Finset.range_add_one,Finset.filter_insert]
  split
  · rw [Finset.card_insert_of_notMem (by simp)]
  · simp

theorem impar_luego_par (v : ℕ) (hv : ¬v%2=0) : collatz v%2=0 := by
  simp only [collatz,if_neg hv]; omega

/-- t pasos del atajo desde n son t+(impares) pasos clásicos, y t de ellos son mitades. -/
theorem orbita (t n : ℕ) :
    sx t n=((collatz^[t+sp t n] n : ℕ):ℤ) ∧ pares n (t+sp t n)=t := by
  induction t with
  | zero => simp [sx,sp,iter,pares]
  | succ t ih =>
    obtain ⟨h1,h2⟩ := ih
    obtain ⟨hT,hI⟩ := Tm_collatz (collatz^[t+sp t n] n)
    rw [sx_succ,sp_succ,h1,hT,hI]
    split_ifs with hv
    · refine ⟨?_,?_⟩
      · rw [show t+1+(sp t n+0)=(t+sp t n)+1 by ring,Function.iterate_succ_apply']
      · rw [show t+1+(sp t n+0)=(t+sp t n)+1 by ring,pares_succ,h2,if_pos hv]
    · refine ⟨?_,?_⟩
      · rw [show t+1+(sp t n+1)=(t+sp t n)+1+1 by ring,Function.iterate_succ_apply',
          Function.iterate_succ_apply']
      · rw [show t+1+(sp t n+1)=(t+sp t n)+1+1 by ring,pares_succ,pares_succ,h2,if_neg hv,
          Function.iterate_succ_apply',if_pos (impar_luego_par _ hv)]

/-- Tras un paso impar, ningún valor del atajo es múltiplo de 3. -/
theorem tres (t : ℕ) (x : ℤ) : 1≤sp t x → sx t x%3≠0 := by
  induction t with
  | zero => intro h; simp [sp,iter] at h
  | succ t ih =>
    intro h
    rw [sx_succ]
    rw [sp_succ] at h
    rcases Int.emod_two_eq_zero_or_one (sx t x) with he | ho
    · rw [Tm_par _ he]
      rw [imp_par _ he] at h
      have := ih (by omega)
      omega
    · rw [Tm_impar _ ho]
      omega

theorem sp_mono (t : ℕ) (x : ℤ) : sp 1 x≤sp (t+1) x := by
  induction t with
  | zero => exact le_refl _
  | succ t ih => rw [sp_succ (t+1)]; omega

theorem sp_impar (t : ℕ) (x : ℤ) (hx : x%2=1) : 1≤sp (t+1) x := by
  have h1 : sp 1 x=1 := by
    rw [sp_succ]
    simp [sp,sx,iter,imp_impar _ hx]
  have := sp_mono t x
  omega

/-! ## 2 es raíz primitiva módulo 3^k -/

theorem cuatro (k : ℕ) : ∃ e : ℤ, (4:ℤ)^(3^k)=1+3^(k+1)*e ∧ e%3≠0 := by
  induction k with
  | zero => exact ⟨1,by norm_num,by norm_num⟩
  | succ k ih =>
    obtain ⟨e,he,he3⟩ := ih
    refine ⟨e+3*(3^k*e^2+3^(2*k)*e^3),?_,?_⟩
    · rw [pow_succ (3:ℕ) k,pow_mul,he]; ring
    · generalize 3^k*e^2+3^(2*k)*e^3=W; omega

theorem dos_genera (k : ℕ) : ∀ c : ℤ, c%3≠0 → ∃ m : ℕ, (3:ℤ)^(k+1) ∣ 2^m-c := by
  induction k with
  | zero =>
    intro c hc
    have : c%3=1 ∨ c%3=2 := by omega
    rcases this with h | h
    · exact ⟨0,by norm_num; omega⟩
    · exact ⟨1,by norm_num; omega⟩
  | succ k ih =>
    intro c hc
    obtain ⟨m,j,hj⟩ := ih c hc
    obtain ⟨e,he,he3⟩ := cuatro k
    have h2m : (2:ℤ)^m=3^(k+1)*j+c := by linarith
    have hce : (c*e)%3≠0 := by
      have h1 : c%3=1 ∨ c%3=2 := by omega
      have h2 : e%3=1 ∨ e%3=2 := by omega
      rw [Int.mul_emod]
      rcases h1 with h1 | h1 <;> rcases h2 with h2 | h2 <;> rw [h1,h2] <;> norm_num
    have hs : j%3=0 ∨ (j+c*e)%3=0 ∨ (j+2*(c*e))%3=0 := by
      generalize c*e=w at hce ⊢
      rcases (by omega : j%3=0 ∨ j%3=1 ∨ j%3=2) with h | h | h <;>
        rcases (by omega : w%3=1 ∨ w%3=2) with g | g <;> omega
    have h4 : ∀ s : ℕ, (2:ℤ)^(m+2*3^k*s)=2^m*(4^(3^k))^s := by
      intro s
      rw [pow_add,pow_mul,pow_mul]; norm_num
    rcases hs with hs | hs | hs
    · obtain ⟨j',hj'⟩ := Int.dvd_of_emod_eq_zero hs
      exact ⟨m,j',by rw [h2m,hj']; ring⟩
    · obtain ⟨j',hj'⟩ := Int.dvd_of_emod_eq_zero hs
      refine ⟨m+2*3^k*1,j'+3^k*j*e,?_⟩
      rw [h4,he,h2m]
      have hj2 : j=3*j'-c*e := by linarith
      subst hj2
      ring
    · obtain ⟨j',hj'⟩ := Int.dvd_of_emod_eq_zero hs
      refine ⟨m+2*3^k*2,j'+3^k*(2*j*e+c*e^2)+3^(2*k+1)*j*e^2,?_⟩
      rw [h4,he,h2m]
      have hj2 : j=3*j'-2*(c*e) := by linarith
      subst hj2
      ring

theorem dos_genera_grande (k : ℕ) (c : ℤ) (hc : c%3≠0) (M : ℕ) :
    ∃ m : ℕ, M≤m ∧ (3:ℤ)^(k+1) ∣ 2^m-c := by
  obtain ⟨m,hm⟩ := dos_genera k c hc
  obtain ⟨e,he,_⟩ := cuatro k
  refine ⟨m+2*3^k*M,?_,?_⟩
  · have : M≤2*3^k*M := Nat.le_mul_of_pos_left M (by positivity)
    omega
  · have h4 : (2:ℤ)^(m+2*3^k*M)=2^m*(4^(3^k))^M := by
      rw [pow_add,pow_mul,pow_mul]; norm_num
    have h1 : (2:ℤ)^(m+2*3^k*M)-c=2^m*((4^(3^k))^M-1)+(2^m-c) := by
      rw [h4]; ring
    rw [h1]
    apply dvd_add _ hm
    apply Dvd.dvd.mul_left
    have h2 : (3:ℤ)^(k+1) ∣ 4^(3^k)-1 := ⟨e,by rw [he]; ring⟩
    exact h2.trans (sub_one_dvd_pow_sub_one _ _)

/-! ## Cota de unión: L residuos consecutivos buenos -/

theorem bloque (t L : ℕ) (S : Finset ℕ) (hS : S ⊆ Finset.range (2^t))
    (h : L*(2^t+L-S.card)<2^t) : ∃ r, ∀ i, i<L → r+i ∈ S := by
  by_contra hno
  push Not at hno
  have hcub : Finset.range (2^t) ⊆ (Finset.range L).biUnion
      (fun i => (Finset.range (2^t)).filter (fun r => r+i ∉ S)) := by
    intro r hr
    obtain ⟨i,hi,hri⟩ := hno r
    simp only [Finset.mem_biUnion,Finset.mem_range,Finset.mem_filter]
    exact ⟨i,hi,Finset.mem_range.mp hr,hri⟩
  have hcada : ∀ i ∈ Finset.range L,
      ((Finset.range (2^t)).filter (fun r => r+i ∉ S)).card≤2^t+L-S.card := by
    intro i hi
    have hi' := Finset.mem_range.mp hi
    have hsub : S ⊆ Finset.range (2^t+L) :=
      hS.trans (Finset.range_subset_range.mpr (by omega))
    calc _ ≤ (Finset.range (2^t+L) \ S).card := by
          apply Finset.card_le_card_of_injOn (fun r => r+i)
          · intro r hr
            rw [Finset.mem_coe,Finset.mem_filter,Finset.mem_range] at hr
            rw [Finset.mem_coe,Finset.mem_sdiff,Finset.mem_range]
            refine ⟨?_,hr.2⟩
            show r+i<2^t+L
            omega
          · intro a _ b _ hab
            simp only at hab
            omega
      _ = 2^t+L-S.card := by rw [Finset.card_sdiff_of_subset hsub,Finset.card_range]
  have h1 := Finset.card_le_card hcub
  have h2 := Finset.card_biUnion_le (s:=Finset.range L)
    (t:=fun i => (Finset.range (2^t)).filter (fun r => r+i ∉ S))
  have h3 := Finset.sum_le_sum hcada
  rw [Finset.sum_const,Finset.card_range,smul_eq_mul] at h3
  rw [Finset.card_range] at h1
  omega

/-! ## Martas da el bloque: L residuos seguidos con su par fusionado -/

theorem bloque_fusion (L : ℕ) : ∃ t r : ℕ, 1≤t ∧ ∀ i, i<L → r+i<2^t ∧
    canon (iter t ⟨((r+i:ℕ):ℤ),((r+i:ℕ):ℤ)+1,0,0⟩)=.fusion := by
  obtain ⟨h0,hh⟩ := MartasGao.martas (1/(2*((L:ℝ)+1))) (by positivity)
  set t := max h0 (2*L*L+1) with ht
  have hPt := hh t (le_max_left _ _)
  set S := (Finset.range (2^t)).filter
    (fun r : ℕ => canon (iter t ⟨(r:ℤ),(r:ℤ)+1,0,0⟩)=.fusion) with hSdef
  -- |S| = 2^t · P(fusión hasta t), como en `TejonasGao.gao`
  have hS : (S.card:ℝ)=(2:ℝ)^t*EnsayoGao.probabilidad_fusion t (.vivo 0 1) := by
    have h := transporte EnsayoGao.fusion t
    unfold EnsayoGao.probabilidad_fusion
    rw [← h,hSdef,Finset.card_filter]
    push_cast
    apply Finset.sum_congr rfl
    intro n _
    unfold EnsayoGao.fusion
    split <;> simp_all
  have hSsub : S ⊆ Finset.range (2^t) := Finset.filter_subset _ _
  have hSle : S.card≤2^t := by simpa using Finset.card_le_card hSsub
  have ht1 : 2*L*L+1≤t := le_max_right _ _
  have ht2 : 2*L*L<2^t := by
    have := Nat.lt_two_pow_self (n:=t)
    omega
  have hkey : L*(2^t+L-S.card)<2^t := by
    have hT : (0:ℝ)<2^t := by positivity
    have hL : (0:ℝ)≤L := Nat.cast_nonneg _
    set q := (2:ℝ)^t/(2*((L:ℝ)+1)) with hq
    have hP : (2:ℝ)^t-S.card≤q := by
      rw [hS]
      have := mul_le_mul_of_nonneg_left hPt (le_of_lt hT)
      calc (2:ℝ)^t-2^t*EnsayoGao.probabilidad_fusion t (.vivo 0 1)
          =2^t*(1-EnsayoGao.probabilidad_fusion t (.vivo 0 1)) := by ring
        _ ≤ 2^t*(1/(2*((L:ℝ)+1))) := this
        _ = q := by rw [hq]; ring
    have hLq : (L:ℝ)*q≤(2:ℝ)^t/2 := by
      rw [hq,mul_div_assoc',div_le_div_iff₀ (by positivity) (by norm_num)]
      nlinarith
    have h2L : 2*(L:ℝ)*L<(2:ℝ)^t := by exact_mod_cast ht2
    have hcast : ((L*(2^t+L-S.card):ℕ):ℝ)=(L:ℝ)*((2:ℝ)^t+L-S.card) := by
      rw [Nat.cast_mul,Nat.cast_sub (by omega)]
      push_cast; ring
    have hLP := mul_le_mul_of_nonneg_left hP hL
    have hreal : (L:ℝ)*((2:ℝ)^t+L-S.card)<(2:ℝ)^t := by
      calc (L:ℝ)*((2:ℝ)^t+L-S.card)=(L:ℝ)*((2:ℝ)^t-S.card)+L*L := by ring
        _ ≤ (L:ℝ)*q+L*L := by linarith
        _ < (2:ℝ)^t := by linarith
    rw [← hcast] at hreal
    exact_mod_cast hreal
  obtain ⟨r,hr⟩ := bloque t L S hSsub hkey
  refine ⟨t,r,by omega,fun i hi => ?_⟩
  have hm := hr i hi
  rw [hSdef,Finset.mem_filter,Finset.mem_range] at hm
  exact ⟨hm.1,by push_cast; exact hm.2⟩

/-! ## Llegada a 1 desde una potencia de 2 -/

theorem potencia_dos (m j : ℕ) (hj : j≤m) : collatz^[j] (2^m)=2^(m-j) := by
  induction j with
  | zero => simp
  | succ j ih =>
    rw [Function.iterate_succ_apply',ih (by omega)]
    have e : m-j=(m-(j+1))+1 := by omega
    rw [e,pow_succ]
    simp [collatz]

/-- Desde 1 sólo se visita el ciclo 1 → 4 → 2 → 1. -/
theorem ciclo (j : ℕ) : collatz^[j] 1=1 ∨ collatz^[j] 1=2 ∨ collatz^[j] 1=4 := by
  induction j with
  | zero => simp
  | succ j ih =>
    rw [Function.iterate_succ_apply']
    rcases ih with h | h | h <;> rw [h] <;> simp [collatz]

theorem pares_cola (n K m : ℕ) (hK : collatz^[K] n=2^m) :
    ∀ j, j≤m → pares n (K+j)=pares n K+j := by
  intro j
  induction j with
  | zero => intro _; simp
  | succ j ih =>
    intro hj
    rw [show K+(j+1)=(K+j)+1 by ring,pares_succ,ih (by omega)]
    have h : collatz^[K+j] n=2^(m-j) := by
      rw [Nat.add_comm,Function.iterate_add_apply,hK,potencia_dos m j (by omega)]
    have hpar : collatz^[K+j] n%2=0 := by
      rw [h,show m-j=(m-j-1)+1 by omega,pow_succ]; simp
    rw [if_pos hpar]
    omega

/-- Si n llega a 2^m (m ≥ 3) en el paso K, su altura es K+m y sus mitades crecen en m. -/
theorem altura_potencia (n K m : ℕ) (hm : 3≤m) (hK : collatz^[K] n=2^m) :
    collatz^[K+m] n=1 ∧ (∀ k, k<K+m → collatz^[k] n≠1) ∧ pares n (K+m)=pares n K+m := by
  have hcola : ∀ j, j≤m → collatz^[K+j] n=2^(m-j) := by
    intro j hj
    rw [Nat.add_comm,Function.iterate_add_apply,hK,potencia_dos m j hj]
  refine ⟨?_,?_,pares_cola n K m hK m le_rfl⟩
  · rw [hcola m le_rfl]; simp
  · intro k hk h1
    by_cases hkK : K≤k
    · obtain ⟨j,rfl⟩ : ∃ j, k=K+j := ⟨k-K,by omega⟩
      rw [hcola j (by omega)] at h1
      have : 1≤m-j := by omega
      have h2 : 2≤2^(m-j) := by
        calc 2=2^1 := by norm_num
          _ ≤ 2^(m-j) := Nat.pow_le_pow_right (by norm_num) this
      omega
    · have e : collatz^[K] n=collatz^[K-k] (collatz^[k] n) := by
        rw [← Function.iterate_add_apply]; congr 1; omega
      rw [h1,hK] at e
      have h8 : 8≤2^m := by
        calc 8=2^3 := by norm_num
          _ ≤ 2^m := Nat.pow_le_pow_right (by norm_num) hm
      rcases ciclo (K-k) with h | h | h <;> omega

/-! ## Alpacas: la conjetura de Garner -/

/-- Para cada L y cada N hay n ≥ N tal que n, n+1, …, n+L llegan a 1 en los mismos h
    pasos clásicos, por primera vez, y con las mismas d mitades. -/
theorem alpacas (L N : ℕ) : ∃ n h d : ℕ, N≤n ∧ ∀ i, i≤L →
    collatz^[h] (n+i)=1 ∧ (∀ k, k<h → collatz^[k] (n+i)≠1) ∧ pares (n+i) h=d := by
  obtain ⟨t,r,ht1,hbl⟩ := bloque_fusion (L+1)
  -- cada par (2^t·u+r+i, 2^t·u+r+i+1) está fusionado
  have hfus : ∀ u : ℕ, ∀ i, i<L+1 →
      sx t ((2^t*u+r+i:ℕ):ℤ)=sx t ((2^t*u+r+i+1:ℕ):ℤ) ∧
        sp t ((2^t*u+r+i:ℕ):ℤ)=sp t ((2^t*u+r+i+1:ℕ):ℤ) := by
    intro u i hi
    obtain ⟨hlt,hc⟩ := hbl i hi
    apply fusion_sx
    have hmod : (2^t*u+r+i)%2^t=r+i := by
      rw [show 2^t*u+r+i=(r+i)+2^t*u by ring,Nat.add_mul_mod_self_left,Nat.mod_eq_of_lt hlt]
    have hcm := canon_modulo t (2^t*u+r+i)
    rw [hmod] at hcm
    rw [show ((2^t*u+r+i+1:ℕ):ℤ)=((2^t*u+r+i:ℕ):ℤ)+1 by push_cast; ring,hcm]
    exact hc
  -- en cadena, todos comparten valor y conteo de impares con el primero
  have hcad : ∀ u : ℕ, ∀ i, i≤L+1 →
      sx t ((2^t*u+r+i:ℕ):ℤ)=sx t ((2^t*u+r:ℕ):ℤ) ∧
        sp t ((2^t*u+r+i:ℕ):ℤ)=sp t ((2^t*u+r:ℕ):ℤ) := by
    intro u i
    induction i with
    | zero => intro _; simp
    | succ i ih =>
      intro hi
      obtain ⟨h1,h2⟩ := ih (by omega)
      obtain ⟨h3,h4⟩ := hfus u i (by omega)
      rw [show 2^t*u+r+(i+1)=2^t*u+r+i+1 by ring]
      exact ⟨h3.symm.trans h1,h4.symm.trans h2⟩
  -- forma afín del primero: 3^a·u + A
  obtain ⟨R',hR'⟩ := iter_rep t ⟨0,0,0,1⟩ r
  have hafin : ∀ u : ℕ, sx t ((2^t*u+r:ℕ):ℤ)=3^R'.p*u+R'.a ∧ sp t ((2^t*u+r:ℕ):ℤ)=R'.p := by
    intro u
    have h := hR' (u:ℤ)
    have e : par_rep ⟨0,0,0,1⟩ ((2:ℤ)^t*u+r)=⟨((2^t*u+r:ℕ):ℤ),((2^t*u+r:ℕ):ℤ)+1,0,0⟩ := by
      simp [par_rep]
    rw [e] at h
    obtain ⟨hx,hp⟩ := par_x t ((2^t*u+r:ℕ):ℤ) (((2^t*u+r:ℕ):ℤ)+1)
    rw [h] at hx hp
    exact ⟨hx.symm,hp.symm⟩
  have h0 := hafin 0
  simp only [mul_zero,zero_add,Nat.cast_zero] at h0
  -- a ≥ 1: r o r+1 es impar y comparten el conteo
  have ht' : t-1+1=t := by omega
  have ha : 1≤R'.p := by
    have hc1 := (hcad 0 1 (by omega)).2
    simp only [mul_zero,zero_add] at hc1
    rcases Nat.even_or_odd r with hr | hr
    · have := sp_impar (t-1) ((r+1:ℕ):ℤ) (by obtain ⟨k,hk⟩ := hr; omega)
      rw [ht'] at this
      omega
    · have := sp_impar (t-1) (r:ℤ) (by obtain ⟨k,hk⟩ := hr; omega)
      rw [ht'] at this
      omega
  -- 3 no divide a A
  have hA3 : R'.a%3≠0 := by
    have := tres t (r:ℤ) (by rw [h0.2]; exact ha)
    rw [h0.1] at this
    exact this
  -- A es un natural: el valor clásico de r en el paso t+a
  obtain ⟨hor1,_⟩ := orbita t r
  rw [h0.1,h0.2] at hor1
  set A' := collatz^[t+R'.p] r with hA'
  -- u con 3^a·u + A = 2^m, u ≥ N y m ≥ 3
  obtain ⟨m,hmM,hdiv⟩ := dos_genera_grande (R'.p-1) R'.a hA3 (A'+3^R'.p*N+3)
  rw [show R'.p-1+1=R'.p by omega] at hdiv
  obtain ⟨u,hu⟩ := hdiv
  have hm2 : (m:ℤ)<2^m := by exact_mod_cast Nat.lt_two_pow_self (n:=m)
  have hMz : ((A'+3^R'.p*N+3:ℕ):ℤ)≤m := by exact_mod_cast hmM
  push_cast at hMz
  have h3pos : (0:ℤ)<3^R'.p := by positivity
  have huN : (N:ℤ)<u := by
    have : (3:ℤ)^R'.p*N<3^R'.p*u := by rw [← hu,hor1]; linarith
    exact lt_of_mul_lt_mul_left this (le_of_lt h3pos)
  have hu0 : 0≤u := by have := Nat.cast_nonneg (α:=ℤ) N; linarith
  obtain ⟨u',rfl⟩ : ∃ u' : ℕ, u=u' := ⟨u.toNat,(Int.toNat_of_nonneg hu0).symm⟩
  have hm3 : 3≤m := by omega
  -- todos valen 2^m en el paso clásico t+a, con t mitades
  refine ⟨2^t*u'+r,t+R'.p+m,t+m,?_,fun i hi => ?_⟩
  · have : (N:ℤ)<u' := huN
    have h1 : u'≤2^t*u' := Nat.le_mul_of_pos_left u' (by positivity)
    omega
  obtain ⟨hsx,hsp⟩ := hcad u' i (by omega)
  obtain ⟨ho1,ho2⟩ := orbita t (2^t*u'+r+i)
  rw [hsp,(hafin u').2] at ho1 ho2
  rw [hsx,(hafin u').1] at ho1
  have hval : collatz^[t+R'.p] (2^t*u'+r+i)=2^m := by
    have : (((collatz^[t+R'.p] (2^t*u'+r+i)):ℕ):ℤ)=((2^m:ℕ):ℤ) := by
      rw [← ho1]; push_cast; linarith
    exact_mod_cast this
  obtain ⟨g1,g2,g3⟩ := altura_potencia (2^t*u'+r+i) (t+R'.p) m hm3 hval
  exact ⟨g1,g2,by rw [g3,ho2]⟩

end AlpacasGarner

#print axioms AlpacasGarner.alpacas
