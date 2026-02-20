# reads .yaml and return Rule objects
# potentialy we could introduce json readers 

import os 
import logging 
from typing import List, Optional

import yaml

from domain.entities import Rule, Severity
from domain.interfaces import IRuleLoader

logger = logging.getLogger(__name__)

_SEVERITY_MAP = {
    "LOW": Severity.LOW,
    "MEDIUM": Severity.MEDIUM,
    "HIGH": Severity.HIGH,
    "CRITICAL": Severity.CRITICAL,
}

_REQUIRED_FIELDS = {
    "name", "event_id", "description", "mitre_technique", "mitre_name", "severity",
}

class YamlRuleLoader(IRuleLoader):
    
    def load(self, source: str) -> List[Rule]:
        if not os.path.isdir(source):
            raise NotADirectoryError(F"rules directory not found")

        rules: List[Rule] = []

        for filename in sorted(os.listdir(source)):
            if not filename.endswith(".yml"):
                continue

            rule = self._load_file(os.path.join(source, filename))
            if rule is not None:
                rules.append(rule)

        logger.info(f"loaded {len(rules)} rules from '{source}'")
        return rules


#private helpers

    def _load_file(self, filepath: str) -> Optional[Rule]:
        #parse one yaml file into a rule class
        try:
            with open(filepath) as f:
                data = yaml.safe_load(f)

            missing = _REQUIRED_FIELDS - set (data.keys())
            if missing:
                logger.warning(f"skipping '{filepath}': missing fileds {missing}")
                return None
            
            severity_str = str(data["severity"]).upper()
            if severity_str not in _SEVERITY_MAP:
                logger.warning(
                    f"skipping path '{filepath}': invalid severity '{severity_str}'"
                )
                return None
            

            return Rule(
                name = str(data["name"]),
                event_id = str(data["event_id"]),
                description = str(data["description"]),
                mitre_technique = str(data["mitre_technique"]),
                mitre_name = str(data["mitre_name"]),
                severity = _SEVERITY_MAP[severity_str],
                threshold = int(data.get("threshold", 1)),

            )

        except yaml.YAMLError as exc:
            logger.warning(f" skipping '{filepath}' because of a yaml error {exc}")
            return None

        except Exception as exc:
            logger.warning(f"skipping '{filepath}' because of an unxpected error {exc}")
            return None