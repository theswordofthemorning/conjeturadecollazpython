import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_248_h0_h1 : comprobar 341045747 190537 22 4921983 16384 19683 5913050 9 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_248_h1_h0 : comprobar 341045747 190537 22 4917887 16384 59049 17724388 10 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_248_h1_h1_h0 : comprobar 341045747 190537 22 4926079 32768 177147 26630869 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_248_h1_h1_h1_h0 : comprobar 341045747 190537 22 4942463 65536 531441 40079164 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_248_h1_h1_h1_h1_h0 : comprobar 341045747 190537 22 4975231 131072 1594323 60517327 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_248_h1_h1_h1_h1_h1 : comprobar 341045747 190537 22 5040767 131072 4782969 183943466 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_249_h0_h0_h0 : comprobar 341045747 190537 22 4915839 32768 531441 79726531 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_249_h0_h0_h1_h0_h0_h0 : comprobar 341045747 190537 22 4932223 262144 14348907 269973850 15 3 false 110 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_248_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_248_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_248_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_248_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_248_h1_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_248_h1_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_249_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_249_h0_h0_h1_h0_h0_h0
