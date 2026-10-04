import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_334_h0_h1_h0_h1_h1_h0_h0 : comprobar 341045747 190537 22 5023167 524288 129140163 1237283221 17 2 false 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_334_h0_h1_h0_h1_h1_h0_h1_h0 : comprobar 341045747 190537 22 5285311 1048576 387420489 1952779954 18 2 false 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_334_h0_h1_h0_h1_h1_h0_h1_h1 : comprobar 341045747 190537 22 5809599 1048576 1162261467 6439470596 19 2 true 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_334_h0_h1_h0_h1_h1_h1_h0 : comprobar 341045747 190537 22 5154239 524288 129140163 1269568262 17 3 true 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_334_h0_h1_h0_h1_h1_h1_h1 : comprobar 341045747 190537 22 5416383 524288 43046721 444712781 16 2 false 109 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_334_h0_h1_h0_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_334_h0_h1_h0_h1_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_334_h0_h1_h0_h1_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_334_h0_h1_h0_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_334_h0_h1_h0_h1_h1_h1_h1
