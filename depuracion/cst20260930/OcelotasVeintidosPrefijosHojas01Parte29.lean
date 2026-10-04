import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_31_h0_h0_h0_h0 : comprobar 341045747 190537 22 4914023 65536 531441 39848543 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_31_h0_h0_h0_h1 : comprobar 341045747 190537 22 4946791 65536 177147 13371421 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_31_h0_h0_h1 : comprobar 341045747 190537 22 4930407 32768 59049 8884756 10 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_31_h0_h1 : comprobar 341045747 190537 22 4922215 16384 19683 5913329 9 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_31_h1_h0 : comprobar 341045747 190537 22 4918119 16384 59049 17725225 10 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_31_h1_h1_h0_h0 : comprobar 341045747 190537 22 4926311 65536 531441 39948187 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_31_h1_h1_h0_h1_h0 : comprobar 341045747 190537 22 4959079 131072 4782969 180962585 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_31_h1_h1_h0_h1_h1 : comprobar 341045747 190537 22 5024615 131072 1594323 61118023 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_31_h1_h1_h1 : comprobar 341045747 190537 22 4942695 32768 177147 26720698 11 3 false 113 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_31_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_31_h0_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_31_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_31_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_31_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_31_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_31_h1_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_31_h1_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_31_h1_h1_h1
