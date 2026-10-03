import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintiunaPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_270 : comprobar 325543668 190537 21 4912895 4096 59049 70825585 10 2 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_271_h0_h0 : comprobar 325543668 190537 21 4914943 16384 531441 159423997 12 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_271_h0_h1_h0_h0 : comprobar 325543668 190537 21 4923135 65536 4782969 359301865 14 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_271_h0_h1_h0_h1_h0_h0 : comprobar 325543668 190537 21 4955903 262144 43046721 813810037 16 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_271_h0_h1_h0_h1_h0_h1 : comprobar 325543668 190537 21 5086975 262144 129140163 2506000193 17 2 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_271_h0_h1_h0_h1_h1 : comprobar 325543668 190537 21 5021439 131072 14348907 549714478 15 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_271_h0_h1_h1 : comprobar 325543668 190537 21 4939519 32768 1594323 240331738 13 2 false 113 = true := by
  decide +kernel
end Alto

end OcelotasVeintiunaPrefijos
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_270
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_271_h0_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_271_h0_h1_h0_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_271_h0_h1_h0_h1_h0_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_271_h0_h1_h0_h1_h0_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_271_h0_h1_h0_h1_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_271_h0_h1_h1
