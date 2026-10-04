import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_509_h1_h0_h1_h1_h0_h0_h0 : comprobar 341045747 190537 22 4966171 524288 43046721 407748107 16 2 false 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_509_h1_h0_h1_h1_h0_h0_h1 : comprobar 341045747 190537 22 5228315 524288 129140163 1287814403 17 3 true 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_509_h1_h0_h1_h1_h0_h1_h0 : comprobar 341045747 190537 22 5097243 524288 129140163 1255529362 17 2 false 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_509_h1_h0_h1_h1_h0_h1_h1_h0 : comprobar 341045747 190537 22 5359387 1048576 1162261467 5940447497 19 2 true 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_509_h1_h0_h1_h1_h0_h1_h1_h1 : comprobar 341045747 190537 22 5883675 1048576 387420489 2173859410 18 2 false 108 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_509_h1_h0_h1_h1_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_509_h1_h0_h1_h1_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_509_h1_h0_h1_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_509_h1_h0_h1_h1_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_509_h1_h0_h1_h1_h0_h1_h1_h1
