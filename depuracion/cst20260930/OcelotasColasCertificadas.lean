import OcelotasColaParametrica

/-! Certificados de colas, sin afirmar descenso en los tiempos restantes. -/
namespace OcelotasColasCertificadas
open Ocelotas OcelotasContador OcelotasLMNFuente

set_option maxRecDepth 100000
set_option maxHeartbeats 1000000

theorem region_21 (hL : LMN23) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 21) (hf : n ≤ T^[k] n) :
    k < 2 ^ 32 ∧ n < 2 ^ (19 * (32 + 32) ^ 2 + 5) :=
  OcelotasColaParametrica.region_del_fallo_corolario (R := 21)
    (A := 32237) (c := 5) (H := 32) hL
    (by decide +kernel) (by decide +kernel) (by decide +kernel) hn hk hr hf

theorem region_22 (hL : LMN23) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 22) (hf : n ≤ T^[k] n) :
    k < 2 ^ 33 ∧ n < 2 ^ (19 * (33 + 32) ^ 2 + 5) :=
  OcelotasColaParametrica.region_del_fallo_corolario (R := 22)
    (A := 51580) (c := 5) (H := 33) hL
    (by decide +kernel) (by decide +kernel) (by decide +kernel) hn hk hr hf

theorem region_23 (hL : LMN23) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 23) (hf : n ≤ T^[k] n) :
    k < 2 ^ 34 ∧ n < 2 ^ (19 * (34 + 32) ^ 2 + 5) :=
  OcelotasColaParametrica.region_del_fallo_corolario (R := 23)
    (A := 82528) (c := 5) (H := 34) hL
    (by decide +kernel) (by decide +kernel) (by decide +kernel) hn hk hr hf

theorem region_50 (hL : LMN23) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 50) (hf : n ≤ T^[k] n) :
    k < 2 ^ 53 ∧ n < 2 ^ (19 * (53 + 32) ^ 2 + 6) :=
  OcelotasColaParametrica.region_del_fallo_corolario (R := 50)
    (A := 26782300736) (c := 6) (H := 53) hL
    (by decide +kernel) (by decide +kernel) (by decide +kernel) hn hk hr hf

theorem region_75 (hL : LMN23) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 75) (hf : n ≤ T^[k] n) :
    k < 2 ^ 70 ∧ n < 2 ^ (19 * (70 + 32) ^ 2 + 7) :=
  OcelotasColaParametrica.region_del_fallo_corolario (R := 75)
    (A := 3395059960557476) (c := 7) (H := 70) hL
    (by decide +kernel) (by decide +kernel) (by decide +kernel) hn hk hr hf

theorem region_100 (hL : LMN23) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 100) (hf : n ≤ T^[k] n) :
    k < 2 ^ 88 ∧ n < 2 ^ (19 * (88 + 32) ^ 2 + 7) :=
  OcelotasColaParametrica.region_del_fallo_corolario (R := 100)
    (A := 430374979681151431608) (c := 7) (H := 88) hL
    (by decide +kernel) (by decide +kernel) (by decide +kernel) hn hk hr hf

theorem region_1000 (hL : LMN23) {n k : ℕ} (hn : 2 ≤ n)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 1000) (hf : n ≤ T^[k] n) :
    k < 2 ^ 703 ∧ n < 2 ^ (19 * (703 + 32) ^ 2 + 10) :=
  OcelotasColaParametrica.region_del_fallo_corolario (R := 1000)
    (A := 2197006822384905166839816323727652271973365268488787948488005750402928213521390758513292020528687005523490126080119470506407802949040096880288510408752030673090779074064481492721495107128665655006097758820) (c := 10) (H := 703) hL
    (by decide +kernel) (by decide +kernel) (by decide +kernel) hn hk hr hf

end OcelotasColasCertificadas
#print axioms OcelotasColasCertificadas.region_21
#print axioms OcelotasColasCertificadas.region_22
#print axioms OcelotasColasCertificadas.region_23
#print axioms OcelotasColasCertificadas.region_50
#print axioms OcelotasColasCertificadas.region_75
#print axioms OcelotasColasCertificadas.region_100
#print axioms OcelotasColasCertificadas.region_1000
