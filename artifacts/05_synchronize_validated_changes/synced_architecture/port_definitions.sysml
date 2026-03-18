package UCWorkflow {
  port def ControlSignals {
    attribute Aircraft_State : Integer;
    attribute TLiquid : Real;
  }

  port def FluidState {
    attribute X[1] : Real;
    attribute X[2] : Real;
    attribute X[3] : Real;
    attribute h : Real;
    attribute hn : Real;
    attribute m : Real;
    attribute p : Real;
  }

  port def ScalarSignal {
    attribute value : Real;
  }
}
