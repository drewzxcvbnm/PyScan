import psutil
import win32api
import win32con
import win32process
import os
import ctypes


def get_pid_by_name(name):
    for proc in psutil.process_iter():
        if name in proc.name():
            return proc.pid
    raise Exception(f"Cannot find process {name}")


def chunkstring(string, length):
    return (string[0 + i:length + i] for i in range(0, len(string), length))


name = "chrome"
# pid = os.getpid()
pid = get_pid_by_name(name)
module = psutil.Process(pid).exe()
print(module)
module = win32api.GetModuleHandle(module)
test = ctypes.c_int(15)

phandle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)

addr = ctypes.addressof(test)

res = win32process.ReadProcessMemory(phandle, module, 4000)

for i in chunkstring(str(res).replace('\\x', ' '), 70):
    print(i)
