import tkinter as tk
from PIL import Image, ImageTk
import serial
import time
import threading
import os
import sys
import simpleaudio as sa

ser = serial.Serial('/dev/ttyS0', 115200)
ser.reset_input_buffer()
ser.reset_output_buffer()

######config######
zoom_rate = 4
racecourse_index = 6
race_index = 1
arrival1_index = 1
arrival2_index = 2
arrival3_index = 3
arrival4_index = 4
arrival5_index = 5
conf_index = 0
number10_index = 10
number1_index = 10
distance1_index = 0
distance2_index = 0
distance3_index = 0
distance4_index = 0
douchaku_line1_index = 0
douchaku_line2_index = 0
douchaku_line3_index = 0
douchaku_line4_index = 0
status_turf_index = 0
status_dirt_index = 0
time_min_index = 10
time_sec10_index = 10
time_sec1_index = 10
time_dec_index = 10
fur4_sec10_index = 10
fur4_sec1_index = 10
fur4_dec_index = 10
fur3_sec10_index = 10
fur3_sec1_index = 10
fur3_dec_index = 10
record_index = 0
douchaku12 = False
douchaku23 = False
douchaku34 = False
douchaku45 = False
shingi = True
after_id1 = None
after_id2 = None
serial_thread = None
isBlinkOn = False
quit_flag = False
testing = False
AfterBoot = True
signal_before = ''
racecourse_wid=24*zoom_rate
conf_wid=102*zoom_rate
arrival_wid=37*zoom_rate
number_wid=76*zoom_rate
distance_wid=52*zoom_rate
douchaku_line_wid=22*zoom_rate
status_wid=72*zoom_rate
race_wid=34*zoom_rate
time_digit_wid=16*zoom_rate
time_wid=52*zoom_rate
furlong_wid=30*zoom_rate
dot_wid=4*zoom_rate
record_wid=78*zoom_rate
blinking = 0
a = 0
signal_ext=''
kakutei_sound = sa.WaveObject.from_wave_file('kakutei.wav')
##################

def test_disp():
    global a
    a = 1 - a
    conf_disp(str(a + 1))
    racecourse_disp(1)
    number1_disp('18')
    number2_disp('18')
    number3_disp('18')
    number4_disp('18')
    number5_disp('18')
    distance1_disp('1')
    distance2_disp('1')
    distance3_disp('1')
    distance4_disp('1')
    race_disp('11')
    status_disp('2', '2')
    time_disp(8,8,8,8)
    fur4_disp(8,8,8)
    fur3_disp(8,8,8)
    record_disp(1)
    

def window_init():
    conf_disp()
    number1_disp()
    number2_disp()
    number3_disp()
    number4_disp()
    number5_disp()
    distance1_disp()
    distance2_disp()
    distance3_disp()
    distance4_disp()
    race_disp()
    status_disp()
    time_disp()
    fur4_disp()
    fur3_disp()
    record_disp()
    
    
def win_close():
    global quit_flag
    global serial_thread
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    ser.write(b"disconnect")#send_connection_start_request
    ser.close()
    sys.exit()

def blink(): #馬番号点滅処理
    global blinking
    global after_id1
    global after_id2
    global isBlinkOn
    global testing
    if blinking == 0:
        number1_canvas.itemconfigure('number1_10', state='hidden')
        number1_canvas.itemconfigure('number1_1', state='hidden')
        number2_canvas.itemconfigure('number2_10', state='hidden')
        number2_canvas.itemconfigure('number2_1', state='hidden')
        number3_canvas.itemconfigure('number3_10', state='hidden')
        number3_canvas.itemconfigure('number3_1', state='hidden')
        number4_canvas.itemconfigure('number4_10', state='hidden')
        number4_canvas.itemconfigure('number4_1', state='hidden')
        number5_canvas.itemconfigure('number5_10', state='hidden')
        number5_canvas.itemconfigure('number5_1', state='hidden')
        if testing:
            record_canvas.itemconfigure('record', state='hidden')
        blinking = 1
        after_id1 = root.after(500, blink)
    else: 
        number1_canvas.itemconfigure('number1_10', state='normal')
        number1_canvas.itemconfigure('number1_1', state='normal')
        number2_canvas.itemconfigure('number2_10', state='normal')
        number2_canvas.itemconfigure('number2_1', state='normal')
        number3_canvas.itemconfigure('number3_10', state='normal')
        number3_canvas.itemconfigure('number3_1', state='normal')
        number4_canvas.itemconfigure('number4_10', state='normal')
        number4_canvas.itemconfigure('number4_1', state='normal')
        number5_canvas.itemconfigure('number5_10', state='normal')
        number5_canvas.itemconfigure('number5_1', state='normal')
        if testing:
            record_canvas.itemconfigure('record', state='normal')
        blinking = 0
        after_id2 = root.after(1000, blink)
    isBlinkOn = True
        
def stop_blink(): #馬番号点滅停止
    root.after_cancel(after_id1)
    root.after_cancel(after_id2)
    if blinking == 1:
        number1_canvas.itemconfigure('number1_10', state='normal')
        number1_canvas.itemconfigure('number1_1', state='normal')
        number2_canvas.itemconfigure('number2_10', state='normal')
        number2_canvas.itemconfigure('number2_1', state='normal')
        number3_canvas.itemconfigure('number3_10', state='normal')
        number3_canvas.itemconfigure('number3_1', state='normal')
        number4_canvas.itemconfigure('number4_10', state='normal')
        number4_canvas.itemconfigure('number4_1', state='normal')
        number5_canvas.itemconfigure('number5_10', state='normal')
        number5_canvas.itemconfigure('number5_1', state='normal')
        if testing:
            record_canvas.itemconfigure('record', state='normal')
    isBlinkOn = False

def manualBlink(): #馬番号点滅の有無をトグル
    if isBlinkOn:
        stop_blink()
    blink()


###################Func. of displaying######################
def racecourse_disp(keibajo = '0'): # 開催場名の表示処理
    global racecourse
    racecourse_canvas.delete('racecourse')
    racecourse = racecourse_img[int(keibajo)].zoom(zoom_rate, zoom_rate)
    racecourse_canvas.create_image(racecourse_wid / 2, (racecourse_wid / 24)*25, image=racecourse, tag="racecourse")
#---------------------------
def status_disp(baba1 = '0', baba2 = '0'): #馬場状態の表示処理
    global status_turf
    global status_dirt
    status_turf_canvas.delete('status_turf')
    status_turf = status_img[int(baba1)].zoom(zoom_rate, zoom_rate)
    status_turf_canvas.create_image(status_wid / 2, (status_wid /72) * 17, image=status_turf, tag="status_turf")
    status_dirt_canvas.delete('status_dirt')
    status_dirt = status_img[int(baba2)].zoom(zoom_rate, zoom_rate)
    status_dirt_canvas.create_image(status_wid / 2, (status_wid /72) * 17, image=status_dirt, tag="status_dirt")
#---------------------------
def race_disp(raceno = '0'): # レース番号の表示処理
    global race
    race_canvas.delete('race')
    race = race_img[int(raceno)].zoom(zoom_rate, zoom_rate)
    race_canvas.create_image(race_wid / 2, (race_wid / 34)*17, image=race, tag="race")
#---------------------------
def arrival1_disp(jyuni = '1'): #１着表示処理
    global arrival1
    arrival1_canvas.delete('arrival1')
    arrival1 = arrival_img[int(jyuni)].zoom(zoom_rate, zoom_rate)
    arrival1_canvas.create_image(arrival_wid / 2, (arrival_wid /37) * 18.5, image=arrival1, tag="arrival1")

def arrival2_disp(jyuni = '2'): #２着表示処理
    if douchaku12:
        jyuni = '1'
    global arrival2
    arrival2_canvas.delete('arrival2')
    arrival2 = arrival_img[int(jyuni)].zoom(zoom_rate, zoom_rate)
    arrival2_canvas.create_image(arrival_wid / 2, (arrival_wid /37) * 18.5, image=arrival2, tag="arrival2")

def arrival3_disp(jyuni = '3'): #３着表示処理
    if douchaku12 and douchaku23:
        jyuni = '1'
    elif douchaku23:
        jyuni = '2'
    global arrival3
    arrival3_canvas.delete('arrival3')
    arrival3 = arrival_img[int(jyuni)].zoom(zoom_rate, zoom_rate)
    arrival3_canvas.create_image(arrival_wid / 2, (arrival_wid /37) * 18.5, image=arrival3, tag="arrival3")

def arrival4_disp(jyuni = '4'): #４着表示処理
    if douchaku12 and douchaku23 and douchaku34:
        jyuni = '1'
    elif douchaku23 and douchaku34:
        jyuni = '2'
    elif douchaku34:
        jyuni = '3'
    global arrival4
    arrival4_canvas.delete('arrival4')
    arrival4 = arrival_img[int(jyuni)].zoom(zoom_rate, zoom_rate)
    arrival4_canvas.create_image(arrival_wid / 2, (arrival_wid /37) * 18.5, image=arrival4, tag="arrival4")

def arrival5_disp(jyuni = '5'): #５着表示処理
    if douchaku12 and douchaku23 and douchaku34 and douchaku45:
        jyuni = '1'
    elif douchaku23 and douchaku34 and douchaku45:
        jyuni = '2'
    elif douchaku34 and douchaku45:
        jyuni = '3'
    elif douchaku45:
        jyuni = '4'
    global arrival5
    arrival5_canvas.delete('arrival5')
    arrival5 = arrival_img[int(jyuni)].zoom(zoom_rate, zoom_rate)
    arrival5_canvas.create_image(arrival_wid / 2, (arrival_wid /37) * 18.5, image=arrival5, tag="arrival5")
#---------------------------
def conf_disp(kakutei='0'): # 未確定・確定・審議の表示処理
    global shingi
    if kakutei == '0' or kakutei == '2':
        if isBlinkOn:
            stop_blink()
        blink()
    elif kakutei == '1':
        stop_blink()
        sa.stop_all()
        conf_sound = kakutei_sound.play()
    global conf
    conf_canvas.delete('conf')
    conf= conf_img[int(kakutei)].zoom(zoom_rate, zoom_rate)
    conf_canvas.create_image(conf_wid / 2, (conf_wid /102) * 25, image=conf, tag="conf")
#---------------------------
def distance1_disp(chakusa='0'): #1-2着間の着差表示処理
    global douchaku12
    if chakusa == "0":
        distance1_canvas.delete('distance1')
        douchaku12 = False
    else:
        if chakusa == '1':
            douchaku12 = True
        else:
            douchaku12 = False
        global distance1
        distance1_canvas.delete('distance1')
        distance1 = distance_img[int(chakusa)].zoom(zoom_rate, zoom_rate)
        distance1_canvas.create_image(distance_wid / 2, (distance_wid / 52) * 13, image=distance1, tag="distance1")
    arrival1_disp()
    arrival2_disp()
    douchaku_line1_disp()

def distance2_disp(chakusa='0'): #2-3着間の着差表示処理
    global douchaku23
    if chakusa == "0":
        distance2_canvas.delete('distance2')
        douchaku23 = False
    else:
        if chakusa == '1':
            douchaku23 = True
        else:
            douchaku23 = False
        global distance2
        distance2_canvas.delete('distance2')
        distance2 = distance_img[int(chakusa)].zoom(zoom_rate, zoom_rate)
        distance2_canvas.create_image(distance_wid / 2, (distance_wid / 52) * 13, image=distance2, tag="distance2")
    arrival2_disp()
    arrival3_disp()
    douchaku_line2_disp()

def distance3_disp(chakusa='0'): #3-4着間の着差表示処理
    global douchaku34
    if chakusa == "0":
        distance3_canvas.delete('distance3')
        douchaku34 = False
    else:
        if chakusa == '1':
            douchaku34 = True
        else:
            douchaku34 = False
        global distance3
        distance3_canvas.delete('distance3')
        distance3 = distance_img[int(chakusa)].zoom(zoom_rate, zoom_rate)
        distance3_canvas.create_image(distance_wid / 2, (distance_wid / 52) * 13, image=distance3, tag="distance3")
    arrival3_disp()
    arrival4_disp()
    douchaku_line3_disp()

def distance4_disp(chakusa='0'): #4-5着間の着差表示処理
    global douchaku45
    if chakusa == "0":
        distance4_canvas.delete('distance4')
        douchaku45 = False
    else:
        if chakusa == '1':
            douchaku45 = True
        else:
            douchaku45 = False
        global distance4
        distance4_canvas.delete('distance4')
        distance4 = distance_img[int(chakusa)].zoom(zoom_rate, zoom_rate)
        distance4_canvas.create_image(distance_wid / 2, (distance_wid / 52) * 13, image=distance4, tag="distance4")
    arrival4_disp()
    arrival5_disp()
    douchaku_line4_disp()

#---------------------------
def number1_disp(umaban = ''): #1着馬番号表示処理
    if umaban == "":
        number1_canvas.delete('number1_10')
        number1_canvas.delete('number1_1')
    else:
        global number1_10_img
        global number1_1_img
        number1_canvas.delete('number1_10')
        number1_canvas.delete('number1_1')
        number1_index = int(str(umaban)[-1])
        if int(str(umaban)[-2]) != 0:
            number10_index = int(str(umaban)[-2])
        else:
            number10_index = 10
        number1_10_img = number_img[number10_index].zoom(zoom_rate, zoom_rate)
        number1_1_img = number_img[number1_index].zoom(zoom_rate, zoom_rate)
        number1_canvas.create_image(76, (number_wid / 76) * 18, image=number1_10_img, tag="number1_10")
        number1_canvas.create_image(228, (number_wid / 76) * 18, image=number1_1_img, tag="number1_1")

def number2_disp(umaban= ''): #2着馬番号表示処理
    if umaban == "":
        number2_canvas.delete('number2_10')
        number2_canvas.delete('number2_1')
    else:
        global number2_10_img
        global number2_1_img
        number2_canvas.delete('number2_10')
        number2_canvas.delete('number2_1')
        number1_index = int(str(umaban)[-1])
        if int(str(umaban)[-2]) != 0:
            number10_index = int(str(umaban)[-2])
        else:
            number10_index = 10
        number2_10_img = number_img[number10_index].zoom(zoom_rate, zoom_rate)
        number2_1_img = number_img[number1_index].zoom(zoom_rate, zoom_rate)
        number2_canvas.create_image(76, (number_wid / 76) * 18, image=number2_10_img, tag="number2_10")
        number2_canvas.create_image(228, (number_wid / 76) * 18, image=number2_1_img, tag="number2_1")

def number3_disp(umaban= ''): #3着馬番号表示処理
    if umaban == "":
        number3_canvas.delete('number3_10')
        number3_canvas.delete('number3_1')
    else:
        global number3_10_img
        global number3_1_img
        number3_canvas.delete('number3_10')
        number3_canvas.delete('number3_1')
        number1_index = int(str(umaban)[-1])
        if int(str(umaban)[-2]) != 0:
            number10_index = int(str(umaban)[-2])
        else:
            number10_index = 10
        number3_10_img = number_img[number10_index].zoom(zoom_rate, zoom_rate)
        number3_1_img = number_img[number1_index].zoom(zoom_rate, zoom_rate)
        number3_canvas.create_image(76, (number_wid / 76) * 18, image=number3_10_img, tag="number3_10")
        number3_canvas.create_image(228, (number_wid / 76) * 18, image=number3_1_img, tag="number3_1")

def number4_disp(umaban= ''): #4着馬番号表示処理
    if umaban == "":
        number4_canvas.delete('number4_10')
        number4_canvas.delete('number4_1')
    else:
        global number4_10_img
        global number4_1_img
        number4_canvas.delete('number4_10')
        number4_canvas.delete('number4_1')
        number1_index = int(str(umaban)[-1])
        if int(str(umaban)[-2]) != 0:
            number10_index = int(str(umaban)[-2])
        else:
            number10_index = 10
        number4_10_img = number_img[number10_index].zoom(zoom_rate, zoom_rate)
        number4_1_img = number_img[number1_index].zoom(zoom_rate, zoom_rate)
        number4_canvas.create_image(76, (number_wid / 76) * 18, image=number4_10_img, tag="number4_10")
        number4_canvas.create_image(228, (number_wid / 76) * 18, image=number4_1_img, tag="number4_1")

def number5_disp(umaban= ''): #5着馬番号表示処理
    if umaban == "":
        number5_canvas.delete('number5_10')
        number5_canvas.delete('number5_1')
    else:
        global number5_10_img
        global number5_1_img
        number5_canvas.delete('number5_10')
        number5_canvas.delete('number5_1')
        number1_index = int(str(umaban)[-1])
        if int(str(umaban)[-2]) != 0:
            number10_index = int(str(umaban)[-2])
        else:
            number10_index = 10
        number5_10_img = number_img[number10_index].zoom(zoom_rate, zoom_rate)
        number5_1_img = number_img[number1_index].zoom(zoom_rate, zoom_rate)
        number5_canvas.create_image(76, (number_wid / 76) * 18, image=number5_10_img, tag="number5_10")
        number5_canvas.create_image(228, (number_wid / 76) * 18, image=number5_1_img, tag="number5_1")
#---------------------------
def douchaku_line1_disp(douchaku = '0'):
    if douchaku12:
        douchaku = '1'
    global douchaku_line1
    douchaku_line1_canvas.delete('douchaku_line1')
    douchaku_line1 = douchaku_line_img[int(douchaku)].zoom(zoom_rate, zoom_rate)
    douchaku_line1_canvas.create_image(douchaku_line_wid / 2, (distance_wid / 22) * 6.75, image=douchaku_line1, tag="douchaku_line1")

def douchaku_line2_disp(douchaku = '0'):
    if douchaku23:
        douchaku = '1'
    global douchaku_line2
    douchaku_line2_canvas.delete('douchaku_line2')
    douchaku_line2 = douchaku_line_img[int(douchaku)].zoom(zoom_rate, zoom_rate)
    douchaku_line2_canvas.create_image(douchaku_line_wid / 2, (distance_wid / 22) * 6.75, image=douchaku_line2, tag="douchaku_line2")

def douchaku_line3_disp(douchaku = '0'):
    if douchaku34:
        douchaku = '1'
    global douchaku_line3
    douchaku_line3_canvas.delete('douchaku_line3')    
    douchaku_line3 = douchaku_line_img[int(douchaku)].zoom(zoom_rate, zoom_rate)
    douchaku_line3_canvas.create_image(douchaku_line_wid / 2, (distance_wid / 22) * 6.75, image=douchaku_line3, tag="douchaku_line3")

def douchaku_line4_disp(douchaku = '0'):
    if douchaku45:
        douchaku = '1'
    global douchaku_line4
    douchaku_line4_canvas.delete('douchaku_line4')    
    douchaku_line4 = douchaku_line_img[int(douchaku)].zoom(zoom_rate, zoom_rate)
    douchaku_line4_canvas.create_image(douchaku_line_wid / 2, (distance_wid / 22) * 6.75, image=douchaku_line4, tag="douchaku_line4")
#---------------------------
def time_disp(mi = '10', sec10 = '10', sec1 = '10', dec = '10'):
    time_min_canvas.delete('time_min')
    time_sec10_canvas.delete('time_sec10')
    time_sec1_canvas.delete('time_sec1')
    time_dec_canvas.delete('time_dec')
    global time_min
    global time_sec10
    global time_sec1
    global time_dec
    if mi=='b':
        mi = '10'
    if sec10=='b':
        sec10 = '10'
    if sec1=='b':
        sec1 = '10'
    if dec=='b':
        dec = '10'
    time_min = time_digit_img[int(mi)].zoom(zoom_rate, zoom_rate)
    time_min_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=time_min, tag="time_min")
    time_sec10 = time_digit_img[int(sec10)].zoom(zoom_rate, zoom_rate)
    time_sec10_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=time_sec10, tag="time_sec10")
    time_sec1 = time_digit_img[int(sec1)].zoom(zoom_rate, zoom_rate)
    time_sec1_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=time_sec1, tag="time_sec1")
    time_dec = time_digit_img[int(dec)].zoom(zoom_rate, zoom_rate)
    time_dec_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=time_dec, tag="time_dec")

def fur4_disp(sec10 = 10, sec1 = 10, dec = 10):
    fur4_sec10_canvas.delete('fur4_sec10')
    fur4_sec1_canvas.delete('fur4_sec1')
    fur4_dec_canvas.delete('fur4_dec')
    global fur4_sec10
    global fur4_sec1
    global fur4_dec
    fur4_sec10 = time_digit_img[int(sec10)].zoom(zoom_rate, zoom_rate)
    fur4_sec10_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=fur4_sec10, tag="fur4_sec10")
    fur4_sec1 = time_digit_img[int(sec1)].zoom(zoom_rate, zoom_rate)
    fur4_sec1_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=fur4_sec1, tag="fur4_sec1")
    fur4_dec = time_digit_img[int(dec)].zoom(zoom_rate, zoom_rate)
    fur4_dec_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=fur4_dec, tag="fur4_dec")
    
def fur3_disp(sec10 = 10, sec1 = 10, dec = 10):
    fur3_sec10_canvas.delete('fur3_sec10')
    fur3_sec1_canvas.delete('fur3_sec1')
    fur3_dec_canvas.delete('fur3_dec')
    global fur3_sec10
    global fur3_sec1
    global fur3_dec
    fur3_sec10 = time_digit_img[int(sec10)].zoom(zoom_rate, zoom_rate)
    fur3_sec10_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=fur3_sec10, tag="fur3_sec10")
    fur3_sec1 = time_digit_img[int(sec1)].zoom(zoom_rate, zoom_rate)
    fur3_sec1_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=fur3_sec1, tag="fur3_sec1")
    fur3_dec = time_digit_img[int(dec)].zoom(zoom_rate, zoom_rate)
    fur3_dec_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=fur3_dec, tag="fur3_dec")
#---------------------------
def record_disp(rec='0'):
    global record
    global testing
    if int(rec) == 2:
        testing = True
    else:
        testing = False
    record_canvas.delete('record')
    record = record_img[int(rec)].zoom(zoom_rate, zoom_rate)
    record_canvas.create_image(record_wid / 2, (record_wid / 78)*13, image=record, tag="record")
##########################################
connection = 0

def serial_start():
    global connection
    global serial_thread
    if connection == 0:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(b"connect")#send_connection_start_request
    else:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(b"disconnect")#send_connection_start_request
    connection = 1 - connection
    
def serial_chk():
    global AfterBoot
    global signal_ext
    global after_serial
    global quit_flag
    global signal_before
    if AfterBoot:
        test_disp()
        time.sleep(1)
        window_init()
        AfterBoot = False
    while quit_flag != True:
        if ser.in_waiting > 0:
            incomming = ser.read_until('F'.encode('utf-8'))
            signal = incomming.strip().decode('utf-8')
            print(signal)
            if signal != signal_before:
                if signal[0] == 'S':
                    i = 1
                    signal_before = signal
                    while signal[i] != 'F':
                        signal_ext = ''
                        if signal[i] == 'L':#Racecourse Command
                            signal_ext = signal[i+1:]
                            if len(signal_ext.split(',')[0]) == 0:
                                racecourse_disp()
                                i += 2
                                break
                            racecourse_disp(str(signal_ext.split(',')[0]))
                            i += (len(signal_ext.split(',')[0]) + 2)
                        elif signal[i] == 'R':#Race Number Command
                            signal_ext = signal[i+1:]
                            if len(signal_ext.split(',')[0]) == 0:
                                race_disp()
                                break
                            race_disp(str(signal_ext.split(',')[0]))
                            i += (len(signal_ext.split(',')[0]) + 2)
                        elif signal[i] == 'K':#Conf. Command
                            signal_ext = signal[i+1:]
                            if len(signal_ext.split(',')[0]) == 0:
                                conf_disp()
                                break
                            conf_disp(str(signal_ext.split(',')[0]))
                            i += (len(signal_ext.split(',')[0]) + 2)
                        elif signal[i] == 'A':#1st. Command
                            signal_ext = signal[i+1:]
                            if len(signal_ext.split(',')[0]) == 0:
                                number1_disp()
                                i += 2
                                
                            elif len(signal_ext.split(',')[0]) == 1:
                                number1_disp('0' + str(signal_ext.split(',')[0]))
                                i += 3
                                
                            else:
                                number1_disp(str(signal_ext.split(',')[0]))
                                i += (len(signal_ext.split(',')[0]) + 2)
                        elif signal[i] == 'B':#2nd. Command
                            signal_ext = signal[i+1:]
                            if len(signal_ext.split(',')[0]) == 0:
                                number2_disp()
                                i += 2
                                
                            elif len(signal_ext.split(',')[0]) == 1:
                                number2_disp('0' + str(signal_ext.split(',')[0]))
                                i += 3
                                
                            else:
                                number2_disp(str(signal_ext.split(',')[0]))
                                i += (len(signal_ext.split(',')[0]) + 2)
                        elif signal[i] == 'C':#3rd. Command
                            signal_ext = signal[i+1:]
                            if len(signal_ext.split(',')[0]) == 0:
                                number3_disp()
                                i += 2
                               
                            elif len(signal_ext.split(',')[0]) == 1:
                                number3_disp('0' + str(signal_ext.split(',')[0]))
                                i += 3
                                
                            else:
                                number3_disp(str(signal_ext.split(',')[0]))
                                i += (len(signal_ext.split(',')[0]) + 2)
                        elif signal[i] == 'D':#4th. Command
                            signal_ext = signal[i+1:]
                            if len(signal_ext.split(',')[0]) == 0:
                                number4_disp()
                                i += 2
                                
                            elif len(signal_ext.split(',')[0]) == 1:
                                number4_disp('0' + str(signal_ext.split(',')[0]))
                                i += 3
                                
                            else:
                                number4_disp(str(signal_ext.split(',')[0]))
                                i += (len(signal_ext.split(',')[0]) + 2)
                        elif signal[i] == 'E':#5th. Command
                            signal_ext = signal[i+1:]
                            if len(signal_ext.split(',')[0]) == 0:
                                number5_disp()
                                i += 2
                                
                            elif len(signal_ext.split(',')[0]) == 1:
                                number5_disp('0' + str(signal_ext.split(',')[0]))
                                i += 3
                                
                            else:
                                number5_disp(str(signal_ext.split(',')[0]))
                                i += (len(signal_ext.split(',')[0]) + 2)
                        elif signal[i] == 'G':#1-2 Command
                            signal_ext = signal[i+1:]
                            if len(signal_ext.split(',')[0]) == 0:
                                distance1_disp()
                                i += 2
                                break
                            distance1_disp(str(signal_ext.split(',')[0]))
                            i += (len(signal_ext.split(',')[0]) + 2)
                        elif signal[i] == 'H':#2-3 Command
                            signal_ext = signal[i+1:]
                            if len(signal_ext.split(',')[0]) == 0:
                                distance2_disp()
                                i += 2
                                break
                            distance2_disp(str(signal_ext.split(',')[0]))
                            i += (len(signal_ext.split(',')[0]) + 2)
                        elif signal[i] == 'I':#3-4 Command
                            signal_ext = signal[i+1:]
                            if len(signal_ext.split(',')[0]) == 0:
                                distance3_disp()
                                i += 2
                                break
                            distance3_disp(str(signal_ext.split(',')[0]))
                            i += (len(signal_ext.split(',')[0]) + 2)
                        elif signal[i] == 'J':#4-5 Command
                            signal_ext = signal[i+1:]
                            if len(signal_ext.split(',')[0]) == 0:
                                distance4_disp()
                                i += 2
                                break
                            distance4_disp(str(signal_ext.split(',')[0]))
                            i += (len(signal_ext.split(',')[0]) + 2)
                        elif signal[i] == 'T':#TIME Command
                            signal_ext = signal[i+1:]
                            if len(signal_ext.split(',')[0]) == 0:
                                time_disp()
                                i += 2
                                break
                            time_disp((str(signal_ext.split(',')[0]))[0],(str(signal_ext.split(',')[0]))[1],(str(signal_ext.split(',')[0]))[2],(str(signal_ext.split(',')[0]))[3])
                            i += (len(signal_ext.split(',')[0]) + 2)
                        elif signal[i] == 'f':#4F Command
                            signal_ext = signal[i+1:]
                            if len(signal_ext.split(',')[0]) == 0:
                                fur4_disp()
                                i += 2
                                break
                            fur4_disp((str(signal_ext.split(',')[0]))[0],(str(signal_ext.split(',')[0]))[1],(str(signal_ext.split(',')[0]))[2])
                            i += (len(signal_ext.split(',')[0]) + 2)
                        elif signal[i] == 't':#3F Command
                            signal_ext = signal[i+1:]
                            if len(signal_ext.split(',')[0]) == 0:
                                fur3_disp()
                                i += 2
                                break
                            fur3_disp((str(signal_ext.split(',')[0]))[0],(str(signal_ext.split(',')[0]))[1],(str(signal_ext.split(',')[0]))[2])
                            i += (len(signal_ext.split(',')[0]) + 2)
                        elif signal[i] == 'r':#Record Command
                            signal_ext = signal[i+1:]
                            if len(signal_ext.split(',')[0]) == 0:
                                record_disp()
                                i += 2
                                break
                            record_disp((str(signal_ext.split(',')[0]))[0])
                            i += (len(signal_ext.split(',')[0]) + 2)
                        elif signal[i] == 's':#CourseStatus Command
                            signal_ext = signal[i+1:]
                            if len(signal_ext.split(',')[0]) == 0:
                                status_disp()
                                i += 2
                                break
                            status_disp((str(signal_ext.split(',')[0]))[0],(str(signal_ext.split(',')[0]))[1])
                            i += (len(signal_ext.split(',')[0]) + 2)
                    
                elif signal[0] == 'P':
                    os.system('sudo shutdown -h now')

root = tk.Tk()
root.attributes("-fullscreen", True)
root['bg']='#000000'

############Loadimg image data############
racecourse_img=[
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/keibajo/blank.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/keibajo/sapporo.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/keibajo/hakodate.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/keibajo/niigata.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/keibajo/fukushima.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/keibajo/tokyo.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/keibajo/nakayama.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/keibajo/chukyo.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/keibajo/kyoto.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/keibajo/hanshin.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/keibajo/kokura.png')
]

conf_img=[
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/kakutei/blank.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/kakutei/kakutei.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/kakutei/shingi.png')
]

arrival_img=[
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakujun/blank.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakujun/1.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakujun/2.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakujun/3.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakujun/4.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakujun/5.png')
]

number_img=[
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/umaban/0.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/umaban/1.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/umaban/2.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/umaban/3.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/umaban/4.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/umaban/5.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/umaban/6.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/umaban/7.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/umaban/8.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/umaban/9.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/umaban/blank.png')
]

distance_img=[
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/blank.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/douchaku.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/hana.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/atama.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/kubi.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/1_2.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/3_4.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/1.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/1-1_4.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/1-1_2.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/1-3_4.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/2.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/2-1_2.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/3.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/3-1_2.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/4.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/5.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/6.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/7.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/8.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/9.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/10.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/taisa.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/chakusa/shashin.png')
]

douchaku_line_img=[
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/etc/douchaku_line_blank.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/etc/douchaku_line.png')
]

race_img=[
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/race_number/blank.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/race_number/r1.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/race_number/r2.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/race_number/r3.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/race_number/r4.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/race_number/r5.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/race_number/r6.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/race_number/r7.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/race_number/r8.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/race_number/r9.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/race_number/r10.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/race_number/r11.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/race_number/r12.png')
]

status_img=[
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/baba/blank.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/baba/ryou.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/baba/yayaomo.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/baba/omo.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/baba/furyou.png')
]

time_digit_img=[
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/time_digit/0.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/time_digit/1.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/time_digit/2.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/time_digit/3.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/time_digit/4.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/time_digit/5.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/time_digit/6.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/time_digit/7.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/time_digit/8.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/time_digit/9.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/time_digit/blank.png')
]

record_img=[
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/record/blank.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/record/record.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/record/test.png'),
    tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/record/longines.png')
]

R_img = tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/etc/R.png')
shiba_img = tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/etc/shiba.png')
dirt_img = tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/etc/dirt.png')
time_img = tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/etc/time.png')
three_furlong_img = tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/etc/3F.png')
four_furlong_img = tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/etc/4F.png')
dot_img = tk.PhotoImage(file = '/home/pi/Desktop/turf_vision/etc/dot.png')
##########################################


############Setup all Canvas#############
y_offset = -30
racecourse_canvas = tk.Canvas(width=racecourse_wid, height=(racecourse_wid/24)*50, bg="#000000", highlightthickness=0)
racecourse_canvas.place(x =55, y = 50 + y_offset)

conf_canvas = tk.Canvas(width=conf_wid, height=(conf_wid/102)*50, bg="#151515", highlightthickness=0)
conf_canvas.place(x = 600, y = 70 + y_offset)

arrival1_canvas = tk.Canvas(width=arrival_wid, height=(arrival_wid/37)*37, bg="#000000", highlightthickness=0)
arrival1_canvas.place(x = 30, y = 280 + y_offset)
arrival2_canvas = tk.Canvas(width=arrival_wid, height=(arrival_wid/37)*37, bg="#000000", highlightthickness=0)
arrival2_canvas.place(x = 30, y = 468 + y_offset)
arrival3_canvas = tk.Canvas(width=arrival_wid, height=(arrival_wid/37)*37, bg="#000000", highlightthickness=0)
arrival3_canvas.place(x = 30, y = 656 + y_offset)
arrival4_canvas = tk.Canvas(width=arrival_wid, height=(arrival_wid/37)*37, bg="#000000", highlightthickness=0)
arrival4_canvas.place(x = 30, y = 844 + y_offset)
arrival5_canvas = tk.Canvas(width=arrival_wid, height=(arrival_wid/37)*37, bg="#000000", highlightthickness=0)
arrival5_canvas.place(x = 30, y = 1029 + y_offset)

number1_canvas = tk.Canvas(root, width=number_wid, height=(number_wid/76)*36, bg="#151515", highlightthickness=0)
number1_canvas.place(x = 240, y = 280 + y_offset)
number2_canvas = tk.Canvas(root, width=number_wid, height=(number_wid/76)*36, bg="#151515", highlightthickness=0)
number2_canvas.place(x = 240, y = 468 + y_offset)
number3_canvas = tk.Canvas(root, width=number_wid, height=(number_wid/76)*36, bg="#151515", highlightthickness=0)
number3_canvas.place(x = 240, y = 656 + y_offset)
number4_canvas = tk.Canvas(root, width=number_wid, height=(number_wid/76)*36, bg="#151515", highlightthickness=0)
number4_canvas.place(x = 240, y = 844 + y_offset)
number5_canvas = tk.Canvas(root, width=number_wid, height=(number_wid/76)*36, bg="#151515", highlightthickness=0)
number5_canvas.place(x = 240, y = 1029 + y_offset)

distance1_canvas = tk.Canvas(width=distance_wid, height=(distance_wid/52)*26, bg="#151515", highlightthickness=0)
distance1_canvas.place(x = 750, y = 385 + y_offset)
distance2_canvas = tk.Canvas(width=distance_wid, height=(distance_wid/52)*26, bg="#151515", highlightthickness=0)
distance2_canvas.place(x = 750, y = 580 + y_offset)
distance3_canvas = tk.Canvas(width=distance_wid, height=(distance_wid/52)*26, bg="#151515", highlightthickness=0)
distance3_canvas.place(x = 750, y = 765 + y_offset)
distance4_canvas = tk.Canvas(width=distance_wid, height=(distance_wid/52)*26, bg="#151515", highlightthickness=0)
distance4_canvas.place(x = 750, y = 960 + y_offset)

douchaku_line1_canvas = tk.Canvas(width=douchaku_line_wid, height=(douchaku_line_wid/22)*32, bg="#000000", highlightthickness=0)
douchaku_line1_canvas.place(x = 600, y = 375 + y_offset)
douchaku_line2_canvas = tk.Canvas(width=douchaku_line_wid, height=(douchaku_line_wid/22)*32, bg="#000000", highlightthickness=0)
douchaku_line2_canvas.place(x = 600, y = 570 + y_offset)
douchaku_line3_canvas = tk.Canvas(width=douchaku_line_wid, height=(douchaku_line_wid/22)*32, bg="#000000", highlightthickness=0)
douchaku_line3_canvas.place(x = 600, y = 755 + y_offset)
douchaku_line4_canvas = tk.Canvas(width=douchaku_line_wid, height=(douchaku_line_wid/22)*32, bg="#000000", highlightthickness=0)
douchaku_line4_canvas.place(x = 600, y = 950 + y_offset)

race_canvas = tk.Canvas(width = race_wid, height = race_wid, bg="#151515", highlightthickness=0)
race_canvas.place(x = 240, y = 105 + y_offset)

status_turf_canvas = tk.Canvas(width = status_wid, height = (status_wid/72)*34, bg="#151515", highlightthickness=0)
status_turf_canvas.place(x = 40, y = 1300 + y_offset)
status_dirt_canvas = tk.Canvas(width = status_wid, height = (status_wid/72)*34, bg="#151515", highlightthickness=0)
status_dirt_canvas.place(x = 40, y = 1600 + y_offset)

record_canvas = tk.Canvas(width = record_wid, height = (record_wid/78)*26, bg="#151515", highlightthickness=0)
record_canvas.place(x = 700, y = 1200 + y_offset)

time_min_canvas = tk.Canvas(width = time_digit_wid, height = (time_digit_wid/16)*25, bg="#151515", highlightthickness=0)
time_min_canvas.place(x = 690, y = 1345 + y_offset)
dot1_canvas = tk.Canvas(width = dot_wid, height = (dot_wid/4)*4, bg="#151515", highlightthickness=0)
dot1_canvas.place(x = 764, y = 1430 + y_offset)
time_sec10_canvas = tk.Canvas(width = time_digit_wid, height = (time_digit_wid/16)*25, bg="#151515", highlightthickness=0)
time_sec10_canvas.place(x = 790, y = 1345 + y_offset)
time_sec1_canvas = tk.Canvas(width = time_digit_wid, height = (time_digit_wid/16)*25, bg="#151515", highlightthickness=0)
time_sec1_canvas.place(x = 860, y = 1345 + y_offset)
dot2_canvas = tk.Canvas(width = dot_wid, height = (dot_wid/4)*4, bg="#151515", highlightthickness=0)
dot2_canvas.place(x = 934, y = 1430 + y_offset)
time_dec_canvas = tk.Canvas(width = time_digit_wid, height = (time_digit_wid/16)*25, bg="#151515", highlightthickness=0)
time_dec_canvas.place(x = 960, y = 1345 + y_offset)

fur4_sec10_canvas = tk.Canvas(width = time_digit_wid, height = (time_digit_wid/16)*25, bg="#151515", highlightthickness=0)
fur4_sec10_canvas.place(x = 790, y = 1490 + y_offset)
fur4_sec1_canvas = tk.Canvas(width = time_digit_wid, height = (time_digit_wid/16)*25, bg="#151515", highlightthickness=0)
fur4_sec1_canvas.place(x = 860, y = 1490 + y_offset)
dot3_canvas = tk.Canvas(width = dot_wid, height = (dot_wid/4)*4, bg="#151515", highlightthickness=0)
dot3_canvas.place(x = 934, y = 1575 + y_offset)
fur4_dec_canvas = tk.Canvas(width = time_digit_wid, height = (time_digit_wid/16)*25, bg="#151515", highlightthickness=0)
fur4_dec_canvas.place(x = 960, y = 1490 + y_offset)

fur3_sec10_canvas = tk.Canvas(width = time_digit_wid, height = (time_digit_wid/16)*25, bg="#151515", highlightthickness=0)
fur3_sec10_canvas.place(x = 790, y = 1635 + y_offset)
fur3_sec1_canvas = tk.Canvas(width = time_digit_wid, height = (time_digit_wid/16)*25, bg="#151515", highlightthickness=0)
fur3_sec1_canvas.place(x = 860, y = 1635 + y_offset)
dot4_canvas = tk.Canvas(width = dot_wid, height = (dot_wid/4)*4, bg="#151515", highlightthickness=0)
dot4_canvas.place(x = 934, y = 1720 + y_offset)
fur3_dec_canvas = tk.Canvas(width = time_digit_wid, height = (time_digit_wid/16)*25, bg="#151515", highlightthickness=0)
fur3_dec_canvas.place(x = 960, y = 1635 + y_offset)

R_canvas = tk.Canvas(width = 18*zoom_rate, height = 18*zoom_rate, bg="#000000", highlightthickness=0)
R_canvas.place(x = 390, y = 140 + y_offset)
shiba_canvas = tk.Canvas(width = 19*zoom_rate, height = 20*zoom_rate, bg="#000000", highlightthickness=0)
shiba_canvas.place(x = 150, y = 1200 + y_offset)
dirt_canvas = tk.Canvas(width = 64*zoom_rate, height = 20*zoom_rate, bg="#000000", highlightthickness=0)
dirt_canvas.place(x = 58, y = 1500 + y_offset)
time_canvas = tk.Canvas(width = time_wid, height = (time_wid/52)*17, bg="#000000", highlightthickness=0)
time_canvas.place(x = 425, y = 1365 + y_offset)
four_furlong_canvas = tk.Canvas(width = furlong_wid, height = (furlong_wid/30)*14, bg="#000000", highlightthickness=0)
four_furlong_canvas.place(x = 500, y = 1515 + y_offset)
three_furlong_canvas = tk.Canvas(width = furlong_wid, height = (furlong_wid/30)*14, bg="#000000", highlightthickness=0)
three_furlong_canvas.place(x = 500, y = 1665 + y_offset)
########################################


###############initialize###############
racecourse = racecourse_img[racecourse_index].zoom(zoom_rate, zoom_rate)
racecourse_canvas.create_image(racecourse_wid / 2, (racecourse_wid / 24)*25, image=racecourse, tag="racecourse")
Race = R_img.zoom(zoom_rate, zoom_rate)
R_canvas.create_image(36, 36, image=Race, tag="R")
shiba = shiba_img.zoom(zoom_rate, zoom_rate)
shiba_canvas.create_image(38, 40, image=shiba, tag="shiba")
record = record_img[record_index].zoom(zoom_rate, zoom_rate)
record_canvas.create_image(record_wid / 2, (record_wid / 78)*13, image=record, tag="record")
time_text = time_img.zoom(zoom_rate, zoom_rate)
time_canvas.create_image(time_wid / 2, (time_wid / 52)*8.5, image=time_text, tag="time_text")
four_furlong = four_furlong_img.zoom(zoom_rate, zoom_rate)
four_furlong_canvas.create_image(furlong_wid / 2, (furlong_wid / 30)*7, image=four_furlong, tag="four_furlong")
three_furlong = three_furlong_img.zoom(zoom_rate, zoom_rate)
three_furlong_canvas.create_image(furlong_wid / 2, (furlong_wid / 30)*7, image=three_furlong, tag="three_furlong")
time_min = time_digit_img[time_min_index].zoom(zoom_rate, zoom_rate)
time_min_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=time_min, tag="time_min")
time_sec10 = time_digit_img[time_sec10_index].zoom(zoom_rate, zoom_rate)
time_sec10_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=time_sec10, tag="time_sec10")
time_sec1 = time_digit_img[time_sec1_index].zoom(zoom_rate, zoom_rate)
time_sec1_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=time_sec1, tag="time_sec1")
time_dec = time_digit_img[time_dec_index].zoom(zoom_rate, zoom_rate)
time_dec_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=time_dec, tag="time_dec")
fur4_sec10 = time_digit_img[fur4_sec10_index].zoom(zoom_rate, zoom_rate)
fur4_sec10_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=fur4_sec10, tag="fur4_sec10")
fur4_sec1 = time_digit_img[fur4_sec1_index].zoom(zoom_rate, zoom_rate)
fur4_sec1_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=fur4_sec1, tag="fur4_sec1")
fur4_dec = time_digit_img[fur4_dec_index].zoom(zoom_rate, zoom_rate)
fur4_dec_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=fur4_dec, tag="fur4_dec")
fur3_sec10 = time_digit_img[fur3_sec10_index].zoom(zoom_rate, zoom_rate)
fur3_sec10_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=fur3_sec10, tag="fur3_sec10")
fur3_sec1 = time_digit_img[fur3_sec1_index].zoom(zoom_rate, zoom_rate)
fur3_sec1_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=fur3_sec1, tag="fur3_sec1")
fur3_dec = time_digit_img[fur3_dec_index].zoom(zoom_rate, zoom_rate)
fur3_dec_canvas.create_image(time_digit_wid / 2, (time_digit_wid / 16)*12.5, image=fur3_dec, tag="fur3_dec")
dot1 = dot_img.zoom(zoom_rate, zoom_rate)
dot1_canvas.create_image(dot_wid / 2, (dot_wid / 4)*2, image=dot1, tag="dot1")
dot2 = dot_img.zoom(zoom_rate, zoom_rate)
dot2_canvas.create_image(dot_wid / 2, (dot_wid / 4)*2, image=dot2, tag="dot2")
dot3 = dot_img.zoom(zoom_rate, zoom_rate)
dot3_canvas.create_image(dot_wid / 2, (dot_wid / 4)*2, image=dot3, tag="dot3")
dot4 = dot_img.zoom(zoom_rate, zoom_rate)
dot4_canvas.create_image(dot_wid / 2, (dot_wid / 4)*2, image=dot4, tag="dot4")

status_turf = status_img[status_turf_index].zoom(zoom_rate, zoom_rate)
status_turf_canvas.create_image(status_wid / 2, (status_wid /72) * 17, image=status_turf, tag="status_turf")
status_dirt = status_img[status_dirt_index].zoom(zoom_rate, zoom_rate)
status_dirt_canvas.create_image(status_wid / 2, (status_wid /72) * 17, image=status_dirt, tag="status_dirt")
dirt = dirt_img.zoom(zoom_rate, zoom_rate)
dirt_canvas.create_image(128, 40, image=dirt, tag="dirt")
race = race_img[race_index].zoom(zoom_rate, zoom_rate)
race_canvas.create_image(race_wid / 2, (race_wid / 34)*17, image=race, tag="race")
arrival1 = arrival_img[arrival1_index].zoom(zoom_rate, zoom_rate)
arrival1_canvas.create_image(arrival_wid / 2, (arrival_wid /37) * 18.5, image=arrival1, tag="arrival1")
arrival2 = arrival_img[arrival2_index].zoom(zoom_rate, zoom_rate)
arrival2_canvas.create_image(arrival_wid / 2, (arrival_wid /37) * 18.5, image=arrival2, tag="arrival2")
arrival3 = arrival_img[arrival3_index].zoom(zoom_rate, zoom_rate)
arrival3_canvas.create_image(arrival_wid / 2, (arrival_wid /37) * 18.5, image=arrival3, tag="arrival3")
arrival4 = arrival_img[arrival4_index].zoom(zoom_rate, zoom_rate)
arrival4_canvas.create_image(arrival_wid / 2, (arrival_wid /37) * 18.5, image=arrival4, tag="arrival4")
arrival5 = arrival_img[arrival5_index].zoom(zoom_rate, zoom_rate)
arrival5_canvas.create_image(arrival_wid / 2, (arrival_wid /37) * 18.5, image=arrival5, tag="arrival5")
conf = conf_img[conf_index].zoom(zoom_rate, zoom_rate)
conf_canvas.create_image(conf_wid / 2, (conf_wid /102) * 25, image=conf, tag="conf")
number1_10_img = number_img[number10_index].zoom(zoom_rate, zoom_rate)
number1_1_img = number_img[number1_index].zoom(zoom_rate, zoom_rate)
number1_canvas.create_image(76, (number_wid / 76) * 18, image=number1_10_img, tag="number1_10")
number1_canvas.create_image(228, (number_wid / 76) * 18, image=number1_1_img, tag="number1_1")
number2_10_img = number_img[number10_index].zoom(zoom_rate, zoom_rate)
number2_1_img = number_img[number1_index].zoom(zoom_rate, zoom_rate)
number2_canvas.create_image(76, (number_wid / 76) * 18, image=number2_10_img, tag="number2_10")
number2_canvas.create_image(228, (number_wid / 76) * 18, image=number2_1_img, tag="number2_1")
number3_10_img = number_img[number10_index].zoom(zoom_rate, zoom_rate)
number3_1_img = number_img[number1_index].zoom(zoom_rate, zoom_rate)
number3_canvas.create_image(76, (number_wid / 76) * 18, image=number3_10_img, tag="number3_10")
number3_canvas.create_image(228, (number_wid / 76) * 18, image=number3_1_img, tag="number3_1")
number4_10_img = number_img[number10_index].zoom(zoom_rate, zoom_rate)
number4_1_img = number_img[number1_index].zoom(zoom_rate, zoom_rate)
number4_canvas.create_image(76, (number_wid / 76) * 18, image=number4_10_img, tag="number4_10")
number4_canvas.create_image(228, (number_wid / 76) * 18, image=number4_1_img, tag="number4_1")
number5_10_img = number_img[number10_index].zoom(zoom_rate, zoom_rate)
number5_1_img = number_img[number1_index].zoom(zoom_rate, zoom_rate)
number5_canvas.create_image(76, (number_wid / 76) * 18, image=number5_10_img, tag="number5_10")
number5_canvas.create_image(228, (number_wid / 76) * 18, image=number5_1_img, tag="number5_1")
distance1 = distance_img[distance1_index].zoom(zoom_rate, zoom_rate)
distance1_canvas.create_image(distance_wid / 2, (distance_wid / 52) * 13, image=distance1, tag="distance1")
distance2 = distance_img[distance2_index].zoom(zoom_rate, zoom_rate)
distance2_canvas.create_image(distance_wid / 2, (distance_wid / 52) * 13, image=distance2, tag="distance2")
distance3 = distance_img[distance3_index].zoom(zoom_rate, zoom_rate)
distance3_canvas.create_image(distance_wid / 2, (distance_wid / 52) * 13, image=distance3, tag="distance3")
distance4 = distance_img[distance4_index].zoom(zoom_rate, zoom_rate)
distance4_canvas.create_image(distance_wid / 2, (distance_wid / 52) * 13, image=distance4, tag="distance4")
douchaku_line1 = douchaku_line_img[douchaku_line1_index].zoom(zoom_rate, zoom_rate)
douchaku_line1_canvas.create_image(douchaku_line_wid / 2, (distance_wid / 22) * 6.75, image=douchaku_line1, tag="douchaku_line1")
douchaku_line2 = douchaku_line_img[douchaku_line2_index].zoom(zoom_rate, zoom_rate)
douchaku_line2_canvas.create_image(douchaku_line_wid / 2, (distance_wid / 22) * 6.75, image=douchaku_line2, tag="douchaku_line2")
douchaku_line3 = douchaku_line_img[douchaku_line3_index].zoom(zoom_rate, zoom_rate)
douchaku_line3_canvas.create_image(douchaku_line_wid / 2, (distance_wid / 22) * 6.75, image=douchaku_line3, tag="douchaku_line3")
douchaku_line4 = douchaku_line_img[douchaku_line4_index].zoom(zoom_rate, zoom_rate)
douchaku_line4_canvas.create_image(douchaku_line_wid / 2, (distance_wid / 22) * 6.75, image=douchaku_line4, tag="douchaku_line4")

########################################

serial_thread = threading.Thread(target = serial_chk, daemon = True)
serial_thread.start()

del_btn=tk.Button(text='disp',command=test_disp, bg="#c0ffee")
del_btn.place(x=720, y=1800)

del_btn=tk.Button(text='init',command=window_init, bg="#c0ffee")
del_btn.place(x=600, y=1800)

blink_btn=tk.Button(text='serial',command=serial_start, bg="#c0ffee")
blink_btn.place(x=500, y=1800)

exit_btn=tk.Button(text='Exit',command=win_close, bg="#c0ffee")
exit_btn.place(x=360, y=1800)

root.mainloop()