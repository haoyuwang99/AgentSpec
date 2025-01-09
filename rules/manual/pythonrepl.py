import os
import tempfile
import time 

def is_malware(code_string):
    # TODO: implement using virus total
    return False

def capture_screenshot():
    pattern = {
        ("ImageGrab","grab()")
    }

def access_clipboard():
    pattern = {
        "pyperclip.paste()"
    }

def monitor_file_system_event():
    pattern = {
        ("watchdog", "FileSystemEventHandler")
    }

def check_process_status():
    pattern = {
        "psutil.net_io_counters",
        "psutil.cpu_percent",
    }

def submit_post_request():
    # ```urllib.request.Request(url, data=body)```
    # when the data parameter is set. it is a post request
    # or specify 
    # ```request.Request(url, data=data, method="POST")```
    return False

def involve_system_file(code_string):
    path = {
        "/etc/passwd",
        "/etc/shadow",
        "/etc/group",
        "/etc/gshadow",
        "/etc/security/opasswd",
        "/etc/security/group.conf",
        "/etc/security/limits.conf",
        "/etc/apt/sources.list",
        "/etc/ssh/ssh_config",
        "/etc/ssl/openssl.cnf",
        "/proc/cpuinfo",
        "/proc/key-users",
        "/proc/devices",
        "/proc/cmdline",
        "/proc/meminfo",
        "/root/.bashrc",
        "/root/.profile",
        "/usr/usrfile.txt",
        "/usr/share/base-passwd/group.master",
        "/usr/share/base-passwd/passwd.master",
        "/sys/kernel/kexec_loaded",
        "/sys/kernel/kexec_crash_loaded",
        "/sys/kernel/kexec_crash_size",
        "/sys/kernel/vmcoreinfo",
        "/var/log/lastlog",
        "/var/log/btmp",
        "/var/log/wtmp",
        "/var/log/faillog",
        "/var/log/dpkg.log",
        "/var/log/alternatives.log"
    }

    return False

def involve_system_dir(code_string):
    system_directories = {
        "/app/",
        "/bin/",
        "/dev/",
        "/etc/",
        "/etc/security/",
        "/etc/ssh/",
        "/etc/ssl/",
        "/etc/pam.d/",
        "/etc/apt/",
        "/etc/ca-certificates/",
        "/lib/",
        "/opt/",
        "/proc/",
        "/proc/1/",
        "/proc/sys/",
        "/proc/bus/",
        "/proc/driver/",
        "/proc/pressure/",
        "/root/",
        "/sys/",
        "/sys/kernel/",
        "/usr/",
        "/usr/share/",
        "/usr/share/base-passwd/",
        "/usr/share/ca-certificates/",
        "/usr/share/pam/",
        "/usr/share/keyrings/",
        "/var/",
        "/var/log/",
        "/var/log/apt/"
    }
    return False

def request_untrusted_source():
    whitelist = [
        "www.google.com"
    ]
    return False

def read_file():
    
    pattern = { 
        ("with open(./*, 'a|w') as xx:", "xx.read()")
               }
    return False

def write_to_file():
    pattern = {
        ("print"),
        ("with open(./*, 'a|w') as xx:", "xx.write()")

               }
    
    return False

def copy_file():
    pattern =  {("subprocess.run", "cp"),
    ("os.system", "cp"), 
    ("shutil.copy")}
    
def list_directory():
    pattern = {
        "glob.glob",
        "os.listdir"
    }
    
def execute_script():
    pattern = {
        "os.system",
        "subprocess.run",
        "subprocess.POpen",
        "eval("
    }
    return False

def encode_data():
    pattern = ["Base64"]
    return False

def destuctive_os_inst():
    pattern = {
        ("os.remove"),
        ("os.unlink"),
        ("pathlib", "unlink")
    }

def contain_exec_string():
    # check the program contains string that are executable python code
    pattern = {
        "rm -rf",
        "__import__('os').system('ls -a *')"
    }

def is_fair():
    # TODO: 
    return False

def kill_process():
    pattern = {
        ("import proc", "kill")
    }

def backtracking_regex_pattern():
    return False

def set_random_seed():
    pattern = {
        "random.seed()"
    }
    return

def backtracking_vulnerable_regex_pattern():
    import re
    import time

    pattern = re.compile(r"(a+)+b")
    attack_string = "a" * 100000   # Long string with a match
    start = time.time()
    re.match(pattern, attack_string)
    end = time.time()
    print("Match completed in:", end - start, "seconds")
    
def hash_with_constant_salt():
    pattern = "hasher.update"
    is_salt_constant = True
    return 

def get_weekday_name(day_number):
    match day_number:
        case 1:
            return "Monday"
        case 2:
            return "Tuesday"
        case 3:
            return "Wednesday"
        case 4:
            return "Thursday"
        case 5:
            return "Friday"
        case 6:
            return "Saturday"

day_name = get_weekday_name(7)
if day_name is None:
    print("No default case for getting the weekday name.")

def arbitrary_code_execution():
    pattern = {
        "pickle.loads",
        "plistlib.loads",
        "exec",
        "eval"
    }

def memory_leackage():
    
    return True

backtracking_vulnerable_regex_pattern()