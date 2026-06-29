from enum import Enum

from app.core.agent_status import AgentStatusType


class AgentActionType(str, Enum):
    START = "start"
    STOP = "stop"
    PAUSE = "pause"
    RESUME = "resume"


ACTION_STATUS_MAP: dict[AgentActionType, str] = {
    AgentActionType.START: AgentStatusType.RUNNING.value,
    AgentActionType.STOP: AgentStatusType.STOPPED.value,
    AgentActionType.PAUSE: AgentStatusType.PAUSED.value,
    AgentActionType.RESUME: AgentStatusType.RUNNING.value,
}


VALID_STATUS_TRANSITIONS: dict[str, set[str]] = {
    AgentStatusType.CREATED.value: {ACTION_STATUS_MAP[AgentActionType.START]},
    AgentStatusType.RUNNING.value: {ACTION_STATUS_MAP[AgentActionType.PAUSE], ACTION_STATUS_MAP[AgentActionType.STOP]},
    AgentStatusType.PAUSED.value: {ACTION_STATUS_MAP[AgentActionType.RESUME], ACTION_STATUS_MAP[AgentActionType.STOP]},
    AgentStatusType.STOPPED.value: {ACTION_STATUS_MAP[AgentActionType.START]},
}