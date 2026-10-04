import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_280_h1_h1_h1_h1 : comprobar 341045747 190537 22 4977407 65536 1594323 121087588 13 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_283_h0_h0_h0 : comprobar 341045747 190537 22 4913407 32768 59049 8854121 10 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_283_h0_h0_h1_h0 : comprobar 341045747 190537 22 4929791 65536 531441 39976406 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_283_h0_h0_h1_h1 : comprobar 341045747 190537 22 4962559 65536 177147 13414042 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_283_h0_h1_h0_h0 : comprobar 341045747 190537 22 4921599 65536 177147 13303325 11 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_283_h0_h1_h0_h1 : comprobar 341045747 190537 22 4954367 65536 531441 40175696 12 3 true 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_280_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_283_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_283_h0_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_283_h0_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_283_h0_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_283_h0_h1_h0_h1
