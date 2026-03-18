package UCWorkflow {
  part def AdaptionUnit {
    doc /* Adapts plant outputs into the software control-signal bundle. */
    in port LHexTout : ScalarSignal;
    out port sWsignals : ControlSignals;
  }

  part def Atmos {
    doc /* Provides ambient conditions to the thermal subsystem chain. */
    attribute atmosphere_margin = 0.0;

    in port Alt : ScalarSignal;
    in port Ma : ScalarSignal;
    out port Pamb : ScalarSignal;
    out port Tamb : ScalarSignal;
  }

  part def Consumer {
    doc /* Representative heat consumer connected to the ECS and later fuel loop. */
    attribute heatLoadNominal_W = 2500.0;

    in port Alt : ScalarSignal;
    in port Mach : ScalarSignal;
    in port Pamb : ScalarSignal;
    in port Tamb : ScalarSignal;
    in port heatLoad : ScalarSignal;
    in port consumerFeed : FluidState;
    out port consumerRet : FluidState;
    out port inletTemp : ScalarSignal;
    out port outletTemp : ScalarSignal;
  }

  part def ECS_HW {
    doc /* ECS plant model exposing fluid and scalar interfaces for analysis export. */
    attribute coolingTarget_K = 285.0;

    in port Alt : ScalarSignal;
    in port Mach : ScalarSignal;
    in port Pamb : ScalarSignal;
    in port Tamb : ScalarSignal;
    in port reqCoolingTemperature : ScalarSignal;
    in port consumerRet : FluidState;
    out port LHexTout : ScalarSignal;
    out port consumerFeed : FluidState;
  }

  part def OpenSW_busInput {
    doc /* Software controller receiving normalized adaptation signals. */
    in port Input : ControlSignals;
    out port TCoolingPack : ScalarSignal;
  }
}
