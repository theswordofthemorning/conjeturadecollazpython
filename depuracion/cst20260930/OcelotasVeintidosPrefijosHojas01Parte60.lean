import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_220_h1_h0_h1_h1 : comprobar 341045747 190537 22 4969167 65536 531441 40295717 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_220_h1_h1 : comprobar 341045747 190537 22 4928207 16384 19683 5920528 9 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_223_h0_h0 : comprobar 341045747 190537 22 4913359 16384 59049 17708071 10 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_223_h0_h1_h0_h0_h0 : comprobar 341045747 190537 22 4921551 131072 1594323 59864386 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_223_h0_h1_h0_h0_h1 : comprobar 341045747 190537 22 4987087 131072 4782969 181984643 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_223_h0_h1_h0_h1 : comprobar 341045747 190537 22 4954319 65536 531441 40175311 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_223_h0_h1_h1 : comprobar 341045747 190537 22 4937935 32768 177147 26694967 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_223_h1 : comprobar 341045747 190537 22 4917455 8192 19683 11815222 9 3 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_224 : comprobar 341045747 190537 22 4915407 4096 6561 7873534 8 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_226_h0 : comprobar 341045747 190537 22 4914383 8192 6561 3935947 8 3 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_226_h1_h0_h0_h0 : comprobar 341045747 190537 22 4918479 65536 177147 13294894 11 3 false 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_220_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_220_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_223_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_223_h0_h1_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_223_h0_h1_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_223_h0_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_223_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_223_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_224
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_226_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_226_h1_h0_h0_h0
