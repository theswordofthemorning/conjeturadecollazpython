import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintiunaPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_271_h1 : comprobar 325543668 190537 21 4919039 8192 177147 106371238 11 2 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_273 : comprobar 325543668 190537 21 4913919 4096 19683 23613449 9 2 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_274 : comprobar 325543668 190537 21 4915967 4096 59049 70869872 10 3 true 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_277_h0_h0 : comprobar 325543668 190537 21 4913407 16384 59049 17708242 10 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_277_h0_h1_h0 : comprobar 325543668 190537 21 4921599 32768 177147 26606650 11 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_277_h0_h1_h1_h0_h0 : comprobar 325543668 190537 21 4937983 131072 4782969 180192761 14 2 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_277_h0_h1_h1_h0_h1 : comprobar 325543668 190537 21 5003519 131072 1594323 60861415 13 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_277_h0_h1_h1_h1 : comprobar 325543668 190537 21 4970751 65536 531441 40308556 12 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_277_h1 : comprobar 325543668 190537 21 4917503 8192 19683 11815336 9 2 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_278_h0 : comprobar 325543668 190537 21 4915455 8192 6561 3936805 8 1 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_278_h1_h0_h0 : comprobar 325543668 190537 21 4919551 32768 59049 8865193 10 2 false 113 = true := by
  decide +kernel
end Alto

end OcelotasVeintiunaPrefijos
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_271_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_273
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_274
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_277_h0_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_277_h0_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_277_h0_h1_h1_h0_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_277_h0_h1_h1_h0_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_277_h0_h1_h1_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_277_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_278_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_278_h1_h0_h0
