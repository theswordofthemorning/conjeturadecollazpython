import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_260_h1_h0_h1_h1_h0 : comprobar 341045747 190537 22 4966271 131072 4782969 181225025 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_260_h1_h0_h1_h1_h1 : comprobar 341045747 190537 22 5031807 131072 1594323 61205503 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_260_h1_h1 : comprobar 341045747 190537 22 4925311 16384 59049 17751145 10 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_261_h0_h0_h0 : comprobar 341045747 190537 22 4915071 32768 59049 8857120 10 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_261_h0_h0_h1_h0 : comprobar 341045747 190537 22 4931455 65536 177147 13329967 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_261_h0_h0_h1_h1 : comprobar 341045747 190537 22 4964223 65536 531441 40255622 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_261_h0_h1 : comprobar 341045747 190537 22 4923263 16384 19683 5914588 9 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_261_h1 : comprobar 341045747 190537 22 4919167 8192 6561 3939778 8 2 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_263_h0_h0_h0 : comprobar 341045747 190537 22 4914047 32768 177147 26565823 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_263_h0_h0_h1_h0 : comprobar 341045747 190537 22 4930431 65536 531441 39981595 12 3 false 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_260_h1_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_260_h1_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_260_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_261_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_261_h0_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_261_h0_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_261_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_261_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_263_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_263_h0_h0_h1_h0
