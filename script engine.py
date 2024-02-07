import os
import time
import subprocess

def log_message(message, log_file_path):
    """Log a message with a timestamp to a specified log file."""
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def run_executable(executable_path, log_file_path):
    """Log the running of an executable and then run it."""
    log_message(f"Running executable: {executable_path}", log_file_path)
    subprocess.run(executable_path, shell=True)

def restart_computer(log_file_path):
    """Log the restarting of the computer and then restart using a specified AHK script."""
    log_message("Restarting computer using reboot.ahk.", log_file_path)
    reboot_ahk_path = "C:\\Users\\ReynoldsPurge\\Documents\\live\\reboot.ahk"
    subprocess.run(f'"{reboot_ahk_path}"', shell=True)

def check_and_execute(go_file, executable, engine_dir, live_dir, log_file_path):
    """Check for a 'go' file, run the associated executable, wait for a 'done' file, and handle timeouts."""
    go_file_path = os.path.join(engine_dir, go_file)
    if os.path.exists(go_file_path):
        log_message(f"Found 'go' file: {go_file_path}", log_file_path)
        
        executable_path = os.path.join(live_dir, executable)
        run_executable(executable_path, log_file_path)

        done_file = go_file.replace("go", "done")
        done_file_path = os.path.join(engine_dir, done_file)
        start_time = time.time()
        
        # Special timeout for goidmdeal.txt
        timeout_seconds = 3 * 60 * 60 if go_file == "goidmdeal.txt" else 2 * 60 * 60

        while not os.path.exists(done_file_path):
            if time.time() - start_time > timeout_seconds:
                restart_computer(log_file_path)
                return
            time.sleep(5)  # Check every 5 seconds

        log_message(f"'Done' file found: {done_file_path}", log_file_path)
        os.remove(go_file_path)
        os.remove(done_file_path)
        log_message(f"Deleted 'go' and 'done' files: {go_file_path}, {done_file_path}", log_file_path)

def main():
    engine_dir = "C:\\engine"
    live_dir = "C:\\Users\\ReynoldsPurge\\Documents\\live"
    log_file_path = os.path.join(engine_dir, "log.txt")

    log_message("Script started", log_file_path)

    file_exe_map = {
        "gostockin.txt": "stock in report export.exe",
        "gopdi.txt": "pdi_export.exe",
        "godealervault.txt": "DealerVault.exe",
        "go dd date.txt": "dd date.exe",
        "goreceivedate5.txt": "receive date 5.exe",
        "gopayroll.txt": "payroll.exe",
        "govehiclecomments.txt": "vehicle comments.exe",
        "gokeytrak.txt": "keytrak export.exe",
        "goidmdeal.txt": "idm import deals.exe",
        "goinvoice.txt": "Floorplan Amount.exe"
    }

    while True:
        for go_file, executable in file_exe_map.items():
            check_and_execute(go_file, executable, engine_dir, live_dir, log_file_path)
        time.sleep(5)  # Wait for 5 seconds before next iteration

if __name__ == "__main__":
    main()
