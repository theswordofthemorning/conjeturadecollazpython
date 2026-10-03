import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintiunaPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_285_h1_h1_h1_h0_h1_h0 : comprobar 325543668 190537 21 5007359 262144 43046721 822259633 16 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_285_h1_h1_h1_h0_h1_h1 : comprobar 325543668 190537 21 5138431 262144 129140163 2531348981 17 2 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_285_h1_h1_h1_h1 : comprobar 325543668 190537 21 4974591 65536 4782969 363057241 14 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_286_h0_h0_h0_h0_h0_h0 : comprobar 325543668 190537 21 4915199 262144 129140163 2421378056 17 2 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_286_h0_h0_h0_h0_h0_h1_h0 : comprobar 325543668 190537 21 5046271 524288 129140163 1242974069 17 2 true 109 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_286_h0_h0_h0_h0_h0_h1_h1 : comprobar 325543668 190537 21 5308415 524288 43046721 435848050 16 1 false 109 = true := by
  decide +kernel
end Alto

end OcelotasVeintiunaPrefijos
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_285_h1_h1_h1_h0_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_285_h1_h1_h1_h0_h1_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_285_h1_h1_h1_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_286_h0_h0_h0_h0_h0_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_286_h0_h0_h0_h0_h0_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_286_h0_h0_h0_h0_h0_h1_h1
