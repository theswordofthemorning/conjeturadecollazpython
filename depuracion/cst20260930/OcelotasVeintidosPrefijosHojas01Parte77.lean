import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_263_h1_h0_h1_h0_h0_h1_h1_h0 : comprobar 341045747 190537 22 5327743 1048576 387420489 1968457463 18 2 true 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_263_h1_h0_h1_h0_h0_h1_h1_h1 : comprobar 341045747 190537 22 5852031 1048576 129140163 720722569 17 2 false 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_263_h1_h0_h1_h0_h1_h0 : comprobar 341045747 190537 22 5000063 262144 14348907 273687194 15 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_263_h1_h0_h1_h0_h1_h1 : comprobar 341045747 190537 22 5131135 262144 4782969 93620549 14 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_263_h1_h0_h1_h1_h0 : comprobar 341045747 190537 22 4967295 131072 4782969 181262387 14 3 true 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_263_h1_h0_h1_h0_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_263_h1_h0_h1_h0_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_263_h1_h0_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_263_h1_h0_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_263_h1_h0_h1_h1_h0
