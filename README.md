# Windows logs threat detection tool

A Python command-line tool that parses Windows Event Log files (`.evtx`), runs them against MITRE ATT&CK-mapped detection rules, and generates a Markdown report with prioritized alerts

Built as a portfolio project demonstrating clean architecture, SOLID principles, and practical blue team security engineering

---
## Demo

```
$ python src/presentation/cli.py -f samples/credential_access.evtx

Report saved -> reports/report_20240215_143022.md
```

![Demo screenshot](images/image.png)
---

1. Parses binary `.evtx` Windows Event Log files
2. Matches events against YAML-defined detection rules
3. Maps every alert to a MITRE ATT&CK technique
---

## Detection Rules

eight rules of the most encountered windows system attacks:

| Event ID | Rule                      | MITRE Technique | Severity |
| -------- | ------------------------- | --------------- | -------- |
| 4625     | brute force login attempt | T1110           | HIGH     |
| 4698     | scheduled task created    | T1053           | MEDIUM   |
| 7045     | new service installed     | T1543           | HIGH     |
| 4720     | new user account created  | T1136           | MEDIUM   |
| 4732     | user added to admin group | T1098           | HIGH     |
| 1102     | audit log cleared         | T1070           | CRITICAL |

to add a new rule for a new attack type or the update the old ones post `.yml` file in the `rules/` folder

---

## Architecture

built with Clean Architecture and SOLID principles for easy scaling

```
windows-threat-detector/
├── src/
│   ├── domain/
│   │   ├── entities.py
│   │   └── interfaces.py
│   ├── application/
│   │   └── use_cases.py
│   ├── infrastructure/
│   │   ├── parsers/evtx_parser.py
│   │   ├── loaders/yaml_rule_loader.py
│   │   ├── detectors/rule_based_detector.py
│   │   └── reporters/markdown_reporter.py
│   └── presentation/
│       └── cli.py
├── rules/
│   ├── brute_force.yml
│   ├── log_cleared.yml
│   └── ... (8 rules total)
├── tests/
│   ├── test_rule_based_detector.py
│   ├── test_yaml_rule_loader.py
│   └── test_use_case.py
├── samples/        # place .evtx files here (see above)
├── reports/        # generated reports saved here
└── requirements.txt
```


---

## Set up

**1. Clone and setup venv

```bash
git clone https://github.com/YOUR_USERNAME/windows-threat-detector.git
cd windows-threat-detector

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

**2. Add sample log files**
add you ovn .evtx 
or as i did

download `.evtx`  samples from [EVTX-ATTACK-SAMPLES](https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES) (GPL-3.0, sbousseaden) and place them in the `samples/` folder. 
I used: `Credential Access/`, `Defense Evasion/`, `Persistence/`, `Lateral Movement/`folders 

**3. Run**

```bash
python src/presentation/cli.py -f samples/example.evtx
```

Report is saved to `reports/report_TIMESTAMP.md`

**Optional — custom output path:**

```bash
python src/presentation/cli.py -f samples/example.evtx -o reports/my_report.md
```

**Optional — custom rules directory:**

```bash
python src/presentation/cli.py -f samples/example.evtx --rules-dir custom_rules/
```

---

## Adding a Custom Rule

Create a new `.yml` file in `rules/` following the structure:

```yaml
name: 
event_id: 
description: 
mitre_technique: 
mitre_name: 
severity: 
threshold:
```


Required fields: `name`, `event_id`, `description`, `mitre_technique`, `mitre_name`, `severity` 
Optional: `threshold` (default is 1)

## Used libraries 

|Library|Purpose|
|---|---|
|[python-evtx](https://github.com/williballenthin/python-evtx)|Parse `.evtx` binary files|
|[PyYAML](https://pyyaml.org/)|Load YAML detection rules|
|[lxml](https://lxml.de/)|XML parsing for event records