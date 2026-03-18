package UCWorkflow {
  part def AdaptionUnit {
    in port LHexTout : ScalarSignal;
    out port sWsignals : ControlSignals;
  }

  part def Atmos {
    attribute atmosphere_margin = 0.0;
    in port Alt : ScalarSignal;
    in port Ma : ScalarSignal;
    out port Pamb : ScalarSignal;
    out port Tamb : ScalarSignal;
  }

  part def Consumer {
    attribute heatLoadNominal_W = 2500.0;
    in port Alt : ScalarSignal;
    in port Mach : ScalarSignal;
    in port Pamb : ScalarSignal;
    in port Tamb : ScalarSignal;
    in port consumerFeed : FluidState;
    out port consumerRet : FluidState;
    in port heatLoad : ScalarSignal;
    out port inletTemp : ScalarSignal;
    out port outletTemp : ScalarSignal;
  }

  part def ECS_HW {
    attribute coolingTarget_K = 285.0;
    in port Alt : ScalarSignal;
    out port LHexTout : ScalarSignal;
    in port Mach : ScalarSignal;
    in port Pamb : ScalarSignal;
    in port Tamb : ScalarSignal;
    out port consumerFeed : FluidState;
    in port consumerRet : FluidState;
    in port reqCoolingTemperature : ScalarSignal;
  }

  part def OpenSW_busInput {
    in port Input : ControlSignals;
    out port TCoolingPack : ScalarSignal;
  }
}
