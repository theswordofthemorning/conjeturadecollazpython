import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintidosPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Bajo
theorem nodo_260 : comprobar 6003186 79335 22 4913023 4096 19683 23609144 9 3 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_261 : comprobar 6003186 79335 22 4915071 4096 6561 7872995 8 2 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_263 : comprobar 6003186 79335 22 4914047 4096 59049 70842194 10 2 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_264 : comprobar 6003186 79335 22 4916095 4096 19683 23623906 9 2 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_267 : comprobar 6003186 79335 22 4913535 4096 6561 7870535 8 2 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_268 : comprobar 6003186 79335 22 4915583 4096 2187 2624605 7 1 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_270 : comprobar 6003186 79335 22 4914559 4096 6561 7872175 8 2 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_271 : comprobar 6003186 79335 22 4916607 4096 19683 23626367 9 2 true 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_276 : comprobar 6003186 79335 22 4912895 4096 59049 70825585 10 2 false 116 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_277_h0 : comprobar 6003186 79335 22 4914943 8192 531441 318847994 12 2 true 115 = true := by
  decide +kernel
end Bajo

namespace Bajo
theorem nodo_277_h1 : comprobar 6003186 79335 22 4919039 8192 177147 106371238 11 2 false 115 = true := by
  decide +kernel
end Bajo

end OcelotasVeintidosPrefijos
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_260
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_261
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_263
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_264
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_267
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_268
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_270
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_271
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_276
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_277_h0
#print axioms OcelotasVeintidosPrefijos.Bajo.nodo_277_h1
