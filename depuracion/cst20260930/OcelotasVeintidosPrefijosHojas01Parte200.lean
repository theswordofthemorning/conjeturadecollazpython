import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_377_h0_h0_h1_h1 : comprobar 341045747 190537 22 4965535 65536 531441 40266260 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_377_h0_h1 : comprobar 341045747 190537 22 4924575 16384 19683 5916164 9 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_377_h1_h0 : comprobar 341045747 190537 22 4920479 16384 59049 17733730 10 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_377_h1_h1_h0 : comprobar 341045747 190537 22 4928671 32768 177147 26644882 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_377_h1_h1_h1_h0_h0 : comprobar 341045747 190537 22 4945055 131072 4782969 180450827 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_377_h1_h1_h1_h0_h1 : comprobar 341045747 190537 22 5010591 131072 1594323 60947437 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_377_h1_h1_h1_h1 : comprobar 341045747 190537 22 4977823 65536 531441 40365904 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_381 : comprobar 341045747 190537 22 4913055 4096 6561 7869766 8 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_382_h0 : comprobar 341045747 190537 22 4915103 8192 19683 11809570 9 3 false 115 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_377_h0_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_377_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_377_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_377_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_377_h1_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_377_h1_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_377_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_381
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_382_h0
