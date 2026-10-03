import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintiunaPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_285_h0_h1_h0_h1 : comprobar 325543668 190537 21 4954111 65536 177147 13391206 11 1 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_285_h0_h1_h1_h0 : comprobar 325543668 190537 21 4937727 65536 531441 40040758 12 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_285_h0_h1_h1_h1_h0 : comprobar 325543668 190537 21 4970495 131072 1594323 60459718 13 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_285_h0_h1_h1_h1_h1 : comprobar 325543668 190537 21 5036031 131072 4782969 183770639 14 2 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_285_h1_h0 : comprobar 325543668 190537 21 4917247 16384 531441 159498730 12 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_285_h1_h1_h0 : comprobar 325543668 190537 21 4925439 32768 1594323 239646676 13 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_285_h1_h1_h1_h0_h0 : comprobar 325543668 190537 21 4941823 131072 14348907 540998635 15 2 false 111 = true := by
  decide +kernel
end Alto

end OcelotasVeintiunaPrefijos
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_285_h0_h1_h0_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_285_h0_h1_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_285_h0_h1_h1_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_285_h0_h1_h1_h1_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_285_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_285_h1_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_285_h1_h1_h1_h0_h0
