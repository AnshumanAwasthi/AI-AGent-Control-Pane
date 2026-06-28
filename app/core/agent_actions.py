from enum import Enum


class AgentActionType(str, Enum):
    START = "start"
    STOP = "stop"
    PAUSE = "pause"
    RESUME = "resume"


ACTION_STATUS_MAP: dict[AgentActionType, str] = {
    AgentActionType.START: "running",
    AgentActionType.STOP: "stopped",
    AgentActionType.PAUSE: "paused",
    AgentActionType.RESUME: "running",
}


VALID_STATUS_TRANSITIONS: dict[str, set[str]] = {
    "created": {ACTION_STATUS_MAP[AgentActionType.START]},
    "running": {ACTION_STATUS_MAP[AgentActionType.PAUSE], ACTION_STATUS_MAP[AgentActionType.STOP]},
    "paused": {ACTION_STATUS_MAP[AgentActionType.RESUME], ACTION_STATUS_MAP[AgentActionType.STOP]},
    "stopped": {ACTION_STATUS_MAP[AgentActionType.START]},
}