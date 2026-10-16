import OcelotasOchentaYTres
import OcelotasRoosendaal
import OcelotasColaRhin

/-! Enunciados finales para responder a Rozier.
La unica hipotesis numerica externa es DelayHasta: todos los enteros del
intervalo llegan a 1 en a lo sumo 2480 pasos clasicos. Ni esa cobertura
ni los teoremas trascendentes LMN/Rhin se demuestran en este archivo.
-/

namespace OcelotasRozier

open Ocelotas OcelotasTrayectorias OcelotasContador OcelotasRoosendaal

def RecordRoosendaal : Prop := DelayHasta 46645791847966786687 2480

theorem cst_hasta_record (hD : RecordRoosendaal) :
    OcelotasOchentaYTres.CSTHastaRecord20260928 := by
  intro n k hn hN hk
  exact cst_de_delay hD hn hN hk

theorem cst_83_lmn (hL : OcelotasLMNFuente.LMN23) (hD : RecordRoosendaal)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hr : rachas n k ≤ 83) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n :=
  OcelotasOchentaYTres.cst_condicional hL (cst_hasta_record hD) hn hk hr

theorem cst_83_rhin (hR : OcelotasRhin.RhinHomogenea 2) (hD : RecordRoosendaal)
    {n k : ℕ} (hn : 2 ≤ n) (hk : PrimerCruce n k) (hr : rachas n k ≤ 83) :
    (∀ j, j < k → n ≤ T^[j] n) ∧ T^[k] n < n := by
  refine ⟨fun _ hj => no_desciende_antes hk hj, ?_⟩
  by_cases hpar : n % 2 = 0
  · exact OcelotasCierre.descenso_par hn hpar hk
  · by_contra h
    have hf : n ≤ T^[k] n := by omega
    obtain ⟨hpos, a, b, hw, he⟩ := palabra_del_cruce (by omega : n % 2 = 1) hk
    have hkw : PrimerCruce n (tiempo a b (rachas n k)) := by rwa [he]
    have hfw : n ≤ T^[tiempo a b (rachas n k)] n := by rwa [he]
    by_cases hq : S k n < 101189215254399926676993
    · have hsmall := OcelotasOchentaYTresTabla.pequeno_de_tabla hw hpos hr hkw hfw
        (by simpa [he] using hq)
      have hd := cst_de_delay hD hn (by omega) hk
      omega
    · have hqk := OcelotasRoosendaal.impares_le_tiempo k n
      have hp : (2 : ℕ) ^ 68 = 295147905179352825856 := by norm_num
      have hd := OcelotasColaRhin.cola_ochenta_y_tres hR hn hk hr (by omega)
      omega

end OcelotasRozier

#print axioms OcelotasRozier.cst_hasta_record
#print axioms OcelotasRozier.cst_83_lmn
#print axioms OcelotasRozier.cst_83_rhin
#print OcelotasRozier.cst_83_lmn
#print OcelotasRozier.cst_83_rhin
