import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_330_h0_h0_h0_h1_h0_h1 : comprobar 341045747 190537 22 5077439 262144 43046721 833767505 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_330_h0_h0_h0_h1_h1 : comprobar 341045747 190537 22 5011903 131072 4782969 182890183 14 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_330_h0_h0_h1 : comprobar 341045747 190537 22 4929983 32768 531441 79955923 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_330_h0_h1 : comprobar 341045747 190537 22 4921791 16384 177147 53215375 11 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_330_h1 : comprobar 341045747 190537 22 4917695 8192 59049 35447392 10 3 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_331_h0_h0 : comprobar 341045747 190537 22 4915647 16384 59049 17716315 10 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_331_h0_h1_h0_h0_h0 : comprobar 341045747 190537 22 4923839 131072 4782969 179676629 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_331_h0_h1_h0_h0_h1 : comprobar 341045747 190537 22 4989375 131072 1594323 60689371 13 3 false 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_330_h0_h0_h0_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_330_h0_h0_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_330_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_330_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_330_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_331_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_331_h0_h1_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_331_h0_h1_h0_h0_h1
