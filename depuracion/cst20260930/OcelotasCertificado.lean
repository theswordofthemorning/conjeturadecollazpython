import OcelotasCriba

/-! Certificado generado por generar_criba_lean.py.
Cada bloque comprueba en el núcleo su punto inicial y sus pasos.
La cobertura final incluye todos los exponentes 1,...,82696. -/

set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace OcelotasCertificado

open Ocelotas OcelotasFinito OcelotasCriba OcelotasTrayectorias

theorem bloque_000 (q : ℕ) (hlo : 1 ≤ q)
    (hhi : q ≤ 1024) : CertificadoAritmetico q := by
  have he : Encierra 0 ⟨140737488355328, 140737488355328, 1⟩ := by decide +kernel
  have hc : recorrer 0 ⟨140737488355328, 140737488355328, 1⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 0 ⟨140737488355328, 140737488355328, 1⟩ he hc q (by omega) (by omega)

theorem bloque_001 (q : ℕ) (hlo : 1025 ≤ q)
    (hhi : q ≤ 2048) : CertificadoAritmetico q := by
  have he : Encierra 1024 ⟨140893729925694, 140893729925695, 1624⟩ := by decide +kernel
  have hc : recorrer 1024 ⟨140893729925694, 140893729925695, 1624⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 1024 ⟨140893729925694, 140893729925695, 1624⟩ he hc q (by omega) (by omega)

theorem bloque_002 (q : ℕ) (hlo : 2049 ≤ q)
    (hhi : q ≤ 3072) : CertificadoAritmetico q := by
  have he : Encierra 2048 ⟨141050144949690, 141050144949691, 3247⟩ := by decide +kernel
  have hc : recorrer 2048 ⟨141050144949690, 141050144949691, 3247⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 2048 ⟨141050144949690, 141050144949691, 3247⟩ he hc q (by omega) (by omega)

theorem bloque_003 (q : ℕ) (hlo : 3073 ≤ q)
    (hhi : q ≤ 4096) : CertificadoAritmetico q := by
  have he : Encierra 3072 ⟨141206733619879, 141206733619880, 4870⟩ := by decide +kernel
  have hc : recorrer 3072 ⟨141206733619879, 141206733619880, 4870⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 3072 ⟨141206733619879, 141206733619880, 4870⟩ he hc q (by omega) (by omega)

theorem bloque_004 (q : ℕ) (hlo : 4097 ≤ q)
    (hhi : q ≤ 5120) : CertificadoAritmetico q := by
  have he : Encierra 4096 ⟨141363496129036, 141363496129037, 6493⟩ := by decide +kernel
  have hc : recorrer 4096 ⟨141363496129036, 141363496129037, 6493⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 4096 ⟨141363496129036, 141363496129037, 6493⟩ he hc q (by omega) (by omega)

theorem bloque_005 (q : ℕ) (hlo : 5121 ≤ q)
    (hhi : q ≤ 6144) : CertificadoAritmetico q := by
  have he : Encierra 5120 ⟨141520432670151, 141520432670152, 8116⟩ := by decide +kernel
  have hc : recorrer 5120 ⟨141520432670151, 141520432670152, 8116⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 5120 ⟨141520432670151, 141520432670152, 8116⟩ he hc q (by omega) (by omega)

theorem bloque_006 (q : ℕ) (hlo : 6145 ≤ q)
    (hhi : q ≤ 7168) : CertificadoAritmetico q := by
  have he : Encierra 6144 ⟨141677543436427, 141677543436428, 9739⟩ := by decide +kernel
  have hc : recorrer 6144 ⟨141677543436427, 141677543436428, 9739⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 6144 ⟨141677543436427, 141677543436428, 9739⟩ he hc q (by omega) (by omega)

theorem bloque_007 (q : ℕ) (hlo : 7169 ≤ q)
    (hhi : q ≤ 8192) : CertificadoAritmetico q := by
  have he : Encierra 7168 ⟨141834828621283, 141834828621284, 11362⟩ := by decide +kernel
  have hc : recorrer 7168 ⟨141834828621283, 141834828621284, 11362⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 7168 ⟨141834828621283, 141834828621284, 11362⟩ he hc q (by omega) (by omega)

theorem bloque_008 (q : ℕ) (hlo : 8193 ≤ q)
    (hhi : q ≤ 9216) : CertificadoAritmetico q := by
  have he : Encierra 8192 ⟨141992288418352, 141992288418353, 12985⟩ := by decide +kernel
  have hc : recorrer 8192 ⟨141992288418352, 141992288418353, 12985⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 8192 ⟨141992288418352, 141992288418353, 12985⟩ he hc q (by omega) (by omega)

theorem bloque_009 (q : ℕ) (hlo : 9217 ≤ q)
    (hhi : q ≤ 10240) : CertificadoAritmetico q := by
  have he : Encierra 9216 ⟨142149923021482, 142149923021483, 14608⟩ := by decide +kernel
  have hc : recorrer 9216 ⟨142149923021482, 142149923021483, 14608⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 9216 ⟨142149923021482, 142149923021483, 14608⟩ he hc q (by omega) (by omega)

theorem bloque_010 (q : ℕ) (hlo : 10241 ≤ q)
    (hhi : q ≤ 11264) : CertificadoAritmetico q := by
  have he : Encierra 10240 ⟨142307732624736, 142307732624737, 16231⟩ := by decide +kernel
  have hc : recorrer 10240 ⟨142307732624736, 142307732624737, 16231⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 10240 ⟨142307732624736, 142307732624737, 16231⟩ he hc q (by omega) (by omega)

theorem bloque_011 (q : ℕ) (hlo : 11265 ≤ q)
    (hhi : q ≤ 12288) : CertificadoAritmetico q := by
  have he : Encierra 11264 ⟨142465717422392, 142465717422393, 17854⟩ := by decide +kernel
  have hc : recorrer 11264 ⟨142465717422392, 142465717422393, 17854⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 11264 ⟨142465717422392, 142465717422393, 17854⟩ he hc q (by omega) (by omega)

theorem bloque_012 (q : ℕ) (hlo : 12289 ≤ q)
    (hhi : q ≤ 13312) : CertificadoAritmetico q := by
  have he : Encierra 12288 ⟨142623877608946, 142623877608947, 19477⟩ := by decide +kernel
  have hc : recorrer 12288 ⟨142623877608946, 142623877608947, 19477⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 12288 ⟨142623877608946, 142623877608947, 19477⟩ he hc q (by omega) (by omega)

theorem bloque_013 (q : ℕ) (hlo : 13313 ≤ q)
    (hhi : q ≤ 14336) : CertificadoAritmetico q := by
  have he : Encierra 13312 ⟨142782213379108, 142782213379109, 21100⟩ := by decide +kernel
  have hc : recorrer 13312 ⟨142782213379108, 142782213379109, 21100⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 13312 ⟨142782213379108, 142782213379109, 21100⟩ he hc q (by omega) (by omega)

theorem bloque_014 (q : ℕ) (hlo : 14337 ≤ q)
    (hhi : q ≤ 15360) : CertificadoAritmetico q := by
  have he : Encierra 14336 ⟨142940724927803, 142940724927804, 22723⟩ := by decide +kernel
  have hc : recorrer 14336 ⟨142940724927803, 142940724927804, 22723⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 14336 ⟨142940724927803, 142940724927804, 22723⟩ he hc q (by omega) (by omega)

theorem bloque_015 (q : ℕ) (hlo : 15361 ≤ q)
    (hhi : q ≤ 16384) : CertificadoAritmetico q := by
  have he : Encierra 15360 ⟨143099412450175, 143099412450176, 24346⟩ := by decide +kernel
  have hc : recorrer 15360 ⟨143099412450175, 143099412450176, 24346⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 15360 ⟨143099412450175, 143099412450176, 24346⟩ he hc q (by omega) (by omega)

theorem bloque_016 (q : ℕ) (hlo : 16385 ≤ q)
    (hhi : q ≤ 17408) : CertificadoAritmetico q := by
  have he : Encierra 16384 ⟨143258276141584, 143258276141585, 25969⟩ := by decide +kernel
  have hc : recorrer 16384 ⟨143258276141584, 143258276141585, 25969⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 16384 ⟨143258276141584, 143258276141585, 25969⟩ he hc q (by omega) (by omega)

theorem bloque_017 (q : ℕ) (hlo : 17409 ≤ q)
    (hhi : q ≤ 18432) : CertificadoAritmetico q := by
  have he : Encierra 17408 ⟨143417316197605, 143417316197606, 27592⟩ := by decide +kernel
  have hc : recorrer 17408 ⟨143417316197605, 143417316197606, 27592⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 17408 ⟨143417316197605, 143417316197606, 27592⟩ he hc q (by omega) (by omega)

theorem bloque_018 (q : ℕ) (hlo : 18433 ≤ q)
    (hhi : q ≤ 19456) : CertificadoAritmetico q := by
  have he : Encierra 18432 ⟨143576532814032, 143576532814033, 29215⟩ := by decide +kernel
  have hc : recorrer 18432 ⟨143576532814032, 143576532814033, 29215⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 18432 ⟨143576532814032, 143576532814033, 29215⟩ he hc q (by omega) (by omega)

theorem bloque_019 (q : ℕ) (hlo : 19457 ≤ q)
    (hhi : q ≤ 20480) : CertificadoAritmetico q := by
  have he : Encierra 19456 ⟨143735926186876, 143735926186877, 30838⟩ := by decide +kernel
  have hc : recorrer 19456 ⟨143735926186876, 143735926186877, 30838⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 19456 ⟨143735926186876, 143735926186877, 30838⟩ he hc q (by omega) (by omega)

theorem bloque_020 (q : ℕ) (hlo : 20481 ≤ q)
    (hhi : q ≤ 21504) : CertificadoAritmetico q := by
  have he : Encierra 20480 ⟨143895496512366, 143895496512367, 32461⟩ := by decide +kernel
  have hc : recorrer 20480 ⟨143895496512366, 143895496512367, 32461⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 20480 ⟨143895496512366, 143895496512367, 32461⟩ he hc q (by omega) (by omega)

theorem bloque_021 (q : ℕ) (hlo : 21505 ≤ q)
    (hhi : q ≤ 22528) : CertificadoAritmetico q := by
  have he : Encierra 21504 ⟨144055243986948, 144055243986949, 34084⟩ := by decide +kernel
  have hc : recorrer 21504 ⟨144055243986948, 144055243986949, 34084⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 21504 ⟨144055243986948, 144055243986949, 34084⟩ he hc q (by omega) (by omega)

theorem bloque_022 (q : ℕ) (hlo : 22529 ≤ q)
    (hhi : q ≤ 23552) : CertificadoAritmetico q := by
  have he : Encierra 22528 ⟨144215168807285, 144215168807286, 35707⟩ := by decide +kernel
  have hc : recorrer 22528 ⟨144215168807285, 144215168807286, 35707⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 22528 ⟨144215168807285, 144215168807286, 35707⟩ he hc q (by omega) (by omega)

theorem bloque_023 (q : ℕ) (hlo : 23553 ≤ q)
    (hhi : q ≤ 24576) : CertificadoAritmetico q := by
  have he : Encierra 23552 ⟨144375271170262, 144375271170263, 37330⟩ := by decide +kernel
  have hc : recorrer 23552 ⟨144375271170262, 144375271170263, 37330⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 23552 ⟨144375271170262, 144375271170263, 37330⟩ he hc q (by omega) (by omega)

theorem bloque_024 (q : ℕ) (hlo : 24577 ≤ q)
    (hhi : q ≤ 25600) : CertificadoAritmetico q := by
  have he : Encierra 24576 ⟨144535551272979, 144535551272980, 38953⟩ := by decide +kernel
  have hc : recorrer 24576 ⟨144535551272979, 144535551272980, 38953⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 24576 ⟨144535551272979, 144535551272980, 38953⟩ he hc q (by omega) (by omega)

theorem bloque_025 (q : ℕ) (hlo : 25601 ≤ q)
    (hhi : q ≤ 26624) : CertificadoAritmetico q := by
  have he : Encierra 25600 ⟨144696009312756, 144696009312757, 40576⟩ := by decide +kernel
  have hc : recorrer 25600 ⟨144696009312756, 144696009312757, 40576⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 25600 ⟨144696009312756, 144696009312757, 40576⟩ he hc q (by omega) (by omega)

theorem bloque_026 (q : ℕ) (hlo : 26625 ≤ q)
    (hhi : q ≤ 27648) : CertificadoAritmetico q := by
  have he : Encierra 26624 ⟨144856645487132, 144856645487133, 42199⟩ := by decide +kernel
  have hc : recorrer 26624 ⟨144856645487132, 144856645487133, 42199⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 26624 ⟨144856645487132, 144856645487133, 42199⟩ he hc q (by omega) (by omega)

theorem bloque_027 (q : ℕ) (hlo : 27649 ≤ q)
    (hhi : q ≤ 28672) : CertificadoAritmetico q := by
  have he : Encierra 27648 ⟨145017459993866, 145017459993867, 43822⟩ := by decide +kernel
  have hc : recorrer 27648 ⟨145017459993866, 145017459993867, 43822⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 27648 ⟨145017459993866, 145017459993867, 43822⟩ he hc q (by omega) (by omega)

theorem bloque_028 (q : ℕ) (hlo : 28673 ≤ q)
    (hhi : q ≤ 29696) : CertificadoAritmetico q := by
  have he : Encierra 28672 ⟨145178453030936, 145178453030937, 45445⟩ := by decide +kernel
  have hc : recorrer 28672 ⟨145178453030936, 145178453030937, 45445⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 28672 ⟨145178453030936, 145178453030937, 45445⟩ he hc q (by omega) (by omega)

theorem bloque_029 (q : ℕ) (hlo : 29697 ≤ q)
    (hhi : q ≤ 30720) : CertificadoAritmetico q := by
  have he : Encierra 29696 ⟨145339624796540, 145339624796541, 47068⟩ := by decide +kernel
  have hc : recorrer 29696 ⟨145339624796540, 145339624796541, 47068⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 29696 ⟨145339624796540, 145339624796541, 47068⟩ he hc q (by omega) (by omega)

theorem bloque_030 (q : ℕ) (hlo : 30721 ≤ q)
    (hhi : q ≤ 31744) : CertificadoAritmetico q := by
  have he : Encierra 30720 ⟨145500975489096, 145500975489097, 48691⟩ := by decide +kernel
  have hc : recorrer 30720 ⟨145500975489096, 145500975489097, 48691⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 30720 ⟨145500975489096, 145500975489097, 48691⟩ he hc q (by omega) (by omega)

theorem bloque_031 (q : ℕ) (hlo : 31745 ≤ q)
    (hhi : q ≤ 32768) : CertificadoAritmetico q := by
  have he : Encierra 31744 ⟨145662505307241, 145662505307242, 50314⟩ := by decide +kernel
  have hc : recorrer 31744 ⟨145662505307241, 145662505307242, 50314⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 31744 ⟨145662505307241, 145662505307242, 50314⟩ he hc q (by omega) (by omega)

theorem bloque_032 (q : ℕ) (hlo : 32769 ≤ q)
    (hhi : q ≤ 33792) : CertificadoAritmetico q := by
  have he : Encierra 32768 ⟨145824214449834, 145824214449835, 51937⟩ := by decide +kernel
  have hc : recorrer 32768 ⟨145824214449834, 145824214449835, 51937⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 32768 ⟨145824214449834, 145824214449835, 51937⟩ he hc q (by omega) (by omega)

theorem bloque_033 (q : ℕ) (hlo : 33793 ≤ q)
    (hhi : q ≤ 34816) : CertificadoAritmetico q := by
  have he : Encierra 33792 ⟨145986103115955, 145986103115956, 53560⟩ := by decide +kernel
  have hc : recorrer 33792 ⟨145986103115955, 145986103115956, 53560⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 33792 ⟨145986103115955, 145986103115956, 53560⟩ he hc q (by omega) (by omega)

theorem bloque_034 (q : ℕ) (hlo : 34817 ≤ q)
    (hhi : q ≤ 35840) : CertificadoAritmetico q := by
  have he : Encierra 34816 ⟨146148171504904, 146148171504905, 55183⟩ := by decide +kernel
  have hc : recorrer 34816 ⟨146148171504904, 146148171504905, 55183⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 34816 ⟨146148171504904, 146148171504905, 55183⟩ he hc q (by omega) (by omega)

theorem bloque_035 (q : ℕ) (hlo : 35841 ≤ q)
    (hhi : q ≤ 36864) : CertificadoAritmetico q := by
  have he : Encierra 35840 ⟨146310419816202, 146310419816203, 56806⟩ := by decide +kernel
  have hc : recorrer 35840 ⟨146310419816202, 146310419816203, 56806⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 35840 ⟨146310419816202, 146310419816203, 56806⟩ he hc q (by omega) (by omega)

theorem bloque_036 (q : ℕ) (hlo : 36865 ≤ q)
    (hhi : q ≤ 37888) : CertificadoAritmetico q := by
  have he : Encierra 36864 ⟨146472848249594, 146472848249595, 58429⟩ := by decide +kernel
  have hc : recorrer 36864 ⟨146472848249594, 146472848249595, 58429⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 36864 ⟨146472848249594, 146472848249595, 58429⟩ he hc q (by omega) (by omega)

theorem bloque_037 (q : ℕ) (hlo : 37889 ≤ q)
    (hhi : q ≤ 38912) : CertificadoAritmetico q := by
  have he : Encierra 37888 ⟨146635457005043, 146635457005044, 60052⟩ := by decide +kernel
  have hc : recorrer 37888 ⟨146635457005043, 146635457005044, 60052⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 37888 ⟨146635457005043, 146635457005044, 60052⟩ he hc q (by omega) (by omega)

theorem bloque_038 (q : ℕ) (hlo : 38913 ≤ q)
    (hhi : q ≤ 39936) : CertificadoAritmetico q := by
  have he : Encierra 38912 ⟨146798246282737, 146798246282738, 61675⟩ := by decide +kernel
  have hc : recorrer 38912 ⟨146798246282737, 146798246282738, 61675⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 38912 ⟨146798246282737, 146798246282738, 61675⟩ he hc q (by omega) (by omega)

theorem bloque_039 (q : ℕ) (hlo : 39937 ≤ q)
    (hhi : q ≤ 40960) : CertificadoAritmetico q := by
  have he : Encierra 39936 ⟨146961216283085, 146961216283086, 63298⟩ := by decide +kernel
  have hc : recorrer 39936 ⟨146961216283085, 146961216283086, 63298⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 39936 ⟨146961216283085, 146961216283086, 63298⟩ he hc q (by omega) (by omega)

theorem bloque_040 (q : ℕ) (hlo : 40961 ≤ q)
    (hhi : q ≤ 41984) : CertificadoAritmetico q := by
  have he : Encierra 40960 ⟨147124367206718, 147124367206719, 64921⟩ := by decide +kernel
  have hc : recorrer 40960 ⟨147124367206718, 147124367206719, 64921⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 40960 ⟨147124367206718, 147124367206719, 64921⟩ he hc q (by omega) (by omega)

theorem bloque_041 (q : ℕ) (hlo : 41985 ≤ q)
    (hhi : q ≤ 43008) : CertificadoAritmetico q := by
  have he : Encierra 41984 ⟨147287699254491, 147287699254492, 66544⟩ := by decide +kernel
  have hc : recorrer 41984 ⟨147287699254491, 147287699254492, 66544⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 41984 ⟨147287699254491, 147287699254492, 66544⟩ he hc q (by omega) (by omega)

theorem bloque_042 (q : ℕ) (hlo : 43009 ≤ q)
    (hhi : q ≤ 44032) : CertificadoAritmetico q := by
  have he : Encierra 43008 ⟨147451212627481, 147451212627482, 68167⟩ := by decide +kernel
  have hc : recorrer 43008 ⟨147451212627481, 147451212627482, 68167⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 43008 ⟨147451212627481, 147451212627482, 68167⟩ he hc q (by omega) (by omega)

theorem bloque_043 (q : ℕ) (hlo : 44033 ≤ q)
    (hhi : q ≤ 45056) : CertificadoAritmetico q := by
  have he : Encierra 44032 ⟨147614907526989, 147614907526990, 69790⟩ := by decide +kernel
  have hc : recorrer 44032 ⟨147614907526989, 147614907526990, 69790⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 44032 ⟨147614907526989, 147614907526990, 69790⟩ he hc q (by omega) (by omega)

theorem bloque_044 (q : ℕ) (hlo : 45057 ≤ q)
    (hhi : q ≤ 46080) : CertificadoAritmetico q := by
  have he : Encierra 45056 ⟨147778784154539, 147778784154540, 71413⟩ := by decide +kernel
  have hc : recorrer 45056 ⟨147778784154539, 147778784154540, 71413⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 45056 ⟨147778784154539, 147778784154540, 71413⟩ he hc q (by omega) (by omega)

theorem bloque_045 (q : ℕ) (hlo : 46081 ≤ q)
    (hhi : q ≤ 47104) : CertificadoAritmetico q := by
  have he : Encierra 46080 ⟨147942842711878, 147942842711879, 73036⟩ := by decide +kernel
  have hc : recorrer 46080 ⟨147942842711878, 147942842711879, 73036⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 46080 ⟨147942842711878, 147942842711879, 73036⟩ he hc q (by omega) (by omega)

theorem bloque_046 (q : ℕ) (hlo : 47105 ≤ q)
    (hhi : q ≤ 48128) : CertificadoAritmetico q := by
  have he : Encierra 47104 ⟨148107083400978, 148107083400979, 74659⟩ := by decide +kernel
  have hc : recorrer 47104 ⟨148107083400978, 148107083400979, 74659⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 47104 ⟨148107083400978, 148107083400979, 74659⟩ he hc q (by omega) (by omega)

theorem bloque_047 (q : ℕ) (hlo : 48129 ≤ q)
    (hhi : q ≤ 49152) : CertificadoAritmetico q := by
  have he : Encierra 48128 ⟨148271506424036, 148271506424037, 76282⟩ := by decide +kernel
  have hc : recorrer 48128 ⟨148271506424036, 148271506424037, 76282⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 48128 ⟨148271506424036, 148271506424037, 76282⟩ he hc q (by omega) (by omega)

theorem bloque_048 (q : ℕ) (hlo : 49153 ≤ q)
    (hhi : q ≤ 50176) : CertificadoAritmetico q := by
  have he : Encierra 49152 ⟨148436111983471, 148436111983472, 77905⟩ := by decide +kernel
  have hc : recorrer 49152 ⟨148436111983471, 148436111983472, 77905⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 49152 ⟨148436111983471, 148436111983472, 77905⟩ he hc q (by omega) (by omega)

theorem bloque_049 (q : ℕ) (hlo : 50177 ≤ q)
    (hhi : q ≤ 51200) : CertificadoAritmetico q := by
  have he : Encierra 50176 ⟨148600900281929, 148600900281930, 79528⟩ := by decide +kernel
  have hc : recorrer 50176 ⟨148600900281929, 148600900281930, 79528⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 50176 ⟨148600900281929, 148600900281930, 79528⟩ he hc q (by omega) (by omega)

theorem bloque_050 (q : ℕ) (hlo : 51201 ≤ q)
    (hhi : q ≤ 52224) : CertificadoAritmetico q := by
  have he : Encierra 51200 ⟨148765871522280, 148765871522281, 81151⟩ := by decide +kernel
  have hc : recorrer 51200 ⟨148765871522280, 148765871522281, 81151⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 51200 ⟨148765871522280, 148765871522281, 81151⟩ he hc q (by omega) (by omega)

theorem bloque_051 (q : ℕ) (hlo : 52225 ≤ q)
    (hhi : q ≤ 53248) : CertificadoAritmetico q := by
  have he : Encierra 52224 ⟨148931025907619, 148931025907620, 82774⟩ := by decide +kernel
  have hc : recorrer 52224 ⟨148931025907619, 148931025907620, 82774⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 52224 ⟨148931025907619, 148931025907620, 82774⟩ he hc q (by omega) (by omega)

theorem bloque_052 (q : ℕ) (hlo : 53249 ≤ q)
    (hhi : q ≤ 54272) : CertificadoAritmetico q := by
  have he : Encierra 53248 ⟨149096363641268, 149096363641269, 84397⟩ := by decide +kernel
  have hc : recorrer 53248 ⟨149096363641268, 149096363641269, 84397⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 53248 ⟨149096363641268, 149096363641269, 84397⟩ he hc q (by omega) (by omega)

theorem bloque_053 (q : ℕ) (hlo : 54273 ≤ q)
    (hhi : q ≤ 55296) : CertificadoAritmetico q := by
  have he : Encierra 54272 ⟨149261884926772, 149261884926773, 86020⟩ := by decide +kernel
  have hc : recorrer 54272 ⟨149261884926772, 149261884926773, 86020⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 54272 ⟨149261884926772, 149261884926773, 86020⟩ he hc q (by omega) (by omega)

theorem bloque_054 (q : ℕ) (hlo : 55297 ≤ q)
    (hhi : q ≤ 56320) : CertificadoAritmetico q := by
  have he : Encierra 55296 ⟨149427589967904, 149427589967905, 87643⟩ := by decide +kernel
  have hc : recorrer 55296 ⟨149427589967904, 149427589967905, 87643⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 55296 ⟨149427589967904, 149427589967905, 87643⟩ he hc q (by omega) (by omega)

theorem bloque_055 (q : ℕ) (hlo : 56321 ≤ q)
    (hhi : q ≤ 57344) : CertificadoAritmetico q := by
  have he : Encierra 56320 ⟨149593478968663, 149593478968664, 89266⟩ := by decide +kernel
  have hc : recorrer 56320 ⟨149593478968663, 149593478968664, 89266⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 56320 ⟨149593478968663, 149593478968664, 89266⟩ he hc q (by omega) (by omega)

theorem bloque_056 (q : ℕ) (hlo : 57345 ≤ q)
    (hhi : q ≤ 58368) : CertificadoAritmetico q := by
  have he : Encierra 57344 ⟨149759552133274, 149759552133275, 90889⟩ := by decide +kernel
  have hc : recorrer 57344 ⟨149759552133274, 149759552133275, 90889⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 57344 ⟨149759552133274, 149759552133275, 90889⟩ he hc q (by omega) (by omega)

theorem bloque_057 (q : ℕ) (hlo : 58369 ≤ q)
    (hhi : q ≤ 59392) : CertificadoAritmetico q := by
  have he : Encierra 58368 ⟨149925809666190, 149925809666191, 92512⟩ := by decide +kernel
  have hc : recorrer 58368 ⟨149925809666190, 149925809666191, 92512⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 58368 ⟨149925809666190, 149925809666191, 92512⟩ he hc q (by omega) (by omega)

theorem bloque_058 (q : ℕ) (hlo : 59393 ≤ q)
    (hhi : q ≤ 60416) : CertificadoAritmetico q := by
  have he : Encierra 59392 ⟨150092251772088, 150092251772089, 94135⟩ := by decide +kernel
  have hc : recorrer 59392 ⟨150092251772088, 150092251772089, 94135⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 59392 ⟨150092251772088, 150092251772089, 94135⟩ he hc q (by omega) (by omega)

theorem bloque_059 (q : ℕ) (hlo : 60417 ≤ q)
    (hhi : q ≤ 61440) : CertificadoAritmetico q := by
  have he : Encierra 60416 ⟨150258878655875, 150258878655876, 95758⟩ := by decide +kernel
  have hc : recorrer 60416 ⟨150258878655875, 150258878655876, 95758⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 60416 ⟨150258878655875, 150258878655876, 95758⟩ he hc q (by omega) (by omega)

theorem bloque_060 (q : ℕ) (hlo : 61441 ≤ q)
    (hhi : q ≤ 62464) : CertificadoAritmetico q := by
  have he : Encierra 61440 ⟨150425690522684, 150425690522685, 97381⟩ := by decide +kernel
  have hc : recorrer 61440 ⟨150425690522684, 150425690522685, 97381⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 61440 ⟨150425690522684, 150425690522685, 97381⟩ he hc q (by omega) (by omega)

theorem bloque_061 (q : ℕ) (hlo : 62465 ≤ q)
    (hhi : q ≤ 63488) : CertificadoAritmetico q := by
  have he : Encierra 62464 ⟨150592687577878, 150592687577879, 99004⟩ := by decide +kernel
  have hc : recorrer 62464 ⟨150592687577878, 150592687577879, 99004⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 62464 ⟨150592687577878, 150592687577879, 99004⟩ he hc q (by omega) (by omega)

theorem bloque_062 (q : ℕ) (hlo : 63489 ≤ q)
    (hhi : q ≤ 64512) : CertificadoAritmetico q := by
  have he : Encierra 63488 ⟨150759870027045, 150759870027046, 100627⟩ := by decide +kernel
  have hc : recorrer 63488 ⟨150759870027045, 150759870027046, 100627⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 63488 ⟨150759870027045, 150759870027046, 100627⟩ he hc q (by omega) (by omega)

theorem bloque_063 (q : ℕ) (hlo : 64513 ≤ q)
    (hhi : q ≤ 65536) : CertificadoAritmetico q := by
  have he : Encierra 64512 ⟨150927238076002, 150927238076003, 102250⟩ := by decide +kernel
  have hc : recorrer 64512 ⟨150927238076002, 150927238076003, 102250⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 64512 ⟨150927238076002, 150927238076003, 102250⟩ he hc q (by omega) (by omega)

theorem bloque_064 (q : ℕ) (hlo : 65537 ≤ q)
    (hhi : q ≤ 66560) : CertificadoAritmetico q := by
  have he : Encierra 65536 ⟨151094791930797, 151094791930798, 103873⟩ := by decide +kernel
  have hc : recorrer 65536 ⟨151094791930797, 151094791930798, 103873⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 65536 ⟨151094791930797, 151094791930798, 103873⟩ he hc q (by omega) (by omega)

theorem bloque_065 (q : ℕ) (hlo : 66561 ≤ q)
    (hhi : q ≤ 67584) : CertificadoAritmetico q := by
  have he : Encierra 66560 ⟨151262531797703, 151262531797704, 105496⟩ := by decide +kernel
  have hc : recorrer 66560 ⟨151262531797703, 151262531797704, 105496⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 66560 ⟨151262531797703, 151262531797704, 105496⟩ he hc q (by omega) (by omega)

theorem bloque_066 (q : ℕ) (hlo : 67585 ≤ q)
    (hhi : q ≤ 68608) : CertificadoAritmetico q := by
  have he : Encierra 67584 ⟨151430457883224, 151430457883225, 107119⟩ := by decide +kernel
  have hc : recorrer 67584 ⟨151430457883224, 151430457883225, 107119⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 67584 ⟨151430457883224, 151430457883225, 107119⟩ he hc q (by omega) (by omega)

theorem bloque_067 (q : ℕ) (hlo : 68609 ≤ q)
    (hhi : q ≤ 69632) : CertificadoAritmetico q := by
  have he : Encierra 68608 ⟨151598570394094, 151598570394095, 108742⟩ := by decide +kernel
  have hc : recorrer 68608 ⟨151598570394094, 151598570394095, 108742⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 68608 ⟨151598570394094, 151598570394095, 108742⟩ he hc q (by omega) (by omega)

theorem bloque_068 (q : ℕ) (hlo : 69633 ≤ q)
    (hhi : q ≤ 70656) : CertificadoAritmetico q := by
  have he : Encierra 69632 ⟨151766869537275, 151766869537276, 110365⟩ := by decide +kernel
  have hc : recorrer 69632 ⟨151766869537275, 151766869537276, 110365⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 69632 ⟨151766869537275, 151766869537276, 110365⟩ he hc q (by omega) (by omega)

theorem bloque_069 (q : ℕ) (hlo : 70657 ≤ q)
    (hhi : q ≤ 71680) : CertificadoAritmetico q := by
  have he : Encierra 70656 ⟨151935355519959, 151935355519960, 111988⟩ := by decide +kernel
  have hc : recorrer 70656 ⟨151935355519959, 151935355519960, 111988⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 70656 ⟨151935355519959, 151935355519960, 111988⟩ he hc q (by omega) (by omega)

theorem bloque_070 (q : ℕ) (hlo : 71681 ≤ q)
    (hhi : q ≤ 72704) : CertificadoAritmetico q := by
  have he : Encierra 71680 ⟨152104028549569, 152104028549570, 113611⟩ := by decide +kernel
  have hc : recorrer 71680 ⟨152104028549569, 152104028549570, 113611⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 71680 ⟨152104028549569, 152104028549570, 113611⟩ he hc q (by omega) (by omega)

theorem bloque_071 (q : ℕ) (hlo : 72705 ≤ q)
    (hhi : q ≤ 73728) : CertificadoAritmetico q := by
  have he : Encierra 72704 ⟨152272888833757, 152272888833758, 115234⟩ := by decide +kernel
  have hc : recorrer 72704 ⟨152272888833757, 152272888833758, 115234⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 72704 ⟨152272888833757, 152272888833758, 115234⟩ he hc q (by omega) (by omega)

theorem bloque_072 (q : ℕ) (hlo : 73729 ≤ q)
    (hhi : q ≤ 74752) : CertificadoAritmetico q := by
  have he : Encierra 73728 ⟨152441936580407, 152441936580408, 116857⟩ := by decide +kernel
  have hc : recorrer 73728 ⟨152441936580407, 152441936580408, 116857⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 73728 ⟨152441936580407, 152441936580408, 116857⟩ he hc q (by omega) (by omega)

theorem bloque_073 (q : ℕ) (hlo : 74753 ≤ q)
    (hhi : q ≤ 75776) : CertificadoAritmetico q := by
  have he : Encierra 74752 ⟨152611171997631, 152611171997632, 118480⟩ := by decide +kernel
  have hc : recorrer 74752 ⟨152611171997631, 152611171997632, 118480⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 74752 ⟨152611171997631, 152611171997632, 118480⟩ he hc q (by omega) (by omega)

theorem bloque_074 (q : ℕ) (hlo : 75777 ≤ q)
    (hhi : q ≤ 76800) : CertificadoAritmetico q := by
  have he : Encierra 75776 ⟨152780595293776, 152780595293777, 120103⟩ := by decide +kernel
  have hc : recorrer 75776 ⟨152780595293776, 152780595293777, 120103⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 75776 ⟨152780595293776, 152780595293777, 120103⟩ he hc q (by omega) (by omega)

theorem bloque_075 (q : ℕ) (hlo : 76801 ≤ q)
    (hhi : q ≤ 77824) : CertificadoAritmetico q := by
  have he : Encierra 76800 ⟨152950206677418, 152950206677419, 121726⟩ := by decide +kernel
  have hc : recorrer 76800 ⟨152950206677418, 152950206677419, 121726⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 76800 ⟨152950206677418, 152950206677419, 121726⟩ he hc q (by omega) (by omega)

theorem bloque_076 (q : ℕ) (hlo : 77825 ≤ q)
    (hhi : q ≤ 78848) : CertificadoAritmetico q := by
  have he : Encierra 77824 ⟨153120006357364, 153120006357365, 123349⟩ := by decide +kernel
  have hc : recorrer 77824 ⟨153120006357364, 153120006357365, 123349⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 77824 ⟨153120006357364, 153120006357365, 123349⟩ he hc q (by omega) (by omega)

theorem bloque_077 (q : ℕ) (hlo : 78849 ≤ q)
    (hhi : q ≤ 79872) : CertificadoAritmetico q := by
  have he : Encierra 78848 ⟨153289994542653, 153289994542654, 124972⟩ := by decide +kernel
  have hc : recorrer 78848 ⟨153289994542653, 153289994542654, 124972⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 78848 ⟨153289994542653, 153289994542654, 124972⟩ he hc q (by omega) (by omega)

theorem bloque_078 (q : ℕ) (hlo : 79873 ≤ q)
    (hhi : q ≤ 80896) : CertificadoAritmetico q := by
  have he : Encierra 79872 ⟨153460171442558, 153460171442559, 126595⟩ := by decide +kernel
  have hc : recorrer 79872 ⟨153460171442558, 153460171442559, 126595⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 79872 ⟨153460171442558, 153460171442559, 126595⟩ he hc q (by omega) (by omega)

theorem bloque_079 (q : ℕ) (hlo : 80897 ≤ q)
    (hhi : q ≤ 81920) : CertificadoAritmetico q := by
  have he : Encierra 80896 ⟨153630537266583, 153630537266584, 128218⟩ := by decide +kernel
  have hc : recorrer 80896 ⟨153630537266583, 153630537266584, 128218⟩ 1024 = true := by decide +kernel
  exact recorrer_correcto 1024 80896 ⟨153630537266583, 153630537266584, 128218⟩ he hc q (by omega) (by omega)

theorem bloque_080 (q : ℕ) (hlo : 81921 ≤ q)
    (hhi : q ≤ 82696) : CertificadoAritmetico q := by
  have he : Encierra 81920 ⟨153801092224464, 153801092224465, 129841⟩ := by decide +kernel
  have hc : recorrer 81920 ⟨153801092224464, 153801092224465, 129841⟩ 776 = true := by decide +kernel
  exact recorrer_correcto 776 81920 ⟨153801092224464, 153801092224465, 129841⟩ he hc q (by omega) (by omega)

theorem criba_certificada : ∀ q, 1 ≤ q → q ≤ 82696 → CertificadoAritmetico q := by
  intro q hlo hhi
  by_cases h40960 : q ≤ 40960
  ·
    by_cases h20480 : q ≤ 20480
    ·
      by_cases h10240 : q ≤ 10240
      ·
        by_cases h5120 : q ≤ 5120
        ·
          by_cases h2048 : q ≤ 2048
          ·
            by_cases h1024 : q ≤ 1024
            ·
              exact bloque_000 q (by omega) (by omega)
            ·
              exact bloque_001 q (by omega) (by omega)
          ·
            by_cases h3072 : q ≤ 3072
            ·
              exact bloque_002 q (by omega) (by omega)
            ·
              by_cases h4096 : q ≤ 4096
              ·
                exact bloque_003 q (by omega) (by omega)
              ·
                exact bloque_004 q (by omega) (by omega)
        ·
          by_cases h7168 : q ≤ 7168
          ·
            by_cases h6144 : q ≤ 6144
            ·
              exact bloque_005 q (by omega) (by omega)
            ·
              exact bloque_006 q (by omega) (by omega)
          ·
            by_cases h8192 : q ≤ 8192
            ·
              exact bloque_007 q (by omega) (by omega)
            ·
              by_cases h9216 : q ≤ 9216
              ·
                exact bloque_008 q (by omega) (by omega)
              ·
                exact bloque_009 q (by omega) (by omega)
      ·
        by_cases h15360 : q ≤ 15360
        ·
          by_cases h12288 : q ≤ 12288
          ·
            by_cases h11264 : q ≤ 11264
            ·
              exact bloque_010 q (by omega) (by omega)
            ·
              exact bloque_011 q (by omega) (by omega)
          ·
            by_cases h13312 : q ≤ 13312
            ·
              exact bloque_012 q (by omega) (by omega)
            ·
              by_cases h14336 : q ≤ 14336
              ·
                exact bloque_013 q (by omega) (by omega)
              ·
                exact bloque_014 q (by omega) (by omega)
        ·
          by_cases h17408 : q ≤ 17408
          ·
            by_cases h16384 : q ≤ 16384
            ·
              exact bloque_015 q (by omega) (by omega)
            ·
              exact bloque_016 q (by omega) (by omega)
          ·
            by_cases h18432 : q ≤ 18432
            ·
              exact bloque_017 q (by omega) (by omega)
            ·
              by_cases h19456 : q ≤ 19456
              ·
                exact bloque_018 q (by omega) (by omega)
              ·
                exact bloque_019 q (by omega) (by omega)
    ·
      by_cases h30720 : q ≤ 30720
      ·
        by_cases h25600 : q ≤ 25600
        ·
          by_cases h22528 : q ≤ 22528
          ·
            by_cases h21504 : q ≤ 21504
            ·
              exact bloque_020 q (by omega) (by omega)
            ·
              exact bloque_021 q (by omega) (by omega)
          ·
            by_cases h23552 : q ≤ 23552
            ·
              exact bloque_022 q (by omega) (by omega)
            ·
              by_cases h24576 : q ≤ 24576
              ·
                exact bloque_023 q (by omega) (by omega)
              ·
                exact bloque_024 q (by omega) (by omega)
        ·
          by_cases h27648 : q ≤ 27648
          ·
            by_cases h26624 : q ≤ 26624
            ·
              exact bloque_025 q (by omega) (by omega)
            ·
              exact bloque_026 q (by omega) (by omega)
          ·
            by_cases h28672 : q ≤ 28672
            ·
              exact bloque_027 q (by omega) (by omega)
            ·
              by_cases h29696 : q ≤ 29696
              ·
                exact bloque_028 q (by omega) (by omega)
              ·
                exact bloque_029 q (by omega) (by omega)
      ·
        by_cases h35840 : q ≤ 35840
        ·
          by_cases h32768 : q ≤ 32768
          ·
            by_cases h31744 : q ≤ 31744
            ·
              exact bloque_030 q (by omega) (by omega)
            ·
              exact bloque_031 q (by omega) (by omega)
          ·
            by_cases h33792 : q ≤ 33792
            ·
              exact bloque_032 q (by omega) (by omega)
            ·
              by_cases h34816 : q ≤ 34816
              ·
                exact bloque_033 q (by omega) (by omega)
              ·
                exact bloque_034 q (by omega) (by omega)
        ·
          by_cases h37888 : q ≤ 37888
          ·
            by_cases h36864 : q ≤ 36864
            ·
              exact bloque_035 q (by omega) (by omega)
            ·
              exact bloque_036 q (by omega) (by omega)
          ·
            by_cases h38912 : q ≤ 38912
            ·
              exact bloque_037 q (by omega) (by omega)
            ·
              by_cases h39936 : q ≤ 39936
              ·
                exact bloque_038 q (by omega) (by omega)
              ·
                exact bloque_039 q (by omega) (by omega)
  ·
    by_cases h61440 : q ≤ 61440
    ·
      by_cases h51200 : q ≤ 51200
      ·
        by_cases h46080 : q ≤ 46080
        ·
          by_cases h43008 : q ≤ 43008
          ·
            by_cases h41984 : q ≤ 41984
            ·
              exact bloque_040 q (by omega) (by omega)
            ·
              exact bloque_041 q (by omega) (by omega)
          ·
            by_cases h44032 : q ≤ 44032
            ·
              exact bloque_042 q (by omega) (by omega)
            ·
              by_cases h45056 : q ≤ 45056
              ·
                exact bloque_043 q (by omega) (by omega)
              ·
                exact bloque_044 q (by omega) (by omega)
        ·
          by_cases h48128 : q ≤ 48128
          ·
            by_cases h47104 : q ≤ 47104
            ·
              exact bloque_045 q (by omega) (by omega)
            ·
              exact bloque_046 q (by omega) (by omega)
          ·
            by_cases h49152 : q ≤ 49152
            ·
              exact bloque_047 q (by omega) (by omega)
            ·
              by_cases h50176 : q ≤ 50176
              ·
                exact bloque_048 q (by omega) (by omega)
              ·
                exact bloque_049 q (by omega) (by omega)
      ·
        by_cases h56320 : q ≤ 56320
        ·
          by_cases h53248 : q ≤ 53248
          ·
            by_cases h52224 : q ≤ 52224
            ·
              exact bloque_050 q (by omega) (by omega)
            ·
              exact bloque_051 q (by omega) (by omega)
          ·
            by_cases h54272 : q ≤ 54272
            ·
              exact bloque_052 q (by omega) (by omega)
            ·
              by_cases h55296 : q ≤ 55296
              ·
                exact bloque_053 q (by omega) (by omega)
              ·
                exact bloque_054 q (by omega) (by omega)
        ·
          by_cases h58368 : q ≤ 58368
          ·
            by_cases h57344 : q ≤ 57344
            ·
              exact bloque_055 q (by omega) (by omega)
            ·
              exact bloque_056 q (by omega) (by omega)
          ·
            by_cases h59392 : q ≤ 59392
            ·
              exact bloque_057 q (by omega) (by omega)
            ·
              by_cases h60416 : q ≤ 60416
              ·
                exact bloque_058 q (by omega) (by omega)
              ·
                exact bloque_059 q (by omega) (by omega)
    ·
      by_cases h71680 : q ≤ 71680
      ·
        by_cases h66560 : q ≤ 66560
        ·
          by_cases h63488 : q ≤ 63488
          ·
            by_cases h62464 : q ≤ 62464
            ·
              exact bloque_060 q (by omega) (by omega)
            ·
              exact bloque_061 q (by omega) (by omega)
          ·
            by_cases h64512 : q ≤ 64512
            ·
              exact bloque_062 q (by omega) (by omega)
            ·
              by_cases h65536 : q ≤ 65536
              ·
                exact bloque_063 q (by omega) (by omega)
              ·
                exact bloque_064 q (by omega) (by omega)
        ·
          by_cases h68608 : q ≤ 68608
          ·
            by_cases h67584 : q ≤ 67584
            ·
              exact bloque_065 q (by omega) (by omega)
            ·
              exact bloque_066 q (by omega) (by omega)
          ·
            by_cases h69632 : q ≤ 69632
            ·
              exact bloque_067 q (by omega) (by omega)
            ·
              by_cases h70656 : q ≤ 70656
              ·
                exact bloque_068 q (by omega) (by omega)
              ·
                exact bloque_069 q (by omega) (by omega)
      ·
        by_cases h76800 : q ≤ 76800
        ·
          by_cases h73728 : q ≤ 73728
          ·
            by_cases h72704 : q ≤ 72704
            ·
              exact bloque_070 q (by omega) (by omega)
            ·
              exact bloque_071 q (by omega) (by omega)
          ·
            by_cases h74752 : q ≤ 74752
            ·
              exact bloque_072 q (by omega) (by omega)
            ·
              by_cases h75776 : q ≤ 75776
              ·
                exact bloque_073 q (by omega) (by omega)
              ·
                exact bloque_074 q (by omega) (by omega)
        ·
          by_cases h79872 : q ≤ 79872
          ·
            by_cases h77824 : q ≤ 77824
            ·
              exact bloque_075 q (by omega) (by omega)
            ·
              by_cases h78848 : q ≤ 78848
              ·
                exact bloque_076 q (by omega) (by omega)
              ·
                exact bloque_077 q (by omega) (by omega)
          ·
            by_cases h80896 : q ≤ 80896
            ·
              exact bloque_078 q (by omega) (by omega)
            ·
              by_cases h81920 : q ≤ 81920
              ·
                exact bloque_079 q (by omega) (by omega)
              ·
                exact bloque_080 q (by omega) (by omega)

/-- Descenso para palabras reales de una a diez rachas; Rhin sigue explícito. -/
theorem ocelotas_diez (hR : RhinEntera) {n r : ℕ} {a b : ℕ → ℕ}
    (hn : 2 ≤ n) (hw : Palabra n a b r) (hr : 0 < r) (hr10 : r ≤ 10)
    (hk : PrimerCruce n (tiempo a b r)) : T^[tiempo a b r] n < n :=
  diez_de_certificado hR criba_certificada hn hw hr hr10 hk

end OcelotasCertificado

#print axioms OcelotasCertificado.criba_certificada
#print axioms OcelotasCertificado.ocelotas_diez
