#!/usr/bin/env python3

IP="192.168.0.2"
PORT=1883
TOPIC="Undefined"
ID="YourID"
PW="PassWord"
SEC=10

import json
from paho.mqtt import client as mqtt
import dearpygui.dearpygui as dpg
import numpy as np

class SubScribe:
    def set_plot(self, name):
        
        with dpg.theme() as theme:
        # Plotに有効なテーマ
            with dpg.theme_component(dpg.mvPlot):
                dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 220, 0), category=dpg.mvThemeCat_Plots)
                #dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 220, 0), category=dpg.mvThemeCat_Nodes)

        with dpg.plot(parent=self.sub,anti_aliased=True) as theme_plt:
            if (self.Isfix):
                x_axis = dpg.add_plot_axis(dpg.mvXAxis, time=False)
                #dpg.set_axis_limits(x_axis, 0, self.DisplaySeconds)
            else:
                x_axis = dpg.add_plot_axis(dpg.mvXAxis, time=True)
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label=name)

        l = dpg.add_line_series([], [], label=name, parent=y_axis)

        # テーマ適用
        dpg.bind_item_theme(theme_plt, theme)

        return {name: {'ecg': [], 'x_axis': x_axis, 'y_axis': y_axis, 'ecg_plot': l}}

    def on_message(self, mqttc, obj, msg):
        ecg_dict = json.loads(msg.payload)
        timestamp = ecg_dict['actual msec since epoch']/1000+9*3600
        del ecg_dict['actual msec since epoch']
        self.ti.append(timestamp)
 
        self.datafull = False
        if (timestamp-self.ti[0]) > self.DisplaySeconds:
            self.datafull = True
        
        if self.datafull == True:
            self.ti.pop(0)
    
        if self.Isfix:
            ti_array = np.array(self.ti)+self.DisplaySeconds-timestamp
  
        for key in ecg_dict.keys():
            if (key not in self.graph):
                self.graph |= self.set_plot(key)

            self.graph[key]['ecg'].append(ecg_dict[key])
            if self.datafull:
                self.graph[key]['ecg'].pop(0)

            if timestamp-self.ti[0] <0.2:
                #dpg.set_value(self.graph[key]['ecg_plot'], [[0,self.DisplaySeconds], [-0.6,0.6]])
                dpg.set_value(self.graph[key]['ecg_plot'], [[0,self.DisplaySeconds], [-1.5,1.5]])
                dpg.fit_axis_data(self.graph[key]['y_axis'])
                dpg.fit_axis_data(self.graph[key]['x_axis'])

            if  0.5<=timestamp-self.ti[0] <0.5:
                #dpg.set_value(self.graph[key]['ecg_plot'], [[0,self.DisplaySeconds], [-0.6,0.6]])
                dpg.set_value(self.graph[key]['ecg_plot'], [[0,self.DisplaySeconds], [-1.5,1.5]])


            if timestamp-self.ti[0]>1:
                if self.Isfix:
                    dpg.set_value(self.graph[key]['ecg_plot'], [ti_array, self.graph[key]['ecg']])
                else:
                    dpg.set_value(self.graph[key]['ecg_plot'], [self.ti, self.graph[key]['ecg']])

                if self.Isfix==False:
                    dpg.fit_axis_data(self.graph[key]['x_axis'])




    def __init__(self, host, port, topic, username, password,  sec, fix):
        self.Isfix = fix
        self.DisplaySeconds = sec
  
        self.datafull = False

        self.graph = dict()
        self.ti = list()
        
        self.mainwindow = dpg.add_window()
        dpg.set_primary_window(self.mainwindow, True)
        if (self.Isfix==True):
            self.sub=dpg.add_subplots(rows=6, columns=2,no_title=True, height=-1, width=-1, no_resize=False,parent=self.mainwindow,column_ratios=[1,1],link_all_x=True,link_all_y=True,column_major=True)
        else:
            self.sub=dpg.add_subplots(rows=6, columns=2,no_title=True, height=-1, width=-1, no_resize=False,parent=self.mainwindow,column_ratios=[1,1],link_all_x=False,link_all_y=True,column_major=True)

        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)
        self.client.connect(host, port)
        self.client.subscribe(topic)
        self.client.on_message = self.on_message

        self.client.loop_start()

    def __del__(self):
        self.dissconnect()
        if dpg.does_item_exist(self.mainwindow):
            dpg.delete_item(self.mainwindow)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

dpg.create_context()
dpg.create_viewport(title='ecg', width=1600, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
ss = SubScribe(IP, PORT, TOPIC, ID, PW, sec=SEC, fix=True)
dpg.start_dearpygui()
del ss
dpg.destroy_context()
