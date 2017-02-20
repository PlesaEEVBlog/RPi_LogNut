# xDevs.com Calibration app for Keithley 2400, v0.3
# https://xdevs.com/fix/kei2400
# https://xdevs.com/fix/hp3458a
import sys
import time
import Gpib
import signal
import numbers
from math import log10

dmm_val = 1.0
dmm_temp = 36.6

class Timeout():
  """Timeout class using ALARM signal"""
  class Timeout(Exception): pass

  def __init__(self, sec):
    self.sec = sec

  def __enter__(self):
    signal.signal(signal.SIGALRM, self.raise_timeout)
    signal.alarm(self.sec)

  def __exit__(self, *args):
    signal.alarm(0) # disable alarm

  def raise_timeout(self, *args):
    raise Timeout.Timeout()

class dmm():
    global dmm_val 
    data = ""
    temp = 36.6
    cnti = 12
    
    def __init__(self,gpib,refhp,name):
        self.gpib = gpib
        self.inst = Gpib.Gpib(0,self.gpib, timeout=60) # 3458A GPIB Address = self.gpib
        self.refhp = refhp
        self.name = name
        self.init_inst()

    def init_inst(self):
        # Setup HP 3458A
        self.inst.write ("PRESET NORM")
        self.inst.write ("OFORMAT ASCII")
        self.inst.write ("FUNC DCV,AUTO")
        self.inst.write ("TARM HOLD")
        self.inst.write ("TRIG LINE")
        self.inst.write ("NPLC 50")
        self.inst.write ("AZERO ON")
        self.inst.write ("NRDGS 1,AUTO")
        self.inst.write ("MEM OFF")
        self.inst.write ("END ALWAYS")
        self.inst.write ("NDIG 9")

    def switch_dci(self):
        self.inst.write ("PRESET NORM")
        self.inst.write ("NPLC 50")
        self.inst.write ("AZERO ON")
        self.inst.write ("NRDGS 1,AUTO")
        self.inst.write ("OFORMAT ASCII")
        self.inst.write ("FUNC DCI,AUTO")
        self.inst.write ("NDIG 9")
        
    def read_data(self,cmd):
        data_float = 0.0
        data_str = ""
        self.inst.write(cmd)
        
        try:
            with Timeout(20):
                data_str = self.inst.read()
        except Timeout.Timeout:
            print ("Timeout exception from dmm %s on read_data() inst.read()\n" % self.name)
            return (0,float(0))
        #print ("Reading from dmm %s = %s" % (self.name,data_str))
        try:
            data_float = float(data_str)
        except ValueError:
            print("Exception thrown by dmm %s on read_data() - ValueError = %s\n" % (self.name,data_str))
            return (0,float(0)) # Exception on float conversion, 0 = error
        return (1,data_float) # Good read, 1 = converted to float w/o exception
        
    def get_temp(self):
        global dmm_temp
        print("Reading DMM temp")
        self.inst.write("TARM SGL,1")
        self.temp_status_flag,temp = self.read_data("TEMP?")
        if (self.temp_status_flag):
            self.temp = temp
        dmm_temp = 37.5
        return self.temp
        
    def get_temp_status(self):
        return self.temp_status_flag

    def get_data(self):
        global dmm_val
        self.status_flag,data = self.read_data("TARM SGL,1")
        if (self.status_flag):
            self.data = data
            dmm_val = float(data)
            self.ppm = ((float(self.data) / self.refhp)-1)*1E6
        return self.data
        
    def exec_acal(self):
        sys.stdout.write ("\033[1;35mACAL ALL procedure start, please wait 12 minutes ")
        self.inst.write("ACAL ALL")
        for cnt in range(0 ,48):        # wait 720 seconds, print dot every 15s
            sys.stdout.write ("\033[0;43m*")
            time.sleep(15)
        print("\r\nACAL procedure done...\033[1;39m")
    
    def exec_idn(self):
        self.inst.write ("END ALWAYS")
        self.inst.write ("ID?")
        dat = self.inst.read()
        tstr = dat.split()
        if (tstr[0] == "HP3458A"):
            sys.stdout.write ("\r\n\033[1;32m%s detected...\033[1;39m" % tstr[0])
        else:
            sys.stdout.write ("\r\n\033[1;31mNo DMM present, exiting!\033[1;39m")
            quit()

    def get_data_status(self):
        return self.status_flag

with open('callog_ver.txt','wb') as b:
    kei2400 = Gpib.Gpib(0,24)               # Keithley Model 2400 GPIB address init 24
    kei2400.clear()

    cal_dcv_set = [-0.2, 0, 0.2, 0, -2, 0, 2, 0, -20, 0, 20, 0, -200, 0, 200, 0]
    cal_dcv_rng = [0.2, 0.2, 0.2, 0.2, 2, 2, 2, 2, 20, 20, 20, 20, 200, 200, 200, 200]
    cal_dcv_str = ["-0.2 m"," -Zero"," 0.2 m"," +Zero","   -2 "," -Zero","    2 "," -Zero","  -20 "," +Zero","   20 "," -Zero"," -200 "," +Zero","  200 "," +Zero"]
    cal_dci_set = [-1E-6, 0, 1E-6, 0, -10E-6, 0, 10E-6, 0, -100E-6, 0, 100E-6, 0, -1E-3, 0, 1E-3, 0, -10E-3, 0, 10E-3, 0, -100E-3, 0, 100E-3, 0, -1, 0, 1, 0]
    cal_dci_rng = [1E-6, 1E-6, 1E-6, 1E-6, 10E-6, 10E-6, 10E-6, 10E-6, 100E-6, 100E-6, 100E-6, 100E-6, 1E-3, 1E-3, 1E-3, 1E-3, 10E-3, 10E-3, 10E-3, 10E-3, 100E-3, 100E-3, 100E-3, 100E-3, 1, 1, 1, 1]
    cal_dci_str = ["-1 u","-Zero", " 1 u", "+Zero", " -10 u", "-Zero", " 10 u", "+Zero", "-100 u", "-Zero", " 100 u", "+Zero", "-1 m", "-Zero", " 1 m", "+Zero", " -10 m", "-Zero", " 10 m", "+Zero", "-100 m", "-Zero", " 100 m", "+Zero", " -1 ", "-Zero", " 1 ", "+Zero"]
    test_dcv_set = [0, -0.002, 0.002, -0.02, 0.02, -0.2, 0.2, -1, 1, -2, 2, -10, 10, -15, 15, -20, 20, -100, 100, -200, 200, 0]
    test_dcv_rng = [0.2,  0.2,   0.2,   0.2,  0.2,  0.2, 0.2,  2, 2, 20,20,  20, 20,  20, 20,  20, 20, 200, 200, 200, 200, 20]
    test_dci_set = [0, -1E-9, 1E-9, -10E-9, 10E-9, -100E-9, 100E-9, -1E-6, 1E-6, -10E-6, 10E-6, -100E-6, 100E-6, -1E-3, 1E-3, -4E-3, 4E-3, -10E-3, 10E-3, -20E-3, 20E-3, -100E-3, 100E-3, -500E-3, 500E-3, 1, -1, 0]
    test_dci_rng = [1E-6, 1E-6, 1E-6, 1E-6, 1E-6, 1E-6,  1E-6, 1E-6, 1E-6, 10E-6, 10E-6, 100E-6, 100E-6, 1E-3, 1E-3, 10E-3, 10E-3, 10E-3, 10E-3, 100E-3, 100E-3, 100E-3, 100E-3, 1, 1, 1, 1, 1E-3]
    test_dci_str = ["Zero  ","  -1 n", "   1 n", " -10 n", "  10 n", "-100 n", " 100 n", "  -1 u", "   1 u", " -10 u", "  10 u", "-100 u", " 100 u", "  -1 m", "   1 m", "  -4 m", "   4 m", " -10 m", "  10 m", " -20 m", "  20 m", "-100 m", " 100 m", "-500 m", " 500 m", "  -1  ", "   1  ", "Zero  "]
    kei2400_idn = "KEITHLEY INSTRUMENTS INC."
    kei2400_mdl = "MODEL 2400"
    orig_val = []
    kei_error = 0
    plc = 60 #60 Hz
    cnt = 0
    samples = 0
    nplc = 0
    val = 3.423
    meas = 0.0
    temp = 36.6
    
    for cnt in range(30):
        orig_val.append(0)
        
    sys.stdout.write("\033[0;36m Keithley 2400 calibration tool \r\n  Using NI GPIB adapter with next instruments config: \r\n * GPIB 24 : Keithley 2400 SMU \r\n * GPIB 3 : HP 3458A 8.5-digit DMM \r\n ! Do not swap terminals during calibration, high voltage may be present !\033[0;39m\r\n\r\n")
    
    kei2400.write ("*IDN?")
    idn_str = kei2400.read()
    idmfg = idn_str.split(",")
    if (kei2400_idn == idmfg[0]):
        if (kei2400_mdl == idmfg[1]):
            sys.stdout.write("\033[0;32mKeithley Model 2400 - detected, S/N %s, Version: %s\033[0;39m\r\n" % (idmfg[2], idmfg[3]))
            b.write("\r\nKeithley Model 2400 - detected, S/N %s, Version: %s\r\n" % (idmfg[2], idmfg[3]))
        else:
            print ("\033[0;31mIncorrect Model! Check GPIB address. Calibration cancelled.\033[0;39m")    
            quit()
    else:
        sys.stdout.write ("\033[0;31mNo Keithley instrument detected. Check GPIB address. Calibration cancelled.\033[0;39m")
        quit()
    
    # Keithley Model 2400 detected OK, proceed with reading CAL data
    
    kei2400.write ("*CLS")
    kei2400.write ("*ESE 1;*SRE 32")
    kei2400.write ("*RST")
    kei2400.write (":SENS:FUNC:CONC OFF")
    kei2400.write (":SENS:FUNC 'VOLT:DC'")
    kei2400.write (":SOUR:FUNC VOLT")
    kei2400.write (":OUTP:STAT OFF")
    
    print "Reading Pre-cal calibration data from Model 2400"
    b.write("Pre-cal K2400 Calibration data\r\n")
    
    for cnt in range (0, 4):
        kei2400.write (":SOUR:VOLT:RANGE %3.1f" % cal_dcv_rng[cnt*4])
        kei2400.write (":CAL:PROT:SENS:DATA?")
        kdata = kei2400.read()
        sys.stdout.write ("%s" % kdata)
        b.write("%3.1f DCV Range, SENS:DATA? = %s\r\n" % (cal_dcv_rng[cnt*4], kdata))
        kei2400.write (":CAL:PROT:SOUR:DATA?")
        kdata = kei2400.read()
        sys.stdout.write ("%s" % kdata)
        b.write("%3.1f DCV Range, SOUR:DATA? = %s\r\n" % (cal_dcv_rng[cnt*4], kdata))
        cnt = cnt + 1
    
    kei2400.write (":CAL:PROT:LOCK")
    kei2400.write (":SENS:FUNC 'CURR:DC'")
    kei2400.write (":SOUR:FUNC CURR")
    kei2400.write (":CAL:PROT:CODE 'KI002400'")
    
    for cnt in range (0, 7):
        kei2400.write (":SOUR:CURR:RANGE %3.1e" % cal_dci_rng[cnt*4])
        kei2400.write (":CAL:PROT:SENS:DATA?")
        kdata = kei2400.read()
        sys.stdout.write ("%s" % kdata)
        b.write("%3.1e DCI Range, SENS:DATA? = %s\r\n" % (cal_dci_rng[cnt*4], kdata))
        kei2400.write (":CAL:PROT:SOUR:DATA?")
        kdata = kei2400.read()
        b.write("%3.1e DCI Range, SOUR:DATA? = %s\r\n" % (cal_dci_rng[cnt*4], kdata))
        sys.stdout.write ("%s" % kdata)
        cnt = cnt + 1

    # K2400 data read OK. Detect HP 3458A DMM on GPIB 3
        
    dmm = dmm(3,dmm_val,"3458A") # GPIB 3
    dmm.exec_idn()
    dmm.get_temp()
    print ("\033[0;33mHP3458A TEMP = %2.1f C\033[0;33m" % dmm_temp)
    b.write ("HP 3458A detected\r\n TEMP? = %2.1f C\r\n" % dmm_temp)
    kei2400.write (":SYST:BEEP:IMM 800, 5")
    kei2400.write (":SYST:BEEP:IMM 1400, 3")
    kei2400.write (":SYST:BEEP:IMM 2200, 2")
    kei2400.write (":SYST:BEEP:IMM 3000, 1")
    print ("\033[1;31mConnect DMM volts input to Model 2400 INPUT/OUTPUT jacks.\033[1;39m")
    raw_input("\033[1;33mPress Enter to continue with calibration...\033[1;39m")
    
    dmm.exec_acal()         # Execute ACAL on HP 3458A for best accuracy. Takes 12 minutes to complete.
    
    kei2400.write ("*RST")
    kei2400.write (":SOUR:FUNC VOLT")
    kei2400.write (":SENS:CURR:PROT 0.1")
    kei2400.write (":SENS:CURR:RANG 0.1")
    kei2400.write (":SOUR:VOLT:PROT:LEV MAX")
    kei2400.write (":SYST:RSEN OFF")
    kei2400.write (":CAL:PROT:CODE 'KI002400'")
    kei2400.write (":OUTP:STAT ON")
    
    sys.stdout.write("Starting DCV calibration...\r\n\r\n")
    
    for cnt in range (0, len(cal_dcv_set)):
        #sys.stdout.write(" Calibration step %d " % cnt)
        
        kei2400.write (":SOUR:VOLT:RANGE %3.1f" % cal_dcv_rng[cnt])
        kei2400.write (":SOUR:VOLT %3.1f" % cal_dcv_set[cnt])
        
        val = 0 
        time.sleep(1)
        for samples in range (0, 10):
            dmm.get_data()
            print ("Measured DCV %d : %.9E VDC" % (samples, dmm_val))
            val += dmm_val
        val = val / 10
        
        orig_val[cnt] = val
        sys.stdout.write("DCV Calibration step %sV : %.9E VDC" % (cal_dcv_str[cnt], val))
        
        kei2400.write (":CAL:PROT:SOUR %3.8f;*OPC" % val)
        time.sleep(1)
        kei2400.write (":SYST:ERR?")
        kei_error = kei2400.read().split(",")
        if (int(kei_error[0]) != 0):
            print "\033[1;31mKeithley 2400 error : %d\033[1;39m" % int(kei_error[0])
            quit()
        #kei2400.write ("*STB?")
        #kei2400.write ("*ESR?")
        
        kei2400.write (":CAL:PROT:SENS %3.8f;*OPC" % val)
        time.sleep(1)
        kei2400.write (":SYST:ERR?")
        kei_error = kei2400.read().split(",")
        if (int(kei_error[0]) != 0):
            print "\033[1;31mKeithley 2400 error : %d\033[1;39m" % int(kei_error[0])
            quit()
        #kei2400.write ("*STB?")
        #kei2400.write ("*ESR?")
        
        if (cnt % 2 == 0):
            ppms = ((val / (cal_dcv_set[cnt] + 1E-16)) - 1) * 1E6
            sys.stdout.write("\033[1;35m Delta: %.3f ppm\033[1;39m\r\n" % ppms)
            b.write("DCV Calibration step %sV , measured : %.9E VDC, deviation %.3f ppm\r\n" % (cal_dcv_str[cnt], val, ppms))
        else:
            sys.stdout.write("\r\n")
        cnt = cnt + 1
  
    sys.stdout.write("\r\n")
    sys.stdout.write("\033[0;31;43mConnect DMM CURRENT input to 2400 INPUT/OUTPUT jacks.\033[0;39;49m\r\n")
    
    kei2400.write (":SYST:BEEP:IMM 1000, 5")
    raw_input("Press Enter to continue...")
    
    sys.stdout.write("Starting DCI calibration...\r\n\r\n")
    
    dmm.switch_dci()

    kei2400.write (":SOUR:FUNC CURR")
    kei2400.write (":SENS:VOLT:PROT 20")
    kei2400.write (":SENS:VOLT:RANG 20")
    kei2400.write (":OUTP:STAT ON")
    
    for cnt in range (0, len(cal_dci_set)):
        
        kei2400.write (":SOUR:CURR:RANGE %3.1e" % cal_dci_rng[cnt])
        kei2400.write (":SOUR:CURR %3.1e" % cal_dci_set[cnt])
        
        val = 0 
        time.sleep(1)
        for samples in range (0, 10):
            dmm.get_data()
            print ("Measured DCI %d : %.9E ADC" % (samples, dmm_val))
            val += dmm_val
        val = val / 10

        sys.stdout.write("DCI Calibration step %sA : %.9E ADC" % (cal_dci_str[cnt], val))
        
        kei2400.write (":CAL:PROT:SOUR %3.8e;*OPC" % val)
        time.sleep(1)
        kei2400.write (":SYST:ERR?")
        kei_error = kei2400.read().split(",")
        if (int(kei_error[0]) != 0):
            print "\033[1;31mKeithley 2400 error : %d\033[1;39m" % int(kei_error[0])
            quit()
        #kei2400.write ("*STB?")
        #kei2400.write ("*ESR?")
        
        kei2400.write (":CAL:PROT:SENS %3.8e;*OPC" % val)
        time.sleep(1)
        kei2400.write (":SYST:ERR?")
        kei_error = kei2400.read().split(",")
        if (int(kei_error[0]) != 0):
            print "\033[1;31mKeithley 2400 error : %d\033[1;39m" % int(kei_error[0])
            quit()
        #kei2400.write ("*STB?")
        #kei2400.write ("*ESR?")
        
        if (cnt % 2 == 0):
            ppms = ((val / (cal_dci_set[cnt] + 1E-16)) - 1) * 1E6
            sys.stdout.write("\033[1;36m Delta: %.3f ppm\033[1;39m\r\n" % ppms)
            b.write("DCI Calibration step %sA , measured : %.9E ADC, deviation %.3f ppm\r\n" % (cal_dci_str[cnt], val, ppms))
        else:
            sys.stdout.write("\r\n")
        cnt = cnt + 1
    
    kei2400.write (":CAL:PROT:DATE 2016, 03, 01")
    kei2400.write (":CAL:PROT:NDUE 2016, 09, 01")
    kei2400.write (":CAL:PROT:SAVE")
    kei2400.write (":CAL:PROT:LOCK")
    kei2400.write (":OUTP:STAT OFF")

    print("\033[0;30;42mCalibration complete! www.xDevs.com \033[0;39;49m")
    kei2400.write (":SYST:BEEP:IMM 100, 1")
    kei2400.write (":SYST:BEEP:IMM 300, 1")
    kei2400.write (":SYST:BEEP:IMM 500, 1")
    kei2400.write (":SYST:BEEP:IMM 900, 1")
    kei2400.write (":SYST:BEEP:IMM 1200, 1")
    kei2400.write (":SYST:BEEP:IMM 1500, 1")
    kei2400.write (":SYST:BEEP:IMM 2000, 1")
    
    sys.stdout.write("\r\n\r\nPerformance DCI test\r\n")
    dmm.init_inst()
    dmm.get_temp()
    dmm.switch_dci()
    sys.stdout.write("3458A TEMP? = %02.1f \r\n" % (dmm_temp))
    
    for cnt in range (0, len(test_dci_set)):
        kei2400.write (":SOUR:FUNC CURR")
        kei2400.write (":SENS:VOLT:PROT 20")
        kei2400.write (":SENS:VOLT:RANG 20")
        kei2400.write (":OUTP:STAT ON")
        kei2400.write (":SOUR:CURR:RANGE %3.1e" % test_dci_rng[cnt])
        kei2400.write (":SOUR:CURR %3.1e" % test_dci_set[cnt])
        time.sleep(1)

        val = 0
        for samples in range (0, 5):
            dmm.get_data()
            print ("Test DCI %d : %.9E ADC" % (samples, dmm_val))
            val += dmm_val
        val = val / 5
        ppm = (((val+1e-16) / (test_dci_set[cnt] + 1E-16)) - 1) * 1E6
        sys.stdout.write(" Verification step %sA : %.9E ADC [deviation %6.2f ppm]\r\n" % (test_dci_str[cnt], val, ppm))
        b.write("DCI Verification step %sA , measured : %.9E ADC, deviation %.3f ppm\r\n" % (test_dci_str[cnt], val, ppm))
        cnt = cnt + 1

    kei2400.write (":OUTP:STAT OFF")
    sys.stdout.write("\033[0;31;43mConnect DMM VOLTAGE input to 2400 INPUT/OUTPUT jacks.\033[0;39;49m\r\n\r\n")
    print ":SYST:BEEP:IMM 1000, 5"
    raw_input("Press Enter to continue...")
        
    sys.stdout.write("Performance DCV test\r\n")
    dmm.init_inst()
    dmm.get_temp()
    print ("\033[0;33mHP3458A TEMP = %2.1f C\033[0;33m" % dmm_temp)
    
    for cnt in range (0, len(test_dcv_set)):
        kei2400.write (":SOUR:FUNC VOLT")
        kei2400.write (":SENS:CURR:PROT 0.1")
        kei2400.write (":SENS:CURR:RANG 0.1")
        kei2400.write (":OUTP:STAT ON")
        time.sleep(1)
        kei2400.write (":SOUR:VOLT:RANGE %3.1e" % test_dcv_rng[cnt])
        kei2400.write (":SOUR:VOLT %3.1e" % test_dcv_set[cnt])
        time.sleep(1)

        val = 0
        for samples in range (0, 5):
            dmm.get_data()
            print ("Test DCV %d : %.9E VDC" % (samples, dmm_val))
            val += dmm_val
        val = val / 5
        ppm = (((val+1e-16) / (test_dcv_set[cnt] + 1E-16)) - 1) * 1E6
        
        sys.stdout.write(" Verification step  %02d (%.9E) : %.9E VDC [deviation %6.2f ppm]\r\n" % (cnt, test_dcv_set[cnt], val, ppm))
        b.write("DCV Verification step %02d (%.9E), measured : %.9E VDC, deviation %.3f ppm\r\n" % (cnt, test_dcv_set[cnt], val, ppm))
        cnt = cnt + 1

    # Post-cal constants 
    print "Reading Post-cal calibration data from Model 2400"
    b.write("Post-cal K2400 Calibration data\r\n")
    
    for cnt in range (0, 4):
        kei2400.write (":SOUR:VOLT:RANGE %3.1f" % cal_dcv_rng[cnt*4])
        kei2400.write (":CAL:PROT:SENS:DATA?")
        kdata = kei2400.read()
        sys.stdout.write ("%s" % kdata)
        b.write("%3.1f DCV Range, SENS:DATA? = %s\r\n" % (cal_dcv_rng[cnt*4], kdata))
        kei2400.write (":CAL:PROT:SOUR:DATA?")
        kdata = kei2400.read()
        sys.stdout.write ("%s" % kdata)
        b.write("%3.1f DCV Range, SOUR:DATA? = %s\r\n" % (cal_dcv_rng[cnt*4], kdata))
        cnt = cnt + 1
    
    kei2400.write (":CAL:PROT:LOCK")
    kei2400.write (":SENS:FUNC 'CURR:DC'")
    kei2400.write (":SOUR:FUNC CURR")
    kei2400.write (":CAL:PROT:CODE 'KI002400'")
    
    for cnt in range (0, 7):
        kei2400.write (":SOUR:CURR:RANGE %3.1e" % cal_dci_rng[cnt*4])
        kei2400.write (":CAL:PROT:SENS:DATA?")
        kdata = kei2400.read()
        sys.stdout.write ("%s" % kdata)
        b.write("%3.1e DCI Range, SENS:DATA? = %s\r\n" % (cal_dci_rng[cnt*4], kdata))
        kei2400.write (":CAL:PROT:SOUR:DATA?")
        kdata = kei2400.read()
        b.write("%3.1e DCI Range, SOUR:DATA? = %s\r\n" % (cal_dci_rng[cnt*4], kdata))
        sys.stdout.write ("%s" % kdata)
        cnt = cnt + 1

    kei2400.write (":CAL:PROT:LOCK")
    b.write ("Calibration complete!")
    b.close()