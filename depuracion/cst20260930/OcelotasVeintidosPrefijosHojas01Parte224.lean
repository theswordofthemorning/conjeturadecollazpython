import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_512_h0_h1_h1 : comprobar 341045747 190537 22 4938523 32768 531441 80094433 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_512_h1 : comprobar 341045747 190537 22 4918043 8192 59049 35449903 10 3 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_513_h0_h0_h0 : comprobar 341045747 190537 22 4915995 32768 177147 26576356 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_513_h0_h0_h1_h0_h0 : comprobar 341045747 190537 22 4932379 131072 1594323 59996092 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_513_h0_h0_h1_h0_h1 : comprobar 341045747 190537 22 4997915 131072 4782969 182379761 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_513_h0_h0_h1_h1 : comprobar 341045747 190537 22 4965147 65536 531441 40263115 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_513_h0_h1 : comprobar 341045747 190537 22 4924187 16384 59049 17747095 10 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_513_h1_h0_h0_h0 : comprobar 341045747 190537 22 4920091 65536 177147 13299250 11 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_513_h1_h0_h0_h1 : comprobar 341045747 190537 22 4952859 65536 531441 40163471 12 3 true 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_512_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_512_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_513_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_513_h0_h0_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_513_h0_h0_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_513_h0_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_513_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_513_h1_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_513_h1_h0_h0_h1
