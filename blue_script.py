import argparse
import subprocess
import time

#
# run with sudo 
#

def run_command(command):
    return subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# get ip from ip command
def get_ip():
    command = "ip -o -4 addr list ens33 | awk '{print $4}' | cut -d/ -f1" # need to change interface
    ip = run_command(command)
    return ip

# setup firewall rules based on ip
def firewall(ip, check="check"):
    allowed_ips = ["0.0.0.0", "0.0.0.0"] # change to ip of host and scoring/router
    box_ips = ["10.11.1.3", "192.168.11.1"]

    prelim_commands = "iptables -F; iptables -P INPUT ACCEPT; iptables -P OUTPUT ACCEPT"
    run_command(prelim_commands)
    
    if ip == box_ips[0]:
        print("Setup firewall rules")
        command = f"iptables -A INPUT -p tcp -s {allowed_ips[0]},{allowed_ips[1]} --dport 21 -m state --state ESTABLISHED,NEW -j ACCEPT; iptables -A OUTPUT -p tcp -d {allowed_ips[0]},{allowed_ips[1]} --sport 21 -m state --state ESTABLISHED -j ACCEPT"
        run_command(command)
    elif ip == box_ips[1]:
        print("Setup firewall rules")
        command = f"iptables -A INPUT -p tcp -s {allowed_ips[0]},{allowed_ips[1]} --dport 3306 -m state --state NEW,ESTABLISHED -j ACCEPT; iptables -A OUTPUT -p tcp -d {allowed_ips[0]},{allowed_ips[1]} --sport 3306 -m state --state ESTABLISHED -j ACCEPT"
        run_command(command)
    
    final_commands = "iptables -A INPUT -j DROP; iptables -A OUTPUT -j DROP"
    run_command(final_commands)

    if check == "check":
        time.sleep(5)
        print("Deleted firewall rules")
        flush_command = "iptables -F"
        run_command(flush_command)

# setup pf
def freebsd_setup():
    commands = "pkg install pftop; mv ./pf.conf /etc/pf.conf; sysrc pf_enable=yes; sysrc pflog_enable=yes; service pf start; service pflog start"
    run_command(commands)

# run pf
def freebsd_firewall(check=False):
    command = "pfctl -e ; pfctl -f /etc/pf.conf"
    run_command(command)
    if check == True:
        time.sleep(5)
        flush_command = "pfctl -F all"
        run_command(flush_command)

def print_config():
    config_files = [
        "/etc/hosts",
        "/etc/resolve.conf",
        "/etc/crontab",
        "/etc/bashrc",
        "/etc/profile"]
    
    for file in config_files:
        try:
            print('_'*40,file,'_'*40, end='\n\n')
            with open(file, 'r') as f:
                for _ in f:
                    print(f.read())
                print()
        except FileNotFoundError:
            print(f'File {file} not found')
        except Exception as e:
            print(f'Error reading {file}: {str(e)}')

# main
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--firewall", help="Run iptables firewall. Run with 'nocheck' and 'check' for initial check")
    parser.add_argument("-b", "--bsd", help="Run with 'nocheck' and 'check' for initial check")
    parser.add_argument("-s", "--setup", action="store_true", help="Setup pf firewall")
    parser.add_argument("-c", "--config", action="store_true", help="Print common config files")

    ip = get_ip().stdout.strip()

    try:
        args = parser.parse_args()
        if args.firewall:
            print("Running iptables firewall rules...")
            firewall(ip, args.firewall)
        elif args.bsd:
            print("Running pf firewall...")
            freebsd_firewall(args.bsd)
        elif args.setup:
            print("Setting up pf firewall prelims...")
            freebsd_setup()
        elif args.config:
            print_config()
    except:
        print("oops")

#scuffed