import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_287_h0_h0_h0_h1_h1 : comprobar 341045747 190537 22 5014783 131072 4782969 182995280 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_287_h0_h0_h1 : comprobar 341045747 190537 22 4932863 32768 177147 26667544 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_287_h0_h1 : comprobar 341045747 190537 22 4924671 16384 59049 17748838 10 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_287_h1_h0_h0 : comprobar 341045747 190537 22 4920575 32768 59049 8867038 10 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_287_h1_h0_h1_h0 : comprobar 341045747 190537 22 4936959 65536 177147 13344844 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_287_h1_h0_h1_h1 : comprobar 341045747 190537 22 4969727 65536 531441 40300253 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_287_h1_h1 : comprobar 341045747 190537 22 4928767 16384 19683 5921200 9 2 false 114 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_287_h0_h0_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_287_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_287_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_287_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_287_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_287_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_287_h1_h1
