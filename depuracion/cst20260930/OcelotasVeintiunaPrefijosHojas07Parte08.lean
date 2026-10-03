import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintiunaPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_278_h1_h0_h1_h0 : comprobar 325543668 190537 21 4935935 65536 531441 40026230 12 2 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_278_h1_h0_h1_h1 : comprobar 325543668 190537 21 4968703 65536 177147 13430650 11 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_278_h1_h1 : comprobar 325543668 190537 21 4927743 16384 19683 5919970 9 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_280_h0_h0 : comprobar 325543668 190537 21 4914431 16384 177147 53135797 11 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_280_h0_h1_h0 : comprobar 325543668 190537 21 4922623 32768 531441 79836556 12 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_280_h0_h1_h1_h0 : comprobar 325543668 190537 21 4939007 65536 1594323 120153415 13 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_280_h0_h1_h1_h1_h0 : comprobar 325543668 190537 21 4971775 131072 4782969 181425865 14 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_280_h0_h1_h1_h1_h1_h0 : comprobar 325543668 190537 21 5037311 262144 43046721 827178074 16 2 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_280_h0_h1_h1_h1_h1_h1 : comprobar 325543668 190537 21 5168383 262144 14348907 282900478 15 2 false 110 = true := by
  decide +kernel
end Alto

end OcelotasVeintiunaPrefijos
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_278_h1_h0_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_278_h1_h0_h1_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_278_h1_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_280_h0_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_280_h0_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_280_h0_h1_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_280_h0_h1_h1_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_280_h0_h1_h1_h1_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_280_h0_h1_h1_h1_h1_h1
