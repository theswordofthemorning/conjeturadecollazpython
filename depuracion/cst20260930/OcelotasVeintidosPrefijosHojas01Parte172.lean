import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_333_h1_h1_h0_h0 : comprobar 341045747 190537 22 4926911 65536 531441 39953051 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_333_h1_h1_h0_h1 : comprobar 341045747 190537 22 4959679 65536 177147 13406257 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_333_h1_h1_h1 : comprobar 341045747 190537 22 4943295 32768 59049 8907980 10 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_334_h0_h0_h0_h0 : comprobar 341045747 190537 22 4916671 65536 1594323 119610037 13 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_334_h0_h0_h0_h1_h0 : comprobar 341045747 190537 22 4949439 131072 4782969 180610798 14 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_334_h0_h0_h0_h1_h1_h0 : comprobar 341045747 190537 22 5014975 262144 14348907 274503424 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_334_h0_h0_h0_h1_h1_h1 : comprobar 341045747 190537 22 5146047 262144 43046721 845033633 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_334_h0_h0_h1_h0_h0 : comprobar 341045747 190537 22 4933055 131072 1594323 60004309 13 3 false 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_333_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_333_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_333_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_334_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_334_h0_h0_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_334_h0_h0_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_334_h0_h0_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_334_h0_h0_h1_h0_h0
