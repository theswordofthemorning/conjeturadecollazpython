import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_524 : comprobar 341045747 190537 22 4913179 4096 6561 7869965 8 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_525 : comprobar 341045747 190537 22 4915227 4096 19683 23619737 9 4 true 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_527 : comprobar 341045747 190537 22 4914203 4096 19683 23614816 9 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_528_h0_h0 : comprobar 341045747 190537 22 4916251 16384 177147 53155480 11 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_528_h0_h1_h0_h0 : comprobar 341045747 190537 22 4924443 65536 1594323 119799121 13 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_528_h0_h1_h0_h1_h0 : comprobar 341045747 190537 22 4957211 131072 4782969 180894424 14 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_528_h0_h1_h0_h1_h1_h0 : comprobar 341045747 190537 22 5022747 262144 14348907 274928863 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_528_h0_h1_h0_h1_h1_h1 : comprobar 341045747 190537 22 5153819 262144 43046721 846309950 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_528_h0_h1_h1 : comprobar 341045747 190537 22 4940827 32768 531441 80131801 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_528_h1 : comprobar 341045747 190537 22 4920347 8192 59049 35466511 10 3 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_531 : comprobar 341045747 190537 22 4913691 4096 2187 2623595 7 2 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_532_h0 : comprobar 341045747 190537 22 4915739 8192 6561 3937033 8 3 false 115 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_524
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_525
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_527
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_528_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_528_h0_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_528_h0_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_528_h0_h1_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_528_h0_h1_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_528_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_528_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_531
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_532_h0
