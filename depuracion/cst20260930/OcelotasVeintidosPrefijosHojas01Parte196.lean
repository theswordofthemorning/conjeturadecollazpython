import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_373_h1_h0_h0 : comprobar 341045747 190537 22 4917407 32768 531441 79751962 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_373_h1_h0_h1_h0 : comprobar 341045747 190537 22 4933791 65536 1594323 120026524 13 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_373_h1_h0_h1_h1_h0_h0 : comprobar 341045747 190537 22 4966559 262144 14348907 271853293 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_373_h1_h0_h1_h1_h0_h1 : comprobar 341045747 190537 22 5097631 262144 43046721 837083240 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_373_h1_h0_h1_h1_h1 : comprobar 341045747 190537 22 5032095 131072 4782969 183627013 14 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_373_h1_h1_h0_h0 : comprobar 341045747 190537 22 4925599 65536 177147 13314137 11 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_373_h1_h1_h0_h1 : comprobar 341045747 190537 22 4958367 65536 531441 40208132 12 3 true 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_373_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_373_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_373_h1_h0_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_373_h1_h0_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_373_h1_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_373_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_373_h1_h1_h0_h1
