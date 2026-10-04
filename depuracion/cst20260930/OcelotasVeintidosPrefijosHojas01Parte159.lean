import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_301_h0_h1_h0_h0 : comprobar 341045747 190537 22 4922879 65536 531441 39920354 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h0_h1_h0_h1 : comprobar 341045747 190537 22 4955647 65536 177147 13395358 11 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h0_h1_h1_h0 : comprobar 341045747 190537 22 4939263 65536 531441 40053214 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h0_h1_h1_h1_h0 : comprobar 341045747 190537 22 4972031 131072 1594323 60478402 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h0_h1_h1_h1_h1 : comprobar 341045747 190537 22 5037567 131072 4782969 183826691 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h1_h0_h0_h0 : comprobar 341045747 190537 22 4918783 65536 177147 13295713 11 3 false 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h1_h0_h0_h0
