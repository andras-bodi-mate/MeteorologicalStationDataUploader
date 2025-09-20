import sty
from inspect import stack
import pathlib

from strip_ansi import strip_ansi

class Logger:
    paddedWidth = 24

    @staticmethod
    def log(message: str, level: str):
        callerStackFrame = stack()[2]
        callerFile = callerStackFrame.filename
        callerFileName = f"[{pathlib.Path(callerFile).name}]"
        for lineIndex, line in enumerate(message.split('\n')):
            logInfo = f"{callerFileName} {level}:"
            padding = Logger.paddedWidth - len(strip_ansi(logInfo))

            if lineIndex == 0:
                print(f"{logInfo}{padding * ' '} {line}")
            else:
                print(f"{Logger.paddedWidth * ' '} {line}")

    @staticmethod
    def getMessageFromValues(values):
        return ' '.join(map(str, values))

    @staticmethod
    def logDebug(*values):
        Logger.log(sty.fg.grey + Logger.getMessageFromValues(values) + sty.rs.all, sty.fg.grey + "DEBUG" + sty.rs.all)

    @staticmethod
    def logInfo(*values):
        Logger.log(sty.fg.li_cyan + Logger.getMessageFromValues(values) + sty.rs.all, sty.fg.li_cyan + "INFO" + sty.rs.all)

    @staticmethod
    def logWarning(*values):
        Logger.log(sty.fg.yellow + Logger.getMessageFromValues(values) + sty.rs.all, sty.fg.yellow + sty.ef.bold + "WARNING" + sty.rs.all)

    @staticmethod
    def logError(*values):
        Logger.log(sty.fg.red + sty.ef.bold + Logger.getMessageFromValues(values) + sty.rs.all, sty.fg.red + sty.ef.bold + "ERROR" + sty.rs.all)

    @staticmethod
    def logCriticalError(*values):
        Logger.log(sty.fg.magenta + sty.ef.bold + Logger.getMessageFromValues(values) + sty.rs.all, sty.fg.magenta + sty.ef.bold + "CRITICAL ERROR" + sty.rs.all)
