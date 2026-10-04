import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Bajo
theorem nodo_2 : comprobar 6003186 79335 22 4912741 4 3 3684556 1 1 false 126 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_13 : comprobar 6003186 79335 22 4912743 4096 19683 23607800 9 3 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_14 : comprobar 6003186 79335 22 4914791 4096 6561 7872547 8 3 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_16 : comprobar 6003186 79335 22 4913767 4096 6561 7870907 8 3 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_17 : comprobar 6003186 79335 22 4915815 4096 2187 2624729 7 2 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_20 : comprobar 6003186 79335 22 4913255 4096 19683 23610260 9 4 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_21 : comprobar 6003186 79335 22 4915303 4096 6561 7873367 8 3 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_23 : comprobar 6003186 79335 22 4914279 4096 59049 70845542 10 3 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_24 : comprobar 6003186 79335 22 4916327 4096 19683 23625022 9 3 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_28 : comprobar 6003186 79335 22 4912999 4096 59049 70827088 10 2 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_29 : comprobar 6003186 79335 22 4915047 4096 177147 212569838 11 2 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_31 : comprobar 6003186 79335 22 4914023 4096 19683 23613950 9 2 false 116 = true := by
  decide +kernel
end Bajo

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_2
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_13
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_14
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_16
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_17
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_20
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_21
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_23
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_24
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_28
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_29
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_31
