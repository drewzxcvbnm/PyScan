import psutil
import win32api
import win32con
import win32process
import ctypes
from ctypes.wintypes import *

ps = ctypes.windll.psapi
GetModuleInfo = ps.GetModuleInformation


class ModuleInfo(ctypes.Structure):
    _fields_ = [
        ("lpBaseOfDll", LPVOID),
        ("SizeOfImage", DWORD),
        ("EntryPoint", LPVOID)
    ]


def get_pid_by_name(name):
    for proc in psutil.process_iter():
        if name in proc.name():
            return proc.pid
    raise Exception(f"Cannot find process {name}")


def chunkstring(string, length):
    return (string[0 + i:length + i] for i in range(0, len(string), length))


def base_address(phandle):
    modules = win32process.EnumProcessModules(phandle)
    base_addr = modules[0]
    return base_addr


name = "pycharm"
pid = get_pid_by_name(name)
test = ctypes.c_int(15)

phandle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)

module = base_address(phandle)
print(module)

mod = ModuleInfo()
lpmod = LPPOINT(mod)

GetModuleInfo(HANDLE(phandle.handle), HMODULE(module), lpmod, DWORD(ctypes.sizeof(mod)))
print('info dll base:', mod.lpBaseOfDll)
print('info size:', mod.SizeOfImage)
print('info entry:', mod.EntryPoint)

addr = ctypes.addressof(test)

res = win32process.ReadProcessMemory(phandle, module, mod.SizeOfImage)

for i in chunkstring(str(res).replace('\\x', ' '), 70):
    print(i)
