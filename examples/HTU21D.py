from sensor import HTU21D

# I2C bus=1, Address=0x40
htu = HTU21D(1, 0x40)

h = htu.humidity()  # read humidity
print(h)            # namedtuple
print(h.RH)         # relative humidity

t = htu.temperature()  # read temperature
print(t)               # namedtuple
print(t.F)             # Fahrenheit

h, t = htu.all()  # read both at once