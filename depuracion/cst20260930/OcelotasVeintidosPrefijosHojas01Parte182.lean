import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_347_h1_h0_h1_h1 : comprobar 341045747 190537 22 4968767 65536 531441 40292468 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_347_h1_h1_h0_h0_h0 : comprobar 341045747 190537 22 4927807 131072 1594323 59940476 13 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_347_h1_h1_h0_h0_h1 : comprobar 341045747 190537 22 4993343 131072 531441 20245879 12 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_347_h1_h1_h0_h1_h0 : comprobar 341045747 190537 22 4960575 131072 4782969 181017170 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_347_h1_h1_h0_h1_h1 : comprobar 341045747 190537 22 5026111 131072 1594323 61136218 13 3 false 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_347_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_347_h1_h1_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_347_h1_h1_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_347_h1_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_347_h1_h1_h0_h1_h1
