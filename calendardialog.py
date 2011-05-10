#! /usr/bin/python
# -*- coding: iso-8859-15 -*-
#
__author__='atareao'
__date__ ='$06-jun-2010 12:34:44$'
#
# <one line to give the program's name and a brief idea of what it does.>
#
# Copyright (C) 2010 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
import gtk
import locale
import gettext
#
import comun
from configurator import GConf
from encoderapi import Encoder
#from gcal import GCal


locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(comun.APP, comun.LANGDIR)
gettext.textdomain(comun.APP)
_ = gettext.gettext

def getDay(cadena):
	if cadena.find('T') == 0:
		return cadena.split('-')[2]
	else:
		return cadena.split('T')[0].split('-')[2]

class CalendarDialog(gtk.Dialog):
	def __init__(self,title,parent = None,googlecalendar = None):
		self.ok = False
		self.googlecalendar = googlecalendar
		self.selecteds = {}
		#
		title = comun.APP + ' | '+_('Preferences')
		gtk.Dialog.__init__(self,title,parent,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
		self.set_default_size(50, 450)
		self.set_resizable(False)
		self.set_icon(gtk.gdk.pixbuf_new_from_file(comun.ICON))		
		self.connect('destroy', self.close_application)
		#
		vbox0 = gtk.VBox(spacing = 5)
		vbox0.set_border_width(5)
		self.get_content_area().add(vbox0)
		#
		self.calendar = gtk.Calendar()
		self.calendar.set_display_options(gtk.CALENDAR_SHOW_DAY_NAMES | gtk.CALENDAR_SHOW_HEADING | gtk.CALENDAR_SHOW_WEEK_NUMBERS)
		self.calendar.connect('month-changed',self.on_month_changed)
		self.calendar.connect('day-selected',self.on_day_selected)
		vbox0.add(self.calendar)
		self.on_month_changed(self)
		#
		self.show_all()
	def on_day_selected(self,widget):
		date = self.calendar.get_date()
		print 'dia -> %s' %(date[2])
		print 'mes -> %s' %(date[1]+1)
		print 'año -> %s' %(date[0])
		if date[2] in self.selecteds.keys():
			print 'Si'
			self.calendar.set_tooltip_text(self.selecteds[date[2]])
		else:
			self.calendar.set_tooltip_text('')

	def on_month_changed(self,widget):
		date = self.calendar.get_date()
		if self.googlecalendar != None:
			events = self.googlecalendar.getAllEventsOnMonthOnDefaultCalendar(date[1]+1,date[0])
			self.selecteds = {}
			self._clear_marks()
			for event in events:
				if len(event.when)>0:
					dia = getDay(event.when[0].start)
					self.selecteds[int(dia)] = event.title.text
			self._mark_days()
			
	def _unmark_days(self):
		for key in self.selecteds.keys():
			self.calendar.unmark_day(key)

	def _mark_days(self):
		for key in self.selecteds.keys():
			self.calendar.mark_day(key)
	def _clear_marks(self):
		self.calendar.clear_marks()
			
	def close_application(self,widget):
		self.ok = False
		self.hide()

if __name__ == "__main__":
	cd = CalendarDialog('')
	cd.run()
	exit(0)
		
