import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_510_h1_h1_h1_h0_h0 : comprobar 341045747 190537 22 4943643 131072 4782969 180399311 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_510_h1_h1_h1_h0_h1 : comprobar 341045747 190537 22 5009179 131072 1594323 60930265 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_510_h1_h1_h1_h1 : comprobar 341045747 190537 22 4976411 65536 531441 40354456 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_512_h0_h0 : comprobar 341045747 190537 22 4913947 16384 177147 53130568 11 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_512_h0_h1_h0_h0 : comprobar 341045747 190537 22 4922139 65536 1594323 119743069 13 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_512_h0_h1_h0_h1_h0 : comprobar 341045747 190537 22 4954907 131072 4782969 180810346 14 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_512_h0_h1_h0_h1_h1_h0 : comprobar 341045747 190537 22 5020443 262144 14348907 274802746 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_512_h0_h1_h0_h1_h1_h1 : comprobar 341045747 190537 22 5151515 262144 43046721 845931599 16 3 true 110 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_510_h1_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_510_h1_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_510_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_512_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_512_h0_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_512_h0_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_512_h0_h1_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_512_h0_h1_h0_h1_h1_h1
