import OcelotasRoosendaal

/-! Solo la trayectoria de la semilla record, no el censo hasta ella. -/
namespace OcelotasRecordRoosendaal

open OcelotasRoosendaal

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem llega_en_2480 : Col^[2480] 46645791847966786687 = 1 := by
  decide +kernel

end OcelotasRecordRoosendaal

#print axioms OcelotasRecordRoosendaal.llega_en_2480
