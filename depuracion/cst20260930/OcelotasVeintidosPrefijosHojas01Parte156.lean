import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_299_h1_h1_h1_h1 : comprobar 341045747 190537 22 4977151 65536 531441 40360454 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h0_h0_h0_h0_h0 : comprobar 341045747 190537 22 4914687 131072 4782969 179342657 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h0_h0_h0_h0_h1 : comprobar 341045747 190537 22 4980223 131072 1594323 60578047 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h0_h0_h0_h1_h0 : comprobar 341045747 190537 22 4947455 131072 531441 20059822 12 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h0_h0_h0_h1_h1 : comprobar 341045747 190537 22 5012991 131072 1594323 60976628 13 3 true 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_299_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h0_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h0_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h0_h0_h1_h1
