import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_165_h1_h1_h0_h1_h1_h1 : comprobar 341045747 190537 22 5156079 262144 43046721 846681011 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_165_h1_h1_h1 : comprobar 341045747 190537 22 4943087 32768 531441 80168449 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_166_h0_h0_h0 : comprobar 341045747 190537 22 4916463 32768 531441 79736653 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_166_h0_h0_h1_h0_h0 : comprobar 341045747 190537 22 4932847 131072 4782969 180005341 14 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_166_h0_h0_h1_h0_h1_h0 : comprobar 341045747 190537 22 4998383 262144 43046721 820785716 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_166_h0_h0_h1_h0_h1_h1 : comprobar 341045747 190537 22 5129455 262144 14348907 280769692 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_166_h0_h0_h1_h1 : comprobar 341045747 190537 22 4965615 65536 1594323 120800722 13 3 false 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_165_h1_h1_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_165_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_166_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_166_h0_h0_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_166_h0_h0_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_166_h0_h0_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_166_h0_h0_h1_h1
