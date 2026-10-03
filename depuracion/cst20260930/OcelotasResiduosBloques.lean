import OcelotasResiduos

/-! Generado por generar_residuos_lean.py. Cada bloque se evalúa en el núcleo. -/
namespace OcelotasResiduosBloques
open OcelotasResiduos

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem nodo_1 : comprobar 4912740 2 2 1 1 224 = true := by
  decide +kernel

theorem nodo_5 : comprobar 4912740 3 16 9 2 221 = true := by
  decide +kernel

theorem nodo_7 : comprobar 4912740 11 32 27 10 220 = true := by
  decide +kernel

theorem nodo_13 : comprobar 4912740 27 1024 6561 182 215 = true := by
  decide +kernel

theorem nodo_14 : comprobar 4912740 539 1024 2187 1154 215 = true := by
  decide +kernel

theorem nodo_12 : comprobar 4912740 27 512 2187 121 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_13 nodo_14

theorem nodo_16 : comprobar 4912740 283 1024 6561 1822 215 = true := by
  decide +kernel

theorem nodo_17 : comprobar 4912740 795 1024 19683 15308 215 = true := by
  decide +kernel

theorem nodo_15 : comprobar 4912740 283 512 6561 3644 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_16 nodo_17

theorem nodo_11 : comprobar 4912740 27 256 2187 242 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_12 nodo_15

theorem nodo_20 : comprobar 4912740 155 1024 2187 334 215 = true := by
  decide +kernel

theorem nodo_21 : comprobar 4912740 667 1024 6561 4283 215 = true := by
  decide +kernel

theorem nodo_19 : comprobar 4912740 155 512 2187 668 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_20 nodo_21

theorem nodo_23 : comprobar 4912740 411 1024 2187 881 215 = true := by
  decide +kernel

theorem nodo_24 : comprobar 4912740 923 1024 729 658 215 = true := by
  decide +kernel

theorem nodo_22 : comprobar 4912740 411 512 729 587 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_23 nodo_24

theorem nodo_18 : comprobar 4912740 155 256 729 445 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_19 nodo_22

theorem nodo_10 : comprobar 4912740 27 128 729 161 218 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_11 nodo_18

theorem nodo_28 : comprobar 4912740 91 1024 6561 593 215 = true := by
  decide +kernel

theorem nodo_29 : comprobar 4912740 603 1024 2187 1291 215 = true := by
  decide +kernel

theorem nodo_27 : comprobar 4912740 91 512 2187 395 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_28 nodo_29

theorem nodo_31 : comprobar 4912740 347 1024 729 248 215 = true := by
  decide +kernel

theorem nodo_32 : comprobar 4912740 859 1024 2187 1838 215 = true := by
  decide +kernel

theorem nodo_30 : comprobar 4912740 347 512 729 496 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_31 nodo_32

theorem nodo_26 : comprobar 4912740 91 256 729 263 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_27 nodo_30

theorem nodo_33 : comprobar 4912740 219 256 243 209 217 = true := by
  decide +kernel

theorem nodo_25 : comprobar 4912740 91 128 243 175 218 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_26 nodo_33

theorem nodo_9 : comprobar 4912740 27 64 243 107 219 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_10 nodo_25

theorem nodo_35 : comprobar 4912740 59 128 81 38 218 = true := by
  decide +kernel

theorem nodo_37 : comprobar 4912740 123 256 243 118 217 = true := by
  decide +kernel

theorem nodo_40 : comprobar 4912740 251 1024 6561 1619 215 = true := by
  decide +kernel

theorem nodo_41 : comprobar 4912740 763 1024 2187 1633 215 = true := by
  decide +kernel

theorem nodo_39 : comprobar 4912740 251 512 2187 1079 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_40 nodo_41

theorem nodo_43 : comprobar 4912740 507 1024 729 362 215 = true := by
  decide +kernel

theorem nodo_44 : comprobar 4912740 1019 1024 2187 2180 215 = true := by
  decide +kernel

theorem nodo_42 : comprobar 4912740 507 512 729 724 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_43 nodo_44

theorem nodo_38 : comprobar 4912740 251 256 729 719 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_39 nodo_42

theorem nodo_36 : comprobar 4912740 123 128 243 236 218 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_37 nodo_38

theorem nodo_34 : comprobar 4912740 59 64 81 76 219 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_35 nodo_36

theorem nodo_8 : comprobar 4912740 27 32 81 71 220 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_9 nodo_34

theorem nodo_6 : comprobar 4912740 11 16 27 20 221 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_7 nodo_8

theorem nodo_4 : comprobar 4912740 3 8 9 4 222 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_5 nodo_6

theorem nodo_49 : comprobar 4912740 7 128 81 5 218 = true := by
  decide +kernel

theorem nodo_53 : comprobar 4912740 71 1024 2187 155 215 = true := by
  decide +kernel

theorem nodo_54 : comprobar 4912740 583 1024 729 416 215 = true := by
  decide +kernel

theorem nodo_52 : comprobar 4912740 71 512 729 103 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_53 nodo_54

theorem nodo_56 : comprobar 4912740 327 1024 6561 2105 215 = true := by
  decide +kernel

theorem nodo_57 : comprobar 4912740 839 1024 2187 1795 215 = true := by
  decide +kernel

#print axioms nodo_57

theorem nodo_55 : comprobar 4912740 327 512 2187 1403 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_56 nodo_57

theorem nodo_51 : comprobar 4912740 71 256 729 206 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_52 nodo_55

theorem nodo_58 : comprobar 4912740 199 256 243 190 217 = true := by
  decide +kernel

theorem nodo_50 : comprobar 4912740 71 128 243 137 218 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_51 nodo_58

theorem nodo_48 : comprobar 4912740 7 64 81 10 219 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_49 nodo_50

theorem nodo_61 : comprobar 4912740 39 256 243 38 217 = true := by
  decide +kernel

theorem nodo_64 : comprobar 4912740 167 1024 6561 1079 215 = true := by
  decide +kernel

theorem nodo_65 : comprobar 4912740 679 1024 2187 1453 215 = true := by
  decide +kernel

theorem nodo_63 : comprobar 4912740 167 512 2187 719 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_64 nodo_65

theorem nodo_67 : comprobar 4912740 423 1024 729 302 215 = true := by
  decide +kernel

theorem nodo_68 : comprobar 4912740 935 1024 2187 2000 215 = true := by
  decide +kernel

theorem nodo_66 : comprobar 4912740 423 512 729 604 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_67 nodo_68

theorem nodo_62 : comprobar 4912740 167 256 729 479 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_63 nodo_66

theorem nodo_60 : comprobar 4912740 39 128 243 76 218 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_61 nodo_62

theorem nodo_72 : comprobar 4912740 103 1024 6561 668 215 = true := by
  decide +kernel

theorem nodo_73 : comprobar 4912740 615 1024 2187 1316 215 = true := by
  decide +kernel

theorem nodo_71 : comprobar 4912740 103 512 2187 445 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_72 nodo_73

theorem nodo_75 : comprobar 4912740 359 1024 6561 2308 215 = true := by
  decide +kernel

theorem nodo_76 : comprobar 4912740 871 1024 19683 16766 215 = true := by
  decide +kernel

theorem nodo_74 : comprobar 4912740 359 512 6561 4616 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_75 nodo_76

theorem nodo_70 : comprobar 4912740 103 256 2187 890 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_71 nodo_74

theorem nodo_79 : comprobar 4912740 231 1024 2187 496 215 = true := by
  decide +kernel

theorem nodo_80 : comprobar 4912740 743 1024 6561 4769 215 = true := by
  decide +kernel

theorem nodo_78 : comprobar 4912740 231 512 2187 992 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_79 nodo_80

theorem nodo_82 : comprobar 4912740 487 1024 2187 1043 215 = true := by
  decide +kernel

theorem nodo_83 : comprobar 4912740 999 1024 729 712 215 = true := by
  decide +kernel

theorem nodo_81 : comprobar 4912740 487 512 729 695 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_82 nodo_83

theorem nodo_77 : comprobar 4912740 231 256 729 661 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_78 nodo_81

theorem nodo_69 : comprobar 4912740 103 128 729 593 218 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_70 nodo_77

theorem nodo_59 : comprobar 4912740 39 64 243 152 219 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_60 nodo_69

theorem nodo_47 : comprobar 4912740 7 32 81 20 220 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_48 nodo_59

theorem nodo_84 : comprobar 4912740 23 32 27 20 220 = true := by
  decide +kernel

theorem nodo_46 : comprobar 4912740 7 16 27 13 221 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_47 nodo_84

theorem nodo_88 : comprobar 4912740 15 128 81 10 218 = true := by
  decide +kernel

theorem nodo_90 : comprobar 4912740 79 256 243 76 217 = true := by
  decide +kernel

theorem nodo_93 : comprobar 4912740 207 1024 2187 445 215 = true := by
  decide +kernel

theorem nodo_94 : comprobar 4912740 719 1024 6561 4616 215 = true := by
  decide +kernel

theorem nodo_92 : comprobar 4912740 207 512 2187 890 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_93 nodo_94

theorem nodo_96 : comprobar 4912740 463 1024 2187 992 215 = true := by
  decide +kernel

theorem nodo_97 : comprobar 4912740 975 1024 729 695 215 = true := by
  decide +kernel

theorem nodo_95 : comprobar 4912740 463 512 729 661 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_96 nodo_97

theorem nodo_91 : comprobar 4912740 207 256 729 593 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_92 nodo_95

theorem nodo_89 : comprobar 4912740 79 128 243 152 218 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_90 nodo_91

theorem nodo_87 : comprobar 4912740 15 64 81 20 219 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_88 nodo_89

theorem nodo_102 : comprobar 4912740 47 1024 2187 103 215 = true := by
  decide +kernel

theorem nodo_103 : comprobar 4912740 559 1024 6561 3590 215 = true := by
  decide +kernel

theorem nodo_101 : comprobar 4912740 47 512 2187 206 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_102 nodo_103

theorem nodo_105 : comprobar 4912740 303 1024 2187 650 215 = true := by
  decide +kernel

#print axioms nodo_105

theorem nodo_106 : comprobar 4912740 815 1024 729 581 215 = true := by
  decide +kernel

theorem nodo_104 : comprobar 4912740 303 512 729 433 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_105 nodo_106

theorem nodo_100 : comprobar 4912740 47 256 729 137 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_101 nodo_104

theorem nodo_107 : comprobar 4912740 175 256 243 167 217 = true := by
  decide +kernel

theorem nodo_99 : comprobar 4912740 47 128 243 91 218 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_100 nodo_107

theorem nodo_111 : comprobar 4912740 111 1024 6561 719 215 = true := by
  decide +kernel

theorem nodo_112 : comprobar 4912740 623 1024 2187 1333 215 = true := by
  decide +kernel

theorem nodo_110 : comprobar 4912740 111 512 2187 479 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_111 nodo_112

theorem nodo_114 : comprobar 4912740 367 1024 729 262 215 = true := by
  decide +kernel

theorem nodo_115 : comprobar 4912740 879 1024 2187 1880 215 = true := by
  decide +kernel

theorem nodo_113 : comprobar 4912740 367 512 729 524 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_114 nodo_115

theorem nodo_109 : comprobar 4912740 111 256 729 319 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_110 nodo_113

theorem nodo_118 : comprobar 4912740 239 1024 19683 4616 215 = true := by
  decide +kernel

theorem nodo_119 : comprobar 4912740 751 1024 6561 4819 215 = true := by
  decide +kernel

theorem nodo_117 : comprobar 4912740 239 512 6561 3077 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_118 nodo_119

theorem nodo_121 : comprobar 4912740 495 1024 6561 3179 215 = true := by
  decide +kernel

theorem nodo_122 : comprobar 4912740 1007 1024 2187 2153 215 = true := by
  decide +kernel

theorem nodo_120 : comprobar 4912740 495 512 2187 2119 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_121 nodo_122

theorem nodo_116 : comprobar 4912740 239 256 2187 2051 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_117 nodo_120

theorem nodo_108 : comprobar 4912740 111 128 729 638 218 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_109 nodo_116

theorem nodo_98 : comprobar 4912740 47 64 243 182 219 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_99 nodo_108

theorem nodo_86 : comprobar 4912740 15 32 81 40 220 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_87 nodo_98

theorem nodo_128 : comprobar 4912740 31 1024 6561 206 215 = true := by
  decide +kernel

theorem nodo_129 : comprobar 4912740 543 1024 2187 1162 215 = true := by
  decide +kernel

theorem nodo_127 : comprobar 4912740 31 512 2187 137 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_128 nodo_129

theorem nodo_131 : comprobar 4912740 287 1024 729 205 215 = true := by
  decide +kernel

theorem nodo_132 : comprobar 4912740 799 1024 2187 1709 215 = true := by
  decide +kernel

theorem nodo_130 : comprobar 4912740 287 512 729 410 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_131 nodo_132

theorem nodo_126 : comprobar 4912740 31 256 729 91 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_127 nodo_130

theorem nodo_135 : comprobar 4912740 159 1024 19683 3077 215 = true := by
  decide +kernel

theorem nodo_136 : comprobar 4912740 671 1024 6561 4306 215 = true := by
  decide +kernel

theorem nodo_134 : comprobar 4912740 159 512 6561 2051 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_135 nodo_136

theorem nodo_138 : comprobar 4912740 415 1024 6561 2666 215 = true := by
  decide +kernel

theorem nodo_139 : comprobar 4912740 927 1024 2187 1982 215 = true := by
  decide +kernel

theorem nodo_137 : comprobar 4912740 415 512 2187 1777 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_138 nodo_139

theorem nodo_133 : comprobar 4912740 159 256 2187 1367 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_134 nodo_137

theorem nodo_125 : comprobar 4912740 31 128 729 182 218 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_126 nodo_133

theorem nodo_141 : comprobar 4912740 95 256 243 91 217 = true := by
  decide +kernel

theorem nodo_144 : comprobar 4912740 223 1024 2187 479 215 = true := by
  decide +kernel

theorem nodo_145 : comprobar 4912740 735 1024 729 524 215 = true := by
  decide +kernel

theorem nodo_143 : comprobar 4912740 223 512 729 319 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_144 nodo_145

theorem nodo_147 : comprobar 4912740 479 1024 6561 3077 215 = true := by
  decide +kernel

#print axioms nodo_147

theorem nodo_148 : comprobar 4912740 991 1024 2187 2119 215 = true := by
  decide +kernel

theorem nodo_146 : comprobar 4912740 479 512 2187 2051 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_147 nodo_148

theorem nodo_142 : comprobar 4912740 223 256 729 638 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_143 nodo_146

theorem nodo_140 : comprobar 4912740 95 128 243 182 218 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_141 nodo_142

theorem nodo_124 : comprobar 4912740 31 64 243 121 219 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_125 nodo_140

theorem nodo_153 : comprobar 4912740 63 1024 2187 137 215 = true := by
  decide +kernel

theorem nodo_154 : comprobar 4912740 575 1024 729 410 215 = true := by
  decide +kernel

theorem nodo_152 : comprobar 4912740 63 512 729 91 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_153 nodo_154

theorem nodo_156 : comprobar 4912740 319 1024 6561 2051 215 = true := by
  decide +kernel

theorem nodo_157 : comprobar 4912740 831 1024 2187 1777 215 = true := by
  decide +kernel

theorem nodo_155 : comprobar 4912740 319 512 2187 1367 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_156 nodo_157

theorem nodo_151 : comprobar 4912740 63 256 729 182 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_152 nodo_155

theorem nodo_160 : comprobar 4912740 191 1024 2187 410 215 = true := by
  decide +kernel

theorem nodo_161 : comprobar 4912740 703 1024 6561 4511 215 = true := by
  decide +kernel

theorem nodo_159 : comprobar 4912740 191 512 2187 820 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_160 nodo_161

theorem nodo_163 : comprobar 4912740 447 1024 19683 8612 215 = true := by
  decide +kernel

theorem nodo_164 : comprobar 4912740 959 1024 6561 6151 215 = true := by
  decide +kernel

theorem nodo_162 : comprobar 4912740 447 512 6561 5741 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_163 nodo_164

theorem nodo_158 : comprobar 4912740 191 256 2187 1640 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_159 nodo_162

theorem nodo_150 : comprobar 4912740 63 128 729 364 218 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_151 nodo_158

theorem nodo_168 : comprobar 4912740 127 1024 6561 820 215 = true := by
  decide +kernel

theorem nodo_169 : comprobar 4912740 639 1024 19683 12302 215 = true := by
  decide +kernel

theorem nodo_167 : comprobar 4912740 127 512 6561 1640 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_168 nodo_169

theorem nodo_171 : comprobar 4912740 383 1024 2187 820 215 = true := by
  decide +kernel

theorem nodo_172 : comprobar 4912740 895 1024 6561 5741 215 = true := by
  decide +kernel

theorem nodo_170 : comprobar 4912740 383 512 2187 1640 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_171 nodo_172

theorem nodo_166 : comprobar 4912740 127 256 2187 1093 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_167 nodo_170

theorem nodo_175 : comprobar 4912740 255 1024 6561 1640 215 = true := by
  decide +kernel

theorem nodo_176 : comprobar 4912740 767 1024 19683 14762 215 = true := by
  decide +kernel

theorem nodo_174 : comprobar 4912740 255 512 6561 3280 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_175 nodo_176

theorem nodo_178 : comprobar 4912740 511 1024 19683 9841 215 = true := by
  decide +kernel

theorem nodo_179 : comprobar 4912740 1023 1024 59049 59048 215 = true := by
  decide +kernel

#print axioms nodo_179

theorem nodo_177 : comprobar 4912740 511 512 19683 19682 216 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_178 nodo_179

theorem nodo_173 : comprobar 4912740 255 256 6561 6560 217 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_174 nodo_177

theorem nodo_165 : comprobar 4912740 127 128 2187 2186 218 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_166 nodo_173

theorem nodo_149 : comprobar 4912740 63 64 729 728 219 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_150 nodo_165

theorem nodo_123 : comprobar 4912740 31 32 243 242 220 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_124 nodo_149

theorem nodo_85 : comprobar 4912740 15 16 81 80 221 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_86 nodo_123

theorem nodo_45 : comprobar 4912740 7 8 27 26 222 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_46 nodo_85

theorem nodo_3 : comprobar 4912740 3 4 9 8 223 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_4 nodo_45

theorem nodo_180 : comprobar 4912740 5 4 3 4 223 = true := by
  decide +kernel

theorem nodo_2 : comprobar 4912740 3 2 3 5 224 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_3 nodo_180

theorem nodo_0 : comprobar 4912740 2 1 1 2 225 = true := by
  exact acepta_rama (by decide) (by decide) (by decide)
    nodo_1 nodo_2

theorem intervalo_comprobado : intervalo 4912740 225 = true := nodo_0

end OcelotasResiduosBloques

#print axioms OcelotasResiduosBloques.intervalo_comprobado
