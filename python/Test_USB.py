# Test USB
import usbtmc
instr =  usbtmc.Instrument("USB::0x0957::0x0a07::INSTR")
print(instr.ask("*IDN?"))
