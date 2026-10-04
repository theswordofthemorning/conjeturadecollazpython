import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_32_h0_h0_h0_h0_h0 : comprobar 341045747 190537 22 4916071 131072 4782969 179393170 14 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_32_h0_h0_h0_h0_h1_h0 : comprobar 341045747 190537 22 4981607 262144 14348907 272676982 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_32_h0_h0_h0_h0_h1_h1 : comprobar 341045747 190537 22 5112679 262144 43046721 839554307 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_32_h0_h0_h0_h1 : comprobar 341045747 190537 22 4948839 65536 1594323 120392608 13 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_32_h0_h0_h1 : comprobar 341045747 190537 22 4932455 32768 531441 79996018 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_32_h0_h1 : comprobar 341045747 190537 22 4924263 16384 177147 53242105 11 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_32_h1 : comprobar 341045747 190537 22 4920167 8192 59049 35465212 10 3 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_35_h0 : comprobar 341045747 190537 22 4913511 8192 19683 11805745 9 3 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_35_h1_h0 : comprobar 341045747 190537 22 4917607 16384 59049 17723380 10 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_35_h1_h1_h0 : comprobar 341045747 190537 22 4925799 32768 177147 26629357 11 3 false 113 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_32_h0_h0_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_32_h0_h0_h0_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_32_h0_h0_h0_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_32_h0_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_32_h0_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_32_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_32_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_35_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_35_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_35_h1_h1_h0
