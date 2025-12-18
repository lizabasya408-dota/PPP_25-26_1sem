import json
from datetime import datetime

class LogEntry:
    def __init__(self, level, time, message):
        self.level = level
        self.time = time
        self.message = message

    @classmethod
    def from_string(cls, line):
        raise NotImplementedError

    def get_level(self):
        return self.level

    def get_time(self):
        return self.time

    def get_message(self):
        return self.message

    def to_string(self):
        raise NotImplementedError

class Format1Log(LogEntry):
    @classmethod
    def from_string(cls, line):
        try:
            prefix, msg = line.split('] ', 1)
            timestamp_str = prefix.strip('[')
            level_str, message = msg.split(': ', 1)
            time_obj = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            return cls(level=level_str, time=time_obj, message=message)
        except Exception:
            return None

    def to_string(self):
        return f"[{self.time.strftime('%Y-%m-%d %H:%M:%S')}] {self.level}: {self.message}"

class Format2Log(LogEntry):
    @classmethod
    def from_string(cls, line):
        try:
            level, time_str, message = line.split(';', 2)
            time_obj = datetime.strptime(time_str, "%Y/%m/%d-%H:%M")
            return cls(level=level, time=time_obj, message=message)
        except Exception:
            return None

    def to_string(self):
        return f"{self.level};{self.time.strftime('%Y/%m/%d-%H:%M')};{self.message}"

class JSONLog(LogEntry):
    @classmethod
    def from_string(cls, line):
        try:
            data = json.loads(line)
            time_obj = datetime.fromisoformat(data['time'])
            return cls(level=data['level'], time=time_obj, message=data['msg'])
        except Exception:
            return None

    def to_string(self):
        return json.dumps({
            'level': self.level,
            'time': self.time.isoformat(),
            'msg': self.message
        })

class LogProcessor:
    def __init__(self):
        self.entries = []

    def add_line(self, line):
        for cls in [Format1Log, Format2Log, JSONLog]:
            entry = cls.from_string(line)
            if entry:
                self.entries.append(entry)
                return True
        print(f"Некорректная строка: {line}")
        return False

    def filter_by_level(self, level):
        return [e for e in self.entries if e.get_level() == level]

    def filter_by_time_range(self, start, end):
        return [e for e in self.entries if start <= e.get_time() <= end]

    def count_by_level(self, level):
        return len(self.filter_by_level(level))

    def list_logs(self, level=None):
        if level:
            return self.filter_by_level(level)
        return self.entries

    def get_stats(self):
        stats = {}
        for e in self.entries:
            lvl = e.get_level()
            stats[lvl] = stats.get(lvl, 0) + 1
        return stats

def parse_time_range(start_str, end_str):
    try:
        start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
        return start_dt, end_dt
    except:
        try:
            start_dt = datetime.fromisoformat(start_str)
            end_dt = datetime.fromisoformat(end_str)
            return start_dt, end_dt
        except:
            return None, None
if __name__ == "__main__":
       main()
