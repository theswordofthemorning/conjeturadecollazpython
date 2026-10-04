import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Bajo
theorem nodo_298 : comprobar 6003186 79335 22 4913663 4096 177147 212509970 11 2 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_299 : comprobar 6003186 79335 22 4915711 4096 59049 70866181 10 2 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_301 : comprobar 6003186 79335 22 4914687 4096 59049 70851419 10 2 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_302 : comprobar 6003186 79335 22 4916735 4096 19683 23626981 9 1 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_308 : comprobar 6003186 79335 22 4912831 4096 6561 7869407 8 3 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_309 : comprobar 6003186 79335 22 4914879 4096 19683 23618063 9 4 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_311 : comprobar 6003186 79335 22 4913855 4096 19683 23613142 9 3 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_312 : comprobar 6003186 79335 22 4915903 4096 59049 70868951 10 3 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_315 : comprobar 6003186 79335 22 4913343 4096 2187 2623409 7 2 false 116 = true := by
  decide +kernel
end Bajo

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_298
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_299
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_301
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_302
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_308
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_309
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_311
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_312
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_315
