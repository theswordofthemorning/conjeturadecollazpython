import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_216_h0_h1_h1_h0 : comprobar 341045747 190537 22 4937423 65536 531441 40038299 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_216_h0_h1_h1_h1 : comprobar 341045747 190537 22 4970191 65536 177147 13434673 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_216_h1_h0_h0_h0_h0 : comprobar 341045747 190537 22 4916943 131072 1594323 59808334 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_216_h1_h0_h0_h0_h1 : comprobar 341045747 190537 22 4982479 131072 4782969 181816487 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_216_h1_h0_h0_h1 : comprobar 341045747 190537 22 4949711 65536 531441 40137943 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_216_h1_h0_h1 : comprobar 341045747 190537 22 4933327 32768 177147 26670055 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_216_h1_h1 : comprobar 341045747 190537 22 4925135 16384 59049 17750512 10 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_217_h0_h0_h0_h0_h0 : comprobar 341045747 190537 22 4914895 131072 1594323 59783422 13 3 false 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_216_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_216_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_216_h1_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_216_h1_h0_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_216_h1_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_216_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_216_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_217_h0_h0_h0_h0_h0
