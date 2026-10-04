import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_373_h0_h0_h1_h0_h1_h1 : comprobar 341045747 190537 22 5126303 262144 43046721 841791473 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_373_h0_h0_h1_h1_h0_h0 : comprobar 341045747 190537 22 4962463 262144 1594323 30181010 13 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_373_h0_h0_h1_h1_h0_h1 : comprobar 341045747 190537 22 5093535 262144 4782969 92934515 14 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_373_h0_h0_h1_h1_h1 : comprobar 341045747 190537 22 5027999 131072 4782969 183477545 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_373_h0_h1_h0_h0_h0 : comprobar 341045747 190537 22 4921503 131072 531441 19954598 12 2 false 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_373_h0_h0_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_373_h0_h0_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_373_h0_h0_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_373_h0_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_373_h0_h1_h0_h0_h0
