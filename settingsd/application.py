# -*- coding: utf-8 -*-


import sys
import os
import signal
import syslog

import const
import config
import logger
import server
import daemon


##### Public classes #####
class Application(object) :
	def __init__(self, log_level, use_syslog_flag, bus_type, daemon_mode_flag) :
		object.__init__(self)

		#####

		self._log_level = log_level
		self._use_syslog_flag = use_syslog_flag
		self._bus_type = bus_type
		self._daemon_mode_flag = daemon_mode_flag

		#####

		self._server = server.Server()


	### Public ###

	def run(self) :
		self.prepare()
		if self._daemon_mode_flag :
			logger.info("Run server in daemon mode")
			self.runDaemon()
		else :
			logger.info("Run server in interactive mode")
			self.runInteractive()

	def server(self) :
		return self._server

	###

	def quit(self, signum = None, frame = None) :
		if signum != None :
			logger.info("Recieved signal %d, closing..." % (signum))

		self._server.closeServices()
		self._server.quitLoop()
		logger.info("Closed")


	### Private ###

	def prepare(self) :
		if self._use_syslog_flag == None :
			if self._daemon_mode_flag :
				syslog.openlog(const.MY_NAME, syslog.LOG_PID, syslog.LOG_DAEMON)
				config.setValue(config.RUNTIME_SECTION, "use_syslog", True)
				logger.verbose("Logger used syslog")
		else :
			syslog.openlog(const.MY_NAME, syslog.LOG_PID, ( syslog.LOG_DAEMON if self._daemon_mode_flag else syslog.LOG_USER ))
			config.setValue(config.RUNTIME_SECTION, "use_syslog", True)
			logger.verbose("Logger used syslog")

		try :
			self._server.loadServerConfigs()
		except :
			logger.error("Initialization error")
			logger.attachException()
			raise
		logger.verbose("Preparing complete")

		if self._bus_type != None :
			config.setValue(config.APPLICATION_SECTION, "bus_type", self._bus_type)

		if self._log_level != None :
			config.setValue(config.APPLICATION_SECTION, "log_level", self._log_level)

		config.setValue(config.RUNTIME_SECTION, "application", self)

	###

	def runInteractive(self) :
		try :
			self._server.loadModules()
			self._server.loadServicesConfigs()
			self._server.initBus()
			self._server.initServices()
			logger.info("Initialized")
		except :
			logger.error("Initialization error")
			logger.attachException()
			raise

		try :
			signal.signal(signal.SIGTERM, self.quit)
			signal.signal(signal.SIGQUIT, self.quit)
		except :
			logger.error("signal() error")
			logger.attachException()

		try :
			self._server.runLoop()
		except (SystemExit, KeyboardInterrupt) :
			self.quit()
		except :
			logger.error("Runtime error, trying to close services")
			logger.attachException()
			try :
				self.quit()
			except :
				logger.attachException()
				raise
			raise

	def runDaemon(self) :
		work_dir_path = ( "/" if os.getuid() == 0 else None )
		umask = ( 077 if os.getuid() == 0 else None )

		logger.info("Run server as daemon: uid=%d, dir=%s, umask=%s" % ( os.getuid(),
			( work_dir_path if work_dir_path != None else os.getcwd() ),
			( str(umask) if umask != None else "%.4x" % os.umask(-1) ) ))

		daemon.startDaemon(self.runInteractive, work_dir_path, umask)

