package RecoveredFromSSD {
  port def Port_1 {
    attribute value : Real;
  }

  port def Port_10 {
    attribute Vacc : Real;
    attribute Vacc0 : Real;
    attribute X[1] : Real;
    attribute X[2] : Real;
    attribute X[3] : Real;
    attribute looptype : Integer;
    attribute pempty : Real;
    attribute pfull : Real;
  }

  port def Port_11 {
    attribute currentMinCoolingTemp.k1 : Real;
    attribute currentMinCoolingTemp.k2 : Real;
  }

  port def Port_12 {
    attribute CP_Air.k : Real;
    attribute MaxCoolPower.k : Real;
    attribute MaxMassFlow.verboseRead : Boolean;
    attribute MinFlow.k : Real;
    attribute RelCool.verboseRead : Boolean;
    attribute firstOrder.T : Real;
    attribute firstOrder.k : Real;
    attribute firstOrder.y_start : Real;
    attribute firstOrder1.T : Real;
    attribute firstOrder1.k : Real;
    attribute firstOrder1.y_start : Real;
    attribute gain.k : Real;
    attribute m2km.k : Real;
  }

  port def Port_13 {
    attribute Pin : Real;
    attribute Tin : Real;
    attribute X[1] : Real;
    attribute X[2] : Real;
    attribute X[3] : Real;
    attribute looptype : Integer;
  }

  port def Port_14 {
    attribute Dh : Real;
    attribute L : Real;
    attribute MCp : Real;
    attribute Text_at_Tfric_0 : Real;
    attribute Text_at_Tfric_100 : Real;
    attribute Text_local : Real;
    attribute delayMax : Real;
    attribute hext : Real;
    attribute looptype : Integer;
    attribute rgh : Real;
    attribute tao_Tfrict : Real;
    attribute z : Real;
  }

  port def Port_15 {
    attribute M : Real;
    attribute MF : Real;
    attribute hA : Real;
    attribute looptype : Integer;
    attribute qpump : Real;
  }

  port def Port_16 {
    attribute Aircraft_State : Unknown;
    attribute TLiquid : Real;
  }

  port def Port_2 {
    attribute Aircraft_State : Integer;
    attribute TLiquid : Real;
  }

  port def Port_3 {
    attribute Afact : Real;
    attribute Dh : Real;
    attribute L : Real;
    attribute MCp : Real;
    attribute Text_at_Tfric_0 : Real;
    attribute Text_at_Tfric_100 : Real;
    attribute Text_local : Real;
    attribute Vin : Real;
    attribute hext : Real;
    attribute looptype : Integer;
    attribute rgh : Real;
    attribute tao_Tfrict : Real;
    attribute z : Real;
  }

  port def Port_4 {
    attribute DPlin : Real;
    attribute P0 : Real;
    attribute Tbnd : Real;
    attribute Tfill : Real;
    attribute Timp : Real;
    attribute damp : Real;
    attribute gin[1] : Real;
    attribute gin[2] : Real;
    attribute gin[3] : Real;
    attribute medcold : Integer;
    attribute medhot : Integer;
    attribute medintrm1 : Integer;
    attribute medintrm2 : Integer;
    attribute mmin : Real;
    attribute mnode : Real;
  }

  port def Port_5 {
    attribute k : Real;
  }

  port def Port_6 {
    attribute X[1] : Real;
    attribute X[2] : Real;
    attribute X[3] : Real;
    attribute h : Real;
    attribute hn : Real;
    attribute m : Real;
    attribute p : Real;
  }

  port def Port_7 {
    attribute Alt_filt.k : Real;
    attribute Alt_start : Real;
    attribute Ma_filt.k : Real;
    attribute Ma_start : Real;
    attribute Nx_filt.k : Real;
    attribute Nx_start : Real;
    attribute Ny_filt.k : Real;
    attribute Ny_start : Real;
    attribute Nz_filt.k : Real;
    attribute Nz_start : Real;
    attribute Pamb_filt.k : Real;
    attribute Pamb_start : Real;
    attribute Tamb_filt.k : Real;
    attribute Tamb_start : Real;
    attribute Tbay : Real;
    attribute gain.k : Real;
  }

  port def Port_8 {
    attribute X[1] : Real;
    attribute X[2] : Real;
    attribute X[3] : Real;
    attribute looptype : Integer;
  }

  port def Port_9 {
    attribute Dhc : Real;
    attribute Dhh : Real;
    attribute Kexp : Real;
    attribute Kst : Real;
    attribute M : Real;
    attribute V : Real;
    attribute b : Real;
    attribute fgst : Real;
    attribute h : Real;
    attribute hotrat : Real;
    attribute l : Real;
    attribute looptypBlue : Integer;
    attribute looptypRed : Integer;
    attribute typ : Integer;
  }

  part def 0001_ECS_HW {
    in port AirToL_HEX : Port_9;
    in port Alt : Port_1;
    out port LHexTout : Port_1;
    in port Mach : Port_1;
    in port Pamb : Port_1;
    in port Tamb : Port_1;
    in port acc2_1 : Port_10;
    in port cd : Port_4;
    in port const1 : Port_5;
    in port const3 : Port_5;
    in port const4 : Port_5;
    in port consumerFeed : Port_6;
    in port consumerRet : Port_6;
    in port coolinPackAir : Port_8;
    in port coolingTemp : Port_11;
    in port eCS : Port_12;
    in port fd : Port_7;
    in port nodeAirOutlet : Port_8;
    in port nodeHEXToPipeA : Port_8;
    in port nodePumpToHEX : Port_8;
    in port phSrc : Port_13;
    in port pipeA : Port_14;
    in port pipeB : Port_14;
    in port pipeC : Port_14;
    in port pumpSK01955_1 : Port_15;
    in port reqCoolingTemperature : Port_1;
  }

  part def 0002_ECS_SW {
    in port Input : Port_16;
    out port TCoolingPack : Port_1;
  }

  part def 0003_Consumer {
    in port Alt : Port_1;
    in port ConsumerA : Port_3;
    in port Mach : Port_1;
    in port Pamb : Port_1;
    in port Tamb : Port_1;
    in port cd : Port_4;
    in port const1 : Port_5;
    in port const3 : Port_5;
    in port const4 : Port_5;
    in port consumerFeed : Port_6;
    in port consumerRet : Port_6;
    in port fd : Port_7;
    in port heatLoad : Port_1;
    out port inletTemp : Port_1;
    in port nodeConsumerToPipeB : Port_8;
    in port nodePipeAToConsumer : Port_8;
    out port outletTemp : Port_1;
  }

  part def 0004_Atmos {
    in port Alt : Port_1;
    in port DTisa : Port_1;
    in port Ma : Port_1;
    out port Pamb : Port_1;
    out port Tamb : Port_1;
  }

  part def 0005_AdaptionUnit {
    in port Aircraft_State : Port_1;
    in port LHexTout : Port_1;
    out port sWsignals : Port_2;
  }

  part def UseCaseComposition {
    part AdaptionUnit : 0005_AdaptionUnit;
    part Atmos : 0004_Atmos;
    part Consumer : 0003_Consumer;
    part ECS_HW : 0001_ECS_HW;
    part ECS_SW : 0002_ECS_SW;
    connect AdaptionUnit.sWsignals to ECS_SW.Input;
    connect Atmos.Pamb to Consumer.Pamb;
    connect Atmos.Pamb to ECS_HW.Pamb;
    connect Atmos.Tamb to Consumer.Tamb;
    connect Atmos.Tamb to ECS_HW.Tamb;
    connect Consumer.consumerFeed to ECS_HW.consumerFeed;
    connect Consumer.consumerRet to ECS_HW.consumerRet;
    connect ECS_HW.LHexTout to AdaptionUnit.LHexTout;
    connect ECS_HW.consumerFeed to Consumer.consumerFeed;
    connect ECS_HW.consumerRet to Consumer.consumerRet;
    connect ECS_SW.TCoolingPack to ECS_HW.reqCoolingTemperature;
  }
}
