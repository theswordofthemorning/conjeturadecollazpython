import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Bajo
theorem nodo_551 : comprobar 6003186 79335 22 4913243 4096 59049 70830611 10 3 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_552 : comprobar 6003186 79335 22 4915291 4096 19683 23620045 9 3 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_554 : comprobar 6003186 79335 22 4914267 4096 6561 7871708 8 3 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_555 : comprobar 6003186 79335 22 4916315 4096 19683 23624966 9 4 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_558 : comprobar 6003186 79335 22 4913755 4096 6561 7870888 8 4 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_559 : comprobar 6003186 79335 22 4915803 4096 19683 23622506 9 4 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_561 : comprobar 6003186 79335 22 4914779 4096 2187 2624176 7 3 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_562 : comprobar 6003186 79335 22 4916827 4096 6561 7875809 8 4 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_563 : comprobar 6003186 79335 22 4912755 16 9 2763425 2 1 false 124 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_564 : comprobar 6003186 79335 22 4912742 2 1 2456371 0 0 false 127 = true := by
  decide +kernel
end Bajo

namespace Alto
theorem nodo_2 : comprobar 341045747 190537 22 4912741 4 3 3684556 1 1 false 126 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_13_h0 : comprobar 341045747 190537 22 4912743 8192 19683 11803900 9 3 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_13_h1_h0_h0 : comprobar 341045747 190537 22 4916839 32768 177147 26580919 11 3 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_13_h1_h0_h1_h0 : comprobar 341045747 190537 22 4933223 65536 531441 40004239 12 3 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_13_h1_h0_h1_h1_h0 : comprobar 341045747 190537 22 4965991 131072 4782969 181214819 14 3 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_13_h1_h0_h1_h1_h1 : comprobar 341045747 190537 22 5031527 131072 1594323 61202101 13 3 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_13_h1_h1 : comprobar 341045747 190537 22 4925031 16384 59049 17750137 10 3 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_14 : comprobar 341045747 190537 22 4914791 4096 6561 7872547 8 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_16_h0_h0_h0 : comprobar 341045747 190537 22 4913767 32768 59049 8854771 10 3 false 113 = true := by
  decide +kernel
end Alto

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_551
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_552
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_554
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_555
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_558
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_559
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_561
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_562
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_563
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_564
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_2
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_13_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_13_h1_h0_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_13_h1_h0_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_13_h1_h0_h1_h1_h0
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_13_h1_h0_h1_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_13_h1_h1
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_14
#print axioms OcelotasVeintidosPrefijos.Alto.nodo_16_h0_h0_h0
