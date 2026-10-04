import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_283_h0_h1_h1_h0_h1_h1 : comprobar 341045747 190537 22 5134591 262144 1594323 31227869 13 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_283_h0_h1_h1_h1_h0 : comprobar 341045747 190537 22 4970751 131072 531441 20154278 12 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_283_h0_h1_h1_h1_h1 : comprobar 341045747 190537 22 5036287 131072 1594323 61259996 13 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_283_h1_h0 : comprobar 341045747 190537 22 4917503 16384 19683 5907668 9 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_283_h1_h1_h0_h0 : comprobar 341045747 190537 22 4925695 65536 177147 13314397 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_283_h1_h1_h0_h1 : comprobar 341045747 190537 22 4958463 65536 531441 40208912 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_283_h1_h1_h1 : comprobar 341045747 190537 22 4942079 32768 59049 8905789 10 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_284_h0 : comprobar 341045747 190537 22 4915455 8192 6561 3936805 8 1 false 115 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_283_h0_h1_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_283_h0_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_283_h0_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_283_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_283_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_283_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_283_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_284_h0
