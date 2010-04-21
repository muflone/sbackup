#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# Authors:
#	Ouattara Oumar Aziz ( alias wattazoum ) <wattazoum@gmail.com>
#   Jean-Peer Lorenz <peer.loz@gmx.net>


import logging
import os.path
import nssbackup.managers.FileAccessManager as FAM


def shutdown_logging():
	logging.shutdown()


class LogFactory(object):
	"""
	"""
	logger = None
	created_loggers = []
	
	#create formatter
	formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
	debug_formatter = logging.Formatter("%(asctime)s - %(levelname)s in "\
						"%(module)s.%(funcName)s(%(lineno)d): %(message)s")
	
	def __init__(self):
		pass
	
	def getLogger(name=None, logfile=None, level=20 ) :
		"""Returns last used logger instance. If no instance exists, a new
		one is created.
		
		@param name: The name of the logger
		@param logfile : default=False
		@param level: The level of the logger (default = logging.INFO(20) )
		"""
		if LogFactory.logger :
			if name:
				if LogFactory.logger.name == name :
					return LogFactory.logger
				else :
					return LogFactory.__createLogger(name,logfile,level)
			else :
				return LogFactory.logger
		else :
			return LogFactory.__createLogger(name,logfile,level)

	getLogger = staticmethod(getLogger)
	
	def __createLogger(name=None, logfile=None, level=20):
		"""Private helper method that creates a new logger instance.
		To avoid the overwriting of previous settings, the names of
		already created loggers are stored.
		"""
		if not name:
			name = "NSsbackup"

		_formatter = LogFactory.formatter
		if level == logging.DEBUG:
			_formatter = LogFactory.debug_formatter
			
		#create logger
		LogFactory.logger = logging.getLogger(name)
		if name in LogFactory.created_loggers:
			pass
		else:
			LogFactory.created_loggers.append( name )
			LogFactory.logger.setLevel(level)
			
			#create console handler and set level and formatter
			ch = logging.StreamHandler()
			ch.setLevel(level)
			ch.setFormatter(_formatter)
			LogFactory.logger.addHandler(ch)
			
			if logfile:
				# create the logfile
				if not os.path.exists(logfile) :
					#make sure that the parent directory exist
					parentdir = os.path.dirname(os.path.abspath(logfile))
					if not os.path.exists(parentdir):
						os.makedirs(parentdir)
					FAM.writetofile(logfile, "NSSBackup '%s' Logger\r\n==============\r\n" % name)
				else :
					# clean the logfile
					FAM.rename(logfile, logfile + ".old")
					FAM.writetofile(logfile, "NSSBackup '%s' Logger\r\n==============\r\n" % name)
				ch1 = logging.FileHandler(logfile)
				ch1.setLevel(level)
				ch1.setFormatter(_formatter)
				LogFactory.logger.addHandler(ch1)
		return LogFactory.logger

	__createLogger = staticmethod(__createLogger)
