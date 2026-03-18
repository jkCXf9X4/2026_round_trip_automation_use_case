package UCWorkflow {
  part def FMU_16_aero_interface {
    out port debug : ScalarSignal;
    out port mflowA : ScalarSignal;
    out port mflowB : ScalarSignal;
    out port pLin : ScalarSignal;
    out port pLmax : ScalarSignal;
    out port p_P : ScalarSignal;
    out port p_PS : ScalarSignal;
    out port p_TP : ScalarSignal;
    in port qTA : ScalarSignal;
    in port qTB : ScalarSignal;
    in port u : ScalarSignal;
    out port uA : ScalarSignal;
    out port uB : ScalarSignal;
  }

  part def FS_OPSC {
    attribute valveBias = 0.0;
    in port Mach : ScalarSignal;
    in port P_AMB : ScalarSignal;
    in port T_AMB : ScalarSignal;
    in port eng_mflow : ScalarSignal;
    out port pmh : FluidState;
    in port pmhn : FluidState;
    in port valve_mflowA : ScalarSignal;
    in port valve_mflowB : ScalarSignal;
    out port valve_p1 : ScalarSignal;
    out port valve_p2 : ScalarSignal;
    out port valve_p3 : ScalarSignal;
    out port valve_u : ScalarSignal;
  }

  part def L90LS_UD_OS_OS {
    out port Debug : ScalarSignal;
    in port pA : ScalarSignal;
    in port pB : ScalarSignal;
    out port pL : ScalarSignal;
    in port pLin : ScalarSignal;
    in port pLmax : ScalarSignal;
    in port pP : ScalarSignal;
    in port pTA : ScalarSignal;
    in port pTB : ScalarSignal;
    in port p_PS : ScalarSignal;
    in port p_TP : ScalarSignal;
    out port qA : ScalarSignal;
    out port qB : ScalarSignal;
    out port qP : ScalarSignal;
    out port qTA : ScalarSignal;
    out port qTB : ScalarSignal;
    in port uA : ScalarSignal;
    in port uB : ScalarSignal;
  }
}
