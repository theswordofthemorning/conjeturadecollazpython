import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_400_h0_h1_h0 : comprobar 341045747 190537 22 4922143 32768 177147 26609593 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_400_h0_h1_h1_h0 : comprobar 341045747 190537 22 4938527 65536 531441 40047250 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_400_h0_h1_h1_h1_h0 : comprobar 341045747 190537 22 4971295 131072 1594323 60469456 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_400_h0_h1_h1_h1_h1 : comprobar 341045747 190537 22 5036831 131072 4782969 183799853 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_400_h1 : comprobar 341045747 190537 22 4918047 8192 19683 11816644 9 3 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_401 : comprobar 341045747 190537 22 4915999 4096 6561 7874482 8 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_402 : comprobar 341045747 190537 22 4913439 1024 729 3497947 6 2 false 118 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_406 : comprobar 341045747 190537 22 4913183 4096 6561 7869971 8 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_407 : comprobar 341045747 190537 22 4915231 4096 19683 23619755 9 4 true 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_409 : comprobar 341045747 190537 22 4914207 4096 19683 23614834 9 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_410_h0_h0_h0 : comprobar 341045747 190537 22 4916255 32768 531441 79733281 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_410_h0_h0_h1_h0_h0 : comprobar 341045747 190537 22 4932639 131072 4782969 179997754 14 3 false 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_400_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_400_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_400_h0_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_400_h0_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_400_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_401
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_402
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_406
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_407
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_409
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_410_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_410_h0_h0_h1_h0_h0
