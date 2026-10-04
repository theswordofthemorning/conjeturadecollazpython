import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_439_h1_h0_h1_h1 : comprobar 341045747 190537 22 4966879 65536 531441 40277159 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_439_h1_h1_h0_h0_h0 : comprobar 341045747 190537 22 4925919 131072 531441 19972504 12 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_439_h1_h1_h0_h0_h1 : comprobar 341045747 190537 22 4991455 131072 1594323 60714674 13 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_439_h1_h1_h0_h1_h0 : comprobar 341045747 190537 22 4958687 131072 1594323 60316093 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_439_h1_h1_h0_h1_h1 : comprobar 341045747 190537 22 5024223 131072 4782969 183339764 14 3 true 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_439_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_439_h1_h1_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_439_h1_h1_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_439_h1_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_439_h1_h1_h0_h1_h1
