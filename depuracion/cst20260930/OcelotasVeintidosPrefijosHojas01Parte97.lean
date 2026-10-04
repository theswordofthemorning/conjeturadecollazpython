import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_284_h1_h0_h0 : comprobar 341045747 190537 22 4919551 32768 59049 8865193 10 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_284_h1_h0_h1_h0_h0 : comprobar 341045747 190537 22 4935935 131072 531441 20013115 12 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_284_h1_h0_h1_h0_h1_h0_h0_h0 : comprobar 341045747 190537 22 5001471 1048576 14348907 68441071 15 2 false 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_284_h1_h0_h1_h0_h1_h0_h0_h1 : comprobar 341045747 190537 22 5525759 1048576 43046721 226846574 16 2 true 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_284_h1_h0_h1_h0_h1_h0_h1 : comprobar 341045747 190537 22 5263615 524288 4782969 48018865 14 2 false 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_284_h1_h0_h1_h0_h1_h1 : comprobar 341045747 190537 22 5132543 262144 1594323 31215415 13 2 false 110 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_284_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_284_h1_h0_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_284_h1_h0_h1_h0_h1_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_284_h1_h0_h1_h0_h1_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_284_h1_h0_h1_h0_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_284_h1_h0_h1_h0_h1_h1
