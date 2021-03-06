# -*- coding: utf-8 -*-


##### Public constants #####
MY_NAME = "settingsd"

VERSION = "0.3"
VERSION_STATUS = "beta"
FUNCTIONALITY_LEVEL = 132


FUNCTIONS_DIR = "plugins/functions"
ACTIONS_DIR = "plugins/actions"
CUSTOMS_DIR = "plugins/customs"

FUNCTIONS_DATA_DIR = "data/functions"
ACTIONS_DATA_DIR = "data/actions"
CUSTIOMS_DIR = "data/customs"

CONFIGS_DIR = "configs/settingsd"
CONFIG_FILE_POSTFIX = ".conf"


BUS_TYPE_SYSTEM = "system"
BUS_TYPE_SESSION = "session"
ALL_BUS_TYPES_LIST = (
	BUS_TYPE_SYSTEM,
	BUS_TYPE_SESSION
)

LOG_LEVEL_INFO = 0
LOG_LEVEL_VERBOSE = 1
LOG_LEVEL_DEBUG = 2
ALL_LOG_LEVELS_LIST = (
	LOG_LEVEL_INFO,
	LOG_LEVEL_VERBOSE,
	LOG_LEVEL_DEBUG
)


DEFAULT_SERVICE_NAME = "org.etersoft.%s" % (MY_NAME)
DEFAULT_SERVICE_PATH = "/org/etersoft/%s" % (MY_NAME)
DEFAULT_BUS_TYPE = BUS_TYPE_SYSTEM
DEFAULT_LOG_LEVEL = LOG_LEVEL_INFO
DEFAULT_LOG_USE_COLORS_FLAG = True

