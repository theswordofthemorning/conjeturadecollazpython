import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_302_h1_h1_h0_h0_h1_h0_h1_h0 : comprobar 341045747 190537 22 5256703 1048576 14348907 71933710 15 2 false 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_302_h1_h1_h0_h0_h1_h0_h1_h1 : comprobar 341045747 190537 22 5780991 1048576 43046721 237324491 16 2 true 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_302_h1_h1_h0_h0_h1_h1 : comprobar 341045747 190537 22 5125631 262144 1594323 31173376 13 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_302_h1_h1_h0_h1 : comprobar 341045747 190537 22 4961791 65536 177147 13411966 11 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_302_h1_h1_h1 : comprobar 341045747 190537 22 4945407 32768 59049 8911786 10 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_308 : comprobar 341045747 190537 22 4912831 4096 6561 7869407 8 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_309 : comprobar 341045747 190537 22 4914879 4096 19683 23618063 9 4 true 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_311 : comprobar 341045747 190537 22 4913855 4096 19683 23613142 9 3 false 116 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_302_h1_h1_h0_h0_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_302_h1_h1_h0_h0_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_302_h1_h1_h0_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_302_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_302_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_308
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_309
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_311
