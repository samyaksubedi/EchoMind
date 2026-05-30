import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(service: str):  # service : api / worker
    # create logs/ folder if it doesn't exist
    # exist_ok=True → don't crash if folder already exists
    os.makedirs("logs", exist_ok=True)

    # Formatter — defines how each log line looks
    # %(asctime)s   → timestamp:  2026-05-28 15:52:05
    # %(levelname)s → level:      INFO / ERROR / WARNING
    # %(name)s      → logger name: app.services.media_service
    # %(message)s   → actual message: "PostgreSQL connected"
    # result → "2026-05-28 15:52:05 [INFO] app.main - EchoMind starting..."
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")

    # StreamHandler — prints logs to terminal (stdout)
    # no setLevel → accepts ALL levels (INFO, WARNING, ERROR, CRITICAL)
    # setFormatter → use our formatter for consistent log line format
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # RotatingFileHandler — saves logs to file
    # "logs/echomind.log"        → file path to write to
    # maxBytes=10 * 1024 * 1024  → rotate when file hits 10MB
    # backupCount=5              → keep last 5 rotated files then delete oldest
    # no setLevel                → accepts ALL levels (INFO, WARNING, ERROR, CRITICAL)
    # setFormatter               → use our formatter for consistent log line format
    # rotation example:
    #   echomind.log     → current file (active)
    #   echomind.log.1   → previous file
    #   echomind.log.2   → older file
    #   echomind.log.3   → even older
    #   echomind.log.4   → oldest kept
    #   echomind.log.5   → deleted when new rotation happens
    file_handler = RotatingFileHandler(
        f"logs/echomind_{service}.log", maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(formatter)

    # RotatingFileHandler — saves ONLY errors to separate file
    # same rotation config as file_handler
    # setLevel(ERROR) → filters out INFO and WARNING
    #                 → only saves ERROR and CRITICAL
    # useful for quickly checking what broke without noise
    error_handler = RotatingFileHandler(
        f"logs/echomind_{service}_error.log", maxBytes=10 * 1024 * 1024, backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # root_logger — the parent of ALL loggers in this process
    # logging.getLogger() with no name → returns the root logger
    # every logger created with logging.getLogger(__name__) is a child
    # children propagate logs UP to root automatically
    # so configuring root once = configures entire app
    root_logger = logging.getLogger()

    # setLevel(INFO) on root → root accepts INFO and above
    # filters out DEBUG logs (too noisy for production)
    # levels in order: DEBUG < INFO < WARNING < ERROR < CRITICAL
    root_logger.setLevel(logging.INFO)

    # attach all 3 handlers to root logger
    # root_logger
    #     │
    #     ├── has 3 handlers attached:
    #     │   ├── console_handler  → prints to terminal
    #     │   ├── file_handler     → saves to echomind.log
    #     │   └── error_handler    → saves to echomind_error.log
    #     │
    #     └── ALL child loggers inherit these handlers
    # now every log from every file in this process goes to:
    # console_handler → terminal
    # file_handler    → logs/echomind.log
    # error_handler   → logs/echomind_error.log (ERROR+ only)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
