from si_prefix import si_format

print si_format(.5)
# 500.0 m  (default precision is 1)

print si_format(.01331, precision=2)
# 13.31 m

print si_format(1331, precision=2)
# 1.33 k

print si_format(1331, precision=0)
# 1 k
