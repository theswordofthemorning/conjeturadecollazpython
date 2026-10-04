import OcelotasVeinticuatroPrefijosBajoParte001
import OcelotasVeinticuatroPrefijosBajoParte002
import OcelotasVeinticuatroPrefijosBajoParte003
import OcelotasVeinticuatroPrefijosBajoParte004
import OcelotasVeinticuatroPrefijosBajoParte005
import OcelotasVeinticuatroPrefijosBajoParte006
import OcelotasVeinticuatroPrefijosBajoParte007
import OcelotasVeinticuatroPrefijosBajoParte008
import OcelotasVeinticuatroPrefijosBajoParte009
import OcelotasVeinticuatroPrefijosBajoParte010
import OcelotasVeinticuatroPrefijosBajoParte011
import OcelotasVeinticuatroPrefijosBajoParte012
import OcelotasVeinticuatroPrefijosBajoParte013
import OcelotasVeinticuatroPrefijosBajoParte014
import OcelotasVeinticuatroPrefijosBajoParte015
import OcelotasVeinticuatroPrefijosBajoParte016
import OcelotasVeinticuatroPrefijosBajoParte017
import OcelotasVeinticuatroPrefijosBajoParte018
import OcelotasVeinticuatroPrefijosBajoParte019
import OcelotasVeinticuatroPrefijosBajoParte020
import OcelotasVeinticuatroPrefijosBajoParte021
import OcelotasVeinticuatroPrefijosBajoParte022
import OcelotasVeinticuatroPrefijosBajoParte023
import OcelotasVeinticuatroPrefijosBajoParte024
import OcelotasVeinticuatroPrefijosBajoParte025
import OcelotasVeinticuatroPrefijosBajoParte026
import OcelotasVeinticuatroPrefijosBajoParte027
import OcelotasVeinticuatroPrefijosBajoParte028
import OcelotasVeinticuatroPrefijosBajoParte029
import OcelotasVeinticuatroPrefijosBajoParte030
import OcelotasVeinticuatroPrefijosBajoParte031
import OcelotasVeinticuatroPrefijosBajoParte032
import OcelotasVeinticuatroPrefijosBajoParte033
import OcelotasVeinticuatroPrefijosBajoParte034
import OcelotasVeinticuatroPrefijosBajoParte035
import OcelotasVeinticuatroPrefijosBajoParte036
import OcelotasVeinticuatroPrefijosBajoParte037
import OcelotasVeinticuatroPrefijosBajoParte038
import OcelotasVeinticuatroPrefijosBajoParte039

/-! Propuesta generada; todas las condiciones se comprueban en Lean. -/
namespace OcelotasVeinticuatroPrefijosBajo
open Ocelotas OcelotasContador OcelotasCribaPrefijosBinarios
open OcelotasPrefijosTestigos OcelotasCertificadosTestigos

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem nodo_2 : comprobar 6548930 79335 24 4916839 8192 59049 35441225 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_0 nodo_1

theorem nodo_4 : comprobar 6548930 79335 24 4912743 4096 19683 23607800 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_3 nodo_2

theorem nodo_6 : comprobar 6548930 79335 24 4912743 2048 6561 15738533 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_4 nodo_5

theorem nodo_8 : comprobar 6548930 79335 24 4912743 1024 2187 10492355 7 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_6 nodo_7

theorem nodo_11 : comprobar 6548930 79335 24 4917351 8192 59049 35444915 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_9 nodo_10

theorem nodo_13 : comprobar 6548930 79335 24 4913255 4096 19683 23610260 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_12 nodo_11

theorem nodo_15 : comprobar 6548930 79335 24 4913255 2048 6561 15740173 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_13 nodo_14

theorem nodo_18 : comprobar 6548930 79335 24 4914279 8192 59049 35422771 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_16 nodo_17

theorem nodo_21 : comprobar 6548930 79335 24 4918375 16384 531441 159535331 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_19 nodo_20

theorem nodo_23 : comprobar 6548930 79335 24 4918375 8192 177147 106356887 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_21 nodo_22

theorem nodo_24 : comprobar 6548930 79335 24 4914279 4096 59049 70845542 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_18 nodo_23

theorem nodo_27 : comprobar 6548930 79335 24 4920423 8192 59049 35467058 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_25 nodo_26

theorem nodo_29 : comprobar 6548930 79335 24 4916327 4096 19683 23625022 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_28 nodo_27

theorem nodo_30 : comprobar 6548930 79335 24 4914279 2048 19683 47230361 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_24 nodo_29

theorem nodo_31 : comprobar 6548930 79335 24 4913255 1024 6561 31480346 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_15 nodo_30

theorem nodo_32 : comprobar 6548930 79335 24 4912743 512 2187 20984710 7 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_8 nodo_31

theorem nodo_35 : comprobar 6548930 79335 24 4912999 8192 59049 35413544 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_33 nodo_34

theorem nodo_38 : comprobar 6548930 79335 24 4925287 16384 531441 159759530 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_36 nodo_37

theorem nodo_40 : comprobar 6548930 79335 24 4917095 8192 177147 106329206 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_39 nodo_38

theorem nodo_41 : comprobar 6548930 79335 24 4912999 4096 59049 70827088 10 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_35 nodo_40

theorem nodo_44 : comprobar 6548930 79335 24 4915047 16384 531441 159427379 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_42 nodo_43

theorem nodo_46 : comprobar 6548930 79335 24 4915047 8192 177147 106284919 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_44 nodo_45

theorem nodo_49 : comprobar 6548930 79335 24 4919143 16384 531441 159560239 12 2 false 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_47 nodo_48

theorem nodo_52 : comprobar 6548930 79335 24 4927335 16384 1594323 479477879 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_50 nodo_51

theorem nodo_53 : comprobar 6548930 79335 24 4919143 8192 531441 319120478 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_49 nodo_52

theorem nodo_54 : comprobar 6548930 79335 24 4915047 4096 177147 212569838 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_46 nodo_53

theorem nodo_55 : comprobar 6548930 79335 24 4912999 2048 59049 141654176 10 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_41 nodo_54

theorem nodo_58 : comprobar 6548930 79335 24 4918119 8192 59049 35450450 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_56 nodo_57

theorem nodo_60 : comprobar 6548930 79335 24 4914023 4096 19683 23613950 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_59 nodo_58

theorem nodo_63 : comprobar 6548930 79335 24 4916071 16384 531441 159460595 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_61 nodo_62

theorem nodo_65 : comprobar 6548930 79335 24 4916071 8192 177147 106307063 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_63 nodo_64

theorem nodo_68 : comprobar 6548930 79335 24 4920167 8192 59049 35465212 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_66 nodo_67

theorem nodo_69 : comprobar 6548930 79335 24 4916071 4096 59049 70871375 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_65 nodo_68

theorem nodo_70 : comprobar 6548930 79335 24 4914023 2048 19683 47227900 9 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_60 nodo_69

theorem nodo_71 : comprobar 6548930 79335 24 4912999 1024 19683 94436117 9 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_55 nodo_70

theorem nodo_74 : comprobar 6548930 79335 24 4917607 8192 59049 35446760 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_72 nodo_73

theorem nodo_76 : comprobar 6548930 79335 24 4913511 4096 19683 23611490 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_75 nodo_74

theorem nodo_78 : comprobar 6548930 79335 24 4913511 2048 6561 15740993 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_76 nodo_77

theorem nodo_81 : comprobar 6548930 79335 24 4914535 8192 59049 35424616 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_79 nodo_80

theorem nodo_84 : comprobar 6548930 79335 24 4926823 16384 531441 159809354 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_82 nodo_83

theorem nodo_86 : comprobar 6548930 79335 24 4918631 8192 177147 106362422 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_85 nodo_84

theorem nodo_87 : comprobar 6548930 79335 24 4914535 4096 59049 70849232 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_81 nodo_86

theorem nodo_90 : comprobar 6548930 79335 24 4916583 4096 19683 23626252 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_88 nodo_89

theorem nodo_91 : comprobar 6548930 79335 24 4914535 2048 19683 47232821 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_87 nodo_90

theorem nodo_92 : comprobar 6548930 79335 24 4913511 1024 6561 31481986 8 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_78 nodo_91

theorem nodo_93 : comprobar 6548930 79335 24 4912999 512 6561 62957411 8 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_71 nodo_92

theorem nodo_94 : comprobar 6548930 79335 24 4912743 256 2187 41969420 7 2 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_32 nodo_93

theorem nodo_97 : comprobar 6548930 79335 24 4912871 8192 59049 35412623 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_95 nodo_96

theorem nodo_99 : comprobar 6548930 79335 24 4912871 4096 19683 23608415 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_97 nodo_98

theorem nodo_101 : comprobar 6548930 79335 24 4912871 2048 6561 15738943 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_99 nodo_100

theorem nodo_104 : comprobar 6548930 79335 24 4913895 16384 531441 159390017 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_102 nodo_103

theorem nodo_106 : comprobar 6548930 79335 24 4913895 8192 177147 106260011 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_104 nodo_105

theorem nodo_109 : comprobar 6548930 79335 24 4917991 8192 59049 35449528 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_107 nodo_108

theorem nodo_110 : comprobar 6548930 79335 24 4913895 4096 59049 70840007 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_106 nodo_109

theorem nodo_113 : comprobar 6548930 79335 24 4915943 8192 59049 35434766 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_111 nodo_112

theorem nodo_115 : comprobar 6548930 79335 24 4915943 4096 19683 23623177 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_113 nodo_114

theorem nodo_116 : comprobar 6548930 79335 24 4913895 2048 19683 47226671 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_110 nodo_115

theorem nodo_117 : comprobar 6548930 79335 24 4912871 1024 6561 31477886 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_101 nodo_116

theorem nodo_120 : comprobar 6548930 79335 24 4920551 8192 59049 35467982 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_118 nodo_119

theorem nodo_122 : comprobar 6548930 79335 24 4916455 4096 19683 23625638 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_121 nodo_120

theorem nodo_124 : comprobar 6548930 79335 24 4914407 2048 6561 15743864 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_123 nodo_122

theorem nodo_126 : comprobar 6548930 79335 24 4913383 1024 2187 10493722 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_125 nodo_124

theorem nodo_127 : comprobar 6548930 79335 24 4912871 512 2187 20985257 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_117 nodo_126

theorem nodo_130 : comprobar 6548930 79335 24 4919783 8192 59049 35462447 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_128 nodo_129

theorem nodo_132 : comprobar 6548930 79335 24 4915687 4096 19683 23621948 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_131 nodo_130

theorem nodo_134 : comprobar 6548930 79335 24 4913639 2048 6561 15741404 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_133 nodo_132

theorem nodo_136 : comprobar 6548930 79335 24 4913639 1024 2187 10494269 7 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_134 nodo_135

theorem nodo_138 : comprobar 6548930 79335 24 4913127 512 729 6995450 6 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_137 nodo_136

theorem nodo_139 : comprobar 6548930 79335 24 4912871 256 729 13990171 6 2 false 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_127 nodo_138

theorem nodo_140 : comprobar 6548930 79335 24 4912743 128 729 27979613 6 2 true 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_94 nodo_139

theorem nodo_143 : comprobar 6548930 79335 24 4913831 8192 59049 35419544 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_141 nodo_142

theorem nodo_145 : comprobar 6548930 79335 24 4913831 4096 19683 23613029 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_143 nodo_144

theorem nodo_147 : comprobar 6548930 79335 24 4913831 2048 6561 15742019 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_145 nodo_146

theorem nodo_149 : comprobar 6548930 79335 24 4912807 1024 2187 10492492 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_148 nodo_147

theorem nodo_152 : comprobar 6548930 79335 24 4917415 8192 59049 35445377 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_150 nodo_151

theorem nodo_154 : comprobar 6548930 79335 24 4913319 4096 19683 23610568 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_153 nodo_152

theorem nodo_157 : comprobar 6548930 79335 24 4923559 16384 531441 159703487 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_155 nodo_156

theorem nodo_159 : comprobar 6548930 79335 24 4915367 8192 177147 106291844 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_158 nodo_157

theorem nodo_162 : comprobar 6548930 79335 24 4919463 8192 59049 35460139 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_160 nodo_161

theorem nodo_163 : comprobar 6548930 79335 24 4915367 4096 59049 70861229 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_159 nodo_162

theorem nodo_164 : comprobar 6548930 79335 24 4913319 2048 19683 47221136 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_154 nodo_163

theorem nodo_167 : comprobar 6548930 79335 24 4914343 8192 59049 35423234 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_165 nodo_166

theorem nodo_169 : comprobar 6548930 79335 24 4914343 4096 19683 23615489 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_167 nodo_168

theorem nodo_171 : comprobar 6548930 79335 24 4914343 2048 6561 15743659 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_169 nodo_170

theorem nodo_172 : comprobar 6548930 79335 24 4913319 1024 6561 31480757 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_164 nodo_171

theorem nodo_173 : comprobar 6548930 79335 24 4912807 512 2187 20984984 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_149 nodo_172

theorem nodo_176 : comprobar 6548930 79335 24 4913063 8192 59049 35414009 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_174 nodo_175

theorem nodo_178 : comprobar 6548930 79335 24 4913063 4096 19683 23609339 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_176 nodo_177

theorem nodo_180 : comprobar 6548930 79335 24 4913063 2048 6561 15739559 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_178 nodo_179

theorem nodo_182 : comprobar 6548930 79335 24 4913063 1024 2187 10493039 7 4 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_180 nodo_181

theorem nodo_184 : comprobar 6548930 79335 24 4913063 512 729 6995359 6 3 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_182 nodo_183

theorem nodo_185 : comprobar 6548930 79335 24 4912807 256 729 13989989 6 3 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_173 nodo_184

theorem nodo_187 : comprobar 6548930 79335 24 4912807 128 243 9326659 5 2 false 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_185 nodo_186

theorem nodo_188 : comprobar 6548930 79335 24 4912743 64 243 18653075 5 2 true 122 = true := by
  exact acepta_rama (by decide +kernel) nodo_140 nodo_187

theorem nodo_191 : comprobar 6548930 79335 24 4920135 8192 59049 35464985 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_189 nodo_190

theorem nodo_193 : comprobar 6548930 79335 24 4916039 4096 19683 23623640 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_192 nodo_191

theorem nodo_195 : comprobar 6548930 79335 24 4913991 2048 6561 15742532 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_194 nodo_193

theorem nodo_197 : comprobar 6548930 79335 24 4912967 1024 2187 10492834 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_196 nodo_195

theorem nodo_200 : comprobar 6548930 79335 24 4921671 16384 531441 159642251 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_198 nodo_199

theorem nodo_202 : comprobar 6548930 79335 24 4913479 8192 177147 106251020 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_201 nodo_200

theorem nodo_205 : comprobar 6548930 79335 24 4917575 8192 59049 35446531 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_203 nodo_204

theorem nodo_206 : comprobar 6548930 79335 24 4913479 4096 59049 70834013 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_202 nodo_205

theorem nodo_209 : comprobar 6548930 79335 24 4915527 8192 59049 35431769 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_207 nodo_208

theorem nodo_211 : comprobar 6548930 79335 24 4915527 4096 19683 23621179 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_209 nodo_210

theorem nodo_212 : comprobar 6548930 79335 24 4913479 2048 19683 47222675 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_206 nodo_211

theorem nodo_215 : comprobar 6548930 79335 24 4920647 8192 59049 35468675 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_213 nodo_214

theorem nodo_217 : comprobar 6548930 79335 24 4916551 4096 19683 23626100 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_216 nodo_215

theorem nodo_219 : comprobar 6548930 79335 24 4914503 2048 6561 15744172 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_218 nodo_217

theorem nodo_220 : comprobar 6548930 79335 24 4913479 1024 6561 31481783 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_212 nodo_219

theorem nodo_221 : comprobar 6548930 79335 24 4912967 512 2187 20985668 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_197 nodo_220

theorem nodo_224 : comprobar 6548930 79335 24 4919367 8192 59049 35459450 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_222 nodo_223

theorem nodo_226 : comprobar 6548930 79335 24 4915271 4096 19683 23619950 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_225 nodo_224

theorem nodo_228 : comprobar 6548930 79335 24 4913223 2048 6561 15740072 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_227 nodo_226

theorem nodo_230 : comprobar 6548930 79335 24 4913223 1024 2187 10493381 7 4 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_228 nodo_229

theorem nodo_232 : comprobar 6548930 79335 24 4913223 512 729 6995587 6 3 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_230 nodo_231

theorem nodo_233 : comprobar 6548930 79335 24 4912967 256 729 13990445 6 3 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_221 nodo_232

theorem nodo_235 : comprobar 6548930 79335 24 4912839 128 243 9326720 5 3 true 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_234 nodo_233

theorem nodo_237 : comprobar 6548930 79335 24 4912775 64 81 6217732 4 2 false 122 = true := by
  exact acepta_rama (by decide +kernel) nodo_236 nodo_235

theorem nodo_238 : comprobar 6548930 79335 24 4912743 32 81 12435383 4 2 true 123 = true := by
  exact acepta_rama (by decide +kernel) nodo_188 nodo_237

theorem nodo_240 : comprobar 6548930 79335 24 4912743 16 27 8290255 3 1 false 124 = true := by
  exact acepta_rama (by decide +kernel) nodo_238 nodo_239

theorem nodo_243 : comprobar 6548930 79335 24 4913775 8192 59049 35419139 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_241 nodo_242

theorem nodo_245 : comprobar 6548930 79335 24 4913775 4096 19683 23612759 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_243 nodo_244

theorem nodo_247 : comprobar 6548930 79335 24 4913775 2048 6561 15741839 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_245 nodo_246

theorem nodo_249 : comprobar 6548930 79335 24 4912751 1024 2187 10492372 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_248 nodo_247

theorem nodo_252 : comprobar 6548930 79335 24 4917359 8192 59049 35444972 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_250 nodo_251

theorem nodo_254 : comprobar 6548930 79335 24 4913263 4096 19683 23610298 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_253 nodo_252

theorem nodo_257 : comprobar 6548930 79335 24 4915311 16384 531441 159435944 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_255 nodo_256

theorem nodo_259 : comprobar 6548930 79335 24 4915311 8192 177147 106290629 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_257 nodo_258

theorem nodo_262 : comprobar 6548930 79335 24 4919407 8192 59049 35459734 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_260 nodo_261

theorem nodo_263 : comprobar 6548930 79335 24 4915311 4096 59049 70860419 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_259 nodo_262

theorem nodo_264 : comprobar 6548930 79335 24 4913263 2048 19683 47220596 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_254 nodo_263

theorem nodo_267 : comprobar 6548930 79335 24 4914287 8192 59049 35422829 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_265 nodo_266

theorem nodo_269 : comprobar 6548930 79335 24 4914287 4096 19683 23615219 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_267 nodo_268

theorem nodo_271 : comprobar 6548930 79335 24 4914287 2048 6561 15743479 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_269 nodo_270

theorem nodo_272 : comprobar 6548930 79335 24 4913263 1024 6561 31480397 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_264 nodo_271

theorem nodo_273 : comprobar 6548930 79335 24 4912751 512 2187 20984744 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_249 nodo_272

theorem nodo_276 : comprobar 6548930 79335 24 4913007 8192 59049 35413604 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_274 nodo_275

theorem nodo_278 : comprobar 6548930 79335 24 4913007 4096 19683 23609069 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_276 nodo_277

theorem nodo_280 : comprobar 6548930 79335 24 4913007 2048 6561 15739379 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_278 nodo_279

theorem nodo_282 : comprobar 6548930 79335 24 4913007 1024 2187 10492919 7 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_280 nodo_281

theorem nodo_284 : comprobar 6548930 79335 24 4913007 512 729 6995279 6 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_282 nodo_283

theorem nodo_285 : comprobar 6548930 79335 24 4912751 256 729 13989829 6 2 false 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_273 nodo_284

theorem nodo_288 : comprobar 6548930 79335 24 4919023 8192 59049 35456966 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_286 nodo_287

theorem nodo_290 : comprobar 6548930 79335 24 4914927 4096 19683 23618294 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_289 nodo_288

theorem nodo_292 : comprobar 6548930 79335 24 4912879 2048 6561 15738968 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_291 nodo_290

theorem nodo_295 : comprobar 6548930 79335 24 4913903 8192 59049 35420060 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_293 nodo_294

theorem nodo_297 : comprobar 6548930 79335 24 4913903 4096 19683 23613373 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_295 nodo_296

theorem nodo_300 : comprobar 6548930 79335 24 4915951 8192 59049 35434822 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_298 nodo_299

theorem nodo_303 : comprobar 6548930 79335 24 4928239 16384 531441 159855281 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_301 nodo_302

theorem nodo_305 : comprobar 6548930 79335 24 4920047 8192 177147 106393040 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_304 nodo_303

theorem nodo_306 : comprobar 6548930 79335 24 4915951 4096 59049 70869644 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_300 nodo_305

theorem nodo_307 : comprobar 6548930 79335 24 4913903 2048 19683 47226746 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_297 nodo_306

theorem nodo_308 : comprobar 6548930 79335 24 4912879 1024 6561 31477936 8 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_292 nodo_307

theorem nodo_311 : comprobar 6548930 79335 24 4913391 8192 59049 35416369 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_309 nodo_310

theorem nodo_314 : comprobar 6548930 79335 24 4917487 16384 531441 159506522 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_312 nodo_313

theorem nodo_316 : comprobar 6548930 79335 24 4917487 8192 177147 106337681 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_314 nodo_315

theorem nodo_317 : comprobar 6548930 79335 24 4913391 4096 59049 70832738 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_311 nodo_316

theorem nodo_320 : comprobar 6548930 79335 24 4919535 8192 59049 35460656 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_318 nodo_319

theorem nodo_322 : comprobar 6548930 79335 24 4915439 4096 19683 23620754 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_321 nodo_320

theorem nodo_323 : comprobar 6548930 79335 24 4913391 2048 19683 47221825 9 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_317 nodo_322

theorem nodo_326 : comprobar 6548930 79335 24 4914415 8192 59049 35423750 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_324 nodo_325

theorem nodo_329 : comprobar 6548930 79335 24 4926703 16384 531441 159805457 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_327 nodo_328

theorem nodo_331 : comprobar 6548930 79335 24 4918511 8192 177147 106359824 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_330 nodo_329

theorem nodo_332 : comprobar 6548930 79335 24 4914415 4096 59049 70847500 10 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_326 nodo_331

theorem nodo_335 : comprobar 6548930 79335 24 4916463 16384 531441 159473306 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_333 nodo_334

theorem nodo_337 : comprobar 6548930 79335 24 4916463 8192 177147 106315537 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_335 nodo_336

theorem nodo_340 : comprobar 6548930 79335 24 4920559 16384 531441 159606166 12 2 false 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_338 nodo_339

theorem nodo_343 : comprobar 6548930 79335 24 4928751 16384 1594323 479615660 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_341 nodo_342

theorem nodo_344 : comprobar 6548930 79335 24 4920559 8192 531441 319212332 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_340 nodo_343

theorem nodo_345 : comprobar 6548930 79335 24 4916463 4096 177147 212631074 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_337 nodo_344

theorem nodo_346 : comprobar 6548930 79335 24 4914415 2048 59049 141695000 10 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_332 nodo_345

theorem nodo_347 : comprobar 6548930 79335 24 4913391 1024 19683 94443650 9 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_323 nodo_346

theorem nodo_348 : comprobar 6548930 79335 24 4912879 512 6561 62955872 8 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_308 nodo_347

theorem nodo_351 : comprobar 6548930 79335 24 4918255 8192 59049 35451431 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_349 nodo_350

theorem nodo_353 : comprobar 6548930 79335 24 4914159 4096 19683 23614604 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_352 nodo_351

theorem nodo_355 : comprobar 6548930 79335 24 4914159 2048 6561 15743069 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_353 nodo_354

theorem nodo_357 : comprobar 6548930 79335 24 4913135 1024 2187 10493192 7 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_356 nodo_355

theorem nodo_360 : comprobar 6548930 79335 24 4913647 8192 59049 35418215 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_358 nodo_359

theorem nodo_362 : comprobar 6548930 79335 24 4913647 4096 19683 23612143 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_360 nodo_361

theorem nodo_365 : comprobar 6548930 79335 24 4915695 8192 59049 35432977 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_363 nodo_364

theorem nodo_368 : comprobar 6548930 79335 24 4919791 16384 531441 159581258 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_366 nodo_367

theorem nodo_370 : comprobar 6548930 79335 24 4919791 8192 177147 106387505 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_368 nodo_369

theorem nodo_371 : comprobar 6548930 79335 24 4915695 4096 59049 70865954 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_365 nodo_370

theorem nodo_372 : comprobar 6548930 79335 24 4913647 2048 19683 47224286 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_362 nodo_371

theorem nodo_375 : comprobar 6548930 79335 24 4918767 8192 59049 35455121 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_373 nodo_374

theorem nodo_377 : comprobar 6548930 79335 24 4914671 4096 19683 23617064 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_376 nodo_375

theorem nodo_379 : comprobar 6548930 79335 24 4914671 2048 6561 15744709 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_377 nodo_378

theorem nodo_380 : comprobar 6548930 79335 24 4913647 1024 6561 31482857 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_372 nodo_379

theorem nodo_381 : comprobar 6548930 79335 24 4913135 512 2187 20986384 7 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_357 nodo_380

theorem nodo_382 : comprobar 6548930 79335 24 4912879 256 2187 41970581 7 2 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_348 nodo_381

theorem nodo_383 : comprobar 6548930 79335 24 4912751 128 729 27979658 6 2 true 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_285 nodo_382

theorem nodo_386 : comprobar 6548930 79335 24 4914479 8192 59049 35424215 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_384 nodo_385

theorem nodo_388 : comprobar 6548930 79335 24 4914479 4096 19683 23616143 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_386 nodo_387

theorem nodo_390 : comprobar 6548930 79335 24 4914479 2048 6561 15744095 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_388 nodo_389

theorem nodo_392 : comprobar 6548930 79335 24 4913455 1024 2187 10493876 7 4 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_391 nodo_390

theorem nodo_394 : comprobar 6548930 79335 24 4912943 512 729 6995188 6 3 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_393 nodo_392

theorem nodo_397 : comprobar 6548930 79335 24 4915247 8192 59049 35429750 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_395 nodo_396

theorem nodo_399 : comprobar 6548930 79335 24 4915247 4096 19683 23619833 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_397 nodo_398

theorem nodo_401 : comprobar 6548930 79335 24 4913199 2048 6561 15739994 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_400 nodo_399

theorem nodo_403 : comprobar 6548930 79335 24 4913199 1024 2187 10493329 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_401 nodo_402

theorem nodo_406 : comprobar 6548930 79335 24 4915759 8192 59049 35433440 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_404 nodo_405

theorem nodo_408 : comprobar 6548930 79335 24 4915759 4096 19683 23622293 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_406 nodo_407

theorem nodo_410 : comprobar 6548930 79335 24 4913711 2048 6561 15741634 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_409 nodo_408

theorem nodo_413 : comprobar 6548930 79335 24 4918831 8192 59049 35455583 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_411 nodo_412

theorem nodo_415 : comprobar 6548930 79335 24 4914735 4096 19683 23617372 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_414 nodo_413

theorem nodo_418 : comprobar 6548930 79335 24 4924975 16384 531441 159749414 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_416 nodo_417

theorem nodo_420 : comprobar 6548930 79335 24 4916783 8192 177147 106322462 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_419 nodo_418

theorem nodo_423 : comprobar 6548930 79335 24 4920879 8192 59049 35470345 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_421 nodo_422

theorem nodo_424 : comprobar 6548930 79335 24 4916783 4096 59049 70881641 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_420 nodo_423

theorem nodo_425 : comprobar 6548930 79335 24 4914735 2048 19683 47234744 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_415 nodo_424

theorem nodo_426 : comprobar 6548930 79335 24 4913711 1024 6561 31483268 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_410 nodo_425

theorem nodo_427 : comprobar 6548930 79335 24 4913199 512 2187 20986658 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_403 nodo_426

theorem nodo_428 : comprobar 6548930 79335 24 4912943 256 729 13990376 6 3 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_394 nodo_427

theorem nodo_430 : comprobar 6548930 79335 24 4912815 128 243 9326674 5 2 false 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_429 nodo_428

theorem nodo_431 : comprobar 6548930 79335 24 4912751 64 243 18653105 5 2 true 122 = true := by
  exact acepta_rama (by decide +kernel) nodo_383 nodo_430

theorem nodo_434 : comprobar 6548930 79335 24 4916943 8192 59049 35441975 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_432 nodo_433

theorem nodo_436 : comprobar 6548930 79335 24 4912847 4096 19683 23608300 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_435 nodo_434

theorem nodo_439 : comprobar 6548930 79335 24 4923087 16384 531441 159688178 12 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_437 nodo_438

theorem nodo_441 : comprobar 6548930 79335 24 4914895 8192 177147 106281638 11 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_440 nodo_439

theorem nodo_444 : comprobar 6548930 79335 24 4918991 8192 59049 35456737 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_442 nodo_443

theorem nodo_445 : comprobar 6548930 79335 24 4914895 4096 59049 70854425 10 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_441 nodo_444

theorem nodo_446 : comprobar 6548930 79335 24 4912847 2048 19683 47216600 9 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_436 nodo_445

theorem nodo_449 : comprobar 6548930 79335 24 4913871 8192 59049 35419832 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_447 nodo_448

theorem nodo_451 : comprobar 6548930 79335 24 4913871 4096 19683 23613221 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_449 nodo_450

theorem nodo_453 : comprobar 6548930 79335 24 4913871 2048 6561 15742147 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_451 nodo_452

theorem nodo_454 : comprobar 6548930 79335 24 4912847 1024 6561 31477733 8 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_446 nodo_453

theorem nodo_457 : comprobar 6548930 79335 24 4913359 8192 59049 35416142 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_455 nodo_456

theorem nodo_459 : comprobar 6548930 79335 24 4913359 4096 19683 23610761 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_457 nodo_458

theorem nodo_461 : comprobar 6548930 79335 24 4913359 2048 6561 15740507 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_459 nodo_460

theorem nodo_463 : comprobar 6548930 79335 24 4913359 1024 2187 10493671 7 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_461 nodo_462

theorem nodo_464 : comprobar 6548930 79335 24 4912847 512 2187 20985155 7 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_454 nodo_463

theorem nodo_467 : comprobar 6548930 79335 24 4920783 8192 59049 35469656 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_465 nodo_466

theorem nodo_469 : comprobar 6548930 79335 24 4916687 4096 19683 23626754 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_468 nodo_467

theorem nodo_471 : comprobar 6548930 79335 24 4914639 2048 6561 15744608 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_470 nodo_469

theorem nodo_473 : comprobar 6548930 79335 24 4913615 1024 2187 10494218 7 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_472 nodo_471

theorem nodo_475 : comprobar 6548930 79335 24 4913103 512 729 6995416 6 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_474 nodo_473

theorem nodo_476 : comprobar 6548930 79335 24 4912847 256 729 13990103 6 2 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_464 nodo_475

theorem nodo_478 : comprobar 6548930 79335 24 4912847 128 243 9326735 5 2 true 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_476 nodo_477

theorem nodo_480 : comprobar 6548930 79335 24 4912783 64 81 6217742 4 1 false 122 = true := by
  exact acepta_rama (by decide +kernel) nodo_479 nodo_478

theorem nodo_481 : comprobar 6548930 79335 24 4912751 32 81 12435403 4 1 false 123 = true := by
  exact acepta_rama (by decide +kernel) nodo_431 nodo_480

theorem nodo_484 : comprobar 6548930 79335 24 4912767 8192 59049 35411870 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_482 nodo_483

theorem nodo_487 : comprobar 6548930 79335 24 4925055 16384 531441 159751997 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_485 nodo_486

theorem nodo_489 : comprobar 6548930 79335 24 4916863 8192 177147 106324184 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_488 nodo_487

theorem nodo_490 : comprobar 6548930 79335 24 4912767 4096 59049 70823740 10 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_484 nodo_489

theorem nodo_493 : comprobar 6548930 79335 24 4914815 16384 531441 159419846 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_491 nodo_492

theorem nodo_495 : comprobar 6548930 79335 24 4914815 8192 177147 106279897 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_493 nodo_494

theorem nodo_498 : comprobar 6548930 79335 24 4918911 16384 531441 159552706 12 2 false 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_496 nodo_497

theorem nodo_501 : comprobar 6548930 79335 24 4927103 16384 1594323 479455280 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_499 nodo_500

theorem nodo_502 : comprobar 6548930 79335 24 4918911 8192 531441 319105412 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_498 nodo_501

theorem nodo_503 : comprobar 6548930 79335 24 4914815 4096 177147 212559794 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_495 nodo_502

theorem nodo_504 : comprobar 6548930 79335 24 4912767 2048 59049 141647480 10 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_490 nodo_503

theorem nodo_507 : comprobar 6548930 79335 24 4917887 8192 59049 35448776 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_505 nodo_506

theorem nodo_509 : comprobar 6548930 79335 24 4913791 4096 19683 23612834 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_508 nodo_507

theorem nodo_512 : comprobar 6548930 79335 24 4915839 16384 531441 159453062 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_510 nodo_511

theorem nodo_514 : comprobar 6548930 79335 24 4915839 8192 177147 106302041 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_512 nodo_513

theorem nodo_517 : comprobar 6548930 79335 24 4919935 8192 59049 35463538 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_515 nodo_516

theorem nodo_518 : comprobar 6548930 79335 24 4915839 4096 59049 70868027 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_514 nodo_517

theorem nodo_519 : comprobar 6548930 79335 24 4913791 2048 19683 47225668 9 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_509 nodo_518

theorem nodo_520 : comprobar 6548930 79335 24 4912767 1024 19683 94431653 9 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_504 nodo_519

theorem nodo_523 : comprobar 6548930 79335 24 4917375 8192 59049 35445086 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_521 nodo_522

theorem nodo_525 : comprobar 6548930 79335 24 4913279 4096 19683 23610374 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_524 nodo_523

theorem nodo_527 : comprobar 6548930 79335 24 4913279 2048 6561 15740249 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_525 nodo_526

theorem nodo_530 : comprobar 6548930 79335 24 4914303 8192 59049 35422942 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_528 nodo_529

theorem nodo_533 : comprobar 6548930 79335 24 4926591 16384 531441 159801821 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_531 nodo_532

theorem nodo_535 : comprobar 6548930 79335 24 4918399 8192 177147 106357400 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_534 nodo_533

theorem nodo_536 : comprobar 6548930 79335 24 4914303 4096 59049 70845884 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_530 nodo_535

theorem nodo_539 : comprobar 6548930 79335 24 4920447 8192 59049 35467229 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_537 nodo_538

theorem nodo_541 : comprobar 6548930 79335 24 4916351 4096 19683 23625136 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_540 nodo_539

theorem nodo_542 : comprobar 6548930 79335 24 4914303 2048 19683 47230589 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_536 nodo_541

theorem nodo_543 : comprobar 6548930 79335 24 4913279 1024 6561 31480498 8 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_527 nodo_542

theorem nodo_544 : comprobar 6548930 79335 24 4912767 512 6561 62954435 8 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_520 nodo_543

theorem nodo_547 : comprobar 6548930 79335 24 4917119 8192 59049 35443241 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_545 nodo_546

theorem nodo_549 : comprobar 6548930 79335 24 4913023 4096 19683 23609144 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_548 nodo_547

theorem nodo_551 : comprobar 6548930 79335 24 4913023 2048 6561 15739429 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_549 nodo_550

theorem nodo_554 : comprobar 6548930 79335 24 4914047 8192 59049 35421097 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_552 nodo_553

theorem nodo_557 : comprobar 6548930 79335 24 4918143 16384 531441 159527798 12 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_555 nodo_556

theorem nodo_559 : comprobar 6548930 79335 24 4918143 8192 177147 106351865 11 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_557 nodo_558

theorem nodo_560 : comprobar 6548930 79335 24 4914047 4096 59049 70842194 10 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_554 nodo_559

theorem nodo_563 : comprobar 6548930 79335 24 4920191 8192 59049 35465384 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_561 nodo_562

theorem nodo_565 : comprobar 6548930 79335 24 4916095 4096 19683 23623906 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_564 nodo_563

theorem nodo_566 : comprobar 6548930 79335 24 4914047 2048 19683 47228129 9 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_560 nodo_565

theorem nodo_567 : comprobar 6548930 79335 24 4913023 1024 6561 31478858 8 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_551 nodo_566

theorem nodo_570 : comprobar 6548930 79335 24 4916607 8192 59049 35439551 10 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_568 nodo_569

theorem nodo_572 : comprobar 6548930 79335 24 4916607 4096 19683 23626367 9 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_570 nodo_571

theorem nodo_574 : comprobar 6548930 79335 24 4914559 2048 6561 15744350 8 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_573 nodo_572

theorem nodo_576 : comprobar 6548930 79335 24 4913535 1024 2187 10494046 7 1 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_575 nodo_574

theorem nodo_577 : comprobar 6548930 79335 24 4913023 512 2187 20985905 7 1 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_567 nodo_576

theorem nodo_578 : comprobar 6548930 79335 24 4912767 256 2187 41969623 7 1 false 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_544 nodo_577

theorem nodo_581 : comprobar 6548930 79335 24 4921087 16384 531441 159623288 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_579 nodo_580

theorem nodo_583 : comprobar 6548930 79335 24 4912895 8192 177147 106238378 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_582 nodo_581

theorem nodo_586 : comprobar 6548930 79335 24 4916991 8192 59049 35442317 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_584 nodo_585

theorem nodo_587 : comprobar 6548930 79335 24 4912895 4096 59049 70825585 10 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_583 nodo_586

theorem nodo_590 : comprobar 6548930 79335 24 4914943 16384 531441 159423997 12 2 false 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_588 nodo_589

theorem nodo_593 : comprobar 6548930 79335 24 4923135 16384 1594323 479069153 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_591 nodo_592

theorem nodo_594 : comprobar 6548930 79335 24 4914943 8192 531441 318847994 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_590 nodo_593

theorem nodo_597 : comprobar 6548930 79335 24 4927231 16384 531441 159822578 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_595 nodo_596

theorem nodo_599 : comprobar 6548930 79335 24 4919039 8192 177147 106371238 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_598 nodo_597

theorem nodo_600 : comprobar 6548930 79335 24 4914943 4096 177147 212565329 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_594 nodo_599

theorem nodo_601 : comprobar 6548930 79335 24 4912895 2048 59049 141651170 10 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_587 nodo_600

theorem nodo_604 : comprobar 6548930 79335 24 4913919 8192 59049 35420174 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_602 nodo_603

theorem nodo_606 : comprobar 6548930 79335 24 4913919 4096 19683 23613449 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_604 nodo_605

theorem nodo_609 : comprobar 6548930 79335 24 4915967 8192 59049 35434936 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_607 nodo_608

theorem nodo_612 : comprobar 6548930 79335 24 4928255 16384 531441 159855794 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_610 nodo_611

theorem nodo_614 : comprobar 6548930 79335 24 4920063 8192 177147 106393382 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_613 nodo_612

theorem nodo_615 : comprobar 6548930 79335 24 4915967 4096 59049 70869872 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_609 nodo_614

theorem nodo_616 : comprobar 6548930 79335 24 4913919 2048 19683 47226898 9 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_606 nodo_615

theorem nodo_617 : comprobar 6548930 79335 24 4912895 1024 19683 94434113 9 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_601 nodo_616

theorem nodo_620 : comprobar 6548930 79335 24 4913407 8192 59049 35416484 10 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_618 nodo_619

theorem nodo_622 : comprobar 6548930 79335 24 4913407 4096 19683 23610989 9 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_620 nodo_621

theorem nodo_624 : comprobar 6548930 79335 24 4913407 2048 6561 15740659 8 1 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_622 nodo_623

theorem nodo_627 : comprobar 6548930 79335 24 4922623 16384 531441 159673112 12 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_625 nodo_626

theorem nodo_629 : comprobar 6548930 79335 24 4914431 8192 177147 106271594 11 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_628 nodo_627

theorem nodo_632 : comprobar 6548930 79335 24 4918527 8192 59049 35453389 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_630 nodo_631

theorem nodo_633 : comprobar 6548930 79335 24 4914431 4096 59049 70847729 10 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_629 nodo_632

theorem nodo_636 : comprobar 6548930 79335 24 4916479 8192 59049 35438627 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_634 nodo_635

theorem nodo_638 : comprobar 6548930 79335 24 4916479 4096 19683 23625751 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_636 nodo_637

theorem nodo_639 : comprobar 6548930 79335 24 4914431 2048 19683 47231819 9 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_633 nodo_638

theorem nodo_640 : comprobar 6548930 79335 24 4913407 1024 6561 31481318 8 1 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_624 nodo_639

theorem nodo_641 : comprobar 6548930 79335 24 4912895 512 6561 62956075 8 1 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_617 nodo_640

theorem nodo_644 : comprobar 6548930 79335 24 4913151 16384 531441 159365870 12 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_642 nodo_643

theorem nodo_647 : comprobar 6548930 79335 24 4921343 16384 177147 53210530 11 1 false 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_645 nodo_646

theorem nodo_648 : comprobar 6548930 79335 24 4913151 8192 177147 106243913 11 1 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_644 nodo_647

theorem nodo_651 : comprobar 6548930 79335 24 4917247 16384 531441 159498730 12 2 false 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_649 nodo_650

theorem nodo_654 : comprobar 6548930 79335 24 4925439 16384 1594323 479293352 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_652 nodo_653

theorem nodo_655 : comprobar 6548930 79335 24 4917247 8192 531441 318997460 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_651 nodo_654

theorem nodo_656 : comprobar 6548930 79335 24 4913151 4096 177147 212487826 11 1 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_648 nodo_655

theorem nodo_659 : comprobar 6548930 79335 24 4915199 32768 14348907 2152336049 15 1 true 113 = true := by
  exact acepta_rama (by decide +kernel) nodo_657 nodo_658

theorem nodo_661 : comprobar 6548930 79335 24 4915199 16384 4782969 1434890699 14 1 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_659 nodo_660

theorem nodo_664 : comprobar 6548930 79335 24 4923391 16384 1594323 479094061 13 1 false 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_662 nodo_663

theorem nodo_665 : comprobar 6548930 79335 24 4915199 8192 1594323 956593799 13 1 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_661 nodo_664

theorem nodo_668 : comprobar 6548930 79335 24 4919295 16384 531441 159565160 12 1 false 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_666 nodo_667

theorem nodo_671 : comprobar 6548930 79335 24 4927487 16384 1594323 479492642 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_669 nodo_670

theorem nodo_672 : comprobar 6548930 79335 24 4919295 8192 531441 319130320 12 1 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_668 nodo_671

theorem nodo_673 : comprobar 6548930 79335 24 4915199 4096 531441 637729199 12 1 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_665 nodo_672

theorem nodo_674 : comprobar 6548930 79335 24 4913151 2048 177147 424975652 11 1 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_656 nodo_673

theorem nodo_677 : comprobar 6548930 79335 24 4914175 16384 531441 159399085 12 2 false 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_675 nodo_676

theorem nodo_680 : comprobar 6548930 79335 24 4922367 16384 1594323 478994417 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_678 nodo_679

theorem nodo_681 : comprobar 6548930 79335 24 4914175 8192 531441 318798170 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_677 nodo_680

theorem nodo_684 : comprobar 6548930 79335 24 4926463 16384 531441 159797666 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_682 nodo_683

theorem nodo_686 : comprobar 6548930 79335 24 4918271 8192 177147 106354630 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_685 nodo_684

theorem nodo_687 : comprobar 6548930 79335 24 4914175 4096 177147 212532113 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_681 nodo_686

theorem nodo_690 : comprobar 6548930 79335 24 4916223 8192 59049 35436781 10 1 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_688 nodo_689

theorem nodo_693 : comprobar 6548930 79335 24 4920319 16384 531441 159598376 12 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_691 nodo_692

theorem nodo_695 : comprobar 6548930 79335 24 4920319 8192 177147 106398917 11 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_693 nodo_694

theorem nodo_696 : comprobar 6548930 79335 24 4916223 4096 59049 70873562 10 1 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_690 nodo_695

theorem nodo_697 : comprobar 6548930 79335 24 4914175 2048 59049 141688075 10 1 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_687 nodo_696

theorem nodo_698 : comprobar 6548930 79335 24 4913151 1024 59049 283317101 10 1 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_674 nodo_697

theorem nodo_701 : comprobar 6548930 79335 24 4913663 16384 531441 159382478 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_699 nodo_700

theorem nodo_703 : comprobar 6548930 79335 24 4913663 8192 177147 106254985 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_701 nodo_702

theorem nodo_706 : comprobar 6548930 79335 24 4917759 16384 531441 159515338 12 2 false 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_704 nodo_705

theorem nodo_709 : comprobar 6548930 79335 24 4925951 16384 1594323 479343176 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_707 nodo_708

theorem nodo_710 : comprobar 6548930 79335 24 4917759 8192 531441 319030676 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_706 nodo_709

theorem nodo_711 : comprobar 6548930 79335 24 4913663 4096 177147 212509970 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_703 nodo_710

theorem nodo_714 : comprobar 6548930 79335 24 4923903 16384 531441 159714629 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_712 nodo_713

theorem nodo_716 : comprobar 6548930 79335 24 4915711 8192 177147 106299272 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_715 nodo_714

theorem nodo_719 : comprobar 6548930 79335 24 4919807 8192 59049 35462615 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_717 nodo_718

theorem nodo_720 : comprobar 6548930 79335 24 4915711 4096 59049 70866181 10 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_716 nodo_719

theorem nodo_721 : comprobar 6548930 79335 24 4913663 2048 59049 141673313 10 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_711 nodo_720

theorem nodo_724 : comprobar 6548930 79335 24 4914687 16384 531441 159415694 12 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_722 nodo_723

theorem nodo_726 : comprobar 6548930 79335 24 4914687 8192 177147 106277129 11 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_724 nodo_725

theorem nodo_729 : comprobar 6548930 79335 24 4918783 8192 59049 35455234 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_727 nodo_728

theorem nodo_730 : comprobar 6548930 79335 24 4914687 4096 59049 70851419 10 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_726 nodo_729

theorem nodo_733 : comprobar 6548930 79335 24 4916735 8192 59049 35440472 10 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_731 nodo_732

theorem nodo_735 : comprobar 6548930 79335 24 4916735 4096 19683 23626981 9 1 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_733 nodo_734

theorem nodo_736 : comprobar 6548930 79335 24 4914687 2048 19683 47234279 9 1 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_730 nodo_735

theorem nodo_737 : comprobar 6548930 79335 24 4913663 1024 19683 94448875 9 1 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_721 nodo_736

theorem nodo_738 : comprobar 6548930 79335 24 4913151 512 19683 188878067 9 1 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_698 nodo_737

theorem nodo_739 : comprobar 6548930 79335 24 4912895 256 6561 125912150 8 1 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_641 nodo_738

theorem nodo_740 : comprobar 6548930 79335 24 4912767 128 2187 83939246 7 1 true 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_578 nodo_739

theorem nodo_743 : comprobar 6548930 79335 24 4914879 8192 59049 35427095 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_741 nodo_742

theorem nodo_745 : comprobar 6548930 79335 24 4914879 4096 19683 23618063 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_743 nodo_744

theorem nodo_747 : comprobar 6548930 79335 24 4912831 2048 6561 15738814 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_746 nodo_745

theorem nodo_750 : comprobar 6548930 79335 24 4917951 8192 59049 35449238 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_748 nodo_749

theorem nodo_752 : comprobar 6548930 79335 24 4913855 4096 19683 23613142 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_751 nodo_750

theorem nodo_755 : comprobar 6548930 79335 24 4915903 16384 531441 159455141 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_753 nodo_754

theorem nodo_757 : comprobar 6548930 79335 24 4915903 8192 177147 106303427 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_755 nodo_756

theorem nodo_760 : comprobar 6548930 79335 24 4919999 8192 59049 35464000 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_758 nodo_759

theorem nodo_761 : comprobar 6548930 79335 24 4915903 4096 59049 70868951 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_757 nodo_760

theorem nodo_762 : comprobar 6548930 79335 24 4913855 2048 19683 47226284 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_752 nodo_761

theorem nodo_763 : comprobar 6548930 79335 24 4912831 1024 6561 31477628 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_747 nodo_762

theorem nodo_766 : comprobar 6548930 79335 24 4914367 8192 59049 35423405 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_764 nodo_765

theorem nodo_768 : comprobar 6548930 79335 24 4914367 4096 19683 23615603 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_766 nodo_767

theorem nodo_770 : comprobar 6548930 79335 24 4914367 2048 6561 15743735 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_768 nodo_769

theorem nodo_772 : comprobar 6548930 79335 24 4913343 1024 2187 10493636 7 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_771 nodo_770

theorem nodo_773 : comprobar 6548930 79335 24 4912831 512 2187 20985085 7 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_763 nodo_772

theorem nodo_776 : comprobar 6548930 79335 24 4915135 8192 59049 35428940 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_774 nodo_775

theorem nodo_778 : comprobar 6548930 79335 24 4915135 4096 19683 23619293 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_776 nodo_777

theorem nodo_780 : comprobar 6548930 79335 24 4913087 2048 6561 15739634 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_779 nodo_778

theorem nodo_783 : comprobar 6548930 79335 24 4918207 8192 59049 35451083 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_781 nodo_782

theorem nodo_785 : comprobar 6548930 79335 24 4914111 4096 19683 23614372 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_784 nodo_783

theorem nodo_788 : comprobar 6548930 79335 24 4924351 16384 531441 159729164 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_786 nodo_787

theorem nodo_790 : comprobar 6548930 79335 24 4916159 8192 177147 106308962 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_789 nodo_788

theorem nodo_793 : comprobar 6548930 79335 24 4920255 8192 59049 35465845 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_791 nodo_792

theorem nodo_794 : comprobar 6548930 79335 24 4916159 4096 59049 70872641 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_790 nodo_793

theorem nodo_795 : comprobar 6548930 79335 24 4914111 2048 19683 47228744 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_785 nodo_794

theorem nodo_796 : comprobar 6548930 79335 24 4913087 1024 6561 31479268 8 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_780 nodo_795

theorem nodo_799 : comprobar 6548930 79335 24 4913599 16384 531441 159380405 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_797 nodo_798

theorem nodo_801 : comprobar 6548930 79335 24 4913599 8192 177147 106253603 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_799 nodo_800

theorem nodo_804 : comprobar 6548930 79335 24 4917695 8192 59049 35447392 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_802 nodo_803

theorem nodo_805 : comprobar 6548930 79335 24 4913599 4096 59049 70835735 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_801 nodo_804

theorem nodo_808 : comprobar 6548930 79335 24 4915647 8192 59049 35432630 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_806 nodo_807

theorem nodo_810 : comprobar 6548930 79335 24 4915647 4096 19683 23621753 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_808 nodo_809

theorem nodo_811 : comprobar 6548930 79335 24 4913599 2048 19683 47223823 9 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_805 nodo_810

theorem nodo_814 : comprobar 6548930 79335 24 4922815 16384 531441 159679340 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_812 nodo_813

theorem nodo_816 : comprobar 6548930 79335 24 4914623 8192 177147 106275746 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_815 nodo_814

theorem nodo_819 : comprobar 6548930 79335 24 4918719 8192 59049 35454773 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_817 nodo_818

theorem nodo_820 : comprobar 6548930 79335 24 4914623 4096 59049 70850497 10 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_816 nodo_819

theorem nodo_823 : comprobar 6548930 79335 24 4916671 16384 531441 159480049 12 2 false 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_821 nodo_822

theorem nodo_826 : comprobar 6548930 79335 24 4924863 16384 1594323 479237309 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_824 nodo_825

theorem nodo_827 : comprobar 6548930 79335 24 4916671 8192 531441 318960098 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_823 nodo_826

theorem nodo_830 : comprobar 6548930 79335 24 4928959 16384 531441 159878630 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_828 nodo_829

theorem nodo_832 : comprobar 6548930 79335 24 4920767 8192 177147 106408606 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_831 nodo_830

theorem nodo_833 : comprobar 6548930 79335 24 4916671 4096 177147 212640065 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_827 nodo_832

theorem nodo_834 : comprobar 6548930 79335 24 4914623 2048 59049 141700994 10 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_820 nodo_833

theorem nodo_835 : comprobar 6548930 79335 24 4913599 1024 19683 94447646 9 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_811 nodo_834

theorem nodo_836 : comprobar 6548930 79335 24 4913087 512 6561 62958536 8 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_796 nodo_835

theorem nodo_837 : comprobar 6548930 79335 24 4912831 256 2187 41970170 7 2 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_773 nodo_836

theorem nodo_840 : comprobar 6548930 79335 24 4918079 8192 59049 35450162 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_838 nodo_839

theorem nodo_842 : comprobar 6548930 79335 24 4913983 4096 19683 23613758 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_841 nodo_840

theorem nodo_844 : comprobar 6548930 79335 24 4913983 2048 6561 15742505 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_842 nodo_843

theorem nodo_846 : comprobar 6548930 79335 24 4912959 1024 2187 10492816 7 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_845 nodo_844

theorem nodo_849 : comprobar 6548930 79335 24 4913471 8192 59049 35416946 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_847 nodo_848

theorem nodo_851 : comprobar 6548930 79335 24 4913471 4096 19683 23611297 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_849 nodo_850

theorem nodo_854 : comprobar 6548930 79335 24 4915519 8192 59049 35431708 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_852 nodo_853

theorem nodo_857 : comprobar 6548930 79335 24 4927807 16384 531441 159841268 12 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_855 nodo_856

theorem nodo_859 : comprobar 6548930 79335 24 4919615 8192 177147 106383698 11 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_858 nodo_857

theorem nodo_860 : comprobar 6548930 79335 24 4915519 4096 59049 70863416 10 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_854 nodo_859

theorem nodo_861 : comprobar 6548930 79335 24 4913471 2048 19683 47222594 9 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_851 nodo_860

theorem nodo_864 : comprobar 6548930 79335 24 4918591 8192 59049 35453852 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_862 nodo_863

theorem nodo_866 : comprobar 6548930 79335 24 4914495 4096 19683 23616218 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_865 nodo_864

theorem nodo_868 : comprobar 6548930 79335 24 4914495 2048 6561 15744145 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_866 nodo_867

theorem nodo_869 : comprobar 6548930 79335 24 4913471 1024 6561 31481729 8 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_861 nodo_868

theorem nodo_870 : comprobar 6548930 79335 24 4912959 512 2187 20985632 7 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_846 nodo_869

theorem nodo_873 : comprobar 6548930 79335 24 4917311 8192 59049 35444627 10 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_871 nodo_872

theorem nodo_875 : comprobar 6548930 79335 24 4913215 4096 19683 23610068 9 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_874 nodo_873

theorem nodo_877 : comprobar 6548930 79335 24 4913215 2048 6561 15740045 8 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_875 nodo_876

theorem nodo_879 : comprobar 6548930 79335 24 4913215 1024 2187 10493363 7 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_877 nodo_878

theorem nodo_881 : comprobar 6548930 79335 24 4913215 512 729 6995575 6 1 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_879 nodo_880

theorem nodo_882 : comprobar 6548930 79335 24 4912959 256 729 13990421 6 1 false 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_870 nodo_881

theorem nodo_883 : comprobar 6548930 79335 24 4912831 128 729 27980113 6 1 false 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_837 nodo_882

theorem nodo_884 : comprobar 6548930 79335 24 4912767 64 729 55959497 6 1 true 122 = true := by
  exact acepta_rama (by decide +kernel) nodo_740 nodo_883

theorem nodo_887 : comprobar 6548930 79335 24 4912799 16384 531441 159354458 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_885 nodo_886

theorem nodo_889 : comprobar 6548930 79335 24 4912799 8192 177147 106236305 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_887 nodo_888

theorem nodo_892 : comprobar 6548930 79335 24 4916895 8192 59049 35441626 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_890 nodo_891

theorem nodo_893 : comprobar 6548930 79335 24 4912799 4096 59049 70824203 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_889 nodo_892

theorem nodo_896 : comprobar 6548930 79335 24 4914847 8192 59049 35426864 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_894 nodo_895

theorem nodo_898 : comprobar 6548930 79335 24 4914847 4096 19683 23617909 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_896 nodo_897

theorem nodo_899 : comprobar 6548930 79335 24 4912799 2048 19683 47216135 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_893 nodo_898

theorem nodo_902 : comprobar 6548930 79335 24 4919967 8192 59049 35463770 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_900 nodo_901

theorem nodo_904 : comprobar 6548930 79335 24 4915871 4096 19683 23622830 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_903 nodo_902

theorem nodo_906 : comprobar 6548930 79335 24 4913823 2048 6561 15741992 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_905 nodo_904

theorem nodo_907 : comprobar 6548930 79335 24 4912799 1024 6561 31477423 8 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_899 nodo_906

theorem nodo_910 : comprobar 6548930 79335 24 4913311 16384 1594323 478113191 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_908 nodo_909

theorem nodo_913 : comprobar 6548930 79335 24 4921503 16384 531441 159636784 12 2 false 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_911 nodo_912

theorem nodo_914 : comprobar 6548930 79335 24 4913311 8192 531441 318742127 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_910 nodo_913

theorem nodo_917 : comprobar 6548930 79335 24 4917407 16384 531441 159503924 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_915 nodo_916

theorem nodo_919 : comprobar 6548930 79335 24 4917407 8192 177147 106335949 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_917 nodo_918

theorem nodo_920 : comprobar 6548930 79335 24 4913311 4096 177147 212494751 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_914 nodo_919

theorem nodo_923 : comprobar 6548930 79335 24 4915359 8192 59049 35430554 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_921 nodo_922

theorem nodo_926 : comprobar 6548930 79335 24 4927647 16384 531441 159836075 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_924 nodo_925

theorem nodo_928 : comprobar 6548930 79335 24 4919455 8192 177147 106380236 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_927 nodo_926

theorem nodo_929 : comprobar 6548930 79335 24 4915359 4096 59049 70861108 10 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_923 nodo_928

theorem nodo_930 : comprobar 6548930 79335 24 4913311 2048 59049 141663167 10 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_920 nodo_929

theorem nodo_933 : comprobar 6548930 79335 24 4914335 8192 59049 35423173 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_931 nodo_932

theorem nodo_936 : comprobar 6548930 79335 24 4918431 16384 531441 159537140 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_934 nodo_935

theorem nodo_938 : comprobar 6548930 79335 24 4918431 8192 177147 106358093 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_936 nodo_937

theorem nodo_939 : comprobar 6548930 79335 24 4914335 4096 59049 70846346 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_933 nodo_938

theorem nodo_942 : comprobar 6548930 79335 24 4920479 8192 59049 35467460 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_940 nodo_941

theorem nodo_944 : comprobar 6548930 79335 24 4916383 4096 19683 23625290 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_943 nodo_942

theorem nodo_945 : comprobar 6548930 79335 24 4914335 2048 19683 47230897 9 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_939 nodo_944

theorem nodo_946 : comprobar 6548930 79335 24 4913311 1024 19683 94442111 9 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_930 nodo_945

theorem nodo_947 : comprobar 6548930 79335 24 4912799 512 6561 62954846 8 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_907 nodo_946

theorem nodo_950 : comprobar 6548930 79335 24 4919199 8192 59049 35458235 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_948 nodo_949

theorem nodo_952 : comprobar 6548930 79335 24 4915103 4096 19683 23619140 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_951 nodo_950

theorem nodo_954 : comprobar 6548930 79335 24 4913055 2048 6561 15739532 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_953 nodo_952

theorem nodo_956 : comprobar 6548930 79335 24 4913055 1024 2187 10493021 7 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_954 nodo_955

theorem nodo_959 : comprobar 6548930 79335 24 4919711 8192 59049 35461925 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_957 nodo_958

theorem nodo_961 : comprobar 6548930 79335 24 4915615 4096 19683 23621600 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_960 nodo_959

theorem nodo_963 : comprobar 6548930 79335 24 4913567 2048 6561 15741172 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_962 nodo_961

theorem nodo_966 : comprobar 6548930 79335 24 4914591 8192 59049 35425019 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_964 nodo_965

theorem nodo_968 : comprobar 6548930 79335 24 4914591 4096 19683 23616679 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_966 nodo_967

theorem nodo_971 : comprobar 6548930 79335 24 4916639 8192 59049 35439781 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_969 nodo_970

theorem nodo_974 : comprobar 6548930 79335 24 4920735 16384 531441 159611876 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_972 nodo_973

theorem nodo_976 : comprobar 6548930 79335 24 4920735 8192 177147 106407917 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_974 nodo_975

theorem nodo_977 : comprobar 6548930 79335 24 4916639 4096 59049 70879562 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_971 nodo_976

theorem nodo_978 : comprobar 6548930 79335 24 4914591 2048 19683 47233358 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_968 nodo_977

theorem nodo_979 : comprobar 6548930 79335 24 4913567 1024 6561 31482344 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_963 nodo_978

theorem nodo_980 : comprobar 6548930 79335 24 4913055 512 2187 20986042 7 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_956 nodo_979

theorem nodo_981 : comprobar 6548930 79335 24 4912799 256 2187 41969897 7 2 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_947 nodo_980

theorem nodo_984 : comprobar 6548930 79335 24 4913951 8192 59049 35420408 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_982 nodo_983

theorem nodo_986 : comprobar 6548930 79335 24 4913951 4096 19683 23613605 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_984 nodo_985

theorem nodo_988 : comprobar 6548930 79335 24 4913951 2048 6561 15742403 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_986 nodo_987

theorem nodo_990 : comprobar 6548930 79335 24 4912927 1024 2187 10492748 7 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_989 nodo_988

theorem nodo_992 : comprobar 6548930 79335 24 4912927 512 729 6995165 6 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_990 nodo_991

theorem nodo_995 : comprobar 6548930 79335 24 4915231 8192 59049 35429633 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_993 nodo_994

theorem nodo_997 : comprobar 6548930 79335 24 4915231 4096 19683 23619755 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_995 nodo_996

theorem nodo_999 : comprobar 6548930 79335 24 4913183 2048 6561 15739942 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_998 nodo_997

theorem nodo_1002 : comprobar 6548930 79335 24 4918303 8192 59049 35451776 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1000 nodo_1001

theorem nodo_1004 : comprobar 6548930 79335 24 4914207 4096 19683 23614834 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1003 nodo_1002

theorem nodo_1007 : comprobar 6548930 79335 24 4916255 16384 531441 159466562 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_1005 nodo_1006

theorem nodo_1009 : comprobar 6548930 79335 24 4916255 8192 177147 106311041 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1007 nodo_1008

theorem nodo_1012 : comprobar 6548930 79335 24 4920351 8192 59049 35466538 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1010 nodo_1011

theorem nodo_1013 : comprobar 6548930 79335 24 4916255 4096 59049 70874027 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1009 nodo_1012

theorem nodo_1014 : comprobar 6548930 79335 24 4914207 2048 19683 47229668 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1004 nodo_1013

theorem nodo_1015 : comprobar 6548930 79335 24 4913183 1024 6561 31479884 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_999 nodo_1014

theorem nodo_1018 : comprobar 6548930 79335 24 4914719 8192 59049 35425943 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1016 nodo_1017

theorem nodo_1020 : comprobar 6548930 79335 24 4914719 4096 19683 23617295 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1018 nodo_1019

theorem nodo_1022 : comprobar 6548930 79335 24 4914719 2048 6561 15744863 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1020 nodo_1021

theorem nodo_1024 : comprobar 6548930 79335 24 4913695 1024 2187 10494388 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_1023 nodo_1022

theorem nodo_1025 : comprobar 6548930 79335 24 4913183 512 2187 20986589 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_1015 nodo_1024

theorem nodo_1026 : comprobar 6548930 79335 24 4912927 256 729 13990330 6 2 false 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_992 nodo_1025

theorem nodo_1027 : comprobar 6548930 79335 24 4912799 128 729 27979931 6 2 true 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_981 nodo_1026

theorem nodo_1030 : comprobar 6548930 79335 24 4915423 8192 59049 35431019 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1028 nodo_1029

theorem nodo_1032 : comprobar 6548930 79335 24 4915423 4096 19683 23620679 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1030 nodo_1031

theorem nodo_1034 : comprobar 6548930 79335 24 4913375 2048 6561 15740558 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1033 nodo_1032

theorem nodo_1036 : comprobar 6548930 79335 24 4913375 1024 2187 10493705 7 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_1034 nodo_1035

theorem nodo_1038 : comprobar 6548930 79335 24 4912863 512 729 6995074 6 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_1037 nodo_1036

theorem nodo_1041 : comprobar 6548930 79335 24 4916191 8192 59049 35436554 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1039 nodo_1040

theorem nodo_1043 : comprobar 6548930 79335 24 4916191 4096 19683 23624369 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1041 nodo_1042

theorem nodo_1045 : comprobar 6548930 79335 24 4914143 2048 6561 15743018 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1044 nodo_1043

theorem nodo_1047 : comprobar 6548930 79335 24 4913119 1024 2187 10493158 7 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_1046 nodo_1045

theorem nodo_1050 : comprobar 6548930 79335 24 4913631 8192 59049 35418100 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1048 nodo_1049

theorem nodo_1053 : comprobar 6548930 79335 24 4925919 16384 531441 159780032 12 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_1051 nodo_1052

theorem nodo_1055 : comprobar 6548930 79335 24 4917727 8192 177147 106342874 11 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1054 nodo_1053

theorem nodo_1056 : comprobar 6548930 79335 24 4913631 4096 59049 70836200 10 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1050 nodo_1055

theorem nodo_1059 : comprobar 6548930 79335 24 4919775 8192 59049 35462387 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1057 nodo_1058

theorem nodo_1061 : comprobar 6548930 79335 24 4915679 4096 19683 23621908 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1060 nodo_1059

theorem nodo_1062 : comprobar 6548930 79335 24 4913631 2048 19683 47224133 9 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1056 nodo_1061

theorem nodo_1065 : comprobar 6548930 79335 24 4916703 8192 59049 35440244 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1063 nodo_1064

theorem nodo_1067 : comprobar 6548930 79335 24 4916703 4096 19683 23626829 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1065 nodo_1066

theorem nodo_1069 : comprobar 6548930 79335 24 4914655 2048 6561 15744658 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1068 nodo_1067

theorem nodo_1070 : comprobar 6548930 79335 24 4913631 1024 6561 31482755 8 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_1062 nodo_1069

theorem nodo_1071 : comprobar 6548930 79335 24 4913119 512 2187 20986316 7 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_1047 nodo_1070

theorem nodo_1072 : comprobar 6548930 79335 24 4912863 256 729 13990148 6 2 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_1038 nodo_1071

theorem nodo_1074 : comprobar 6548930 79335 24 4912863 128 243 9326765 5 1 false 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_1072 nodo_1073

theorem nodo_1075 : comprobar 6548930 79335 24 4912799 64 243 18653287 5 1 false 122 = true := by
  exact acepta_rama (by decide +kernel) nodo_1027 nodo_1074

theorem nodo_1076 : comprobar 6548930 79335 24 4912767 32 243 37306331 5 1 true 123 = true := by
  exact acepta_rama (by decide +kernel) nodo_884 nodo_1075

theorem nodo_1077 : comprobar 6548930 79335 24 4912751 16 81 24870806 4 1 true 124 = true := by
  exact acepta_rama (by decide +kernel) nodo_481 nodo_1076

theorem nodo_1078 : comprobar 6548930 79335 24 4912743 8 27 16580510 3 1 true 125 = true := by
  exact acepta_rama (by decide +kernel) nodo_240 nodo_1077

theorem nodo_1081 : comprobar 6548930 79335 24 4918011 8192 59049 35449676 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1079 nodo_1080

theorem nodo_1083 : comprobar 6548930 79335 24 4913915 4096 19683 23613434 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1082 nodo_1081

theorem nodo_1085 : comprobar 6548930 79335 24 4913915 2048 6561 15742289 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1083 nodo_1084

theorem nodo_1087 : comprobar 6548930 79335 24 4912891 1024 2187 10492672 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_1086 nodo_1085

theorem nodo_1090 : comprobar 6548930 79335 24 4913403 8192 59049 35416460 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1088 nodo_1089

theorem nodo_1092 : comprobar 6548930 79335 24 4913403 4096 19683 23610973 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1090 nodo_1091

theorem nodo_1095 : comprobar 6548930 79335 24 4915451 8192 59049 35431222 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1093 nodo_1094

theorem nodo_1098 : comprobar 6548930 79335 24 4927739 16384 531441 159839081 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_1096 nodo_1097

theorem nodo_1100 : comprobar 6548930 79335 24 4919547 8192 177147 106382240 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1099 nodo_1098

theorem nodo_1101 : comprobar 6548930 79335 24 4915451 4096 59049 70862444 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1095 nodo_1100

theorem nodo_1102 : comprobar 6548930 79335 24 4913403 2048 19683 47221946 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1092 nodo_1101

theorem nodo_1105 : comprobar 6548930 79335 24 4918523 8192 59049 35453366 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1103 nodo_1104

theorem nodo_1107 : comprobar 6548930 79335 24 4914427 4096 19683 23615894 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1106 nodo_1105

theorem nodo_1109 : comprobar 6548930 79335 24 4914427 2048 6561 15743929 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1107 nodo_1108

theorem nodo_1110 : comprobar 6548930 79335 24 4913403 1024 6561 31481297 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_1102 nodo_1109

theorem nodo_1111 : comprobar 6548930 79335 24 4912891 512 2187 20985344 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_1087 nodo_1110

theorem nodo_1114 : comprobar 6548930 79335 24 4917243 8192 59049 35444141 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1112 nodo_1113

theorem nodo_1116 : comprobar 6548930 79335 24 4913147 4096 19683 23609744 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1115 nodo_1114

theorem nodo_1118 : comprobar 6548930 79335 24 4913147 2048 6561 15739829 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1116 nodo_1117

theorem nodo_1120 : comprobar 6548930 79335 24 4913147 1024 2187 10493219 7 4 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_1118 nodo_1119

theorem nodo_1122 : comprobar 6548930 79335 24 4913147 512 729 6995479 6 3 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_1120 nodo_1121

theorem nodo_1123 : comprobar 6548930 79335 24 4912891 256 729 13990229 6 3 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_1111 nodo_1122

theorem nodo_1125 : comprobar 6548930 79335 24 4912763 128 243 9326576 5 3 true 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_1124 nodo_1123

theorem nodo_1127 : comprobar 6548930 79335 24 4912763 64 81 6217717 4 2 false 122 = true := by
  exact acepta_rama (by decide +kernel) nodo_1125 nodo_1126

theorem nodo_1130 : comprobar 6548930 79335 24 4918939 8192 59049 35456363 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1128 nodo_1129

theorem nodo_1132 : comprobar 6548930 79335 24 4914843 4096 19683 23617892 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1131 nodo_1130

theorem nodo_1134 : comprobar 6548930 79335 24 4912795 2048 6561 15738700 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1133 nodo_1132

theorem nodo_1137 : comprobar 6548930 79335 24 4913819 8192 59049 35419457 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1135 nodo_1136

theorem nodo_1139 : comprobar 6548930 79335 24 4913819 4096 19683 23612971 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1137 nodo_1138

theorem nodo_1142 : comprobar 6548930 79335 24 4915867 8192 59049 35434219 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1140 nodo_1141

theorem nodo_1145 : comprobar 6548930 79335 24 4919963 16384 531441 159586847 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_1143 nodo_1144

theorem nodo_1147 : comprobar 6548930 79335 24 4919963 8192 177147 106391231 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1145 nodo_1146

theorem nodo_1148 : comprobar 6548930 79335 24 4915867 4096 59049 70868438 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1142 nodo_1147

theorem nodo_1149 : comprobar 6548930 79335 24 4913819 2048 19683 47225942 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1139 nodo_1148

theorem nodo_1150 : comprobar 6548930 79335 24 4912795 1024 6561 31477400 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_1134 nodo_1149

theorem nodo_1153 : comprobar 6548930 79335 24 4918427 8192 59049 35452673 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1151 nodo_1152

theorem nodo_1155 : comprobar 6548930 79335 24 4914331 4096 19683 23615432 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1154 nodo_1153

theorem nodo_1157 : comprobar 6548930 79335 24 4914331 2048 6561 15743621 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1155 nodo_1156

theorem nodo_1159 : comprobar 6548930 79335 24 4913307 1024 2187 10493560 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_1158 nodo_1157

theorem nodo_1160 : comprobar 6548930 79335 24 4912795 512 2187 20984933 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_1150 nodo_1159

theorem nodo_1163 : comprobar 6548930 79335 24 4917659 8192 59049 35447138 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1161 nodo_1162

theorem nodo_1165 : comprobar 6548930 79335 24 4913563 4096 19683 23611742 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1164 nodo_1163

theorem nodo_1167 : comprobar 6548930 79335 24 4913563 2048 6561 15741161 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1165 nodo_1166

theorem nodo_1169 : comprobar 6548930 79335 24 4913563 1024 2187 10494107 7 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_1167 nodo_1168

theorem nodo_1171 : comprobar 6548930 79335 24 4913051 512 729 6995342 6 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_1170 nodo_1169

theorem nodo_1172 : comprobar 6548930 79335 24 4912795 256 729 13989955 6 2 false 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_1160 nodo_1171

theorem nodo_1175 : comprobar 6548930 79335 24 4921115 16384 531441 159624209 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_1173 nodo_1174

theorem nodo_1177 : comprobar 6548930 79335 24 4912923 8192 177147 106238992 11 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1176 nodo_1175

theorem nodo_1180 : comprobar 6548930 79335 24 4917019 16384 1594323 478474046 13 2 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_1178 nodo_1179

theorem nodo_1183 : comprobar 6548930 79335 24 4925211 16384 531441 159757069 12 2 false 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_1181 nodo_1182

theorem nodo_1184 : comprobar 6548930 79335 24 4917019 8192 531441 318982697 12 2 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1180 nodo_1183

theorem nodo_1185 : comprobar 6548930 79335 24 4912923 4096 177147 212477984 11 2 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1177 nodo_1184

theorem nodo_1188 : comprobar 6548930 79335 24 4914971 16384 531441 159424919 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_1186 nodo_1187

theorem nodo_1190 : comprobar 6548930 79335 24 4914971 8192 177147 106283279 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1188 nodo_1189

theorem nodo_1193 : comprobar 6548930 79335 24 4919067 8192 59049 35457284 10 2 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1191 nodo_1192

theorem nodo_1194 : comprobar 6548930 79335 24 4914971 4096 59049 70855519 10 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1190 nodo_1193

theorem nodo_1195 : comprobar 6548930 79335 24 4912923 2048 59049 141651989 10 2 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1185 nodo_1194

theorem nodo_1198 : comprobar 6548930 79335 24 4922139 16384 531441 159657425 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_1196 nodo_1197

theorem nodo_1200 : comprobar 6548930 79335 24 4913947 8192 177147 106261136 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1199 nodo_1198

theorem nodo_1203 : comprobar 6548930 79335 24 4918043 8192 59049 35449903 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1201 nodo_1202

theorem nodo_1204 : comprobar 6548930 79335 24 4913947 4096 59049 70840757 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1200 nodo_1203

theorem nodo_1207 : comprobar 6548930 79335 24 4915995 8192 59049 35435141 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1205 nodo_1206

theorem nodo_1209 : comprobar 6548930 79335 24 4915995 4096 19683 23623427 9 2 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1207 nodo_1208

theorem nodo_1210 : comprobar 6548930 79335 24 4913947 2048 19683 47227171 9 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1204 nodo_1209

theorem nodo_1211 : comprobar 6548930 79335 24 4912923 1024 19683 94434659 9 2 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_1195 nodo_1210

theorem nodo_1214 : comprobar 6548930 79335 24 4915483 8192 59049 35431451 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1212 nodo_1213

theorem nodo_1216 : comprobar 6548930 79335 24 4915483 4096 19683 23620967 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1214 nodo_1215

theorem nodo_1218 : comprobar 6548930 79335 24 4913435 2048 6561 15740750 8 2 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1217 nodo_1216

theorem nodo_1221 : comprobar 6548930 79335 24 4918555 8192 59049 35453594 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1219 nodo_1220

theorem nodo_1223 : comprobar 6548930 79335 24 4914459 4096 19683 23616046 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1222 nodo_1221

theorem nodo_1226 : comprobar 6548930 79335 24 4916507 16384 531441 159474743 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_1224 nodo_1225

theorem nodo_1228 : comprobar 6548930 79335 24 4916507 8192 177147 106316495 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1226 nodo_1227

theorem nodo_1231 : comprobar 6548930 79335 24 4920603 8192 59049 35468356 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1229 nodo_1230

theorem nodo_1232 : comprobar 6548930 79335 24 4916507 4096 59049 70877663 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1228 nodo_1231

theorem nodo_1233 : comprobar 6548930 79335 24 4914459 2048 19683 47232092 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1223 nodo_1232

theorem nodo_1234 : comprobar 6548930 79335 24 4913435 1024 6561 31481500 8 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_1218 nodo_1233

theorem nodo_1235 : comprobar 6548930 79335 24 4912923 512 6561 62956439 8 2 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_1211 nodo_1234

theorem nodo_1238 : comprobar 6548930 79335 24 4915227 8192 59049 35429606 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1236 nodo_1237

theorem nodo_1240 : comprobar 6548930 79335 24 4915227 4096 19683 23619737 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1238 nodo_1239

theorem nodo_1242 : comprobar 6548930 79335 24 4913179 2048 6561 15739930 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1241 nodo_1240

theorem nodo_1245 : comprobar 6548930 79335 24 4918299 8192 59049 35451749 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1243 nodo_1244

theorem nodo_1247 : comprobar 6548930 79335 24 4914203 4096 19683 23614816 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1246 nodo_1245

theorem nodo_1250 : comprobar 6548930 79335 24 4924443 16384 531441 159732161 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_1248 nodo_1249

theorem nodo_1252 : comprobar 6548930 79335 24 4916251 8192 177147 106310960 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1251 nodo_1250

theorem nodo_1255 : comprobar 6548930 79335 24 4920347 8192 59049 35466511 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1253 nodo_1254

theorem nodo_1256 : comprobar 6548930 79335 24 4916251 4096 59049 70873973 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1252 nodo_1255

theorem nodo_1257 : comprobar 6548930 79335 24 4914203 2048 19683 47229632 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1247 nodo_1256

theorem nodo_1258 : comprobar 6548930 79335 24 4913179 1024 6561 31479860 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_1242 nodo_1257

theorem nodo_1261 : comprobar 6548930 79335 24 4914715 8192 59049 35425916 10 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1259 nodo_1260

theorem nodo_1263 : comprobar 6548930 79335 24 4914715 4096 19683 23617277 9 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1261 nodo_1262

theorem nodo_1265 : comprobar 6548930 79335 24 4914715 2048 6561 15744851 8 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1263 nodo_1264

theorem nodo_1267 : comprobar 6548930 79335 24 4913691 1024 2187 10494380 7 2 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_1266 nodo_1265

theorem nodo_1268 : comprobar 6548930 79335 24 4913179 512 2187 20986573 7 2 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_1258 nodo_1267

theorem nodo_1269 : comprobar 6548930 79335 24 4912923 256 2187 41970959 7 2 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_1235 nodo_1268

theorem nodo_1270 : comprobar 6548930 79335 24 4912795 128 729 27979910 6 2 true 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_1172 nodo_1269

theorem nodo_1273 : comprobar 6548930 79335 24 4915035 4096 19683 23618816 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1271 nodo_1272

theorem nodo_1275 : comprobar 6548930 79335 24 4912987 2048 6561 15739316 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1274 nodo_1273

theorem nodo_1277 : comprobar 6548930 79335 24 4912987 1024 2187 10492877 7 4 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_1275 nodo_1276

theorem nodo_1279 : comprobar 6548930 79335 24 4912987 512 729 6995251 6 3 false 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_1277 nodo_1278

theorem nodo_1282 : comprobar 6548930 79335 24 4913243 16384 531441 159368876 12 3 true 114 = true := by
  exact acepta_rama (by decide +kernel) nodo_1280 nodo_1281

theorem nodo_1284 : comprobar 6548930 79335 24 4913243 8192 177147 106245917 11 3 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1282 nodo_1283

theorem nodo_1287 : comprobar 6548930 79335 24 4917339 8192 59049 35444830 10 3 false 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1285 nodo_1286

theorem nodo_1288 : comprobar 6548930 79335 24 4913243 4096 59049 70830611 10 3 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1284 nodo_1287

theorem nodo_1291 : comprobar 6548930 79335 24 4915291 8192 59049 35430068 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1289 nodo_1290

theorem nodo_1293 : comprobar 6548930 79335 24 4915291 4096 19683 23620045 9 3 false 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1291 nodo_1292

theorem nodo_1294 : comprobar 6548930 79335 24 4913243 2048 19683 47220407 9 3 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1288 nodo_1293

theorem nodo_1297 : comprobar 6548930 79335 24 4920411 8192 59049 35466974 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1295 nodo_1296

theorem nodo_1299 : comprobar 6548930 79335 24 4916315 4096 19683 23624966 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1298 nodo_1297

theorem nodo_1301 : comprobar 6548930 79335 24 4914267 2048 6561 15743416 8 3 false 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1300 nodo_1299

theorem nodo_1302 : comprobar 6548930 79335 24 4913243 1024 6561 31480271 8 3 true 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_1294 nodo_1301

theorem nodo_1305 : comprobar 6548930 79335 24 4919899 8192 59049 35463284 10 4 true 115 = true := by
  exact acepta_rama (by decide +kernel) nodo_1303 nodo_1304

theorem nodo_1307 : comprobar 6548930 79335 24 4915803 4096 19683 23622506 9 4 true 116 = true := by
  exact acepta_rama (by decide +kernel) nodo_1306 nodo_1305

theorem nodo_1309 : comprobar 6548930 79335 24 4913755 2048 6561 15741776 8 4 true 117 = true := by
  exact acepta_rama (by decide +kernel) nodo_1308 nodo_1307

theorem nodo_1311 : comprobar 6548930 79335 24 4913755 1024 2187 10494517 7 3 false 118 = true := by
  exact acepta_rama (by decide +kernel) nodo_1309 nodo_1310

theorem nodo_1312 : comprobar 6548930 79335 24 4913243 512 2187 20986847 7 3 true 119 = true := by
  exact acepta_rama (by decide +kernel) nodo_1302 nodo_1311

theorem nodo_1313 : comprobar 6548930 79335 24 4912987 256 729 13990502 6 3 true 120 = true := by
  exact acepta_rama (by decide +kernel) nodo_1279 nodo_1312

theorem nodo_1315 : comprobar 6548930 79335 24 4912859 128 243 9326758 5 2 false 121 = true := by
  exact acepta_rama (by decide +kernel) nodo_1314 nodo_1313

theorem nodo_1316 : comprobar 6548930 79335 24 4912795 64 243 18653273 5 2 true 122 = true := by
  exact acepta_rama (by decide +kernel) nodo_1270 nodo_1315

theorem nodo_1317 : comprobar 6548930 79335 24 4912763 32 81 12435434 4 2 true 123 = true := by
  exact acepta_rama (by decide +kernel) nodo_1127 nodo_1316

theorem nodo_1319 : comprobar 6548930 79335 24 4912747 16 27 8290262 3 2 true 124 = true := by
  exact acepta_rama (by decide +kernel) nodo_1318 nodo_1317

theorem nodo_1321 : comprobar 6548930 79335 24 4912747 8 9 5526841 2 1 false 125 = true := by
  exact acepta_rama (by decide +kernel) nodo_1319 nodo_1320

theorem nodo_1322 : comprobar 6548930 79335 24 4912743 4 9 11053673 2 1 true 126 = true := by
  exact acepta_rama (by decide +kernel) nodo_1078 nodo_1321

theorem nodo_1324 : comprobar 6548930 79335 24 4912741 2 3 7369112 1 1 true 127 = true := by
  exact acepta_rama (by decide +kernel) nodo_1323 nodo_1322

theorem nodo_1326 : comprobar 6548930 79335 24 4912741 1 1 4912741 0 0 false 128 = true := by
  exact acepta_rama (by decide +kernel) nodo_1324 nodo_1325

theorem certificado :
    comprobar 6548930 79335 24 4912741 1 1 4912741 0 0 false 128 = true := nodo_1326

theorem descenso {n k : ℕ} (hinicio : 4912741 ≤ n) (hmax : n ≤ 6548930)
    (hk : PrimerCruce n k) (hr : rachas n k ≤ 24) (hq : 79335 ≤ S k n) :
    T^[k] n < n := OcelotasCribaPrefijosBinarios.certificado_descenso
      certificado hinicio hmax hk hr hq

end OcelotasVeinticuatroPrefijosBajo

#print axioms OcelotasVeinticuatroPrefijosBajo.certificado
#print axioms OcelotasVeinticuatroPrefijosBajo.descenso
