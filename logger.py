from __future__ import annotations

import contextvars
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

_session_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("genui_session_id", default="-")


def set_log_session_id(session_id: str) -> contextvars.Token[str]:
    return _session_id_var.set(session_id)


def reset_log_session_id(token: contextvars.Token[str]) -> None:
    _session_id_var.reset(token)


class SessionContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "session_id"):
            record.session_id = _session_id_var.get("-")
        return True


class SessionFileRouterHandler(logging.Handler):
    def __init__(self, sessions_dir: Path, level: int = logging.INFO) -> None:
        super().__init__(level=level)
        self.sessions_dir = sessions_dir
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self._handlers: dict[str, TimedRotatingFileHandler] = {}

    def emit(self, record: logging.LogRecord) -> None:
        session_id = getattr(record, "session_id", "-")
        if not isinstance(session_id, str) or not session_id or session_id == "-":
            return
        safe_name = "".join(ch for ch in session_id if ch.isalnum() or ch in ("-", "_"))
        if not safe_name:
            return
        handler = self._handlers.get(safe_name)
        if handler is None:
            file_path = self.sessions_dir / f"{safe_name}.log"
            handler = TimedRotatingFileHandler(
                filename=str(file_path),
                when="midnight",
                interval=1,
                backupCount=14,
                encoding="utf-8",
            )
            handler.setLevel(self.level)
            if self.formatter:
                handler.setFormatter(self.formatter)
            self._handlers[safe_name] = handler
        handler.emit(record)

    def close(self) -> None:
        for handler in self._handlers.values():
            handler.close()
        self._handlers.clear()
        super().close()


class LoggerManager:
    def __init__(
        self,
        app_name: str = "genui",
        logs_dir: str | None = None,
        level: int = logging.INFO,
    ) -> None:
        self.app_name = app_name
        self.level = level
        root = Path(__file__).resolve().parent
        self.logs_dir = Path(logs_dir) if logs_dir else root / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.logs_dir / f"{self.app_name}.log"

    def configure(self) -> logging.Logger:
        logger = logging.getLogger()
        logger.setLevel(self.level)
        logger.handlers = []
        session_filter = SessionContextFilter()

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | sid=%(session_id)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(formatter)
        console_handler.addFilter(session_filter)

        file_handler = TimedRotatingFileHandler(
            filename=str(self.log_file),
            when="midnight",
            interval=1,
            backupCount=14,
            encoding="utf-8",
        )
        file_handler.setLevel(self.level)
        file_handler.setFormatter(formatter)
        file_handler.addFilter(session_filter)

        session_router_handler = SessionFileRouterHandler(
            sessions_dir=self.logs_dir / "sessions",
            level=self.level,
        )
        session_router_handler.setFormatter(formatter)
        session_router_handler.addFilter(session_filter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.addHandler(session_router_handler)
        logger.propagate = False

        logging.getLogger("werkzeug").setLevel(logging.INFO)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

        logging.getLogger("genui").info(
            "logger configured app=%s file=%s",
            self.app_name,
            str(self.log_file),
        )
        return logger


def setup_logger() -> logging.Logger:
    return LoggerManager(app_name="genui").configure()
