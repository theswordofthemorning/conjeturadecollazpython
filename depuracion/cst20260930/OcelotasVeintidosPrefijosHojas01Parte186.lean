import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_354_h0_h0 : comprobar 341045747 190537 22 4913215 16384 19683 5902517 9 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_354_h0_h1_h0 : comprobar 341045747 190537 22 4921407 32768 59049 8868538 10 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_354_h0_h1_h1_h0 : comprobar 341045747 190537 22 4937791 65536 177147 13347094 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_354_h0_h1_h1_h1 : comprobar 341045747 190537 22 4970559 65536 531441 40307003 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_354_h1_h0_h0_h0_h0 : comprobar 341045747 190537 22 4917311 131072 531441 19937603 12 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_354_h1_h0_h0_h0_h1 : comprobar 341045747 190537 22 4982847 131072 1594323 60609971 13 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_354_h1_h0_h0_h1_h0_h0 : comprobar 341045747 190537 22 4950079 262144 1594323 30105695 13 2 false 110 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_354_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_354_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_354_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_354_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_354_h1_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_354_h1_h0_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_354_h1_h0_h0_h1_h0_h0
