import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_217_h0_h1_h1_h0_h1_h0_h1 : comprobar 341045747 190537 22 5267151 524288 14348907 144153371 15 2 false 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_217_h0_h1_h1_h0_h1_h1_h0 : comprobar 341045747 190537 22 5136079 524288 43046721 421698433 16 2 false 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_217_h0_h1_h1_h0_h1_h1_h1_h0 : comprobar 341045747 190537 22 5398223 1048576 387420489 1994498072 18 2 true 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_217_h0_h1_h1_h0_h1_h1_h1_h1 : comprobar 341045747 190537 22 5922511 1048576 129140163 729402772 17 2 false 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_217_h0_h1_h1_h1_h0_h0 : comprobar 341045747 190537 22 4972239 262144 1594323 30240469 13 2 false 110 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_217_h0_h1_h1_h0_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_217_h0_h1_h1_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_217_h0_h1_h1_h0_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_217_h0_h1_h1_h0_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_217_h0_h1_h1_h1_h0_h0
