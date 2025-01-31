from typing import Any, Coroutine, NewType

THandlerUploadOrderNumber = NewType("THandlerUploadOrderNumber", int)


TModuleAbsPath = NewType("TModuleAbsPath", str)
TPathToDir = NewType("TPathToDir", str)

TReplyToUserMessage = NewType("TReplyToUserMessage", str)

TEnvName = NewType("TEnvName", str)

# TFMSData - это пара fms_state__какие_то_данные.
# какие_то_данные это id сущности, к примеру User, над которым мы и работаем
TFMSData = NewType("TFMSData", str)
TFMSName = NewType("TFMSName", str)

TReplyToUserText = NewType("TReplyToUserText", str)

TTelegramUserId = NewType("TTelegramUserId", int)

TMethodName = NewType("TMethodName", str)

HandlerFuncReturnType = Coroutine[Any, Any, None]  # функция либо асинхронная, либо синхронная. Возможны оба варианта
