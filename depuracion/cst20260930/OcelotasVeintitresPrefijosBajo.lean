import OcelotasVeintitresPrefijosBajoParte001
import OcelotasVeintitresPrefijosBajoParte002
import OcelotasVeintitresPrefijosBajoParte003
import OcelotasVeintitresPrefijosBajoParte004
import OcelotasVeintitresPrefijosBajoParte005
import OcelotasVeintitresPrefijosBajoParte006
import OcelotasVeintitresPrefijosBajoParte007
import OcelotasVeintitresPrefijosBajoParte008
import OcelotasVeintitresPrefijosBajoParte009
import OcelotasVeintitresPrefijosBajoParte010
import OcelotasVeintitresPrefijosBajoParte011
import OcelotasVeintitresPrefijosBajoParte012
import OcelotasVeintitresPrefijosBajoParte013
import OcelotasVeintitresPrefijosBajoParte014
import OcelotasVeintitresPrefijosBajoParte015
import OcelotasVeintitresPrefijosBajoParte016
import OcelotasVeintitresPrefijosBajoParte017
import OcelotasVeintitresPrefijosBajoParte018
import OcelotasVeintitresPrefijosBajoParte019
import OcelotasVeintitresPrefijosBajoParte020
import OcelotasVeintitresPrefijosBajoParte021
import OcelotasVeintitresPrefijosBajoParte022
import OcelotasVeintitresPrefijosBajoParte023
import OcelotasVeintitresPrefijosBajoParte024
import OcelotasVeintitresPrefijosBajoParte025
import OcelotasVeintitresPrefijosBajoParte026
import OcelotasVeintitresPrefijosBajoParte027
import OcelotasVeintitresPrefijosBajoParte028

/-! Propuesta generada; todas las condiciones se comprueban en Lean. -/
namespace OcelotasVeintitresPrefijosBajo
open Ocelotas OcelotasContador OcelotasCribaPrefijosBinarios
open OcelotasPrefijosTestigos OcelotasCertificadosTestigos

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem nodo_2 : comprobar 6276058 79335 23 4912743 4096 19683 23607800 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_0 nodo_1

theorem nodo_4 : comprobar 6276058 79335 23 4912743 2048 6561 15738533 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_2 nodo_3

theorem nodo_6 : comprobar 6276058 79335 23 4912743 1024 2187 10492355 7 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_4 nodo_5

theorem nodo_9 : comprobar 6276058 79335 23 4913255 2048 6561 15740173 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_7 nodo_8

theorem nodo_12 : comprobar 6276058 79335 23 4918375 8192 177147 106356887 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_10 nodo_11

theorem nodo_14 : comprobar 6276058 79335 23 4914279 4096 59049 70845542 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_13 nodo_12

theorem nodo_17 : comprobar 6276058 79335 23 4916327 4096 19683 23625022 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_15 nodo_16

theorem nodo_18 : comprobar 6276058 79335 23 4914279 2048 19683 47230361 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_14 nodo_17

theorem nodo_19 : comprobar 6276058 79335 23 4913255 1024 6561 31480346 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_9 nodo_18

theorem nodo_20 : comprobar 6276058 79335 23 4912743 512 2187 20984710 7 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_6 nodo_19

theorem nodo_23 : comprobar 6276058 79335 23 4912999 8192 59049 35413544 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_21 nodo_22

theorem nodo_26 : comprobar 6276058 79335 23 4917095 8192 177147 106329206 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_24 nodo_25

theorem nodo_27 : comprobar 6276058 79335 23 4912999 4096 59049 70827088 10 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_23 nodo_26

theorem nodo_30 : comprobar 6276058 79335 23 4915047 8192 177147 106284919 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_28 nodo_29

theorem nodo_33 : comprobar 6276058 79335 23 4927335 16384 1594323 479477879 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_31 nodo_32

theorem nodo_35 : comprobar 6276058 79335 23 4919143 8192 531441 319120478 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_34 nodo_33

theorem nodo_36 : comprobar 6276058 79335 23 4915047 4096 177147 212569838 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_30 nodo_35

theorem nodo_37 : comprobar 6276058 79335 23 4912999 2048 59049 141654176 10 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_27 nodo_36

theorem nodo_40 : comprobar 6276058 79335 23 4914023 4096 19683 23613950 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_38 nodo_39

theorem nodo_43 : comprobar 6276058 79335 23 4916071 8192 177147 106307063 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_41 nodo_42

theorem nodo_45 : comprobar 6276058 79335 23 4916071 4096 59049 70871375 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_43 nodo_44

theorem nodo_46 : comprobar 6276058 79335 23 4914023 2048 19683 47227900 9 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_40 nodo_45

theorem nodo_47 : comprobar 6276058 79335 23 4912999 1024 19683 94436117 9 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_37 nodo_46

theorem nodo_50 : comprobar 6276058 79335 23 4913511 4096 19683 23611490 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_48 nodo_49

theorem nodo_52 : comprobar 6276058 79335 23 4913511 2048 6561 15740993 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_50 nodo_51

theorem nodo_55 : comprobar 6276058 79335 23 4918631 8192 177147 106362422 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_53 nodo_54

theorem nodo_57 : comprobar 6276058 79335 23 4914535 4096 59049 70849232 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_56 nodo_55

theorem nodo_59 : comprobar 6276058 79335 23 4914535 2048 19683 47232821 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_57 nodo_58

theorem nodo_60 : comprobar 6276058 79335 23 4913511 1024 6561 31481986 8 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_52 nodo_59

theorem nodo_61 : comprobar 6276058 79335 23 4912999 512 6561 62957411 8 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_47 nodo_60

theorem nodo_62 : comprobar 6276058 79335 23 4912743 256 2187 41969420 7 2 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_20 nodo_61

theorem nodo_65 : comprobar 6276058 79335 23 4912871 2048 6561 15738943 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_63 nodo_64

theorem nodo_68 : comprobar 6276058 79335 23 4913895 8192 177147 106260011 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_66 nodo_67

theorem nodo_70 : comprobar 6276058 79335 23 4913895 4096 59049 70840007 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_68 nodo_69

theorem nodo_73 : comprobar 6276058 79335 23 4915943 4096 19683 23623177 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_71 nodo_72

theorem nodo_74 : comprobar 6276058 79335 23 4913895 2048 19683 47226671 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_70 nodo_73

theorem nodo_75 : comprobar 6276058 79335 23 4912871 1024 6561 31477886 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_65 nodo_74

theorem nodo_78 : comprobar 6276058 79335 23 4914407 2048 6561 15743864 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_76 nodo_77

theorem nodo_80 : comprobar 6276058 79335 23 4913383 1024 2187 10493722 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_79 nodo_78

theorem nodo_81 : comprobar 6276058 79335 23 4912871 512 2187 20985257 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_75 nodo_80

theorem nodo_84 : comprobar 6276058 79335 23 4915687 4096 19683 23621948 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_82 nodo_83

theorem nodo_86 : comprobar 6276058 79335 23 4913639 2048 6561 15741404 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_85 nodo_84

theorem nodo_88 : comprobar 6276058 79335 23 4913639 1024 2187 10494269 7 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_86 nodo_87

theorem nodo_90 : comprobar 6276058 79335 23 4913127 512 729 6995450 6 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_89 nodo_88

theorem nodo_91 : comprobar 6276058 79335 23 4912871 256 729 13990171 6 2 false 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_81 nodo_90

theorem nodo_92 : comprobar 6276058 79335 23 4912743 128 729 27979613 6 2 true 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_62 nodo_91

theorem nodo_95 : comprobar 6276058 79335 23 4913831 2048 6561 15742019 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_93 nodo_94

theorem nodo_97 : comprobar 6276058 79335 23 4912807 1024 2187 10492492 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_96 nodo_95

theorem nodo_100 : comprobar 6276058 79335 23 4913319 4096 19683 23610568 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_98 nodo_99

theorem nodo_103 : comprobar 6276058 79335 23 4915367 8192 177147 106291844 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_101 nodo_102

theorem nodo_105 : comprobar 6276058 79335 23 4915367 4096 59049 70861229 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_103 nodo_104

theorem nodo_106 : comprobar 6276058 79335 23 4913319 2048 19683 47221136 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_100 nodo_105

theorem nodo_109 : comprobar 6276058 79335 23 4914343 2048 6561 15743659 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_107 nodo_108

theorem nodo_110 : comprobar 6276058 79335 23 4913319 1024 6561 31480757 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_106 nodo_109

theorem nodo_111 : comprobar 6276058 79335 23 4912807 512 2187 20984984 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_97 nodo_110

theorem nodo_114 : comprobar 6276058 79335 23 4913063 2048 6561 15739559 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_112 nodo_113

theorem nodo_116 : comprobar 6276058 79335 23 4913063 1024 2187 10493039 7 4 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_114 nodo_115

theorem nodo_118 : comprobar 6276058 79335 23 4913063 512 729 6995359 6 3 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_116 nodo_117

theorem nodo_119 : comprobar 6276058 79335 23 4912807 256 729 13989989 6 3 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_111 nodo_118

theorem nodo_121 : comprobar 6276058 79335 23 4912807 128 243 9326659 5 2 false 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_119 nodo_120

theorem nodo_122 : comprobar 6276058 79335 23 4912743 64 243 18653075 5 2 true 122 = true := by
  exact acepta_rama (by decide +kernel) nodo_92 nodo_121

theorem nodo_125 : comprobar 6276058 79335 23 4913991 2048 6561 15742532 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_123 nodo_124

theorem nodo_127 : comprobar 6276058 79335 23 4912967 1024 2187 10492834 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_126 nodo_125

theorem nodo_130 : comprobar 6276058 79335 23 4913479 8192 177147 106251020 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_128 nodo_129

theorem nodo_132 : comprobar 6276058 79335 23 4913479 4096 59049 70834013 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_130 nodo_131

theorem nodo_135 : comprobar 6276058 79335 23 4915527 4096 19683 23621179 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_133 nodo_134

theorem nodo_136 : comprobar 6276058 79335 23 4913479 2048 19683 47222675 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_132 nodo_135

theorem nodo_139 : comprobar 6276058 79335 23 4914503 2048 6561 15744172 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_137 nodo_138

theorem nodo_140 : comprobar 6276058 79335 23 4913479 1024 6561 31481783 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_136 nodo_139

theorem nodo_141 : comprobar 6276058 79335 23 4912967 512 2187 20985668 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_127 nodo_140

theorem nodo_144 : comprobar 6276058 79335 23 4913223 2048 6561 15740072 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_142 nodo_143

theorem nodo_146 : comprobar 6276058 79335 23 4913223 1024 2187 10493381 7 4 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_144 nodo_145

theorem nodo_148 : comprobar 6276058 79335 23 4913223 512 729 6995587 6 3 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_146 nodo_147

theorem nodo_149 : comprobar 6276058 79335 23 4912967 256 729 13990445 6 3 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_141 nodo_148

theorem nodo_151 : comprobar 6276058 79335 23 4912839 128 243 9326720 5 3 true 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_150 nodo_149

theorem nodo_153 : comprobar 6276058 79335 23 4912775 64 81 6217732 4 2 false 122 = true := by
  exact acepta_rama (by decide +kernel) nodo_152 nodo_151

theorem nodo_154 : comprobar 6276058 79335 23 4912743 32 81 12435383 4 2 true 123 = true := by
  exact acepta_rama (by decide +kernel) nodo_122 nodo_153

theorem nodo_156 : comprobar 6276058 79335 23 4912743 16 27 8290255 3 1 false 124 = true := by
  exact acepta_rama (by decide +kernel) nodo_154 nodo_155

theorem nodo_159 : comprobar 6276058 79335 23 4913775 2048 6561 15741839 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_157 nodo_158

theorem nodo_161 : comprobar 6276058 79335 23 4912751 1024 2187 10492372 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_160 nodo_159

theorem nodo_164 : comprobar 6276058 79335 23 4913263 4096 19683 23610298 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_162 nodo_163

theorem nodo_167 : comprobar 6276058 79335 23 4915311 8192 177147 106290629 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_165 nodo_166

theorem nodo_169 : comprobar 6276058 79335 23 4915311 4096 59049 70860419 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_167 nodo_168

theorem nodo_170 : comprobar 6276058 79335 23 4913263 2048 19683 47220596 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_164 nodo_169

theorem nodo_173 : comprobar 6276058 79335 23 4914287 2048 6561 15743479 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_171 nodo_172

theorem nodo_174 : comprobar 6276058 79335 23 4913263 1024 6561 31480397 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_170 nodo_173

theorem nodo_175 : comprobar 6276058 79335 23 4912751 512 2187 20984744 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_161 nodo_174

theorem nodo_178 : comprobar 6276058 79335 23 4913007 4096 19683 23609069 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_176 nodo_177

theorem nodo_180 : comprobar 6276058 79335 23 4913007 2048 6561 15739379 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_178 nodo_179

theorem nodo_182 : comprobar 6276058 79335 23 4913007 1024 2187 10492919 7 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_180 nodo_181

theorem nodo_184 : comprobar 6276058 79335 23 4913007 512 729 6995279 6 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_182 nodo_183

theorem nodo_185 : comprobar 6276058 79335 23 4912751 256 729 13989829 6 2 false 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_175 nodo_184

theorem nodo_188 : comprobar 6276058 79335 23 4914927 4096 19683 23618294 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_186 nodo_187

theorem nodo_190 : comprobar 6276058 79335 23 4912879 2048 6561 15738968 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_189 nodo_188

theorem nodo_193 : comprobar 6276058 79335 23 4913903 4096 19683 23613373 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_191 nodo_192

theorem nodo_196 : comprobar 6276058 79335 23 4920047 8192 177147 106393040 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_194 nodo_195

theorem nodo_198 : comprobar 6276058 79335 23 4915951 4096 59049 70869644 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_197 nodo_196

theorem nodo_199 : comprobar 6276058 79335 23 4913903 2048 19683 47226746 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_193 nodo_198

theorem nodo_200 : comprobar 6276058 79335 23 4912879 1024 6561 31477936 8 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_190 nodo_199

theorem nodo_203 : comprobar 6276058 79335 23 4917487 8192 177147 106337681 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_201 nodo_202

theorem nodo_205 : comprobar 6276058 79335 23 4913391 4096 59049 70832738 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_204 nodo_203

theorem nodo_208 : comprobar 6276058 79335 23 4915439 4096 19683 23620754 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_206 nodo_207

theorem nodo_209 : comprobar 6276058 79335 23 4913391 2048 19683 47221825 9 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_205 nodo_208

theorem nodo_212 : comprobar 6276058 79335 23 4914415 8192 59049 35423750 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_210 nodo_211

theorem nodo_215 : comprobar 6276058 79335 23 4918511 8192 177147 106359824 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_213 nodo_214

theorem nodo_216 : comprobar 6276058 79335 23 4914415 4096 59049 70847500 10 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_212 nodo_215

theorem nodo_219 : comprobar 6276058 79335 23 4916463 8192 177147 106315537 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_217 nodo_218

theorem nodo_222 : comprobar 6276058 79335 23 4928751 16384 1594323 479615660 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_220 nodo_221

theorem nodo_224 : comprobar 6276058 79335 23 4920559 8192 531441 319212332 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_223 nodo_222

theorem nodo_225 : comprobar 6276058 79335 23 4916463 4096 177147 212631074 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_219 nodo_224

theorem nodo_226 : comprobar 6276058 79335 23 4914415 2048 59049 141695000 10 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_216 nodo_225

theorem nodo_227 : comprobar 6276058 79335 23 4913391 1024 19683 94443650 9 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_209 nodo_226

theorem nodo_228 : comprobar 6276058 79335 23 4912879 512 6561 62955872 8 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_200 nodo_227

theorem nodo_231 : comprobar 6276058 79335 23 4914159 4096 19683 23614604 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_229 nodo_230

theorem nodo_233 : comprobar 6276058 79335 23 4914159 2048 6561 15743069 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_231 nodo_232

theorem nodo_235 : comprobar 6276058 79335 23 4913135 1024 2187 10493192 7 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_234 nodo_233

theorem nodo_238 : comprobar 6276058 79335 23 4919791 8192 177147 106387505 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_236 nodo_237

theorem nodo_240 : comprobar 6276058 79335 23 4915695 4096 59049 70865954 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_239 nodo_238

theorem nodo_242 : comprobar 6276058 79335 23 4913647 2048 19683 47224286 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_241 nodo_240

theorem nodo_245 : comprobar 6276058 79335 23 4914671 2048 6561 15744709 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_243 nodo_244

theorem nodo_246 : comprobar 6276058 79335 23 4913647 1024 6561 31482857 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_242 nodo_245

theorem nodo_247 : comprobar 6276058 79335 23 4913135 512 2187 20986384 7 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_235 nodo_246

theorem nodo_248 : comprobar 6276058 79335 23 4912879 256 2187 41970581 7 2 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_228 nodo_247

theorem nodo_249 : comprobar 6276058 79335 23 4912751 128 729 27979658 6 2 true 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_185 nodo_248

theorem nodo_252 : comprobar 6276058 79335 23 4914479 2048 6561 15744095 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_250 nodo_251

theorem nodo_254 : comprobar 6276058 79335 23 4913455 1024 2187 10493876 7 4 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_253 nodo_252

theorem nodo_256 : comprobar 6276058 79335 23 4912943 512 729 6995188 6 3 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_255 nodo_254

theorem nodo_259 : comprobar 6276058 79335 23 4913199 2048 6561 15739994 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_257 nodo_258

theorem nodo_261 : comprobar 6276058 79335 23 4913199 1024 2187 10493329 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_259 nodo_260

theorem nodo_264 : comprobar 6276058 79335 23 4913711 2048 6561 15741634 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_262 nodo_263

theorem nodo_267 : comprobar 6276058 79335 23 4914735 4096 19683 23617372 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_265 nodo_266

theorem nodo_270 : comprobar 6276058 79335 23 4916783 8192 177147 106322462 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_268 nodo_269

theorem nodo_272 : comprobar 6276058 79335 23 4916783 4096 59049 70881641 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_270 nodo_271

theorem nodo_273 : comprobar 6276058 79335 23 4914735 2048 19683 47234744 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_267 nodo_272

theorem nodo_274 : comprobar 6276058 79335 23 4913711 1024 6561 31483268 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_264 nodo_273

theorem nodo_275 : comprobar 6276058 79335 23 4913199 512 2187 20986658 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_261 nodo_274

theorem nodo_276 : comprobar 6276058 79335 23 4912943 256 729 13990376 6 3 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_256 nodo_275

theorem nodo_278 : comprobar 6276058 79335 23 4912815 128 243 9326674 5 2 false 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_277 nodo_276

theorem nodo_279 : comprobar 6276058 79335 23 4912751 64 243 18653105 5 2 true 122 = true := by
  exact acepta_rama (by decide +kernel) nodo_249 nodo_278

theorem nodo_282 : comprobar 6276058 79335 23 4912847 4096 19683 23608300 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_280 nodo_281

theorem nodo_285 : comprobar 6276058 79335 23 4914895 8192 177147 106281638 11 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_283 nodo_284

theorem nodo_288 : comprobar 6276058 79335 23 4918991 8192 59049 35456737 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_286 nodo_287

theorem nodo_289 : comprobar 6276058 79335 23 4914895 4096 59049 70854425 10 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_285 nodo_288

theorem nodo_290 : comprobar 6276058 79335 23 4912847 2048 19683 47216600 9 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_282 nodo_289

theorem nodo_293 : comprobar 6276058 79335 23 4913871 4096 19683 23613221 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_291 nodo_292

theorem nodo_295 : comprobar 6276058 79335 23 4913871 2048 6561 15742147 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_293 nodo_294

theorem nodo_296 : comprobar 6276058 79335 23 4912847 1024 6561 31477733 8 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_290 nodo_295

theorem nodo_299 : comprobar 6276058 79335 23 4913359 4096 19683 23610761 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_297 nodo_298

theorem nodo_301 : comprobar 6276058 79335 23 4913359 2048 6561 15740507 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_299 nodo_300

theorem nodo_303 : comprobar 6276058 79335 23 4913359 1024 2187 10493671 7 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_301 nodo_302

theorem nodo_304 : comprobar 6276058 79335 23 4912847 512 2187 20985155 7 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_296 nodo_303

theorem nodo_307 : comprobar 6276058 79335 23 4916687 4096 19683 23626754 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_305 nodo_306

theorem nodo_309 : comprobar 6276058 79335 23 4914639 2048 6561 15744608 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_308 nodo_307

theorem nodo_311 : comprobar 6276058 79335 23 4913615 1024 2187 10494218 7 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_310 nodo_309

theorem nodo_313 : comprobar 6276058 79335 23 4913103 512 729 6995416 6 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_312 nodo_311

theorem nodo_314 : comprobar 6276058 79335 23 4912847 256 729 13990103 6 2 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_304 nodo_313

theorem nodo_316 : comprobar 6276058 79335 23 4912847 128 243 9326735 5 2 true 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_314 nodo_315

theorem nodo_318 : comprobar 6276058 79335 23 4912783 64 81 6217742 4 1 false 122 = true := by
  exact acepta_rama (by decide +kernel) nodo_317 nodo_316

theorem nodo_319 : comprobar 6276058 79335 23 4912751 32 81 12435403 4 1 false 123 = true := by
  exact acepta_rama (by decide +kernel) nodo_279 nodo_318

theorem nodo_322 : comprobar 6276058 79335 23 4912767 8192 59049 35411870 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_320 nodo_321

theorem nodo_325 : comprobar 6276058 79335 23 4916863 8192 177147 106324184 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_323 nodo_324

theorem nodo_326 : comprobar 6276058 79335 23 4912767 4096 59049 70823740 10 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_322 nodo_325

theorem nodo_329 : comprobar 6276058 79335 23 4914815 8192 177147 106279897 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_327 nodo_328

theorem nodo_332 : comprobar 6276058 79335 23 4927103 16384 1594323 479455280 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_330 nodo_331

theorem nodo_334 : comprobar 6276058 79335 23 4918911 8192 531441 319105412 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_333 nodo_332

theorem nodo_335 : comprobar 6276058 79335 23 4914815 4096 177147 212559794 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_329 nodo_334

theorem nodo_336 : comprobar 6276058 79335 23 4912767 2048 59049 141647480 10 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_326 nodo_335

theorem nodo_339 : comprobar 6276058 79335 23 4913791 4096 19683 23612834 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_337 nodo_338

theorem nodo_342 : comprobar 6276058 79335 23 4915839 8192 177147 106302041 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_340 nodo_341

theorem nodo_344 : comprobar 6276058 79335 23 4915839 4096 59049 70868027 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_342 nodo_343

theorem nodo_345 : comprobar 6276058 79335 23 4913791 2048 19683 47225668 9 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_339 nodo_344

theorem nodo_346 : comprobar 6276058 79335 23 4912767 1024 19683 94431653 9 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_336 nodo_345

theorem nodo_349 : comprobar 6276058 79335 23 4913279 4096 19683 23610374 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_347 nodo_348

theorem nodo_351 : comprobar 6276058 79335 23 4913279 2048 6561 15740249 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_349 nodo_350

theorem nodo_354 : comprobar 6276058 79335 23 4918399 8192 177147 106357400 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_352 nodo_353

theorem nodo_356 : comprobar 6276058 79335 23 4914303 4096 59049 70845884 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_355 nodo_354

theorem nodo_359 : comprobar 6276058 79335 23 4916351 4096 19683 23625136 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_357 nodo_358

theorem nodo_360 : comprobar 6276058 79335 23 4914303 2048 19683 47230589 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_356 nodo_359

theorem nodo_361 : comprobar 6276058 79335 23 4913279 1024 6561 31480498 8 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_351 nodo_360

theorem nodo_362 : comprobar 6276058 79335 23 4912767 512 6561 62954435 8 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_346 nodo_361

theorem nodo_365 : comprobar 6276058 79335 23 4913023 4096 19683 23609144 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_363 nodo_364

theorem nodo_367 : comprobar 6276058 79335 23 4913023 2048 6561 15739429 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_365 nodo_366

theorem nodo_370 : comprobar 6276058 79335 23 4918143 8192 177147 106351865 11 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_368 nodo_369

theorem nodo_372 : comprobar 6276058 79335 23 4914047 4096 59049 70842194 10 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_371 nodo_370

theorem nodo_375 : comprobar 6276058 79335 23 4916095 4096 19683 23623906 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_373 nodo_374

theorem nodo_376 : comprobar 6276058 79335 23 4914047 2048 19683 47228129 9 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_372 nodo_375

theorem nodo_377 : comprobar 6276058 79335 23 4913023 1024 6561 31478858 8 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_367 nodo_376

theorem nodo_380 : comprobar 6276058 79335 23 4916607 8192 59049 35439551 10 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_378 nodo_379

theorem nodo_382 : comprobar 6276058 79335 23 4916607 4096 19683 23626367 9 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_380 nodo_381

theorem nodo_384 : comprobar 6276058 79335 23 4914559 2048 6561 15744350 8 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_383 nodo_382

theorem nodo_386 : comprobar 6276058 79335 23 4913535 1024 2187 10494046 7 1 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_385 nodo_384

theorem nodo_387 : comprobar 6276058 79335 23 4913023 512 2187 20985905 7 1 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_377 nodo_386

theorem nodo_388 : comprobar 6276058 79335 23 4912767 256 2187 41969623 7 1 false 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_362 nodo_387

theorem nodo_391 : comprobar 6276058 79335 23 4912895 8192 177147 106238378 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_389 nodo_390

theorem nodo_393 : comprobar 6276058 79335 23 4912895 4096 59049 70825585 10 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_391 nodo_392

theorem nodo_396 : comprobar 6276058 79335 23 4923135 16384 1594323 479069153 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_394 nodo_395

theorem nodo_398 : comprobar 6276058 79335 23 4914943 8192 531441 318847994 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_397 nodo_396

theorem nodo_401 : comprobar 6276058 79335 23 4919039 8192 177147 106371238 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_399 nodo_400

theorem nodo_402 : comprobar 6276058 79335 23 4914943 4096 177147 212565329 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_398 nodo_401

theorem nodo_403 : comprobar 6276058 79335 23 4912895 2048 59049 141651170 10 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_393 nodo_402

theorem nodo_406 : comprobar 6276058 79335 23 4913919 4096 19683 23613449 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_404 nodo_405

theorem nodo_409 : comprobar 6276058 79335 23 4920063 8192 177147 106393382 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_407 nodo_408

theorem nodo_411 : comprobar 6276058 79335 23 4915967 4096 59049 70869872 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_410 nodo_409

theorem nodo_412 : comprobar 6276058 79335 23 4913919 2048 19683 47226898 9 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_406 nodo_411

theorem nodo_413 : comprobar 6276058 79335 23 4912895 1024 19683 94434113 9 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_403 nodo_412

theorem nodo_416 : comprobar 6276058 79335 23 4913407 8192 59049 35416484 10 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_414 nodo_415

theorem nodo_418 : comprobar 6276058 79335 23 4913407 4096 19683 23610989 9 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_416 nodo_417

theorem nodo_420 : comprobar 6276058 79335 23 4913407 2048 6561 15740659 8 1 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_418 nodo_419

theorem nodo_423 : comprobar 6276058 79335 23 4914431 8192 177147 106271594 11 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_421 nodo_422

theorem nodo_425 : comprobar 6276058 79335 23 4914431 4096 59049 70847729 10 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_423 nodo_424

theorem nodo_428 : comprobar 6276058 79335 23 4916479 4096 19683 23625751 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_426 nodo_427

theorem nodo_429 : comprobar 6276058 79335 23 4914431 2048 19683 47231819 9 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_425 nodo_428

theorem nodo_430 : comprobar 6276058 79335 23 4913407 1024 6561 31481318 8 1 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_420 nodo_429

theorem nodo_431 : comprobar 6276058 79335 23 4912895 512 6561 62956075 8 1 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_413 nodo_430

theorem nodo_434 : comprobar 6276058 79335 23 4913151 8192 177147 106243913 11 1 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_432 nodo_433

theorem nodo_437 : comprobar 6276058 79335 23 4925439 16384 1594323 479293352 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_435 nodo_436

theorem nodo_439 : comprobar 6276058 79335 23 4917247 8192 531441 318997460 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_438 nodo_437

theorem nodo_440 : comprobar 6276058 79335 23 4913151 4096 177147 212487826 11 1 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_434 nodo_439

theorem nodo_443 : comprobar 6276058 79335 23 4915199 16384 4782969 1434890699 14 1 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_441 nodo_442

theorem nodo_446 : comprobar 6276058 79335 23 4923391 16384 1594323 479094061 13 1 false 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_444 nodo_445

theorem nodo_447 : comprobar 6276058 79335 23 4915199 8192 1594323 956593799 13 1 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_443 nodo_446

theorem nodo_450 : comprobar 6276058 79335 23 4919295 16384 531441 159565160 12 1 false 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_448 nodo_449

theorem nodo_453 : comprobar 6276058 79335 23 4927487 16384 1594323 479492642 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_451 nodo_452

theorem nodo_454 : comprobar 6276058 79335 23 4919295 8192 531441 319130320 12 1 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_450 nodo_453

theorem nodo_455 : comprobar 6276058 79335 23 4915199 4096 531441 637729199 12 1 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_447 nodo_454

theorem nodo_456 : comprobar 6276058 79335 23 4913151 2048 177147 424975652 11 1 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_440 nodo_455

theorem nodo_459 : comprobar 6276058 79335 23 4922367 16384 1594323 478994417 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_457 nodo_458

theorem nodo_461 : comprobar 6276058 79335 23 4914175 8192 531441 318798170 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_460 nodo_459

theorem nodo_464 : comprobar 6276058 79335 23 4918271 8192 177147 106354630 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_462 nodo_463

theorem nodo_465 : comprobar 6276058 79335 23 4914175 4096 177147 212532113 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_461 nodo_464

theorem nodo_468 : comprobar 6276058 79335 23 4916223 8192 59049 35436781 10 1 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_466 nodo_467

theorem nodo_471 : comprobar 6276058 79335 23 4920319 16384 531441 159598376 12 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_469 nodo_470

theorem nodo_473 : comprobar 6276058 79335 23 4920319 8192 177147 106398917 11 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_471 nodo_472

theorem nodo_474 : comprobar 6276058 79335 23 4916223 4096 59049 70873562 10 1 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_468 nodo_473

theorem nodo_475 : comprobar 6276058 79335 23 4914175 2048 59049 141688075 10 1 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_465 nodo_474

theorem nodo_476 : comprobar 6276058 79335 23 4913151 1024 59049 283317101 10 1 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_456 nodo_475

theorem nodo_479 : comprobar 6276058 79335 23 4913663 8192 177147 106254985 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_477 nodo_478

theorem nodo_482 : comprobar 6276058 79335 23 4925951 16384 1594323 479343176 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_480 nodo_481

theorem nodo_484 : comprobar 6276058 79335 23 4917759 8192 531441 319030676 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_483 nodo_482

theorem nodo_485 : comprobar 6276058 79335 23 4913663 4096 177147 212509970 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_479 nodo_484

theorem nodo_488 : comprobar 6276058 79335 23 4915711 8192 177147 106299272 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_486 nodo_487

theorem nodo_490 : comprobar 6276058 79335 23 4915711 4096 59049 70866181 10 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_488 nodo_489

theorem nodo_491 : comprobar 6276058 79335 23 4913663 2048 59049 141673313 10 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_485 nodo_490

theorem nodo_494 : comprobar 6276058 79335 23 4914687 8192 177147 106277129 11 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_492 nodo_493

theorem nodo_496 : comprobar 6276058 79335 23 4914687 4096 59049 70851419 10 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_494 nodo_495

theorem nodo_499 : comprobar 6276058 79335 23 4916735 8192 59049 35440472 10 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_497 nodo_498

theorem nodo_501 : comprobar 6276058 79335 23 4916735 4096 19683 23626981 9 1 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_499 nodo_500

theorem nodo_502 : comprobar 6276058 79335 23 4914687 2048 19683 47234279 9 1 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_496 nodo_501

theorem nodo_503 : comprobar 6276058 79335 23 4913663 1024 19683 94448875 9 1 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_491 nodo_502

theorem nodo_504 : comprobar 6276058 79335 23 4913151 512 19683 188878067 9 1 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_476 nodo_503

theorem nodo_505 : comprobar 6276058 79335 23 4912895 256 6561 125912150 8 1 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_431 nodo_504

theorem nodo_506 : comprobar 6276058 79335 23 4912767 128 2187 83939246 7 1 true 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_388 nodo_505

theorem nodo_509 : comprobar 6276058 79335 23 4912831 2048 6561 15738814 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_507 nodo_508

theorem nodo_512 : comprobar 6276058 79335 23 4913855 4096 19683 23613142 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_510 nodo_511

theorem nodo_515 : comprobar 6276058 79335 23 4915903 8192 177147 106303427 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_513 nodo_514

theorem nodo_517 : comprobar 6276058 79335 23 4915903 4096 59049 70868951 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_515 nodo_516

theorem nodo_518 : comprobar 6276058 79335 23 4913855 2048 19683 47226284 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_512 nodo_517

theorem nodo_519 : comprobar 6276058 79335 23 4912831 1024 6561 31477628 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_509 nodo_518

theorem nodo_522 : comprobar 6276058 79335 23 4914367 4096 19683 23615603 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_520 nodo_521

theorem nodo_524 : comprobar 6276058 79335 23 4914367 2048 6561 15743735 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_522 nodo_523

theorem nodo_526 : comprobar 6276058 79335 23 4913343 1024 2187 10493636 7 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_525 nodo_524

theorem nodo_527 : comprobar 6276058 79335 23 4912831 512 2187 20985085 7 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_519 nodo_526

theorem nodo_530 : comprobar 6276058 79335 23 4915135 4096 19683 23619293 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_528 nodo_529

theorem nodo_532 : comprobar 6276058 79335 23 4913087 2048 6561 15739634 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_531 nodo_530

theorem nodo_535 : comprobar 6276058 79335 23 4914111 4096 19683 23614372 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_533 nodo_534

theorem nodo_538 : comprobar 6276058 79335 23 4916159 8192 177147 106308962 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_536 nodo_537

theorem nodo_540 : comprobar 6276058 79335 23 4916159 4096 59049 70872641 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_538 nodo_539

theorem nodo_541 : comprobar 6276058 79335 23 4914111 2048 19683 47228744 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_535 nodo_540

theorem nodo_542 : comprobar 6276058 79335 23 4913087 1024 6561 31479268 8 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_532 nodo_541

theorem nodo_545 : comprobar 6276058 79335 23 4913599 8192 177147 106253603 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_543 nodo_544

theorem nodo_547 : comprobar 6276058 79335 23 4913599 4096 59049 70835735 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_545 nodo_546

theorem nodo_550 : comprobar 6276058 79335 23 4915647 4096 19683 23621753 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_548 nodo_549

theorem nodo_551 : comprobar 6276058 79335 23 4913599 2048 19683 47223823 9 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_547 nodo_550

theorem nodo_554 : comprobar 6276058 79335 23 4914623 8192 177147 106275746 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_552 nodo_553

theorem nodo_556 : comprobar 6276058 79335 23 4914623 4096 59049 70850497 10 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_554 nodo_555

theorem nodo_559 : comprobar 6276058 79335 23 4924863 16384 1594323 479237309 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_557 nodo_558

theorem nodo_561 : comprobar 6276058 79335 23 4916671 8192 531441 318960098 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_560 nodo_559

theorem nodo_564 : comprobar 6276058 79335 23 4920767 8192 177147 106408606 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_562 nodo_563

theorem nodo_565 : comprobar 6276058 79335 23 4916671 4096 177147 212640065 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_561 nodo_564

theorem nodo_566 : comprobar 6276058 79335 23 4914623 2048 59049 141700994 10 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_556 nodo_565

theorem nodo_567 : comprobar 6276058 79335 23 4913599 1024 19683 94447646 9 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_551 nodo_566

theorem nodo_568 : comprobar 6276058 79335 23 4913087 512 6561 62958536 8 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_542 nodo_567

theorem nodo_569 : comprobar 6276058 79335 23 4912831 256 2187 41970170 7 2 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_527 nodo_568

theorem nodo_572 : comprobar 6276058 79335 23 4913983 4096 19683 23613758 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_570 nodo_571

theorem nodo_574 : comprobar 6276058 79335 23 4913983 2048 6561 15742505 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_572 nodo_573

theorem nodo_576 : comprobar 6276058 79335 23 4912959 1024 2187 10492816 7 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_575 nodo_574

theorem nodo_579 : comprobar 6276058 79335 23 4913471 4096 19683 23611297 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_577 nodo_578

theorem nodo_582 : comprobar 6276058 79335 23 4927807 16384 531441 159841268 12 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_580 nodo_581

theorem nodo_584 : comprobar 6276058 79335 23 4919615 8192 177147 106383698 11 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_583 nodo_582

theorem nodo_586 : comprobar 6276058 79335 23 4915519 4096 59049 70863416 10 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_585 nodo_584

theorem nodo_587 : comprobar 6276058 79335 23 4913471 2048 19683 47222594 9 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_579 nodo_586

theorem nodo_590 : comprobar 6276058 79335 23 4914495 4096 19683 23616218 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_588 nodo_589

theorem nodo_592 : comprobar 6276058 79335 23 4914495 2048 6561 15744145 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_590 nodo_591

theorem nodo_593 : comprobar 6276058 79335 23 4913471 1024 6561 31481729 8 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_587 nodo_592

theorem nodo_594 : comprobar 6276058 79335 23 4912959 512 2187 20985632 7 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_576 nodo_593

theorem nodo_597 : comprobar 6276058 79335 23 4917311 8192 59049 35444627 10 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_595 nodo_596

theorem nodo_599 : comprobar 6276058 79335 23 4913215 4096 19683 23610068 9 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_598 nodo_597

theorem nodo_601 : comprobar 6276058 79335 23 4913215 2048 6561 15740045 8 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_599 nodo_600

theorem nodo_603 : comprobar 6276058 79335 23 4913215 1024 2187 10493363 7 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_601 nodo_602

theorem nodo_605 : comprobar 6276058 79335 23 4913215 512 729 6995575 6 1 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_603 nodo_604

theorem nodo_606 : comprobar 6276058 79335 23 4912959 256 729 13990421 6 1 false 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_594 nodo_605

theorem nodo_607 : comprobar 6276058 79335 23 4912831 128 729 27980113 6 1 false 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_569 nodo_606

theorem nodo_608 : comprobar 6276058 79335 23 4912767 64 729 55959497 6 1 true 122 = true := by
  exact acepta_rama (by decide +kernel) nodo_506 nodo_607

theorem nodo_611 : comprobar 6276058 79335 23 4912799 8192 177147 106236305 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_609 nodo_610

theorem nodo_613 : comprobar 6276058 79335 23 4912799 4096 59049 70824203 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_611 nodo_612

theorem nodo_616 : comprobar 6276058 79335 23 4914847 4096 19683 23617909 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_614 nodo_615

theorem nodo_617 : comprobar 6276058 79335 23 4912799 2048 19683 47216135 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_613 nodo_616

theorem nodo_620 : comprobar 6276058 79335 23 4915871 4096 19683 23622830 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_618 nodo_619

theorem nodo_622 : comprobar 6276058 79335 23 4913823 2048 6561 15741992 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_621 nodo_620

theorem nodo_623 : comprobar 6276058 79335 23 4912799 1024 6561 31477423 8 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_617 nodo_622

theorem nodo_626 : comprobar 6276058 79335 23 4913311 16384 1594323 478113191 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_624 nodo_625

theorem nodo_628 : comprobar 6276058 79335 23 4913311 8192 531441 318742127 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_626 nodo_627

theorem nodo_631 : comprobar 6276058 79335 23 4917407 8192 177147 106335949 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_629 nodo_630

theorem nodo_632 : comprobar 6276058 79335 23 4913311 4096 177147 212494751 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_628 nodo_631

theorem nodo_635 : comprobar 6276058 79335 23 4919455 8192 177147 106380236 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_633 nodo_634

theorem nodo_637 : comprobar 6276058 79335 23 4915359 4096 59049 70861108 10 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_636 nodo_635

theorem nodo_638 : comprobar 6276058 79335 23 4913311 2048 59049 141663167 10 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_632 nodo_637

theorem nodo_641 : comprobar 6276058 79335 23 4918431 8192 177147 106358093 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_639 nodo_640

theorem nodo_643 : comprobar 6276058 79335 23 4914335 4096 59049 70846346 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_642 nodo_641

theorem nodo_646 : comprobar 6276058 79335 23 4916383 4096 19683 23625290 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_644 nodo_645

theorem nodo_647 : comprobar 6276058 79335 23 4914335 2048 19683 47230897 9 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_643 nodo_646

theorem nodo_648 : comprobar 6276058 79335 23 4913311 1024 19683 94442111 9 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_638 nodo_647

theorem nodo_649 : comprobar 6276058 79335 23 4912799 512 6561 62954846 8 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_623 nodo_648

theorem nodo_652 : comprobar 6276058 79335 23 4915103 4096 19683 23619140 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_650 nodo_651

theorem nodo_654 : comprobar 6276058 79335 23 4913055 2048 6561 15739532 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_653 nodo_652

theorem nodo_656 : comprobar 6276058 79335 23 4913055 1024 2187 10493021 7 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_654 nodo_655

theorem nodo_659 : comprobar 6276058 79335 23 4913567 2048 6561 15741172 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_657 nodo_658

theorem nodo_662 : comprobar 6276058 79335 23 4914591 4096 19683 23616679 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_660 nodo_661

theorem nodo_665 : comprobar 6276058 79335 23 4920735 8192 177147 106407917 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_663 nodo_664

theorem nodo_667 : comprobar 6276058 79335 23 4916639 4096 59049 70879562 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_666 nodo_665

theorem nodo_668 : comprobar 6276058 79335 23 4914591 2048 19683 47233358 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_662 nodo_667

theorem nodo_669 : comprobar 6276058 79335 23 4913567 1024 6561 31482344 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_659 nodo_668

theorem nodo_670 : comprobar 6276058 79335 23 4913055 512 2187 20986042 7 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_656 nodo_669

theorem nodo_671 : comprobar 6276058 79335 23 4912799 256 2187 41969897 7 2 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_649 nodo_670

theorem nodo_674 : comprobar 6276058 79335 23 4913951 4096 19683 23613605 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_672 nodo_673

theorem nodo_676 : comprobar 6276058 79335 23 4913951 2048 6561 15742403 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_674 nodo_675

theorem nodo_678 : comprobar 6276058 79335 23 4912927 1024 2187 10492748 7 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_677 nodo_676

theorem nodo_680 : comprobar 6276058 79335 23 4912927 512 729 6995165 6 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_678 nodo_679

theorem nodo_683 : comprobar 6276058 79335 23 4913183 2048 6561 15739942 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_681 nodo_682

theorem nodo_686 : comprobar 6276058 79335 23 4914207 4096 19683 23614834 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_684 nodo_685

theorem nodo_689 : comprobar 6276058 79335 23 4916255 8192 177147 106311041 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_687 nodo_688

theorem nodo_691 : comprobar 6276058 79335 23 4916255 4096 59049 70874027 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_689 nodo_690

theorem nodo_692 : comprobar 6276058 79335 23 4914207 2048 19683 47229668 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_686 nodo_691

theorem nodo_693 : comprobar 6276058 79335 23 4913183 1024 6561 31479884 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_683 nodo_692

theorem nodo_696 : comprobar 6276058 79335 23 4914719 2048 6561 15744863 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_694 nodo_695

theorem nodo_698 : comprobar 6276058 79335 23 4913695 1024 2187 10494388 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_697 nodo_696

theorem nodo_699 : comprobar 6276058 79335 23 4913183 512 2187 20986589 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_693 nodo_698

theorem nodo_700 : comprobar 6276058 79335 23 4912927 256 729 13990330 6 2 false 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_680 nodo_699

theorem nodo_701 : comprobar 6276058 79335 23 4912799 128 729 27979931 6 2 true 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_671 nodo_700

theorem nodo_704 : comprobar 6276058 79335 23 4915423 4096 19683 23620679 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_702 nodo_703

theorem nodo_706 : comprobar 6276058 79335 23 4913375 2048 6561 15740558 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_705 nodo_704

theorem nodo_708 : comprobar 6276058 79335 23 4913375 1024 2187 10493705 7 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_706 nodo_707

theorem nodo_710 : comprobar 6276058 79335 23 4912863 512 729 6995074 6 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_709 nodo_708

theorem nodo_713 : comprobar 6276058 79335 23 4916191 4096 19683 23624369 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_711 nodo_712

theorem nodo_715 : comprobar 6276058 79335 23 4914143 2048 6561 15743018 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_714 nodo_713

theorem nodo_717 : comprobar 6276058 79335 23 4913119 1024 2187 10493158 7 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_716 nodo_715

theorem nodo_720 : comprobar 6276058 79335 23 4917727 8192 177147 106342874 11 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_718 nodo_719

theorem nodo_722 : comprobar 6276058 79335 23 4913631 4096 59049 70836200 10 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_721 nodo_720

theorem nodo_725 : comprobar 6276058 79335 23 4915679 4096 19683 23621908 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_723 nodo_724

theorem nodo_726 : comprobar 6276058 79335 23 4913631 2048 19683 47224133 9 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_722 nodo_725

theorem nodo_729 : comprobar 6276058 79335 23 4916703 4096 19683 23626829 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_727 nodo_728

theorem nodo_731 : comprobar 6276058 79335 23 4914655 2048 6561 15744658 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_730 nodo_729

theorem nodo_732 : comprobar 6276058 79335 23 4913631 1024 6561 31482755 8 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_726 nodo_731

theorem nodo_733 : comprobar 6276058 79335 23 4913119 512 2187 20986316 7 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_717 nodo_732

theorem nodo_734 : comprobar 6276058 79335 23 4912863 256 729 13990148 6 2 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_710 nodo_733

theorem nodo_736 : comprobar 6276058 79335 23 4912863 128 243 9326765 5 1 false 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_734 nodo_735

theorem nodo_737 : comprobar 6276058 79335 23 4912799 64 243 18653287 5 1 false 122 = true := by
  exact acepta_rama (by decide +kernel) nodo_701 nodo_736

theorem nodo_738 : comprobar 6276058 79335 23 4912767 32 243 37306331 5 1 true 123 = true := by
  exact acepta_rama (by decide +kernel) nodo_608 nodo_737

theorem nodo_739 : comprobar 6276058 79335 23 4912751 16 81 24870806 4 1 true 124 = true := by
  exact acepta_rama (by decide +kernel) nodo_319 nodo_738

theorem nodo_740 : comprobar 6276058 79335 23 4912743 8 27 16580510 3 1 true 125 = true := by
  exact acepta_rama (by decide +kernel) nodo_156 nodo_739

theorem nodo_743 : comprobar 6276058 79335 23 4913915 2048 6561 15742289 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_741 nodo_742

theorem nodo_745 : comprobar 6276058 79335 23 4912891 1024 2187 10492672 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_744 nodo_743

theorem nodo_748 : comprobar 6276058 79335 23 4913403 4096 19683 23610973 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_746 nodo_747

theorem nodo_751 : comprobar 6276058 79335 23 4919547 8192 177147 106382240 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_749 nodo_750

theorem nodo_753 : comprobar 6276058 79335 23 4915451 4096 59049 70862444 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_752 nodo_751

theorem nodo_754 : comprobar 6276058 79335 23 4913403 2048 19683 47221946 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_748 nodo_753

theorem nodo_757 : comprobar 6276058 79335 23 4914427 2048 6561 15743929 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_755 nodo_756

theorem nodo_758 : comprobar 6276058 79335 23 4913403 1024 6561 31481297 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_754 nodo_757

theorem nodo_759 : comprobar 6276058 79335 23 4912891 512 2187 20985344 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_745 nodo_758

theorem nodo_762 : comprobar 6276058 79335 23 4913147 2048 6561 15739829 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_760 nodo_761

theorem nodo_764 : comprobar 6276058 79335 23 4913147 1024 2187 10493219 7 4 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_762 nodo_763

theorem nodo_766 : comprobar 6276058 79335 23 4913147 512 729 6995479 6 3 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_764 nodo_765

theorem nodo_767 : comprobar 6276058 79335 23 4912891 256 729 13990229 6 3 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_759 nodo_766

theorem nodo_769 : comprobar 6276058 79335 23 4912763 128 243 9326576 5 3 true 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_768 nodo_767

theorem nodo_771 : comprobar 6276058 79335 23 4912763 64 81 6217717 4 2 false 122 = true := by
  exact acepta_rama (by decide +kernel) nodo_769 nodo_770

theorem nodo_774 : comprobar 6276058 79335 23 4912795 2048 6561 15738700 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_772 nodo_773

theorem nodo_777 : comprobar 6276058 79335 23 4913819 4096 19683 23612971 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_775 nodo_776

theorem nodo_780 : comprobar 6276058 79335 23 4919963 8192 177147 106391231 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_778 nodo_779

theorem nodo_782 : comprobar 6276058 79335 23 4915867 4096 59049 70868438 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_781 nodo_780

theorem nodo_783 : comprobar 6276058 79335 23 4913819 2048 19683 47225942 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_777 nodo_782

theorem nodo_784 : comprobar 6276058 79335 23 4912795 1024 6561 31477400 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_774 nodo_783

theorem nodo_787 : comprobar 6276058 79335 23 4914331 2048 6561 15743621 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_785 nodo_786

theorem nodo_789 : comprobar 6276058 79335 23 4913307 1024 2187 10493560 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_788 nodo_787

theorem nodo_790 : comprobar 6276058 79335 23 4912795 512 2187 20984933 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_784 nodo_789

theorem nodo_793 : comprobar 6276058 79335 23 4913563 4096 19683 23611742 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_791 nodo_792

theorem nodo_795 : comprobar 6276058 79335 23 4913563 2048 6561 15741161 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_793 nodo_794

theorem nodo_797 : comprobar 6276058 79335 23 4913563 1024 2187 10494107 7 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_795 nodo_796

theorem nodo_799 : comprobar 6276058 79335 23 4913051 512 729 6995342 6 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_798 nodo_797

theorem nodo_800 : comprobar 6276058 79335 23 4912795 256 729 13989955 6 2 false 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_790 nodo_799

theorem nodo_803 : comprobar 6276058 79335 23 4912923 8192 177147 106238992 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_801 nodo_802

theorem nodo_806 : comprobar 6276058 79335 23 4917019 16384 1594323 478474046 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_804 nodo_805

theorem nodo_808 : comprobar 6276058 79335 23 4917019 8192 531441 318982697 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_806 nodo_807

theorem nodo_809 : comprobar 6276058 79335 23 4912923 4096 177147 212477984 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_803 nodo_808

theorem nodo_812 : comprobar 6276058 79335 23 4914971 8192 177147 106283279 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_810 nodo_811

theorem nodo_814 : comprobar 6276058 79335 23 4914971 4096 59049 70855519 10 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_812 nodo_813

theorem nodo_815 : comprobar 6276058 79335 23 4912923 2048 59049 141651989 10 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_809 nodo_814

theorem nodo_818 : comprobar 6276058 79335 23 4913947 8192 177147 106261136 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_816 nodo_817

theorem nodo_820 : comprobar 6276058 79335 23 4913947 4096 59049 70840757 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_818 nodo_819

theorem nodo_823 : comprobar 6276058 79335 23 4915995 4096 19683 23623427 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_821 nodo_822

theorem nodo_824 : comprobar 6276058 79335 23 4913947 2048 19683 47227171 9 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_820 nodo_823

theorem nodo_825 : comprobar 6276058 79335 23 4912923 1024 19683 94434659 9 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_815 nodo_824

theorem nodo_828 : comprobar 6276058 79335 23 4915483 4096 19683 23620967 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_826 nodo_827

theorem nodo_830 : comprobar 6276058 79335 23 4913435 2048 6561 15740750 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_829 nodo_828

theorem nodo_833 : comprobar 6276058 79335 23 4914459 4096 19683 23616046 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_831 nodo_832

theorem nodo_836 : comprobar 6276058 79335 23 4916507 8192 177147 106316495 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_834 nodo_835

theorem nodo_838 : comprobar 6276058 79335 23 4916507 4096 59049 70877663 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_836 nodo_837

theorem nodo_839 : comprobar 6276058 79335 23 4914459 2048 19683 47232092 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_833 nodo_838

theorem nodo_840 : comprobar 6276058 79335 23 4913435 1024 6561 31481500 8 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_830 nodo_839

theorem nodo_841 : comprobar 6276058 79335 23 4912923 512 6561 62956439 8 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_825 nodo_840

theorem nodo_844 : comprobar 6276058 79335 23 4913179 2048 6561 15739930 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_842 nodo_843

theorem nodo_847 : comprobar 6276058 79335 23 4914203 4096 19683 23614816 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_845 nodo_846

theorem nodo_850 : comprobar 6276058 79335 23 4916251 8192 177147 106310960 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_848 nodo_849

theorem nodo_852 : comprobar 6276058 79335 23 4916251 4096 59049 70873973 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_850 nodo_851

theorem nodo_853 : comprobar 6276058 79335 23 4914203 2048 19683 47229632 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_847 nodo_852

theorem nodo_854 : comprobar 6276058 79335 23 4913179 1024 6561 31479860 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_844 nodo_853

theorem nodo_857 : comprobar 6276058 79335 23 4914715 4096 19683 23617277 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_855 nodo_856

theorem nodo_859 : comprobar 6276058 79335 23 4914715 2048 6561 15744851 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_857 nodo_858

theorem nodo_861 : comprobar 6276058 79335 23 4913691 1024 2187 10494380 7 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_860 nodo_859

theorem nodo_862 : comprobar 6276058 79335 23 4913179 512 2187 20986573 7 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_854 nodo_861

theorem nodo_863 : comprobar 6276058 79335 23 4912923 256 2187 41970959 7 2 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_841 nodo_862

theorem nodo_864 : comprobar 6276058 79335 23 4912795 128 729 27979910 6 2 true 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_800 nodo_863

theorem nodo_867 : comprobar 6276058 79335 23 4912987 2048 6561 15739316 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_865 nodo_866

theorem nodo_869 : comprobar 6276058 79335 23 4912987 1024 2187 10492877 7 4 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_867 nodo_868

theorem nodo_871 : comprobar 6276058 79335 23 4912987 512 729 6995251 6 3 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_869 nodo_870

theorem nodo_874 : comprobar 6276058 79335 23 4913243 8192 177147 106245917 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_872 nodo_873

theorem nodo_876 : comprobar 6276058 79335 23 4913243 4096 59049 70830611 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_874 nodo_875

theorem nodo_879 : comprobar 6276058 79335 23 4915291 4096 19683 23620045 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_877 nodo_878

theorem nodo_880 : comprobar 6276058 79335 23 4913243 2048 19683 47220407 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_876 nodo_879

theorem nodo_883 : comprobar 6276058 79335 23 4914267 2048 6561 15743416 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_881 nodo_882

theorem nodo_884 : comprobar 6276058 79335 23 4913243 1024 6561 31480271 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_880 nodo_883

theorem nodo_887 : comprobar 6276058 79335 23 4913755 2048 6561 15741776 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_885 nodo_886

theorem nodo_889 : comprobar 6276058 79335 23 4913755 1024 2187 10494517 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_887 nodo_888

theorem nodo_890 : comprobar 6276058 79335 23 4913243 512 2187 20986847 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_884 nodo_889

theorem nodo_891 : comprobar 6276058 79335 23 4912987 256 729 13990502 6 3 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_871 nodo_890

theorem nodo_893 : comprobar 6276058 79335 23 4912859 128 243 9326758 5 2 false 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_892 nodo_891

theorem nodo_894 : comprobar 6276058 79335 23 4912795 64 243 18653273 5 2 true 122 = true := by
  exact acepta_rama (by decide +kernel) nodo_864 nodo_893

theorem nodo_895 : comprobar 6276058 79335 23 4912763 32 81 12435434 4 2 true 123 = true := by
  exact acepta_rama (by decide +kernel) nodo_771 nodo_894

theorem nodo_897 : comprobar 6276058 79335 23 4912747 16 27 8290262 3 2 true 124 = true := by
  exact acepta_rama (by decide +kernel) nodo_896 nodo_895

theorem nodo_899 : comprobar 6276058 79335 23 4912747 8 9 5526841 2 1 false 125 = true := by
  exact acepta_rama (by decide +kernel) nodo_897 nodo_898

theorem nodo_900 : comprobar 6276058 79335 23 4912743 4 9 11053673 2 1 true 126 = true := by
  exact acepta_rama (by decide +kernel) nodo_740 nodo_899

theorem nodo_902 : comprobar 6276058 79335 23 4912741 2 3 7369112 1 1 true 127 = true := by
  exact acepta_rama (by decide +kernel) nodo_901 nodo_900

theorem nodo_904 : comprobar 6276058 79335 23 4912741 1 1 4912741 0 0 false 128 = true := by
  exact acepta_rama (by decide +kernel) nodo_902 nodo_903

theorem certificado :
    comprobar 6276058 79335 23 4912741 1 1 4912741 0 0 false 128 = true := nodo_904

theorem descenso {n k : ℕ} (hinicio : 4912741 ≤ n) (hmax : n ≤ 6276058)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 23) (hq : 79335 ≤ S k n) :
    T^[k] n < n := OcelotasCribaPrefijosBinarios.certificado_descenso
      certificado hinicio hmax hk hr hq

end OcelotasVeintitresPrefijosBajo

#print axioms OcelotasVeintitresPrefijosBajo.certificado
#print axioms OcelotasVeintitresPrefijosBajo.descenso
