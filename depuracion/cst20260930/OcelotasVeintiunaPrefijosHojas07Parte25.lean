import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintiunaPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_328_h0_h1_h0_h1_h0 : comprobar 325543668 190537 21 4957631 131072 14348907 542729200 15 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_328_h0_h1_h0_h1_h1_h0 : comprobar 325543668 190537 21 5023167 262144 129140163 2474566442 17 2 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_328_h0_h1_h0_h1_h1_h1 : comprobar 325543668 190537 21 5154239 262144 43046721 846378841 16 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_328_h0_h1_h1 : comprobar 325543668 190537 21 4941247 32768 1594323 240415816 13 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_328_h1 : comprobar 325543668 190537 21 4920767 8192 177147 106408606 11 2 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_333 : comprobar 325543668 190537 21 4912959 4096 2187 2623204 7 2 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_334 : comprobar 325543668 190537 21 4915007 4096 6561 7872893 8 3 true 116 = true := by
  decide +kernel
end Alto

end OcelotasVeintiunaPrefijos
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_328_h0_h1_h0_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_328_h0_h1_h0_h1_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_328_h0_h1_h0_h1_h1_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_328_h0_h1_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_328_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_333
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_334
