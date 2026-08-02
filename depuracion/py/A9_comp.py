# A9_comp - comprobacion propia del comparador, tercera implementacion minima.
# Caso comun: trayectoria clasica del 7; caso 6 vs 9 (orden distinto, mismo (A,B));
# y el testigo del agente 2 (n=12 y n=13).
from fractions import Fraction

def paridades(n, k=None):
    seq = []
    while (n != 1 if k is None else len(seq) < k):
        if n % 2 == 0:
            seq.append('P'); n //= 2
        else:
            seq.append('I'); n = 3*n + 1
    return seq

def rumbo(seq, gi, gp):
    r = Fraction(0)
    for p in seq:
        r += gi if p == 'I' else gp
    return r

# caso 7 (agente 1): 16 pasos, A=5, B=11, rumbo con (3,7) = 92
s7 = paridades(7)
A7 = s7.count('I'); B7 = s7.count('P')
print("7:", "largo", len(s7), "A", A7, "B", B7, "rumbo(3,7)", rumbo(s7, 3, 7))
assert len(s7) == 16 and A7 == 5 and B7 == 11 and rumbo(s7, 3, 7) == 92

# caso 6 vs 9 en 4 pasos (agente 1)
s6 = paridades(6, 4); s9 = paridades(9, 4)
print("6:", s6, "9:", s9)
assert s6 != s9
assert s6.count('I') == s9.count('I') == 2 and s6.count('P') == s9.count('P') == 2
assert rumbo(s6, 1000003, 999983) == rumbo(s9, 1000003, 999983)

# testigo del agente 2: n=12 y n=13, mismo (A,B)=(2,7), ordenes distintos, mismo rumbo
s12 = paridades(12); s13 = paridades(13)
print("12:", s12)
print("13:", s13)
gi, gp = Fraction(7,360), Fraction(-13,360)
assert (s12.count('I'), s12.count('P')) == (2, 7) == (s13.count('I'), s13.count('P'))
assert s12 != s13
assert rumbo(s12, gi, gp) == rumbo(s13, gi, gp) == 2*gi + 7*gp

# y el punto 8 de la casa: el enunciado no tiene limite de barrido que importe,
# pero pruebo un n no redondo y angulos irracionales simulados por pares enteros
# independientes (base canonica -> linealidad):
import random
random.seed(123)
for _ in range(500):
    n = random.randrange(2, 10**9)
    s = paridades(n, 60)
    A = s.count('I'); B = s.count('P')
    assert rumbo(s, 1, 0) == A and rumbo(s, 0, 1) == B

print("A9_comp: todo OK")
