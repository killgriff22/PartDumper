import io
from utils import *
in_data = infile.read()
if "--..--..--" in in_data:
    in_data = in_data.split("[Message:     Unity] Lua: --..--..--\n")
    for x in in_data:
        if not x:
            continue
        single(x)
        #input("Press Enter to continue...")
else:
    single(in_data)
