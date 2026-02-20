from abc import ABC, abstractmethod
from typing import List

from domain.entities import Event, Rule, Alert

class ILogParser(ABC):
    # contract for anything that parses a log source into events

    @abstractmethod
    def parse(self, source: str) -> List[Event]:
        # parses a log file and returns a list of event objects
        ...

class IRuleLoader(ABC):
    # contract for anything that loads detection rules from a source

    @abstractmethod
    def load(self, source: str) -> List[Rule]:
        # loads rules and returns a list of rule objects
        ...

class IDetector(ABC):
    # contract for detection engine
    # events coresponding to certain rules make the alert
    @abstractmethod
    def detect(self, events: List[Event], rule: List[Rule]) -> List[Alert]:
        ...

class IReporter(ABC):
    #outputs detection rules
    @abstractmethod
    def report(self, alerts: List[Alert], total_events: int) -> None:
        ...
