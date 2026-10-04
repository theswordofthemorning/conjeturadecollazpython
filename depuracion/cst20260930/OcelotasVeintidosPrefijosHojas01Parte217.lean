import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_509_h0_h1_h0_h1_h1_h0 : comprobar 341045747 190537 22 5019419 262144 14348907 274746694 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_509_h0_h1_h0_h1_h1_h1 : comprobar 341045747 190537 22 5150491 262144 43046721 845763443 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_509_h0_h1_h1 : comprobar 341045747 190537 22 4937499 32768 531441 80077825 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_509_h1_h0_h0_h0_h0_h0 : comprobar 341045747 190537 22 4917019 262144 43046721 807424955 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_509_h1_h0_h0_h0_h0_h1 : comprobar 341045747 190537 22 5048091 262144 14348907 276316105 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_509_h1_h0_h0_h0_h1 : comprobar 341045747 190537 22 4982555 131072 4782969 181819252 14 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_509_h1_h0_h0_h1_h0 : comprobar 341045747 190537 22 4949787 131072 4782969 180623510 14 3 true 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_509_h0_h1_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_509_h0_h1_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_509_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_509_h1_h0_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_509_h1_h0_h0_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_509_h1_h0_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_509_h1_h0_h0_h1_h0
