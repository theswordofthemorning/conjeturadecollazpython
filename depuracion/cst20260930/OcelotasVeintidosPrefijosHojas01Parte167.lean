import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_323_h0_h1_h1_h0 : comprobar 341045747 190537 22 4937663 65536 531441 40040243 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_323_h0_h1_h1_h1 : comprobar 341045747 190537 22 4970431 65536 177147 13435321 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_323_h1 : comprobar 341045747 190537 22 4917183 8192 6561 3938189 8 2 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_324_h0_h0 : comprobar 341045747 190537 22 4915135 16384 59049 17714470 10 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_324_h0_h1_h0 : comprobar 341045747 190537 22 4923327 32768 177147 26615992 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_324_h0_h1_h1_h0_h0 : comprobar 341045747 190537 22 4939711 131072 1594323 60085273 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_324_h0_h1_h1_h0_h1 : comprobar 341045747 190537 22 5005247 131072 4782969 182647304 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_324_h0_h1_h1_h1 : comprobar 341045747 190537 22 4972479 65536 531441 40322569 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_324_h1 : comprobar 341045747 190537 22 4919231 8192 19683 11819488 9 3 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_326 : comprobar 341045747 190537 22 4914111 4096 19683 23614372 9 3 false 116 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_323_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_323_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_323_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_324_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_324_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_324_h0_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_324_h0_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_324_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_324_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_326
