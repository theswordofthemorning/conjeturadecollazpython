import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_298_h1_h1_h1_h0_h1_h0_h1 : comprobar 341045747 190537 22 5270015 524288 43046721 432695216 16 2 false 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_298_h1_h1_h1_h0_h1_h1_h0_h0 : comprobar 341045747 190537 22 5138943 1048576 1162261467 5696102735 19 2 true 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_298_h1_h1_h1_h0_h1_h1_h0_h1 : comprobar 341045747 190537 22 5663231 1048576 387420489 2092411156 18 2 false 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_298_h1_h1_h1_h0_h1_h1_h1 : comprobar 341045747 190537 22 5401087 524288 129140163 1330370689 17 2 false 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_298_h1_h1_h1_h1_h0_h0 : comprobar 341045747 190537 22 4975103 262144 14348907 272320957 15 3 false 110 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_298_h1_h1_h1_h0_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_298_h1_h1_h1_h0_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_298_h1_h1_h1_h0_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_298_h1_h1_h1_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_298_h1_h1_h1_h1_h0_h0
