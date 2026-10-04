import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_301_h1_h0_h0_h1 : comprobar 341045747 190537 22 4951551 65536 531441 40152860 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h1_h0_h1 : comprobar 341045747 190537 22 4935167 32768 59049 8893333 10 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h1_h1_h0_h0 : comprobar 341045747 190537 22 4926975 65536 531441 39953569 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h1_h1_h0_h1_h0 : comprobar 341045747 190537 22 4959743 131072 4782969 180986804 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h1_h1_h0_h1_h1 : comprobar 341045747 190537 22 5025279 131072 1594323 61126096 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h1_h1_h1 : comprobar 341045747 190537 22 4943359 32768 177147 26724286 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_302_h0_h0_h0 : comprobar 341045747 190537 22 4916735 32768 59049 8860118 10 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_302_h0_h0_h1_h0 : comprobar 341045747 190537 22 4933119 65536 177147 13334464 11 3 false 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h1_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h1_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h1_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_302_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_302_h0_h0_h1_h0
