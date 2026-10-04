import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Bajo
theorem nodo_245 : comprobar 6003186 79335 22 4912767 4096 59049 70823740 10 2 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_246_h0 : comprobar 6003186 79335 22 4914815 8192 177147 106279897 11 2 false 115 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_246_h1 : comprobar 6003186 79335 22 4918911 8192 531441 319105412 12 2 true 115 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_248 : comprobar 6003186 79335 22 4913791 4096 19683 23612834 9 2 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_249 : comprobar 6003186 79335 22 4915839 4096 59049 70868027 10 3 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_252 : comprobar 6003186 79335 22 4913279 4096 19683 23610374 9 3 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_253 : comprobar 6003186 79335 22 4915327 4096 6561 7873405 8 2 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_255 : comprobar 6003186 79335 22 4914303 4096 59049 70845884 10 3 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_256 : comprobar 6003186 79335 22 4916351 4096 19683 23625136 9 3 false 116 = true := by
  decide +kernel
end Bajo

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_245
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_246_h0
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_246_h1
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_248
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_249
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_252
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_253
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_255
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_256
