import json
from datetime import datetime

class LogRecord:
    def __init__(self, level, time, message):
        self.level = level
        self.time = time
        self.message = message

    def __str__(self):
        return f"[{self.time}] {self.level} {self.message}"

class LogParser:
    @staticmethod
    def parse(line):
        try:
            if line.startswith("fmt1"):
                content = line[5:]
                time_str = content[1:20]
                rest = content[22:]
                level, msg = rest.split(": ", 1)
                dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                return LogRecord(level, dt, msg.strip())
            
            elif line.startswith("fmt2"):
                content = line[5:]
                parts = content.split(";")
                level = parts[0]
                time_str = parts[1]
                msg = parts[2]
                dt = datetime.strptime(time_str, "%Y/%m/%d-%H:%M")
                return LogRecord(level, dt, msg.strip())
            
            elif line.startswith("json"):
                content = line[5:]
                data = json.loads(content)
                dt = datetime.strptime(data["time"], "%Y-%m-%dT%H:%M:%S")
                return LogRecord(data["level"], dt, data["msg"])
            
            else:
                return None
        except Exception:
            return None

class LogSystem:
    def __init__(self):
        self.records = []
        self.errors = []

    def add_line(self, line):
        record = LogParser.parse(line)
        if record:
            self.records.append(record)
        else:
            self.errors.append(line)

    def execute_command(self, command_line):
        parts = command_line.split()
        cmd = parts[0]

        if cmd == "count":
            key, value = parts[1].split("=")
            if key == "level":
                count = sum(1 for r in self.records if r.level == value)
                print(f"Count of {value}: {count}")

        elif cmd == "list":
            key, value = parts[1].split("=")
            if key == "level":
                print(f"List of {value}:")
                for r in self.records:
                    if r.level == value:
                        print(r)

        elif cmd == "range":
            start_str = f"{parts[1]} {parts[2]}"
            end_str = f"{parts[3]} {parts[4]}"
            start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
            
            print(f"Logs from {start_dt} to {end_dt}:")
            for r in self.records:
                if start_dt <= r.time <= end_dt:
                    print(r)
        
        elif cmd == "errors":
            print("Parsing errors:")
            for err in self.errors:
                print(err)

raw_logs = [
    "fmt1 [2025-10-01 12:34:56] INFO: System started",
    "fmt2 ERROR;2025/10/01-12:35;Disk full",
    "json {\"level\": \"WARNING\", \"time\": \"2025-10-01T12:36:00\", \"msg\": \"High load\"}",
    "fmt1 [2025-10-01 12:40:00] ERROR: Connection lost",
    "broken_log_format example"
]
user_commands = [
    "count level=ERROR",
    "list level=WARNING",
    "range 2025-10-01 12:30 2025-10-01 13:00",
    "errors"
]

system = LogSystem()

for line in raw_logs:
    system.add_line(line)

print("--- Execution Results ---")
for cmd in user_commands:
    print(f"> {cmd}")
    system.execute_command(cmd)
    print("-" * 20)
