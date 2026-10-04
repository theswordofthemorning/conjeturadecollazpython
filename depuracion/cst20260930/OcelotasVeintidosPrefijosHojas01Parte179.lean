import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_342_h1_h1_h0_h1_h0 : comprobar 341045747 190537 22 4959039 131072 4782969 180961127 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_342_h1_h1_h0_h1_h1 : comprobar 341045747 190537 22 5024575 131072 1594323 61117537 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_342_h1_h1_h1 : comprobar 341045747 190537 22 4942655 32768 177147 26720482 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_343 : comprobar 341045747 190537 22 4916031 4096 6561 7874533 8 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_346_h0_h0 : comprobar 341045747 190537 22 4913471 16384 59049 17708473 10 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_346_h0_h1_h0_h0 : comprobar 341045747 190537 22 4921663 65536 531441 39910495 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_346_h0_h1_h0_h1_h0 : comprobar 341045747 190537 22 4954431 131072 4782969 180792971 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_346_h0_h1_h0_h1_h1 : comprobar 341045747 190537 22 5019967 131072 1594323 61061485 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_346_h0_h1_h1 : comprobar 341045747 190537 22 4938047 32768 177147 26695570 11 3 false 113 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_342_h1_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_342_h1_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_342_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_343
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_346_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_346_h0_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_346_h0_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_346_h0_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_346_h0_h1_h1
