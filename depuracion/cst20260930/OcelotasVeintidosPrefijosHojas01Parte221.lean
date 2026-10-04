import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_509_h1_h1_h1_h0_h0 : comprobar 341045747 190537 22 4941595 131072 4782969 180324575 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_509_h1_h1_h1_h0_h1 : comprobar 341045747 190537 22 5007131 131072 1594323 60905353 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_509_h1_h1_h1_h1_h0 : comprobar 341045747 190537 22 4974363 131072 531441 20168924 12 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_509_h1_h1_h1_h1_h1 : comprobar 341045747 190537 22 5039899 131072 1594323 61303934 13 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_510_h0_h0_h0_h0_h0_h0 : comprobar 341045747 190537 22 4914971 262144 14348907 269029552 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_510_h0_h0_h0_h0_h0_h1 : comprobar 341045747 190537 22 5046043 262144 43046721 828612017 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_510_h0_h0_h0_h0_h1 : comprobar 341045747 190537 22 4980507 131072 4782969 181744519 14 3 false 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_509_h1_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_509_h1_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_509_h1_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_509_h1_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_510_h0_h0_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_510_h0_h0_h0_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_510_h0_h0_h0_h0_h1
