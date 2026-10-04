import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_299_h0_h1_h0_h1_h0_h1 : comprobar 341045747 190537 22 5087743 262144 43046721 835459514 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_299_h0_h1_h0_h1_h1 : comprobar 341045747 190537 22 5022207 131072 4782969 183266185 14 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_299_h0_h1_h1 : comprobar 341045747 190537 22 4940287 32768 531441 80123035 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_299_h1_h0_h0_h0_h0 : comprobar 341045747 190537 22 4919807 131072 1594323 59843164 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_299_h1_h0_h0_h0_h1 : comprobar 341045747 190537 22 4985343 131072 4782969 181920977 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_299_h1_h0_h0_h1 : comprobar 341045747 190537 22 4952575 65536 531441 40161163 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_299_h1_h0_h1 : comprobar 341045747 190537 22 4936191 32768 177147 26685535 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_299_h1_h1_h0 : comprobar 341045747 190537 22 4927999 32768 59049 8880416 10 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_299_h1_h1_h1_h0 : comprobar 341045747 190537 22 4944383 65536 177147 13364911 11 3 false 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_299_h0_h1_h0_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_299_h0_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_299_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_299_h1_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_299_h1_h0_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_299_h1_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_299_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_299_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_299_h1_h1_h1_h0
