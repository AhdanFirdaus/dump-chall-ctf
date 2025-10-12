#!/usr/bin/python3
import subprocess
import os
import base64

frieren = b"\x7fELF"

fd = os.memfd_create("sylphiette", 0)
sylphiette = base64.b64decode(input("sylphiette vs frieren cantikan mana? ").strip())

assert len(sylphiette) <= 76, "kegedean"
assert frieren == sylphiette[:4], "harus elf yang cantik"

with os.fdopen(fd, "wb", closefd=False) as f: 
    f.write(sylphiette)

try:
    p = subprocess.Popen([f"/proc/{os.getpid()}/fd/{fd}"], shell=False)
    p.wait()
except:
    os.killpg(os.getpid(), 9)
    exit(1)