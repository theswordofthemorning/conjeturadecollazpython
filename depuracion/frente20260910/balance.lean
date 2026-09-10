/-
  BALANCE DE LAS CASTORAS: paridad, salida y mezcla de corrientes.
  Ingredientes algebraicos del balance de corrientes, sobre racionales.
  No afirma contraccion: separa la identidad del objetivo pendiente.
  Incluye un contraejemplo sintetico exacto, no una orbita alcanzable.
-/

namespace BalanceCorrientes

theorem varianza_dos (a b x y : Rat) :
    (a+b)*(a*x*x+b*y*y) - (a*x+b*y)*(a*x+b*y) =
    a*b*(x-y)*(x-y) := by
  grind

theorem varianza_cuatro (a b c d x y z w : Rat) :
    (a+b+c+d)*(a*x*x+b*y*y+c*z*z+d*w*w) -
      (a*x+b*y+c*z+d*w)*(a*x+b*y+c*z+d*w) =
    a*b*(x-y)*(x-y) + a*c*(x-z)*(x-z) + a*d*(x-w)*(x-w) +
    b*c*(y-z)*(y-z) + b*d*(y-w)*(y-w) + c*d*(z-w)*(z-w) := by
  grind

theorem separar_paridad (a b u v : Rat) (hab : a+b=1) :
    2*a*a*(1+u) + 2*b*b*(1+v) - 1 =
    a*u + b*v + (a-b)*(a-b) + (a-b)*(a*u-b*v) := by
  grind

theorem balance_global (masa salida ep eh energia paridad sesgo
    energiaSalida mezcla : Rat)
    (hp : masa*ep = energia + paridad + sesgo)
    (hh : (2*masa-salida)*eh = 2*energia-salida*energiaSalida-mezcla) :
    (2*masa-salida)*eh =
      2*masa*ep-2*paridad-2*sesgo-salida*energiaSalida-mezcla := by
  grind

theorem margen_medio (ep eh s q r salida delta : Rat)
    (h : (1-s)*eh = ep-q-r-salida-delta) :
    delta+q+r+salida-(1+s)*ep/2 = (1-s)*(ep/2-eh) := by
  grind

theorem contraccion_iff (ep eh s q r salida delta rho : Rat)
    (hs : s < 1) (h : (1-s)*eh = ep-q-r-salida-delta) :
    (eh < rho*ep) <-> ((1-rho*(1-s))*ep < q+r+salida+delta) := by
  have hpos : 0 < 1-s := by grind
  rw [<- Rat.mul_lt_mul_left (a := eh) (b := rho*ep) (c := 1-s) hpos, h]
  constructor <;> intro hc <;> grind

def suma : List Rat -> Rat
  | [] => 0
  | x :: xs => x + suma xs

def cuadrados : List Rat -> Rat
  | [] => 0
  | x :: xs => x*x + cuadrados xs

def exceso (modulo : Rat) (fibras : List (List Rat)) : Rat :=
  modulo * suma (fibras.map (fun f => cuadrados f / suma f)) /
    suma (fibras.map suma) - 1

def paso (k : Nat) (c : Int) (bit : Bool) : Option (Prod Nat Int) :=
  if c % 2 = 0 then
    some (k, if bit then (3*c+1-(3 : Int)^k)/2 else c/2)
  else if bit then
    if k > 2 then some (k-1, (c-(3 : Int)^(k-1))/2) else none
  else some (k+1, (3*c+1)/2)

def entrada : List (Prod Nat Int) :=
  List.replicate 4 (2,0) ++ List.replicate 3 (2,1) ++
  List.replicate 3 (2,3) ++ List.replicate 3 (2,5) ++ List.replicate 3 (2,7)

def llegada : List (Prod Nat Int) :=
  entrada.flatMap (fun (k,c) =>
    ([false,true].filterMap (paso k c)).map (fun (j,d) => (j,d % 4)))

def fila (k : Nat) (n : Nat) (xs : List (Prod Nat Int)) : List Rat :=
  (List.range n).map (fun (r : Nat) => ((xs.count (k, (r : Int)) : Nat) : Rat))

theorem testigo_entrada : fila 2 8 entrada = [4,3,0,3,0,3,0,3] := by decide
theorem testigo_salida_dos : fila 2 4 llegada = [8,0,0,0] := by decide
theorem testigo_salida_tres : fila 3 4 llegada = [3,3,3,3] := by decide
theorem testigo_masas : And (entrada.length = 16) (llegada.length = 20) := by decide
theorem testigo_soporte : llegada.all (fun (k,_) => k == 2 || k == 3) = true := by decide

theorem testigo_exceso_padre : exceso 8 [fila 2 8 entrada] = 5/8 := by
  rw [testigo_entrada]
  simp only [exceso, List.map_cons, List.map_nil, suma, cuadrados]
  grind
theorem testigo_exceso_hija : exceso 4 [fila 2 4 llegada, fila 3 4 llegada] = 6/5 := by
  rw [testigo_salida_dos, testigo_salida_tres]
  simp only [exceso, List.map_cons, List.map_nil, suma, cuadrados]
  grind

theorem testigo_aumenta :
    exceso 4 [fila 2 4 llegada, fila 3 4 llegada] > exceso 8 [fila 2 8 entrada] := by
  rw [testigo_exceso_padre, testigo_exceso_hija]
  grind

theorem testigo_cociente :
    exceso 4 [fila 2 4 llegada, fila 3 4 llegada] / exceso 8 [fila 2 8 entrada] =
      48/25 := by
  rw [testigo_exceso_padre, testigo_exceso_hija]
  grind

def entradaEquilibrada : List (Prod Nat Int) := [(2,0), (2,1)]
def llegadaEquilibrada : List (Prod Nat Int) :=
  entradaEquilibrada.flatMap (fun (k,c) =>
    ([false,true].filterMap (paso k c)).map (fun (j,d) => (j,d % 4)))

theorem testigo_equilibrado_entrada : fila 2 8 entradaEquilibrada = [1,1,0,0,0,0,0,0] := by decide
theorem testigo_equilibrado_dos : fila 2 4 llegadaEquilibrada = [2,0,0,0] := by decide
theorem testigo_equilibrado_tres : fila 3 4 llegadaEquilibrada = [0,0,1,0] := by decide
theorem testigo_equilibrado_masas : And (entradaEquilibrada.length = 2) (llegadaEquilibrada.length = 3) := by decide
theorem testigo_equilibrado_excesos :
    And (exceso 8 [fila 2 8 entradaEquilibrada] = 3)
        (exceso 4 [fila 2 4 llegadaEquilibrada, fila 3 4 llegadaEquilibrada] = 3) := by
  rw [testigo_equilibrado_entrada, testigo_equilibrado_dos, testigo_equilibrado_tres]
  simp only [exceso, List.map_cons, List.map_nil, suma, cuadrados]
  constructor <;> grind

#print axioms varianza_cuatro
#print axioms separar_paridad
#print axioms balance_global
#print axioms margen_medio
#print axioms contraccion_iff
#print axioms testigo_entrada
#print axioms testigo_salida_dos
#print axioms testigo_salida_tres
#print axioms testigo_masas
#print axioms testigo_soporte
#print axioms testigo_exceso_padre
#print axioms testigo_exceso_hija
#print axioms testigo_aumenta
#print axioms testigo_cociente
#print axioms testigo_equilibrado_entrada
#print axioms testigo_equilibrado_dos
#print axioms testigo_equilibrado_tres
#print axioms testigo_equilibrado_masas
#print axioms testigo_equilibrado_excesos

end BalanceCorrientes
