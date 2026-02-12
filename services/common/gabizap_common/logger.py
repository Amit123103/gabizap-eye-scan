from loguru import logger
import sys
import json

def serialize(record):
    subset = {
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "service": record["extra"].get("service", "unknown"),
        "trace_id": record["extra"].get("trace_id", ""),
        "file": record["file"].name,
        "line": record["line"],
    }
    return json.dumps(subset)

def setup_logger(service_name: str):
    logger.remove()
    logger.add(sys.stdout, format="{message}", serialize=True, level="INFO")
    logger.configure(extra={"service": service_name})
    return logger

# Example usage:
# log = setup_logger("auth-service")
# log.info("Service started")
