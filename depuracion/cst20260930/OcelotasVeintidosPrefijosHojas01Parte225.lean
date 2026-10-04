import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_513_h1_h0_h1 : comprobar 341045747 190537 22 4936475 32768 59049 8895691 10 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_513_h1_h1 : comprobar 341045747 190537 22 4928283 16384 19683 5920619 9 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_516_h0_h0_h0_h0 : comprobar 341045747 190537 22 4913435 65536 177147 13281259 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_516_h0_h0_h0_h1 : comprobar 341045747 190537 22 4946203 65536 531441 40109498 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_516_h0_h0_h1 : comprobar 341045747 190537 22 4929819 32768 59049 8883697 10 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_516_h0_h1 : comprobar 341045747 190537 22 4921627 16384 19683 5912623 9 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_516_h1 : comprobar 341045747 190537 22 4917531 8192 6561 3938468 8 2 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_517_h0_h0_h0_h0 : comprobar 341045747 190537 22 4915483 65536 531441 39860383 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_517_h0_h0_h0_h1_h0 : comprobar 341045747 190537 22 4948251 131072 4782969 180567467 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_517_h0_h0_h0_h1_h1 : comprobar 341045747 190537 22 5013787 131072 1594323 60986317 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_517_h0_h0_h1 : comprobar 341045747 190537 22 4931867 32768 177147 26662162 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_517_h0_h1 : comprobar 341045747 190537 22 4923675 16384 59049 17745250 10 3 false 114 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_513_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_513_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_516_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_516_h0_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_516_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_516_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_516_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_517_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_517_h0_h0_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_517_h0_h0_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_517_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_517_h0_h1
