import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintiunaPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_289_h1_h1 : comprobar 325543668 190537 21 4928511 16384 177147 53288032 11 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_292_h0 : comprobar 325543668 190537 21 4913663 8192 177147 106254985 11 2 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_292_h1_h0 : comprobar 325543668 190537 21 4917759 16384 531441 159515338 12 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_292_h1_h1_h0 : comprobar 325543668 190537 21 4925951 32768 1594323 239671588 13 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_292_h1_h1_h1_h0_h0 : comprobar 325543668 190537 21 4942335 131072 14348907 541054687 15 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_292_h1_h1_h1_h0_h1_h0 : comprobar 325543668 190537 21 5007871 262144 43046721 822343711 16 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_292_h1_h1_h1_h0_h1_h1 : comprobar 325543668 190537 21 5138943 262144 129140163 2531601215 17 2 true 110 = true := by
  decide +kernel
end Alto

end OcelotasVeintiunaPrefijos
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_289_h1_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_292_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_292_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_292_h1_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_292_h1_h1_h1_h0_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_292_h1_h1_h1_h0_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_292_h1_h1_h1_h0_h1_h1
