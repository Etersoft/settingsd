# -*- coding: utf-8 -*-


import dbus
import dbus.service
import dbus.glib
import abc

from . import config
from . import tools

from .service_decorators import *


##### Private classes #####
class ServiceInterface(object, metaclass=abc.ABCMeta) :
	@abc.abstractmethod
	def initService(self) :
		pass

	def closeService(self) :
		pass

class ServiceRequisitesInterface(object, metaclass=abc.ABCMeta) :
	@classmethod
	@abc.abstractmethod
	def serviceName(self) :
		pass

	@classmethod
	def options(self) :
		return []


##### Public classes #####
class Service(ServiceInterface, ServiceRequisitesInterface) :
	pass


#####
class CustomObject(dbus.service.Object) :
	def __init__(self, object_path, service_object = None) :
		dbus.service.Object.__init__(self, config.value(config.RUNTIME_SECTION, "bus_name"), object_path)

		self.__object_path = object_path
		self.__service_object = service_object

		#####

		self.__shared = None


	### Public ###

	def name(self) :
		if self.shared() == None :
			return None
		for (shared_object_name, shared_object) in list(self.shared().sharedObjects().items()) :
			if shared_object == self :
				return shared_object_name
		return None

	def path(self) :
		def build_path(shared) :
			if shared != None :
				path = build_path(shared.parentShared())
				return ( shared.name() if path == None else tools.dbus.joinMethod(path, shared.name()) )
			return None
		return build_path(self.shared())

	def objectPath(self) :
		return self.__object_path

	###

	def setService(self, service_object) :
		self.__service_object = service_object

	def service(self) :
		return self.__service_object

	def setShared(self, shared) :
		self.__shared = shared

	def shared(self) :
		return self.__shared

	###

	def addToConnection(self, connection = None, path = None) :
		self.add_to_connection(connection, path)

	def removeFromConnection(self, conneciton = None, path = None) :
		self.remove_from_connection(conneciton, path)


class FunctionObject(CustomObject) :
	def __init__(self, object_path, service_object = None) :
		CustomObject.__init__(self, tools.dbus.joinPath(config.value(config.APPLICATION_SECTION, "service_path"),
			"functions", object_path), service_object)

class ActionObject(CustomObject) :
	def __init__(self, object_path, service_object = None) :
		CustomObject.__init__(self, tools.dbus.joinPath(config.value(config.APPLICATION_SECTION, "service_path"),
			"actions", object_path), service_object)

