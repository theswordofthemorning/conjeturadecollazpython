import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_245_h1_h1_h0_h0 : comprobar 341045747 190537 22 4925055 65536 1594323 119813998 13 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_245_h1_h1_h0_h1_h0_h0 : comprobar 341045747 190537 22 4957823 262144 43046721 814125329 16 3 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_245_h1_h1_h0_h1_h0_h1 : comprobar 341045747 190537 22 5088895 262144 14348907 278549563 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_245_h1_h1_h0_h1_h1 : comprobar 341045747 190537 22 5023359 131072 4782969 183308224 14 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_245_h1_h1_h1 : comprobar 341045747 190537 22 4941439 32768 531441 80141719 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_246_h0_h0_h0 : comprobar 341045747 190537 22 4914815 32768 531441 79709923 12 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_246_h0_h0_h1_h0_h0_h0 : comprobar 341045747 190537 22 4931199 262144 14348907 269917798 15 3 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_246_h0_h0_h1_h0_h0_h1 : comprobar 341045747 190537 22 5062271 262144 43046721 831276755 16 3 true 110 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_245_h1_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_245_h1_h1_h0_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_245_h1_h1_h0_h1_h0_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_245_h1_h1_h0_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_245_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_246_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_246_h0_h0_h1_h0_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_246_h0_h0_h1_h0_h0_h1
