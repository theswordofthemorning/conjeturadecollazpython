import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_440_h0_h1_h0 : comprobar 341045747 190537 22 4923871 32768 59049 8872978 10 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_440_h0_h1_h1_h0 : comprobar 341045747 190537 22 4940255 65536 177147 13353754 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_440_h0_h1_h1_h1 : comprobar 341045747 190537 22 4973023 65536 531441 40326983 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_440_h1_h0_h0_h0 : comprobar 341045747 190537 22 4919775 65536 531441 39895186 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_440_h1_h0_h0_h1_h0 : comprobar 341045747 190537 22 4952543 131072 1594323 60241360 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_440_h1_h0_h0_h1_h1 : comprobar 341045747 190537 22 5018079 131072 4782969 183115565 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_440_h1_h0_h1 : comprobar 341045747 190537 22 4936159 32768 177147 26685364 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_440_h1_h1 : comprobar 341045747 190537 22 4927967 16384 59049 17760718 10 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_442_h0_h0 : comprobar 341045747 190537 22 4914655 16384 19683 5904247 9 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_442_h0_h1_h0 : comprobar 341045747 190537 22 4922847 32768 59049 8871133 10 3 false 113 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_440_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_440_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_440_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_440_h1_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_440_h1_h0_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_440_h1_h0_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_440_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_440_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_442_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_442_h0_h1_h0
