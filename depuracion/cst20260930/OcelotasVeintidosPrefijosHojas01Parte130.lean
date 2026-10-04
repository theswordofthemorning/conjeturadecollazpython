import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_292_h1_h0_h0_h1_h1_h0_h0 : comprobar 341045747 190537 22 5017599 524288 14348907 137323525 15 2 false 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_292_h1_h0_h0_h1_h1_h0_h1_h0 : comprobar 341045747 190537 22 5279743 1048576 43046721 216746968 16 2 false 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_292_h1_h0_h0_h1_h1_h0_h1_h1 : comprobar 341045747 190537 22 5804031 1048576 129140163 714810986 17 2 true 108 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_292_h1_h0_h0_h1_h1_h1 : comprobar 341045747 190537 22 5148671 262144 4782969 93940501 14 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_292_h1_h0_h1_h0_h0 : comprobar 341045747 190537 22 4935679 131072 4782969 180108677 14 3 true 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_292_h1_h0_h0_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_292_h1_h0_h0_h1_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_292_h1_h0_h0_h1_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_292_h1_h0_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_292_h1_h0_h1_h0_h0
