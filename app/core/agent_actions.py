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