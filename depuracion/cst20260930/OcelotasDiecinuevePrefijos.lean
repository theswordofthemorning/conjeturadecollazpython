import OcelotasCribaPrefijos

/-! # Ocelotas: los dos intervalos pendientes de diecinueve rachas

Se reutiliza el descenso certificado hasta 4912740 en el ensamblaje.
Aquí sólo se excluyen fallos con q grande, sin censar todas las órbitas.
-/

namespace OcelotasDiecinuevePrefijos

open Ocelotas OcelotasContador OcelotasCribaPrefijos

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem certificado_bajo :
    comprobar 5184569 79335 19 4912741 1 1 4912741 0 0 false 64 = true := by
  decide +kernel

theorem certificado_alto :
    comprobar 294539509 190537 19 4912741 1 1 4912741 0 0 false 64 = true := by
  decide +kernel

theorem descenso_bajo {n k : ℕ} (hinicio : 4912741 ≤ n) (hmax : n ≤ 5184569)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 19) (hq : 79335 ≤ S k n) :
    T^[k] n < n := certificado_descenso certificado_bajo hinicio hmax hk hr hq

theorem descenso_alto {n k : ℕ} (hinicio : 4912741 ≤ n) (hmax : n ≤ 294539509)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 19) (hq : 190537 ≤ S k n) :
    T^[k] n < n := certificado_descenso certificado_alto hinicio hmax hk hr hq

end OcelotasDiecinuevePrefijos

#print axioms OcelotasDiecinuevePrefijos.certificado_bajo
#print axioms OcelotasDiecinuevePrefijos.certificado_alto
#print axioms OcelotasDiecinuevePrefijos.descenso_bajo
#print axioms OcelotasDiecinuevePrefijos.descenso_alto
