import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_559 : comprobar 341045747 190537 22 4915803 4096 19683 23622506 9 4 true 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_561 : comprobar 341045747 190537 22 4914779 4096 2187 2624176 7 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_562 : comprobar 341045747 190537 22 4916827 4096 6561 7875809 8 4 true 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_563 : comprobar 341045747 190537 22 4912755 16 9 2763425 2 1 false 124 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_564 : comprobar 341045747 190537 22 4912742 2 1 2456371 0 0 false 127 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_559
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_561
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_562
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_563
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_564
