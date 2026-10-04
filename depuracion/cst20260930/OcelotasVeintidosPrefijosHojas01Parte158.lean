import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_301_h0_h0_h1_h0_h1_h0 : comprobar 341045747 190537 22 4996607 262144 4782969 91166006 14 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h0_h0_h1_h0_h1_h1 : comprobar 341045747 190537 22 5127679 262144 14348907 280672472 15 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h0_h0_h1_h1_h0 : comprobar 341045747 190537 22 4963839 131072 4782969 181136270 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h0_h0_h1_h1_h1_h0 : comprobar 341045747 190537 22 5029375 262144 1594323 30587959 13 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h0_h0_h1_h1_h1_h1 : comprobar 341045747 190537 22 5160447 262144 4782969 94155362 14 3 true 110 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h0_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h0_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h0_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h0_h1_h1_h1_h1
