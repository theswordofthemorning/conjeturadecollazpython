import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_295_h1_h0_h1_h1_h1_h0_h0_h0 : comprobar 341045747 190537 22 5035007 1048576 387420489 1860299378 18 2 true 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_295_h1_h0_h1_h1_h1_h0_h0_h1 : comprobar 341045747 190537 22 5559295 1048576 129140163 684669874 17 2 false 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_295_h1_h0_h1_h1_h1_h0_h1 : comprobar 341045747 190537 22 5297151 524288 43046721 434923222 16 2 false 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_295_h1_h0_h1_h1_h1_h1_h0 : comprobar 341045747 190537 22 5166079 524288 43046721 424161542 16 3 true 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_295_h1_h0_h1_h1_h1_h1_h1 : comprobar 341045747 190537 22 5428223 524288 14348907 148561634 15 2 false 109 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_295_h1_h0_h1_h1_h1_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_295_h1_h0_h1_h1_h1_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_295_h1_h0_h1_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_295_h1_h0_h1_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_295_h1_h0_h1_h1_h1_h1_h1
