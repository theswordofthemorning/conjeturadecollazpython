import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_295_h1_h1_h0_h0 : comprobar 341045747 190537 22 4928511 65536 177147 13322008 11 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_295_h1_h1_h0_h1 : comprobar 341045747 190537 22 4961279 65536 531441 40231745 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_295_h1_h1_h1_h0_h0 : comprobar 341045747 190537 22 4944895 131072 1594323 60148327 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_295_h1_h1_h1_h0_h1 : comprobar 341045747 190537 22 5010431 131072 4782969 182836466 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_295_h1_h1_h1_h1 : comprobar 341045747 190537 22 4977663 65536 531441 40364605 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_298_h0_h0_h0 : comprobar 341045747 190537 22 4913663 32768 531441 79691239 12 3 false 113 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_295_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_295_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_295_h1_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_295_h1_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_295_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_298_h0_h0_h0
