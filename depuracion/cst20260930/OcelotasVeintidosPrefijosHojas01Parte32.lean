import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_38_h1_h1_h0 : comprobar 341045747 190537 22 4926823 32768 531441 79904677 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_38_h1_h1_h1_h0_h0 : comprobar 341045747 190537 22 4943207 131072 4782969 180383395 14 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_38_h1_h1_h1_h0_h1_h0 : comprobar 341045747 190537 22 5008743 262144 43046721 822486959 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_38_h1_h1_h1_h0_h1_h1 : comprobar 341045747 190537 22 5139815 262144 14348907 281336773 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_38_h1_h1_h1_h1 : comprobar 341045747 190537 22 4975975 65536 1594323 121052758 13 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_39 : comprobar 341045747 190537 22 4916583 4096 19683 23626252 9 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_44 : comprobar 341045747 190537 22 4912871 4096 19683 23608415 9 4 true 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_45 : comprobar 341045747 190537 22 4914919 4096 6561 7872752 8 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_47_h0_h0_h0_h0 : comprobar 341045747 190537 22 4913895 65536 1594323 119542513 13 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_47_h0_h0_h0_h1_h0 : comprobar 341045747 190537 22 4946663 131072 4782969 180509512 14 3 false 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_38_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_38_h1_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_38_h1_h1_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_38_h1_h1_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_38_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_39
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_44
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_45
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_47_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_47_h0_h0_h0_h1_h0
