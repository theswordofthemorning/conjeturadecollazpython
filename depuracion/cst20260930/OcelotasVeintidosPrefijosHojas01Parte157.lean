import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_301_h0_h0_h1_h0_h0_h0_h0_h0 : comprobar 341045747 190537 22 4931071 1048576 387420489 1821897845 18 2 true 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h0_h0_h1_h0_h0_h0_h0_h1 : comprobar 341045747 190537 22 5455359 1048576 129140163 671869363 17 2 false 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h0_h0_h1_h0_h0_h0_h1 : comprobar 341045747 190537 22 5193215 524288 43046721 426389548 16 2 false 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h0_h0_h1_h0_h0_h1_h0 : comprobar 341045747 190537 22 5062143 524288 43046721 415627868 16 3 true 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_301_h0_h0_h1_h0_h0_h1_h1 : comprobar 341045747 190537 22 5324287 524288 14348907 145717076 15 2 false 109 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h0_h1_h0_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h0_h1_h0_h0_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h0_h1_h0_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h0_h1_h0_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_301_h0_h0_h1_h0_h0_h1_h1
