package UCWorkflow {
  part def UseCaseComposition {
    doc /* Maintained analysis architecture normalized from the imported uc_v1 SSD. */

    part adaption : AdaptionUnit;
    part atmos : Atmos;
    part consumer : Consumer;
    part ecs_hw : ECS_HW;
    part ecs_sw : OpenSW_busInput;

    connect adaption.sWsignals to ecs_sw.Input;
    connect atmos.Pamb to consumer.Pamb;
    connect atmos.Pamb to ecs_hw.Pamb;
    connect atmos.Tamb to consumer.Tamb;
    connect atmos.Tamb to ecs_hw.Tamb;
    connect consumer.consumerRet to ecs_hw.consumerRet;
    connect ecs_hw.LHexTout to adaption.LHexTout;
    connect ecs_hw.consumerFeed to consumer.consumerFeed;
    connect ecs_sw.TCoolingPack to ecs_hw.reqCoolingTemperature;
  }
}
