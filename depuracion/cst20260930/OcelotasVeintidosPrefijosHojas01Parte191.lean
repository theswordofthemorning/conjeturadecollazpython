import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_370_h1_h1_h0_h0 : comprobar 341045747 190537 22 4928159 65536 531441 39963172 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_370_h1_h1_h0_h1_h0 : comprobar 341045747 190537 22 4960927 131072 1594323 60343339 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_370_h1_h1_h0_h1_h1 : comprobar 341045747 190537 22 5026463 131072 4782969 183421502 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_370_h1_h1_h1 : comprobar 341045747 190537 22 4944543 32768 177147 26730688 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_373_h0_h0_h0_h0_h0_h0_h0 : comprobar 341045747 190537 22 4913311 524288 129140163 1210224017 17 3 true 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_373_h0_h0_h0_h0_h0_h0_h1 : comprobar 341045747 190537 22 5175455 524288 43046721 424931366 16 2 false 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_373_h0_h0_h0_h0_h0_h1_h0_h0 : comprobar 341045747 190537 22 5044383 1048576 1162261467 5591290760 19 2 true 108 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_370_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_370_h1_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_370_h1_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_370_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_373_h0_h0_h0_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_373_h0_h0_h0_h0_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_373_h0_h0_h0_h0_h0_h1_h0_h0
