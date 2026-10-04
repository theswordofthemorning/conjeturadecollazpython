import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_354_h1_h0_h1_h0 : comprobar 341045747 190537 22 4933695 65536 177147 13336022 11 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_354_h1_h0_h1_h1 : comprobar 341045747 190537 22 4966463 65536 531441 40273787 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_354_h1_h1_h0 : comprobar 341045747 190537 22 4925503 32768 59049 8875919 10 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_354_h1_h1_h1_h0 : comprobar 341045747 190537 22 4941887 65536 531441 40074497 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_354_h1_h1_h1_h1 : comprobar 341045747 190537 22 4974655 65536 177147 13446739 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_355_h0_h0_h0_h0 : comprobar 341045747 190537 22 4915263 65536 177147 13286200 11 3 false 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_354_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_354_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_354_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_354_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_354_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_355_h0_h0_h0_h0
