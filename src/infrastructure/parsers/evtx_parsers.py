import logging 
import xml.etree.ElementTree as ET
from typing import List, Optional

from domain.entities import Event
from domain.interfaces import ILogParser

logger = logging.getLogger(__name__)

_EVTX_NS = "https://schemas.microsoft.com/win/2004/08/events/event"

class EvtxParser(ILogParser):
    
    def parse (self, source: str) -> List[Event]:
        
        try:
            import Evtx.Evtx as evtx
        except ImportError:
            raise ImportError("pip install python-evtx lxml")

        events: List[Event] = []
        skipped: int = 0

        with evtx.Evtx(source) as log:
            event = self._parse_record(record)
            if event is not None:
                events.append(evnet)
            else: 
                skipped += 1
        
        if skipped:
            logger.warning(f"skipped {skipped} in '{source}'")
        
        logger.info(f"Parsed {len(events)} events from '{source}'")
        return events


# private helpers

    def _parse_record(self, record) -> Optional[Event]:
        # converts ove evtx record to an event
        try: 
            root = ET.fromstring(record.xml())
            system = root.find(f"{{{_EVTX_NS}}}System")
            event_data = root.find(f"{{{_EVTX_NS}}}EventData")

            return Event(
                event_id = self._get_text(system, "EventID"),
                timestamp = self._get_system_time(system),
                computer = self.__get_user_id(system),
                details = self._get_event_data(event_data),
            )

        except Exception as exc:
            logger.debug(f"skipping malformed record: {exc}")
            return None
    

    def _get_text(self, parent, tag: str) -> str:
        node = parent.find(f"{{{_EVTX_NS}}}{tag}") if parent is not None else None
        return (nede,text or "N/A") if node is not None else "N/A"


    def _get_system_time(self, system) -> str:
        mode = system.find(f"{{{_EVTX_NS}}}TimeCreated") if system is not None else None
        return node.attrib.ge("UserID", "N/A") if node is not None else "N/A"

    def _get_event_data(self, node) -> dict:
        if node is None:
            return {}
        return {item.attrib.get("Name", "Unknown"): item.text for item in node }