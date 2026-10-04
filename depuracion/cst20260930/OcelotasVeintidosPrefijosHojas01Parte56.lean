import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_217_h0_h1_h0_h1_h0 : comprobar 341045747 190537 22 4955855 131072 1594323 60281648 13 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_217_h0_h1_h0_h1_h1 : comprobar 341045747 190537 22 5021391 131072 531441 20359603 12 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_217_h0_h1_h1_h0_h0_h0 : comprobar 341045747 190537 22 4939471 262144 4782969 90123536 14 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_217_h0_h1_h1_h0_h0_h1 : comprobar 341045747 190537 22 5070543 262144 14348907 277545062 15 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_217_h0_h1_h1_h0_h1_h0_h0 : comprobar 341045747 190537 22 5005007 524288 43046721 410936753 16 3 true 109 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_217_h0_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_217_h0_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_217_h0_h1_h1_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_217_h0_h1_h1_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_217_h0_h1_h1_h0_h1_h0_h0
