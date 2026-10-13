
from enum import Enum
from time import time


class QoSPolicy(Enum):
    NORMAL = "QOS-NORMAL"
    PEAK = "QOS-PEAK"
    BURST = "QOS-BURST"
    PEAK_BURST = "QOS-PEAKBURST"


class QoSController:
    def __init__(self, cooldown_seconds=30):
        self.current_policy = QoSPolicy.NORMAL
        self.last_change_time = 0
        self.cooldown_seconds = cooldown_seconds

    def select_policy(
        self,
        scheduled_peak,
        utilization_percent,
        burst_detected,
        now=None
    ):
        if now is None:
            now = time()

        congested = utilization_percent >= 75

        if scheduled_peak and (congested or burst_detected):
            desired = QoSPolicy.PEAK_BURST
        elif scheduled_peak or congested:
            desired = QoSPolicy.PEAK
        elif burst_detected:
            desired = QoSPolicy.BURST
        else:
            desired = QoSPolicy.NORMAL

        if desired == self.current_policy:
            return self.current_policy, "No change needed"

        elapsed = now - self.last_change_time

        if self.last_change_time != 0 and elapsed < self.cooldown_seconds:
            return self.current_policy, "Cooldown active"

        previous = self.current_policy
        self.current_policy = desired
        self.last_change_time = now

        reason = (
            f"Policy changed from {previous.value} "
            f"to {desired.value}"
        )

        return self.current_policy, reason


controller = QoSController(cooldown_seconds=30)

scenarios = [
    (False, 30, False),
    (True, 82, False),
    (False, 45, True),
    (True, 90, True),
]

for i, scenario in enumerate(scenarios):
    policy, reason = controller.select_policy(
        *scenario,
        now=100 + i * 10
    )

    print(f"Scenario {i + 1}: {policy.value}")
    print(f"Reason: {reason}")
    print()
