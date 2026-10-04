import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_16_h0_h0_h1_h0 : comprobar 341045747 190537 22 4930151 65536 531441 39979331 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_16_h0_h0_h1_h1 : comprobar 341045747 190537 22 4962919 65536 177147 13415017 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_16_h0_h1 : comprobar 341045747 190537 22 4921959 16384 19683 5913022 9 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_16_h1 : comprobar 341045747 190537 22 4917863 8192 6561 3938734 8 3 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_17 : comprobar 341045747 190537 22 4915815 4096 2187 2624729 7 2 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_20 : comprobar 341045747 190537 22 4913255 4096 19683 23610260 9 4 true 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_21 : comprobar 341045747 190537 22 4915303 4096 6561 7873367 8 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_23_h0 : comprobar 341045747 190537 22 4914279 8192 59049 35422771 10 3 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_23_h1_h0_h0_h0_h0 : comprobar 341045747 190537 22 4918375 131072 4782969 179477248 14 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_23_h1_h0_h0_h0_h1_h0 : comprobar 341045747 190537 22 4983911 262144 14348907 272803099 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_23_h1_h0_h0_h0_h1_h1 : comprobar 341045747 190537 22 5114983 262144 43046721 839932658 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_23_h1_h0_h0_h1 : comprobar 341045747 190537 22 4951143 65536 1594323 120448660 13 3 false 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_16_h0_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_16_h0_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_16_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_16_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_17
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_20
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_21
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_23_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_23_h1_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_23_h1_h0_h0_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_23_h1_h0_h0_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_23_h1_h0_h0_h1
