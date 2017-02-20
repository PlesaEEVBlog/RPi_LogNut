# Following part is test USB connection
import usbtmc
instr =  usbtmc.Instrument("USB::0x05e6::0x2604::INSTR")
print(instr.ask("*IDN?"))
