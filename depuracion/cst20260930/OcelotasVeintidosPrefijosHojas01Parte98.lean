import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_284_h1_h0_h1_h1 : comprobar 341045747 190537 22 4968703 65536 177147 13430650 11 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_284_h1_h1 : comprobar 341045747 190537 22 4927743 16384 19683 5919970 9 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_286_h0_h0_h0_h0 : comprobar 341045747 190537 22 4914431 65536 531441 39851848 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_286_h0_h0_h0_h1_h0 : comprobar 341045747 190537 22 4947199 131072 1594323 60176353 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_286_h0_h0_h0_h1_h1 : comprobar 341045747 190537 22 5012735 131072 4782969 182920544 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_286_h0_h0_h1_h0 : comprobar 341045747 190537 22 4930815 65536 177147 13328236 11 2 false 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_284_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_284_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_286_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_286_h0_h0_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_286_h0_h0_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_286_h0_h0_h1_h0
