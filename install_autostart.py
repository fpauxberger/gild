#!/usr/bin/env python3
"""Make the GIT website start automatically (at login/boot) so server.py never has to be run by hand.
  python3 install_autostart.py            install and start now
  python3 install_autostart.py uninstall  remove again
Supports Windows, macOS and Linux (systemd). Then just open http://localhost:8000"""
import os, platform, subprocess, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
SERVER = os.path.join(ROOT, "server.py")
PY = sys.executable
action = sys.argv[1] if len(sys.argv) > 1 else "install"
system = platform.system()
home = os.path.expanduser("~")

def run(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

if system == "Windows":
    startup = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    vbs = os.path.join(startup, "GIT-website.vbs")
    pyw = PY.replace("python.exe", "pythonw.exe")  # no console window
    if action == "uninstall":
        if os.path.exists(vbs): os.remove(vbs)
        print("Removed autostart. (A running server stops at next logout, or end 'pythonw.exe' in Task Manager.)")
    else:
        with open(vbs, "w") as f:
            f.write(f'CreateObject("WScript.Shell").Run """{pyw}"" ""{SERVER}""", 0, False\n')
        subprocess.Popen([pyw, SERVER], cwd=ROOT, creationflags=0x00000008 | 0x00000200)
        print("Installed. The site starts automatically at login and is running now: http://localhost:8000")
elif system == "Darwin":
    plist = os.path.join(home, "Library", "LaunchAgents", "com.gild.git-website.plist")
    if action == "uninstall":
        run("launchctl", "unload", plist)
        if os.path.exists(plist): os.remove(plist)
        print("Removed autostart.")
    else:
        os.makedirs(os.path.dirname(plist), exist_ok=True)
        with open(plist, "w") as f:
            f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict><key>Label</key><string>com.gild.git-website</string>
<key>ProgramArguments</key><array><string>{PY}</string><string>{SERVER}</string></array>
<key>WorkingDirectory</key><string>{ROOT}</string><key>RunAtLoad</key><true/><key>KeepAlive</key><true/></dict></plist>''')
        run("launchctl", "unload", plist); run("launchctl", "load", plist)
        print("Installed. The site starts automatically at login and is running now: http://localhost:8000")
else:  # Linux / systemd user service
    unit_dir = os.path.join(home, ".config", "systemd", "user")
    unit = os.path.join(unit_dir, "git-website.service")
    if action == "uninstall":
        run("systemctl", "--user", "disable", "--now", "git-website.service")
        if os.path.exists(unit): os.remove(unit)
        print("Removed autostart.")
    else:
        os.makedirs(unit_dir, exist_ok=True)
        with open(unit, "w") as f:
            f.write(f"[Unit]\nDescription=GIT website\n\n[Service]\nExecStart={PY} {SERVER}\nWorkingDirectory={ROOT}\nRestart=always\n\n[Install]\nWantedBy=default.target\n")
        run("systemctl", "--user", "daemon-reload")
        r = run("systemctl", "--user", "enable", "--now", "git-website.service")
        print("Installed. The site starts automatically and is running now: http://localhost:8000" if r.returncode == 0
              else "systemd user services not available here:\n" + r.stderr)
