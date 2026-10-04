import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_166_h0_h1_h0_h0 : comprobar 341045747 190537 22 4924655 65536 531441 39934757 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_166_h0_h1_h0_h1 : comprobar 341045747 190537 22 4957423 65536 177147 13400159 11 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_166_h0_h1_h1_h0 : comprobar 341045747 190537 22 4941039 65536 531441 40067617 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_166_h0_h1_h1_h1_h0 : comprobar 341045747 190537 22 4973807 131072 4782969 181500020 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_166_h0_h1_h1_h1_h1 : comprobar 341045747 190537 22 5039343 131072 1594323 61297168 13 3 false 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_166_h0_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_166_h0_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_166_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_166_h0_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_166_h0_h1_h1_h1_h1
