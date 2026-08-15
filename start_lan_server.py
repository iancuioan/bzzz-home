import socket
import subprocess
import os

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    ip = get_local_ip()
    print(f"🌐 IP detectat: {ip}")
    print("🔧 Pornesc serverul Django...")

    # setează folderul unde e manage.py
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    venv_python = os.path.join("venv", "Scripts", "python.exe")  # dacă venv e în folderul proiectului

    subprocess.run([venv_python, "manage.py", "runserver", f"{ip}:8000"])
