from datetime import datetime
from turtle import pd
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):

    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        self.json_indent = 4

        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
        log_record["threadName"] = record.threadName
        log_record["processName"] = record.processName
        log_record["msecs"] = record.msecs
        log_record["process"] = record.process
        log_record["filename"] = record.filename
        log_record["funcName"] = record.funcName
        log_record["lineno"] = record.lineno
        log_record["name"] = record.name
