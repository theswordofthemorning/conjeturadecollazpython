import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_302_h0_h1_h1_h1_h0_h0 : comprobar 341045747 190537 22 4974079 262144 1594323 30251657 13 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_302_h0_h1_h1_h1_h0_h1 : comprobar 341045747 190537 22 5105151 262144 4782969 93146456 14 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_302_h0_h1_h1_h1_h1_h0_h0_h0 : comprobar 341045747 190537 22 5039615 1048576 43046721 206889106 16 2 false 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_302_h0_h1_h1_h1_h1_h0_h0_h1 : comprobar 341045747 190537 22 5563903 1048576 129140163 685237400 17 2 true 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_302_h0_h1_h1_h1_h1_h0_h1 : comprobar 341045747 190537 22 5301759 524288 14348907 145100524 15 2 false 109 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_302_h0_h1_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_302_h0_h1_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_302_h0_h1_h1_h1_h1_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_302_h0_h1_h1_h1_h1_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_302_h0_h1_h1_h1_h1_h0_h1
