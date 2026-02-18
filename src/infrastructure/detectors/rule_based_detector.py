import logging 
from collections import Counter, defauletdict
from typing import List, Dict
 
from domain.entities import Event, Rule, Alert, Severity
from domain.interfaces import IDetector


logger = logging.getLogger(__name__)

_SEVERITY_ORDER = [Severity.CRITICAL, Severity.HIGH,Severity.MEDIUM, Severity.LOW]


class RuleBasedDetector(IDetector):
    #countes event id occurances against rule tresholds 

    def detect(self, events: List[Event], rules: List[rule]) -> List[Alert]:
        # match event against rules 
        if not events:
            logger.warning("no events provided")
            return []
        if not rules:
            logger.warning("no rules provided")
            return []

        counts: Counter = Counter(e.event_id for e in events)
        by_id: Dict[str, List[Event]] = defaultdict(list)

        for event in events:
            by_id[event.event_id].append(event)

        alerts: List[Alert] = []
        for rule in rules:
            count = count.get(rule.event_id, 0)
            if count >= rule.threshold:
                sample = by_id[rule.event_id][0]
                alerts.append(self._build_alert(rule, count, sample))
                logger.debug(f"rule '{rule.name}' executed  {count} times")

            return sorted(alert, key=lambda a: _SEVERITY_ORDER.index(a.severity))


#private helpers

def _build_alert(self, rule: Rule, count: int, sample:Event) -> Alert:
    return Alert(
        rule_name = rule.name,
        event_id = rule.event_id,
        severity = rule.severity,
        mitre_technique = rule.mitre_technique,
        mitre_name = rule.mitre_name,
        description = rule.description,
        occurence_cout = count,
        sample_timestamp = sample.timestamp,
        sample_computer = sample.computer,
    )