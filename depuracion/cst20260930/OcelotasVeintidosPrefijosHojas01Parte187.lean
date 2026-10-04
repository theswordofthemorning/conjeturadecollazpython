import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_354_h1_h0_h0_h1_h0_h1 : comprobar 341045747 190537 22 5081151 262144 4782969 92708570 14 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_354_h1_h0_h0_h1_h1_h0_h0_h0 : comprobar 341045747 190537 22 5015615 1048576 129140163 617711588 17 2 true 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_354_h1_h0_h0_h1_h1_h0_h0_h1 : comprobar 341045747 190537 22 5539903 1048576 43046721 227427223 16 2 false 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_354_h1_h0_h0_h1_h1_h0_h1 : comprobar 341045747 190537 22 5277759 524288 14348907 144443695 15 2 false 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_354_h1_h0_h0_h1_h1_h1 : comprobar 341045747 190537 22 5146687 262144 4782969 93904312 14 2 false 110 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_354_h1_h0_h0_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_354_h1_h0_h0_h1_h1_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_354_h1_h0_h0_h1_h1_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_354_h1_h0_h0_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_354_h1_h0_h0_h1_h1_h1
