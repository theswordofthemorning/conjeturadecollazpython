import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_463 : comprobar 341045747 190537 22 4913403 4096 19683 23610973 9 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_464_h0 : comprobar 341045747 190537 22 4915451 8192 59049 35431222 10 3 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_464_h1_h0 : comprobar 341045747 190537 22 4919547 16384 177147 53191120 11 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_464_h1_h1_h0_h0 : comprobar 341045747 190537 22 4927739 65536 1594323 119879311 13 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_464_h1_h1_h0_h1_h0 : comprobar 341045747 190537 22 4960507 131072 4782969 181014709 14 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_464_h1_h1_h0_h1_h1_h0 : comprobar 341045747 190537 22 5026043 262144 43046721 825327872 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_464_h1_h1_h0_h1_h1_h1 : comprobar 341045747 190537 22 5157115 262144 14348907 282283744 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_464_h1_h1_h1 : comprobar 341045747 190537 22 4944123 32768 531441 80185261 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_466 : comprobar 341045747 190537 22 4914427 4096 19683 23615894 9 4 true 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_467 : comprobar 341045747 190537 22 4916475 4096 6561 7875245 8 3 false 116 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_463
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_464_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_464_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_464_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_464_h1_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_464_h1_h1_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_464_h1_h1_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_464_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_466
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_467
