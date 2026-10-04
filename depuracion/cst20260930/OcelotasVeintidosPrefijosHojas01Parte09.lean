import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Bajo
theorem nodo_279 : comprobar 6003186 79335 22 4913919 4096 19683 23613449 9 2 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_280 : comprobar 6003186 79335 22 4915967 4096 59049 70869872 10 3 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_283 : comprobar 6003186 79335 22 4913407 4096 19683 23610989 9 2 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_284 : comprobar 6003186 79335 22 4915455 4096 6561 7873610 8 1 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_286 : comprobar 6003186 79335 22 4914431 4096 59049 70847729 10 2 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_287 : comprobar 6003186 79335 22 4916479 4096 19683 23625751 9 2 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_291_h0 : comprobar 6003186 79335 22 4913151 8192 177147 106243913 11 1 false 115 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_291_h1 : comprobar 6003186 79335 22 4917247 8192 531441 318997460 12 2 true 115 = true := by
  decide +kernel
end Bajo

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_279
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_280
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_283
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_284
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_286
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_287
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_291_h0
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_291_h1
