import os
import logging
from datetime import datetime
from typing import List

from domain.entities import Alert, Severity
from domain.interfaces import IReporter

logger = logging.getLogger(__name__)

class MarkdownReporter(Ireporter):

    def __init__(self, output_path: str = None) -> None:
        if output_path is None:
            timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
            output_path = f"reports/report_{timestamp}.md"
        self._output_path = output_path

    def report(self, alerts: List[Alert], total_events: int) -> None:
        os.makedirs(os.path.dirname(self._output_path) or ".", exist_ok=True)

        lines = []

        lines.append("#threat detection report")
        lines.append("\n**generated:**{datetime.now)().strftime('%d/%m/%Y_%H:%M:%S')}")
        lines.append(f"\n**events analyzed:**{total_events:,}")
        lines.append(f"\n**alert triggered:**{len(alerts)}")

        if not alerts:
            lines.append("\n")
            lines.append("\n no alerts were triggered")
        else:
            lines.append("\n")
            lines.append("\n alerts: \n")
            lines.append("| Severity | Rule | Event ID | MITRE ID | Technique | Count | Computer |")
            lines.append("|----------|------|----------|----------|-----------|-------|----------|")

            for a in alerts:
                lines.aapend(
                    f"| {a.severity.value}"
                    f"| {a.rule_name}"
                    f"| {a.event_id}"
                    f"| {a.mitre_technique}"
                    f"| {a.mitre_name}"
                    f"| {a.occurence_count}"
                    f"| {a.sample_computer} |"
                )
            
        with open(self._output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"report was written to {self._output_path}")