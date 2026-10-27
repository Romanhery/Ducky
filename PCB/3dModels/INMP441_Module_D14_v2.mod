PCBNEW-LibModule-V1  2026-10-22 00:00:00
# encoding utf-8
Units mm
$INDEX
INMP441_Module_D14_v2
$EndINDEX
$MODULE INMP441_Module_D14_v2
Po 0 0 0 15 00000000 00000000 ~~
Li INMP441_Module_D14_v2
Cd INMP441 I2S MEMS microphone breakout, round 14 mm board, 2x3 THT, 7.62 mm row spacing
Kw INMP441 I2S microphone module
Sc 0
At STD
AR
Op 0 0 0
T0 0 -9 1 1 0 0.15 N V 21 N "REF**"
T1 0 9 1 1 0 0.15 N V 33 N "INMP441"
DC 0 0 7.1 0 0.12 21
DC 0 0 6.9 0 0.1 33
DC 0 0 7.4 0 0.05 31
$PAD
Sh "VDD" R 1.7 1.7 0 0 0
Dr 1 0 0
At STD N 00E0FFFF
Ne 0 ""
Po -3.81 -2.54
$EndPAD
$PAD
Sh "GND" C 1.7 1.7 0 0 0
Dr 1 0 0
At STD N 00E0FFFF
Ne 0 ""
Po -3.81 0
$EndPAD
$PAD
Sh "SD" C 1.7 1.7 0 0 0
Dr 1 0 0
At STD N 00E0FFFF
Ne 0 ""
Po -3.81 2.54
$EndPAD
$PAD
Sh "SCK" C 1.7 1.7 0 0 0
Dr 1 0 0
At STD N 00E0FFFF
Ne 0 ""
Po 3.81 -2.54
$EndPAD
$PAD
Sh "WS" C 1.7 1.7 0 0 0
Dr 1 0 0
At STD N 00E0FFFF
Ne 0 ""
Po 3.81 0
$EndPAD
$PAD
Sh "L/R" C 1.7 1.7 0 0 0
Dr 1 0 0
At STD N 00E0FFFF
Ne 0 ""
Po 3.81 2.54
$EndPAD
$SHAPE3D
Na "${KIPRJMOD}/INMP441_I2S_Microphone_Module_v15.step"
Sc 1 1 1
Of 0 0 0.0988
Ro -90 0 0
$EndSHAPE3D
$EndMODULE INMP441_Module_D14_v2
$EndLIBRARY
