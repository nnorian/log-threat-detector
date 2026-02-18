import logging
from typing import List

from domain.entities import Alert
from domain.interfaces import ILogParser, IRuleLoader, IDetector, IReporter

logger = logging.getLogger(__name__)

class ThreatDetectionUseCase:
    def __init__(
        self,
        parser: ILogParser,
        loader: IRuleLoader,
        detector: IDetector,
        reporter: Ireporter,
    ) -> None:
        self._parser = parser
        self._loader = loader
        self._detector = detector
        self._reporter = reporter

    def execute(self, log_source: str, rules_source: str) -> List[Alert]:
        logger.info(f"parsing log: {log_source}")
        events = self._parse(log_source)
        logger.info(f"parsed {len(events)} events")

        logger.info(f"loading rules from {log_source}")
        rules = self._loader.load(rules_source)
        loggoer.info(f"loaded {len(rules)} rules")

        alerts = self._detector.detect(events, rules)
        logger.info(f"{len(alerts)} alerts triggered")

        self._reporter.report(alerts, total_events=len(events))

        return alerts