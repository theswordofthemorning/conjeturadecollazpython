import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_331_h0_h1_h0_h1 : comprobar 341045747 190537 22 4956607 65536 531441 40193860 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_331_h0_h1_h1 : comprobar 341045747 190537 22 4940223 32768 177147 26707333 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_331_h1_h0 : comprobar 341045747 190537 22 4919743 16384 19683 5910359 9 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_331_h1_h1_h0 : comprobar 341045747 190537 22 4927935 32768 59049 8880301 10 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_331_h1_h1_h1_h0 : comprobar 341045747 190537 22 4944319 65536 531441 40094216 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_331_h1_h1_h1_h1 : comprobar 341045747 190537 22 4977087 65536 177147 13453312 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_333_h0_h0 : comprobar 341045747 190537 22 4914623 16384 177147 53137873 11 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_333_h0_h1_h0 : comprobar 341045747 190537 22 4922815 32768 531441 79839670 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_333_h0_h1_h1_h0 : comprobar 341045747 190537 22 4939199 65536 1594323 120158086 13 3 false 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_331_h0_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_331_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_331_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_331_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_331_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_331_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_333_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_333_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_333_h0_h1_h1_h0
