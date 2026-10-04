import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_510_h0_h0_h0_h1 : comprobar 341045747 190537 22 4947739 65536 1594323 120365851 13 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_510_h0_h0_h1 : comprobar 341045747 190537 22 4931355 32768 531441 79978180 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_510_h0_h1 : comprobar 341045747 190537 22 4923163 16384 177147 53230213 11 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_510_h1_h0_h0 : comprobar 341045747 190537 22 4919067 32768 59049 8864321 10 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_510_h1_h0_h1_h0 : comprobar 341045747 190537 22 4935451 65536 531441 40022306 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_510_h1_h0_h1_h1 : comprobar 341045747 190537 22 4968219 65536 177147 13429342 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_510_h1_h1_h0 : comprobar 341045747 190537 22 4927259 32768 177147 26637250 11 3 false 113 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_510_h0_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_510_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_510_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_510_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_510_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_510_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_510_h1_h1_h0
