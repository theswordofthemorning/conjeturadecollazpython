import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_255_h1_h1_h0_h1_h0_h0 : comprobar 341045747 190537 22 4959359 262144 43046721 814377563 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_255_h1_h1_h0_h1_h0_h1 : comprobar 341045747 190537 22 5090431 262144 14348907 278633641 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_255_h1_h1_h0_h1_h1 : comprobar 341045747 190537 22 5024895 131072 4782969 183364276 14 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_255_h1_h1_h1 : comprobar 341045747 190537 22 4942975 32768 531441 80166631 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_256 : comprobar 341045747 190537 22 4916351 4096 19683 23625136 9 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_260_h0 : comprobar 341045747 190537 22 4913023 8192 19683 11804572 9 3 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_260_h1_h0_h0 : comprobar 341045747 190537 22 4917119 32768 177147 26582431 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_260_h1_h0_h1_h0 : comprobar 341045747 190537 22 4933503 65536 531441 40006507 12 3 false 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_255_h1_h1_h0_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_255_h1_h1_h0_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_255_h1_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_255_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_256
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_260_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_260_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_260_h1_h0_h1_h0
