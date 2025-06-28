class Error(Exception):
    """Base class for other exceptions"""
    pass

class FrameError(Error):
    pass

class AgentCompareError(Error):
    """Raised when the input value is too small"""
    pass


class ScenarioTraceMatchError(Error):
    """Raised when the input value is too large"""
    pass

class TrafficReferenceTraceError(Error):
    pass

class SafetyAssertionError(Error):
    pass

class SpecAgentError(Error):
    pass

class LaneError(Error):
    pass

class AssertionTypeError(Error):
    pass

class StatementTypeError(Error):
    pass

class DistanceTypeError(Error):
    pass

class PerceptionDiffError(Error):
    pass

class AssertionPositionError(Error):
    pass

