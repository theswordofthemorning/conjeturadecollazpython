import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_252_h1_h1_h0_h0_h1 : comprobar 341045747 190537 22 4991103 131072 4782969 182131172 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_252_h1_h1_h0_h1 : comprobar 341045747 190537 22 4958335 65536 531441 40207873 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_252_h1_h1_h1 : comprobar 341045747 190537 22 4941951 32768 177147 26716675 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_253_h0_h0 : comprobar 341045747 190537 22 4915327 16384 19683 5905054 9 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_253_h0_h1_h0_h0 : comprobar 341045747 190537 22 4923519 65536 531441 39925547 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_253_h0_h1_h0_h1 : comprobar 341045747 190537 22 4956287 65536 177147 13397089 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_253_h0_h1_h1 : comprobar 341045747 190537 22 4939903 32768 59049 8901868 10 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_253_h1 : comprobar 341045747 190537 22 4919423 8192 6561 3939983 8 2 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_255_h0 : comprobar 341045747 190537 22 4914303 8192 59049 35422942 10 3 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_255_h1_h0 : comprobar 341045747 190537 22 4918399 16384 177147 53178700 11 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_255_h1_h1_h0_h0 : comprobar 341045747 190537 22 4926591 65536 1594323 119851366 13 3 false 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_252_h1_h1_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_252_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_252_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_253_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_253_h0_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_253_h0_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_253_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_253_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_255_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_255_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_255_h1_h1_h0_h0
