import OcelotasPrefijosBloques

/-! Particion por coste; cada hoja se comprueba en el nucleo. -/
namespace OcelotasVeintiunaPrefijos
open Ocelotas OcelotasContador OcelotasCribaPrefijos OcelotasPrefijosBloques
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Alto
theorem nodo_295_h1 : comprobar 325543668 190537 21 4918783 8192 59049 35455234 10 2 false 115 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_296_h0_h0 : comprobar 325543668 190537 21 4916735 16384 59049 17720236 10 2 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_296_h0_h1_h0 : comprobar 325543668 190537 21 4924927 32768 177147 26624641 11 2 false 113 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_296_h0_h1_h1_h0 : comprobar 325543668 190537 21 4941311 65536 531441 40069822 12 2 false 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_296_h0_h1_h1_h1_h0 : comprobar 325543668 190537 21 4974079 131072 1594323 60503314 13 2 false 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_296_h0_h1_h1_h1_h1 : comprobar 325543668 190537 21 5039615 131072 4782969 183901427 14 2 true 111 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_296_h1_h0 : comprobar 325543668 190537 21 4920831 16384 19683 5911666 9 1 false 114 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_296_h1_h1_h0_h0 : comprobar 325543668 190537 21 4929023 65536 531441 39970178 12 2 true 112 = true := by
  decide +kernel
end Alto

namespace Alto
theorem nodo_296_h1_h1_h0_h1 : comprobar 325543668 190537 21 4961791 65536 177147 13411966 11 2 false 112 = true := by
  decide +kernel
end Alto

end OcelotasVeintiunaPrefijos
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_295_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_296_h0_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_296_h0_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_296_h0_h1_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_296_h0_h1_h1_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_296_h0_h1_h1_h1_h1
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_296_h1_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_296_h1_h1_h0_h0
#print axioms OcelotasVeintiunaPrefijos.Alto.nodo_296_h1_h1_h0_h1
