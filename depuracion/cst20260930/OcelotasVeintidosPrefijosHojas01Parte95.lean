import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_283_h0_h1_h1_h0_h0_h0_h0 : comprobar 341045747 190537 22 4937983 524288 14348907 135144571 15 2 false 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_283_h0_h1_h1_h0_h0_h0_h1_h0 : comprobar 341045747 190537 22 5200127 1048576 43046721 213478537 16 2 false 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_283_h0_h1_h1_h0_h0_h0_h1_h1 : comprobar 341045747 190537 22 5724415 1048576 129140163 705005693 17 2 true 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_283_h0_h1_h1_h0_h0_h1 : comprobar 341045747 190537 22 5069055 262144 4782969 92487865 14 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_283_h0_h1_h1_h0_h1_h0 : comprobar 341045747 190537 22 5003519 262144 4782969 91292123 14 3 true 110 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_283_h0_h1_h1_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_283_h0_h1_h1_h0_h0_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_283_h0_h1_h1_h0_h0_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_283_h0_h1_h1_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_283_h0_h1_h1_h0_h1_h0
