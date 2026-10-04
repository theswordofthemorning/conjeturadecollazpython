import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_333_h0_h1_h1_h1_h0_h0 : comprobar 341045747 190537 22 4971967 262144 43046721 816447923 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_333_h0_h1_h1_h1_h0_h1 : comprobar 341045747 190537 22 5103039 262144 14348907 279323761 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_333_h0_h1_h1_h1_h1 : comprobar 341045747 190537 22 5037503 131072 4782969 183824356 14 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_333_h1_h0_h0 : comprobar 341045747 190537 22 4918719 32768 177147 26591080 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_333_h1_h0_h1_h0_h0 : comprobar 341045747 190537 22 4935103 131072 1594323 60029221 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_333_h1_h0_h1_h0_h1 : comprobar 341045747 190537 22 5000639 131072 4782969 182479148 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_333_h1_h0_h1_h1 : comprobar 341045747 190537 22 4967871 65536 531441 40285201 12 3 false 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_333_h0_h1_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_333_h0_h1_h1_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_333_h0_h1_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_333_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_333_h1_h0_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_333_h1_h0_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_333_h1_h0_h1_h1
