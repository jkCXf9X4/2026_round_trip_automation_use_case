package UCWorkflow {
  port def ScalarSignal {
    doc /* Shared scalar proxy port used for single-value SSP connectors. */
    attribute value : Real;
  }

  port def ControlSignals {
    doc /* Canonical ECS software input bundle normalized from external SSP naming. */
    attribute Aircraft_State : Integer;
    attribute TLiquid : Real;
  }

  port def FluidState {
    doc /* Shared thermal-fluid state passed between ECS, consumer, and fuel subsystems. */
    attribute X[1] : Real;
    attribute X[2] : Real;
    attribute X[3] : Real;
    attribute h : Real;
    attribute hn : Real;
    attribute m : Real;
    attribute p : Real;
  }
}
