import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintiunaPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_210 : comprobar 325543668 190537 21 4912847 4096 19683 23608300 9 2 false 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_211_h0_h0 : comprobar 325543668 190537 21 4914895 16384 177147 53140819 11 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_211_h0_h1_h0 : comprobar 325543668 190537 21 4923087 32768 531441 79844089 12 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_211_h0_h1_h1_h0_h0 : comprobar 325543668 190537 21 4939471 131072 4782969 180247072 14 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_211_h0_h1_h1_h0_h1_h0 : comprobar 325543668 190537 21 5005007 262144 14348907 273957835 15 2 false 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_211_h0_h1_h1_h0_h1_h1 : comprobar 325543668 190537 21 5136079 262144 43046721 843396866 16 2 true 110 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_211_h0_h1_h1_h1 : comprobar 325543668 190537 21 4972239 65536 1594323 120961876 13 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_211_h1 : comprobar 325543668 190537 21 4918991 8192 59049 35456737 10 2 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_213 : comprobar 325543668 190537 21 4913871 4096 19683 23613221 9 3 true 116 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_214 : comprobar 325543668 190537 21 4915919 4096 6561 7874354 8 2 false 116 = true := by
  decide +kernel
end Alto

end OcelotasVeintiunaPrefijos
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_210
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_211_h0_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_211_h0_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_211_h0_h1_h1_h0_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_211_h0_h1_h1_h0_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_211_h0_h1_h1_h0_h1_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_211_h0_h1_h1_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_211_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_213
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_214
