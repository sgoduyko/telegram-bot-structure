import logging
from typing import Dict, Optional, Type

from bot.const.const import REGISTRATION_FMS_NAME
from bot.const.types import TFMSName
from bot.modules.fms_data_pipeline.base import BaseFMSDataPipeline
from bot.modules.fms_data_pipeline.registration import SighInFMSDataPipeline


class FMSDataPipelinePool:
    def __init__(self) -> None:
        self.fms_pipeline_pool: Dict[str, Type[BaseFMSDataPipeline]] = {}
        for fms_name, fms_pipeline in ((REGISTRATION_FMS_NAME, SighInFMSDataPipeline),):
            self.fms_pipeline_pool[fms_name] = fms_pipeline

    def get_pipeline(self, fms_name: Optional[TFMSName]) -> Type[BaseFMSDataPipeline]:
        if not fms_name:
            logging.warning(f"FMS name not provided. fms_name={fms_name}")

        pipeline = self.fms_pipeline_pool.get(str(fms_name))
        if pipeline is None:
            logging.error("FMS data pipeline didn't find")
            raise Exception("FMS data pipeline didn't find")
        return pipeline
