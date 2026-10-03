import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintiunaPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_240_h1_h1_h1_h0_h1_h0 : comprobar 325543668 190537 21 5009023 262144 129140163 2467598660 17 2 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_240_h1_h1_h1_h0_h1_h1 : comprobar 325543668 190537 21 5140095 262144 43046721 844056247 16 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_240_h1_h1_h1_h1 : comprobar 325543668 190537 21 4976255 65536 4782969 363178687 14 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_242 : comprobar 325543668 190537 21 4913791 4096 19683 23612834 9 2 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_243 : comprobar 325543668 190537 21 4915839 4096 59049 70868027 10 3 true 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_246 : comprobar 325543668 190537 21 4913279 4096 19683 23610374 9 3 true 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_247 : comprobar 325543668 190537 21 4915327 4096 6561 7873405 8 2 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_249 : comprobar 325543668 190537 21 4914303 4096 59049 70845884 10 3 true 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_250 : comprobar 325543668 190537 21 4916351 4096 19683 23625136 9 3 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_254 : comprobar 325543668 190537 21 4913023 4096 19683 23609144 9 3 true 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_255 : comprobar 325543668 190537 21 4915071 4096 6561 7872995 8 2 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_257_h0 : comprobar 325543668 190537 21 4914047 8192 59049 35421097 10 2 false 115 = true := by
  decide +kernel
end Alto

end OcelotasVeintiunaPrefijos
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_240_h1_h1_h1_h0_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_240_h1_h1_h1_h0_h1_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_240_h1_h1_h1_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_242
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_243
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_246
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_247
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_249
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_250
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_254
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_255
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_257_h0
