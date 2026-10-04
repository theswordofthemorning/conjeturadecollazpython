import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_162_h1_h0_h0 : comprobar 341045747 190537 22 4917487 32768 531441 79753261 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_162_h1_h0_h1_h0_h0 : comprobar 341045747 190537 22 4933871 131072 4782969 180042709 14 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_162_h1_h0_h1_h0_h1_h0 : comprobar 341045747 190537 22 4999407 262144 43046721 820953872 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_162_h1_h0_h1_h0_h1_h1 : comprobar 341045747 190537 22 5130479 262144 14348907 280825744 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_162_h1_h0_h1_h1 : comprobar 341045747 190537 22 4966639 65536 1594323 120825634 13 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_162_h1_h1 : comprobar 341045747 190537 22 4925679 16384 177147 53257414 11 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_163_h0_h0_h0 : comprobar 341045747 190537 22 4915439 32768 59049 8857783 10 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_163_h0_h0_h1_h0 : comprobar 341045747 190537 22 4931823 65536 531441 39992885 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_163_h0_h0_h1_h1 : comprobar 341045747 190537 22 4964591 65536 177147 13419535 11 3 false 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_162_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_162_h1_h0_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_162_h1_h0_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_162_h1_h0_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_162_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_162_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_163_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_163_h0_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_163_h0_h0_h1_h1
