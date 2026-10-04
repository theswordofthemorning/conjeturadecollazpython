import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_163_h0_h1 : comprobar 341045747 190537 22 4923631 16384 19683 5915030 9 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_163_h1_h0 : comprobar 341045747 190537 22 4919535 16384 59049 17730328 10 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_163_h1_h1_h0 : comprobar 341045747 190537 22 4927727 32768 177147 26639779 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_163_h1_h1_h1_h0 : comprobar 341045747 190537 22 4944111 65536 531441 40092529 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_163_h1_h1_h1_h1_h0 : comprobar 341045747 190537 22 4976879 131072 4782969 181612124 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_163_h1_h1_h1_h1_h1 : comprobar 341045747 190537 22 5042415 131072 1594323 61334536 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_165_h0_h0_h0_h0 : comprobar 341045747 190537 22 4914415 65536 531441 39851720 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_165_h0_h0_h0_h1 : comprobar 341045747 190537 22 4947183 65536 177147 13372480 11 3 false 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_163_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_163_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_163_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_163_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_163_h1_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_163_h1_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_165_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_165_h0_h0_h0_h1
