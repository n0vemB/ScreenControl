from flask import Flask, render_template, send_from_directory
import os
import socket
import logging
import subprocess
import pythoncom
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# 全局变量
window_stack = []  # 用于存储窗口进程
is_muted = False
LOCAL_IP = get_local_ip()

def add_window(process):
    """添加新窗口到栈中"""
    global window_stack
    # 等待一小段时间确保进程完全启动
    try:
        process.wait(timeout=0.5)
    except subprocess.TimeoutExpired:
        pass
    window_stack.append(process)

def close_current_window():
    """关闭最近打开的窗口"""
    global window_stack
    if window_stack:
        try:
            process = window_stack.pop()  # 获取最后打开的窗口
            if process:
                # 获取进程的所有子进程
                cmd = f'wmic process where "ParentProcessId={process.pid}" get ProcessId'
                child_pids = subprocess.check_output(cmd, shell=True).decode()
                
                # 关闭子进程（Chrome 标签页）
                for pid in child_pids.strip().split('\n')[1:]:  # 跳过标题行
                    try:
                        if pid.strip():
                            subprocess.run(f'taskkill /F /PID {pid.strip()}', shell=True)
                    except:
                        pass
                
                # 关闭主进程
                process.terminate()
            return True
        except Exception as e:
            logger.error(f"Error closing window: {e}")
            return False
    return False

@app.route('/')
def home():
    return render_template('mobile_control.html')

@app.route('/video/<path:filename>')
def serve_video(filename):
    return send_from_directory('static/video', filename)

@app.route('/play_video')
def play_video():
    try:
        server_url = f'http://{LOCAL_IP}:8080/fullscreen'
        chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        cmd = [
            chrome_path,
            '--kiosk',
            '--autoplay-policy=no-user-gesture-required',
            '--disable-infobars',
            server_url
        ]
        process = subprocess.Popen(cmd)
        add_window(process)  # 将新窗口添加到栈中
        return {"status": "success", "message": "视频开始播放"}
    except Exception as e:
        logger.error(f"Error playing video: {e}")
        return {"status": "error", "message": str(e)}

@app.route('/show_webpage')
def show_webpage():
    try:
        url = "https://workspace.easyv.cloud/shareScreen/eyJzY3JlZW5JZCI6MzE1NDM1NywiZXhwaXJlZEF0IjoiMjAyNC0xMi0wNlQwMjoyMjo1NC4wOThaIn0="  # 替换为你的数据大屏URL
        process = subprocess.Popen([
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            '--new-window',  # 使用新窗口而不是新标签
            '--kiosk',
            url
        ])
        add_window(process)  # 将新窗口添加到栈中
        return {"status": "success", "message": "数据大屏1已打开"}
    except Exception as e:
        logger.error(f"Error showing webpage: {e}")
        return {"status": "error", "message": str(e)}

@app.route('/show_webpage2')
def show_webpage2():
    try:
        url = "https://workspace.easyv.cloud/shareScreen/eyJzY3JlZW5JZCI6MzE1NDM4MywiZXhwaXJlZEF0IjoiMjAyNC0xMi0wNlQwMjoyNDo0NC45NDZaIn0=?timeStamp=19375bc4b39"  # 替换为你的第二个数据大屏URL
        process = subprocess.Popen([
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            '--new-window',  # 使用新窗口而不是新标签
            '--kiosk',
            url
        ])
        add_window(process)  # 将新窗口添加到栈中
        return {"status": "success", "message": "数据大屏2已打开"}
    except Exception as e:
        logger.error(f"Error showing webpage: {e}")
        return {"status": "error", "message": str(e)}

@app.route('/show_webpage3')
def show_webpage2():
    try:
        url = "https://workspace.easyv.cloud/shareScreen/eyJzY3JlZW5JZCI6MzE1NDM3NSwiZXhwaXJlZEF0IjoiMjAyNC0xMi0wNlQwMjoxNjo1Ni41OTlaIn0=?timeStamp=19375bd9c51"  # 替换为你的第三个数据大屏URL
        process = subprocess.Popen([
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            '--new-window',  # 使用新窗口而不是新标签
            '--kiosk',
            url
        ])
        add_window(process)  # 将新窗口添加到栈中
        return {"status": "success", "message": "数据大屏2已打开"}
    except Exception as e:
        logger.error(f"Error showing webpage: {e}")
        return {"status": "error", "message": str(e)}

@app.route('/show_webpage4')
def show_webpage2():
    try:
        url = "https://workspace.easyv.cloud/shareScreen/eyJzY3JlZW5JZCI6MzE0OTE1MywiZXhwaXJlZEF0IjoiMjAyNC0xMi0wNlQwMjoyNzoxOC4zNDVaIn0=?timeStamp=19375bea2bd"  # 替换为你的第四个数据大屏URL
        process = subprocess.Popen([
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            '--new-window',  # 使用新窗口而不是新标签
            '--kiosk',
            url
        ])
        add_window(process)  # 将新窗口添加到栈中
        return {"status": "success", "message": "数据大屏2已打开"}
    except Exception as e:
        logger.error(f"Error showing webpage: {e}")
        return {"status": "error", "message": str(e)}

@app.route('/close_current')
def close_current():
    try:
        if close_current_window():
            return {"status": "success", "message": "已关闭当前窗口"}
        return {"status": "success", "message": "没有窗口可关闭"}
    except Exception as e:
        logger.error(f"Error closing current window: {e}")
        return {"status": "error", "message": str(e)}

@app.route('/fullscreen')
def fullscreen():
    return render_template('fullscreen.html')

if __name__ == '__main__':
    print(f"\n服务器地址: http://{LOCAL_IP}:8080")
    print("本地测试地址: http://localhost:8080")
    print("\n正在启动服务器...\n")
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)