import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_35_h1_h1_h1_h0 : comprobar 341045747 190537 22 4942183 65536 531441 40076896 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_35_h1_h1_h1_h1_h0 : comprobar 341045747 190537 22 4974951 131072 1594323 60513925 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_35_h1_h1_h1_h1_h1 : comprobar 341045747 190537 22 5040487 131072 4782969 183933260 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_36_h0_h0 : comprobar 341045747 190537 22 4915559 16384 19683 5905333 9 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_36_h0_h1_h0 : comprobar 341045747 190537 22 4923751 32768 59049 8872762 10 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_36_h0_h1_h1_h0 : comprobar 341045747 190537 22 4940135 65536 177147 13353430 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_36_h0_h1_h1_h1 : comprobar 341045747 190537 22 4972903 65536 531441 40326011 12 3 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_36_h1 : comprobar 341045747 190537 22 4919655 8192 6561 3940169 8 2 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_38_h0 : comprobar 341045747 190537 22 4914535 8192 59049 35424616 10 3 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_38_h1_h0 : comprobar 341045747 190537 22 4918631 16384 177147 53181211 11 3 false 114 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_35_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_35_h1_h1_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_35_h1_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_36_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_36_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_36_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_36_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_36_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_38_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_38_h1_h0
