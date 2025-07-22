# I removed the comments just for the code to look better
# ~ Kamerzystanasyt

from genericpath import exists
import os
import string
import sys
import shutil
import hashlib
import ctypes
from datetime import datetime

MB_ABORTRETRYIGNORE = 0x00000002
MB_CANCELTRYCONTINUE = 0x00000006
MB_HELP = 0x00004000
MB_OK = 0x00000000
MB_OKCANCEL = 0x00000001
MB_RETRYCANCEL = 0x00000005
MB_YESNO = 0x00000004
MB_YESNOCANCEL = 0x00000003

MB_ICONWARNING = 0x00000030
MB_ICONINFORMATION = 0x00000040
MB_ICONQUESTION = 0x00000020
MB_ICONSTOP = 0x00000010
MB_ICONERROR = 0x00000010

MB_DEFBUTTON1 = 0x00000000
MB_DEFBUTTON2 = 0x00000100
MB_DEFBUTTON3 = 0x00000200
MB_DEFBUTTON4 = 0x00000300

def _msg(title: str, message: str, style: int):

    return ctypes.windll.user32.MessageBoxW(None, message, title, style)
def showinfo(title: str, message: str):
    _msg(title, message, MB_ICONINFORMATION | MB_OK)
def showwarning(title: str, message: str):
    _msg(title, message, MB_ICONWARNING | MB_OK)
def showerror(title: str, message: str):
    _msg(title, message, MB_ICONERROR | MB_OK)

SYS32DLL = "ware.dll"
SYSWOW64DLL = "sex.dll"
BASE_NAME = "Windows.ApplicationModel.Store"
BASE_PATH = "C:\\Windows\\"
SYSWOW64 = os.path.join(BASE_PATH, "SysWOW64")
SYSTEM32 = os.path.join(BASE_PATH, "System32")
BACKUP_DIR = os.path.join(os.getenv('APPDATA'), "KangarooBackup")

def get_embedded_file_path(filename):
    """Get the path to an embedded file in the Nuitka executable."""
    if getattr(sys, 'frozen', False):  
        base_path = sys._MEIPASS  
        return os.path.join(base_path, filename)
    else:

        return os.path.join(os.path.dirname(__file__), filename)

def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    exe = sys.argv[0] if getattr(sys, 'frozen', False) else sys.executable
    params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
    if ctypes.windll.shell32.ShellExecuteW(None, "runas", exe, params, None, 1) <= 32:
        sys.exit(1)
    sys.exit(0)

def log(msg: str):
    print(msg)
    os.makedirs(BACKUP_DIR, exist_ok=True)  
    with open(os.path.join(BACKUP_DIR, "logs.txt"), "a", encoding="utf-8") as f:
        f.write(f"[LOG] [{datetime.now().strftime('%H:%M:%S')}] {msg}\n")

if __name__ == "__main__":
    try:
        if not is_admin():
            _msg(".gg/kangarooleaks", "niga u need to run this with administrator.", MB_ICONINFORMATION | MB_OK);
            run_as_admin()

        src_sys32dll = get_embedded_file_path(SYS32DLL)
        src_syswow64dll = get_embedded_file_path(SYSWOW64DLL)

        unpatched_sys32dll_hash = "fadc062256511952e6ddbc3d80e9bb4cf0506a06ef1ac1b0230485f86b68cde6" 
        unpatched_syswow64dll_hash = "6fb7fe2f352be0aedd1df5233ef505f843fe4289fe7e8af23225733c4b8c99d5" 

        def file_sha256(path: str) -> str:
            with open(path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()

        hash_sys32 = file_sha256(src_sys32dll)
        hash_syswow64 = file_sha256(src_syswow64dll)

        if not os.path.exists(src_sys32dll):
            raise FileNotFoundError(f"[*] DLL not found on system: {src_sys32dll}")
        if not os.path.exists(src_syswow64dll):
            raise FileNotFoundError(f"[*] DLL not found on system: {src_syswow64dll}")

        os.makedirs(SYSTEM32, exist_ok=True)
        os.makedirs(SYSWOW64, exist_ok=True)

        if not os.path.exists(BACKUP_DIR):
            os.system('rundll32 url.dll,FileProtocolHandler https://discord.gg/kangarooleaks')

        os.makedirs(BACKUP_DIR, exist_ok=True)

        if hash_sys32 != unpatched_sys32dll_hash:
            log(f"[-] sys32.dll patched ignoring...")
        else: 

            shutil.copy2(os.path.join(SYSTEM32, SYS32DLL), os.path.join(BACKUP_DIR, SYS32DLL))
            log(f"[+] sys32.dll not patched, backing up...")

        if hash_syswow64 != unpatched_syswow64dll_hash:
            log(f"[-] syswow64.dll patched ignoring...")
        else:

            shutil.copy2(os.path.join(SYSWOW64, SYSWOW64DLL), os.path.join(BACKUP_DIR, SYSWOW64DLL))
            log(f"[+] syswow64.dll not patched, backing up...")

        shutil.copy2(src_sys32dll, os.path.join(SYSTEM32, SYS32DLL))
        shutil.copy2(src_syswow64dll, os.path.join(SYSWOW64, SYSWOW64DLL))

        log("[+] DLLs moved successfully")

        _msg(".gg/kangarooleaks", "bedrock has been succesfully cracked.", MB_ICONINFORMATION | MB_OK);

    except Exception as e:
        log(f"ERROR: {e}")
