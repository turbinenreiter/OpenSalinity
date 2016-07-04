#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import threading
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

        self.raw = serial.Serial("/dev/ttyACM0", 9600)
        self.conds = [deque(10*[0], 10) for _ in range(8)]

        self.connect('destroy', lambda w: Gtk.main_quit())
        self.set_default_size(1920, 1080)

        self.drawingarea = Gtk.DrawingArea()
        self.add(self.drawingarea)
        self.drawingarea.connect('draw', self.draw)

        self.show_all()

        GLib.timeout_add(1, self.queue)

    def queue(self):
        self.drawingarea.queue_draw_area(0, 0, 1920, 1080)
        return True

    def draw(self, widget, context):

        t0 = time.time()

        w, h = self.get_size()
        sc = -(h)*0.9
        st = w*0.9/8
        context.translate(w*0, h*0.9)

        context.set_line_width(1)
        context.set_source_rgb(0.878, 0.878, 0.878)
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

        data = str(self.raw.readline()).split(' ')

        if data.pop(0) != "b'#":
            return
        data.pop(-1)

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
