import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_298_h1_h1_h1_h1_h0_h1 : comprobar 341045747 190537 22 5106175 262144 43046721 838486232 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_298_h1_h1_h1_h1_h1_h0 : comprobar 341045747 190537 22 5040639 262144 14348907 275908184 15 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_298_h1_h1_h1_h1_h1_h1 : comprobar 341045747 190537 22 5171711 262144 4782969 94360879 14 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_299_h0_h0 : comprobar 341045747 190537 22 4915711 16384 177147 53149636 11 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_299_h0_h1_h0_h0 : comprobar 341045747 190537 22 4923903 65536 1594323 119785972 13 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_299_h0_h1_h0_h1_h0_h0 : comprobar 341045747 190537 22 4956671 262144 14348907 271312051 15 3 false 110 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_298_h1_h1_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_298_h1_h1_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_298_h1_h1_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_299_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_299_h0_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_299_h0_h1_h0_h1_h0_h0
