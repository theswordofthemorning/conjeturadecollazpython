import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintiunaPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_280_h1 : comprobar 325543668 190537 21 4918527 8192 59049 35453389 10 2 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_281 : comprobar 325543668 190537 21 4916479 4096 19683 23625751 9 2 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_285_h0_h0_h0 : comprobar 325543668 190537 21 4913151 32768 531441 79682935 12 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_285_h0_h0_h1_h0_h0_h0 : comprobar 325543668 190537 21 4929535 262144 43046721 809480141 16 2 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_285_h0_h0_h1_h0_h0_h1 : comprobar 325543668 190537 21 5060607 262144 14348907 277001167 15 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_285_h0_h0_h1_h0_h1 : comprobar 325543668 190537 21 4995071 131072 4782969 182275960 14 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_285_h0_h0_h1_h1 : comprobar 325543668 190537 21 4962303 65536 1594323 120720145 13 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_285_h0_h1_h0_h0 : comprobar 325543668 190537 21 4921343 65536 531441 39907898 12 2 true 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintiunaPrefijos
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_280_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_281
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_285_h0_h0_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_285_h0_h0_h1_h0_h0_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_285_h0_h0_h1_h0_h0_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_285_h0_h0_h1_h0_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_285_h0_h0_h1_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_285_h0_h1_h0_h0
