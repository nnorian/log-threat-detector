import sys
import os
import argparse
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from application.use_cases import ThreatDetectionUseCase

from infrastructure.parsers.evtx_parser import EvtxParser
from infrastructure.loaders.yaml_rule_loader import YamlRuleLoader
from infrastructure.detectors.rule_based_detector import RuleBasedDetector
from infrastructure.reporters.markdown_reporter import MarkdownReporter

def main() -> int:
    parser = argparse.ArgumentParser(description="threat detection tool")
    parser.add_argument("-f", "--file", required=True, help="path to .evtx file")
    parser.add_argument("-o", "--output", default=None, help="output .md report path")
    parser.add_argument("--rules-dir", default="rules", help="rules directory")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"error: file not found")
        return 1

    ThreatDetectionUseCase(
        parser = EvtxParser(),
        loader = YamlRuleLoader(),
        detector = RuleBasedDetector(),
        reporter = MarkdownReporter(output_path=args.output),
    ).execute(args.file, args.rules_dir)

    return 0

if __name__ == "__main__":
    sys.exit(main())