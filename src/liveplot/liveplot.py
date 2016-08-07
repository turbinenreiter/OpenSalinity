#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import serial
import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib
from collections import deque

class LivePlot(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="LivePlot")

        # Serial port
        self.raw = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)
        self.conds = [deque(10*[0], 10) for _ in range(8)] # conditioned data
        self.raw.write(b'\x03') # cancel

        # filename
        self.filename = None

        # Window
        self.connect('destroy', lambda w: Gtk.main_quit())
        self.set_default_size(1920, 1080)

        # HeaderBar
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = 'OpenSalinity GUI'
        self.set_titlebar(self.header)

        # Start/Stop Button
        self.control_btn = Gtk.ToggleButton('Start')
        self.header.pack_start(self.control_btn)
        self.control_btn.connect('toggled', self.control, 'control')

        # Save Button
        self.save_btn = Gtk.Button("Save")
        self.header.pack_end(self.save_btn)
        self.save_btn.connect('clicked', self.save)

        # DrawingArea
        self.drawingarea = Gtk.DrawingArea()
        self.add(self.drawingarea)
        self.drawingarea.connect('draw', self.draw)

        self.show_all()

        #GLib.timeout_add(1, self.queue)

    def queue(self):
        self.drawingarea.queue_draw_area(0, 0, 1920, 1080)
        return self.queue_return

    def control(self, btn, name):
        if self.filename is None:
            return

        if btn.get_active():
            self.raw.write(b'\x04') # reset
            self.control_btn.set_label('Stop')
            GLib.timeout_add(1, self.queue)
            self.queue_return = True
        else:
            self.raw.write(b'\x03') # cancel
            self.control_btn.set_label('Start')
            self.queue_return = False

    def save(self, uk):
        dialog = Gtk.FileChooserDialog("Save file", self,
                               Gtk.FileChooserAction.SAVE,
                               (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                               Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        timestr = time.strftime('%d%m%Y%H%M', time.localtime())
        dialog.set_current_name('log-'+timestr+'.csv')

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.filename = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            pass
        self.set_title('OpenSalinity GUI - ' + self.filename)
        dialog.destroy()

    def draw(self, widget, context):

        t0 = time.time()

        w, h = self.get_size()
        sc = -(h)*0.9
        st = w*0.9/8
        context.translate(w*0, h*0.9)

        context.set_line_width(1)
        context.set_source_rgb(0,0,0)#0.878, 0.878, 0.878)
        context.set_font_size(16)

        context.move_to(w*0.05, -h*0.85)
        context.show_text('max ')
        context.line_to(w*0.95, -h*0.85)
        context.stroke()
        context.move_to(w*0.05, -h*0)
        context.show_text('min ')
        context.line_to(w*0.95, -h*0)
        context.stroke()

        context.set_line_width(50)
        context.set_source_rgb(1, 0.341, 0.133)

        line = str(self.raw.readline(), 'utf-8')
        data = line.split(' ')

        if len(data) == 17:
            with open(self.filename, 'a') as log:
                log.write(line)
        else:
            data = [0]*17

        #if data.pop(0) != "b'#":
        #    return
        #data.pop(-1)

        values = []
        for i, val in enumerate(data):
            if i%2:
                values.append((int(val)/4096))
            else:
                pass

        for i, cond in enumerate(values):

            if cond > 0 and cond < 1:
                self.conds[i].append(cond)

            val = sum(self.conds[i])/len(self.conds[i])
            context.set_source_rgb(1-val*0.95, 0.341-val*0.25, 0.133+val*0.15)
            context.move_to((i+1)*st, 0)
            context.line_to((i+1)*st, val*sc)
            context.move_to((i+1)*st-25, sc*-0.05)
            context.set_font_size(24)
            context.show_text('#'+str(i+1))
            context.stroke()

        #print(1/(time.time()-t0))

if __name__ == '__main__':
    plot = LivePlot()
    Gtk.main()
