import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_298_h1_h0_h1_h0_h1_h0 : comprobar 341045747 190537 22 4999679 262144 43046721 820998503 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_298_h1_h0_h1_h0_h1_h1 : comprobar 341045747 190537 22 5130751 262144 14348907 280840621 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_298_h1_h0_h1_h1 : comprobar 341045747 190537 22 4966911 65536 1594323 120832246 13 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_298_h1_h1_h0_h0_h0_h0 : comprobar 341045747 190537 22 4925951 262144 4782969 89876846 14 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_298_h1_h1_h0_h0_h0_h1 : comprobar 341045747 190537 22 5057023 262144 1594323 30756110 13 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_298_h1_h1_h0_h0_h1 : comprobar 341045747 190537 22 4991487 131072 4782969 182145176 14 3 true 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_298_h1_h0_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_298_h1_h0_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_298_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_298_h1_h1_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_298_h1_h1_h0_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_298_h1_h1_h0_h0_h1
