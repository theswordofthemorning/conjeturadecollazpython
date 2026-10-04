import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_23_h1_h0_h1 : comprobar 341045747 190537 22 4934759 32768 531441 80033386 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_23_h1_h1 : comprobar 341045747 190537 22 4926567 16384 177147 53267017 11 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_24 : comprobar 341045747 190537 22 4916327 4096 19683 23625022 9 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_28_h0_h0_h0 : comprobar 341045747 190537 22 4912999 32768 59049 8853386 10 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_28_h0_h0_h1_h0 : comprobar 341045747 190537 22 4929383 65536 177147 13324366 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_28_h0_h0_h1_h1 : comprobar 341045747 190537 22 4962151 65536 531441 40238819 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_28_h0_h1_h0 : comprobar 341045747 190537 22 4921191 32768 177147 26604445 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_28_h0_h1_h1_h0 : comprobar 341045747 190537 22 4937575 65536 531441 40039528 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_28_h0_h1_h1_h1_h0 : comprobar 341045747 190537 22 4970343 131072 1594323 60457873 13 3 false 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_23_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_23_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_24
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_28_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_28_h0_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_28_h0_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_28_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_28_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_28_h0_h1_h1_h1_h0
