from enum import Enum


class AgentStatusType(str, Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
    CREATED = "created"
