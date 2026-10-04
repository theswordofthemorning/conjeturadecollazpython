import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_334_h0_h0_h1_h0_h1 : comprobar 341045747 190537 22 4998591 131072 4782969 182404412 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_334_h0_h0_h1_h1_h0 : comprobar 341045747 190537 22 4965823 131072 1594323 60402890 13 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_334_h0_h0_h1_h1_h1 : comprobar 341045747 190537 22 5031359 131072 531441 20400017 12 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_334_h0_h1_h0_h0_h0_h0 : comprobar 341045747 190537 22 4924863 262144 14348907 269570987 15 3 true 110 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_334_h0_h0_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_334_h0_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_334_h0_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_334_h0_h1_h0_h0_h0_h0
