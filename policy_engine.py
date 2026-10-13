
from enum import Enum


class QoSPolicy(Enum):
    NORMAL = "QOS-NORMAL"
    PEAK = "QOS-PEAK"
    BURST = "QOS-BURST"
    PEAK_BURST = "QOS-PEAKBURST"


def select_policy(
    scheduled_peak: bool,
    utilization_percent: float,
    burst_detected: bool
) -> QoSPolicy:

    congested = utilization_percent >= 75

    if scheduled_peak and (congested or burst_detected):
        return QoSPolicy.PEAK_BURST

    if scheduled_peak or congested:
        return QoSPolicy.PEAK

    if burst_detected:
        return QoSPolicy.BURST

    return QoSPolicy.NORMAL


print("Scenario 1:",
      select_policy(False, 30, False).value)

print("Scenario 2:",
      select_policy(True, 82, False).value)

print("Scenario 3:",
      select_policy(False, 45, True).value)

print("Scenario 4:",
      select_policy(True, 90, True).value)
