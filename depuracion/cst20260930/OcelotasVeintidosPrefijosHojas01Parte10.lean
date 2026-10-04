import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Bajo
theorem nodo_292_h0 : comprobar 6003186 79335 22 4915199 8192 1594323 956593799 13 1 true 115 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_292_h1 : comprobar 6003186 79335 22 4919295 8192 531441 319130320 12 1 false 115 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_294_h0 : comprobar 6003186 79335 22 4914175 8192 531441 318798170 12 2 true 115 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_294_h1 : comprobar 6003186 79335 22 4918271 8192 177147 106354630 11 2 false 115 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_295 : comprobar 6003186 79335 22 4916223 4096 59049 70873562 10 1 false 116 = true := by
  decide +kernel
end Bajo

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_292_h0
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_292_h1
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_294_h0
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_294_h1
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_295
