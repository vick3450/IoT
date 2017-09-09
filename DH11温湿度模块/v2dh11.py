#!/usr/bin/python
#coding=utf-8
#ע�Ȿ������python3������
import RPi.GPIO as GPIO
import time
from ctypes import *
import os

#���ʱ������
data = [0 for i in range(40)]

def driver():
        pin = 24	
        # �������ϵ��Ҫ�ȴ�1s��Խ�����ȶ�״̬
        GPIO.setmode(GPIO.BCM)
        time.sleep(1)
        # ���򴫸������Ϳ�ʼ�źţ�����-LOW-
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        # �������������ͱ������18���룬�������20����
        time.sleep(0.02)
        # Ȼ���������߲���ʱ�ȴ�����������Ӧ
        GPIO.output(pin, GPIO.HIGH)
        # ִ��1����Ҫʮ��΢��
        # �ȴ���������������Ӧ�źź������ź�
        GPIO.setup(pin, GPIO.IN)
        while GPIO.input(pin) == 0:
                continue
        # ����Ϊ�͵�ƽ��˵��������������Ӧ�źţ�80us�͵�ƽ
        while GPIO.input(pin) == 1:
                continue
        # Ȼ�󴫸����ٰ���������80us��Ȼ���׼����������
        # ��ʼ��������
        # һ������������Ϊ40bit����λ�ȳ�
        # 8bitʪ����������+8bitʪ��С������+8bit�¶���������+8bit�¶�С������+8bitУ���
        j = 0
        while j < 40:
                k = 0
                #ÿһλ����ʼ�źţ�����50us�͵�ƽ��ʼ
                while GPIO.input(pin) == 0:
                        continue
                #ÿһλ����ֵ�źţ��ߵ�ƽ�ĳ��̾���������λ��0����1��
                while GPIO.input(pin) == 1:
                        #��Ҫ֪��ÿ��ѭ���ĺ�ʱ������֪��k < x�Ǳ�ʾ0
                        k += 1
                        if k > 100:
                                break
                # �ߵ�ƽ����26-28us��ʾ0�� �ߵ�ƽ����70us��ʾ1
                if k < 17:
                        data[j] = 0
                else:
                        data[j] = 1
                j += 1
        print "Raw data Vick2:\n", data
#2������ʪ�ȡ��¶ȡ�У���
#����ÿ8λת����һ��ʮ��������
def compute():
        humidity_bit = data[0:8]
        humidity_point_bit = data[8:16]
        temperature_bit = data[16:24]
        temperature_point_bit = data[24:32]
        check_bit = data[32:40]
        humidity = 0
        humidity_point = 0
        temperature = 0
        temperature_point = 0
        check = 0
        for i in range(8):
               # ʪ����������
                humidity += humidity_bit[i] * 2**(7-i)
                humidity_point += humidity_point_bit[i] * 2**(7-i)
               # �¶���������
                temperature += temperature_bit[i] * 2**(7-i)
                temperature_point += temperature_point_bit[i] * 2**(7-i)
                check += check_bit[i] * 2**(7-i)
        sum = humidity + humidity_point + temperature + temperature_point
        if check == sum:
                print("temperature:", temperature, ", humidity:", humidity)
        else:
                print("wrong!", check, "!=",  sum)

#��ģ�鱻ֱ������ʱ�����´���齫�����У���ģ���Ǳ�����ʱ������鲻������
if __name__ == "__main__":
        driver()
        compute()
        GPIO.cleanup()