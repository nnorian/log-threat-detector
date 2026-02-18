@dataclass(frozen=True)
#detection rule loaded from yaml which wich tells what to look for
class Rule:
    name: str
    event_id: str
    description: str
    mitre_technique: str
    mitre_name: str
    severity: Severity
    # the number of times it should be met to trigger an allert
    threshold: int = 1

@dataclass
#the final output passed to reporters once the rule matches an event
class Alert:
    rule_name: str
    event_id: str
    severity: Severity
    mitre_name: str
    description: str
    occurence_count: int
    sample_timestamp: str
    sample_computer: str

