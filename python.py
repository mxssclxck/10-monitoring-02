import datetime
import json
import os

def get_cpu_info():
    with open("/proc/cpuinfo", "r") as f:
        cpu_info = f.read().split("\n\n")[0].split("\n")
    cpu_info_dict = {line.split(":")[0].strip(): line.split(":")[1].strip() for line in cpu_info if ":" in line}
    return {
        "model": cpu_info_dict["model name"],
        "cores": int(cpu_info_dict["cpu cores"]),
        "freq": float(cpu_info_dict["cpu MHz"]) / 1000,
    }

def get_mem_info():
    with open("/proc/meminfo", "r") as f:
        mem_info = f.read().split("\n")
    mem_info_dict = {line.split(":")[0].strip(): line.split(":")[1].strip() for line in mem_info if ":" in line}
    return {
        "total": int(mem_info_dict["MemTotal"].split()[0]) / 1024,
        "free": int(mem_info_dict["MemFree"].split()[0]) / 1024,
        "available": int(mem_info_dict["MemAvailable"].split()[0]) / 1024,
    }

def get_disk_info():
	with open("/proc/diskstats", "r") as f:
		disk_info = f.read().split("\n")
	return {
		"reads": int(disk_info[2].split()[3]),
		"writes": int(disk_info[2].split()[7]),
		"read_bytes": int(disk_info[2].split()[5]),
		"write_bytes": int(disk_info[2].split()[9]),
	}

def get_uptime():
    with open("/proc/uptime", "r") as f:
        uptime = f.read().split(" ")[0]
    return float(uptime)

def main():
	timestamp = int(datetime.datetime.now().timestamp())
	metrics = {
		"timestamp": timestamp,
		"cpu": get_cpu_info(),
		"memory": get_mem_info(),
		"disk": get_disk_info(),
		"uptime": get_uptime(),
	}

	log_file = "/var/log/YY-MM-DD-awesome-monitoring.log".replace("YY", str(datetime.datetime.now().year)).replace("MM", str(datetime.datetime.now().month).zfill(2)).replace(
		"DD", str(datetime.datetime.now().day).zfill(2))
	
	with open(log_file, "a") as f:
		f.write(json.dumps(metrics, indent=4) + "\n")

if __name__ == "__main__":
	main()