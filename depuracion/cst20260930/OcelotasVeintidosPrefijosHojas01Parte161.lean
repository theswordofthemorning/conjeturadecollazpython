import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_302_h0_h0_h1_h1 : comprobar 341045747 190537 22 4965887 65536 531441 40269113 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_302_h0_h1_h0_h0 : comprobar 341045747 190537 22 4924927 65536 531441 39936962 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_302_h0_h1_h0_h1 : comprobar 341045747 190537 22 4957695 65536 177147 13400894 11 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_302_h0_h1_h1_h0_h0 : comprobar 341045747 190537 22 4941311 131072 531441 20034911 12 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_302_h0_h1_h1_h0_h1 : comprobar 341045747 190537 22 5006847 131072 1594323 60901895 13 3 true 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_302_h0_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_302_h0_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_302_h0_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_302_h0_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_302_h0_h1_h1_h0_h1
