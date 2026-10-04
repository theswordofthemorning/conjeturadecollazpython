import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_291_h0_h1_h1_h1_h1_h0_h1 : comprobar 341045747 190537 22 5298175 524288 14348907 145002433 15 2 false 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_291_h0_h1_h1_h1_h1_h1 : comprobar 341045747 190537 22 5167103 262144 4782969 94276804 14 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_291_h1_h0_h0_h0_h0 : comprobar 341045747 190537 22 4917247 131072 1594323 59812024 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_291_h1_h0_h0_h0_h1 : comprobar 341045747 190537 22 4982783 131072 4782969 181827557 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_291_h1_h0_h0_h1_h0 : comprobar 341045747 190537 22 4950015 131072 1594323 60210605 13 3 true 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_291_h0_h1_h1_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_291_h0_h1_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_291_h1_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_291_h1_h0_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_291_h1_h0_h0_h1_h0
