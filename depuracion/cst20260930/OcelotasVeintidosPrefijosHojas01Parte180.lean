import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_346_h1_h0 : comprobar 341045747 190537 22 4917567 16384 19683 5907745 9 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_346_h1_h1_h0 : comprobar 341045747 190537 22 4925759 32768 59049 8876380 10 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_346_h1_h1_h1_h0 : comprobar 341045747 190537 22 4942143 65536 177147 13358857 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_346_h1_h1_h1_h1 : comprobar 341045747 190537 22 4974911 65536 531441 40342292 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_347_h0_h0_h0 : comprobar 341045747 190537 22 4915519 32768 59049 8857927 10 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_347_h0_h0_h1_h0 : comprobar 341045747 190537 22 4931903 65536 531441 39993533 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_347_h0_h0_h1_h1 : comprobar 341045747 190537 22 4964671 65536 177147 13419751 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_347_h0_h1_h0 : comprobar 341045747 190537 22 4923711 32768 177147 26618068 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_347_h0_h1_h1_h0_h0 : comprobar 341045747 190537 22 4940095 131072 1594323 60089944 13 3 false 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_346_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_346_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_346_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_346_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_347_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_347_h0_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_347_h0_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_347_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_347_h0_h1_h1_h0_h0
