#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import sys
import time
import os
import getpass
import subprocess
#from paramiko import SSHClient
#import paramiko

def how_many_rules(rules):
    end_ip = ""
    if (rules <= 250):
        end_ip = "10.0.0.%s" % rules
    elif (rules <= 500):
        end_ip = "10.0.1.%s" % (rules - 250)
    elif (rules <= 1000):
        end_ip = "10.0.3.%s" % (rules - 750)
    elif (rules <= 2000):
        end_ip = "10.0.7.%s" % (rules - 1750)
    elif (rules <= 3000):
        end_ip = "10.0.11.%s" % (rules - 2750)
    elif (rules <= 4000):
        end_ip = "10.0.15.%s" % (rules - 3750)
    elif (rules <= 5000):
        end_ip = "10.0.19.%s" % (rules - 4750)
    elif (rules <= 6000):
        end_ip = "10.0.23.%s" % (rules - 5750)
    elif (rules <= 7000):
        end_ip = "10.0.27.%s" % (rules - 6750)
    elif (rules <= 8000):
        end_ip = "10.0.31.%s" % (rules - 7750)
    elif (rules <= 9000):
        end_ip = "10.0.35.%s" % (rules - 8750)
    elif (rules <= 10000):
        end_ip = "10.0.39.%s" % (rules - 9750)
    elif (rules <= 11000):
        end_ip = "10.0.43.%s" % (rules - 10750)
    elif (rules <= 12000):
        end_ip = "10.0.47.%s" % (rules - 11750)
    elif (rules <= 13000):
        end_ip = "10.0.51.%s" % (rules - 12750)
    elif (rules <= 14000):
        end_ip = "10.0.55.%s" % (rules - 13750)
    elif (rules <= 15000):
        end_ip = "10.0.59.%s" % (rules - 14750)
    elif (rules <= 16000):
        end_ip = "10.0.63.%s" % (rules - 15750)
    elif (rules <= 17000):
        end_ip = "10.0.67.%s" % (rules - 16750)
    elif (rules <= 18000):
        end_ip = "10.0.71.%s" % (rules - 17750)
    elif (rules <= 19000):
        end_ip = "10.0.75.%s" % (rules - 18750)
    elif (rules <= 20000):
        end_ip = "10.0.79.%s" % (rules - 19750)
    return end_ip


def source_ipRange(start_ip, end_ip):
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start
    ip_range = []
    ip_range.append(start_ip)
    while temp != end:
       start[3] += 1
       for i in (3, 2, 1):
          if temp[i] == 256:
             temp[i] = 0
             temp[i-1] += 1
       ip_range.append(".".join(map(str, temp)))    
    return ip_range

# Standard rules
# iptables -A INPUT -s 10.127.0.0/16 -j ACCEPT
# iptables -A FORWARD -s 10.127.0.0/16 -j ACCEPT
# iptables -A OUTPUT -s 10.127.0.0/16 -j ACCEPT 
#
def iptables_forward_rules(source_ip, destination_ip, test_type):
    #import pdb; pdb.set_trace()
    count = 0
    count_rules = len(ip_range)
    try:
        if (test_type == "first_rule"):
            print "We are going to create %s iptables rules and the allowing rule is in the first one" % (count_rules)
            os.popen("""iptables-restore < /root/testes/iptables-original""")
            os.popen("""iptables -A INPUT -s 10.127.0.0/16 -j ACCEPT""")
            os.popen("""iptables -A OUTPUT -s 10.127.0.0/16 -j ACCEPT""")
            os.popen("""iptables -A FORWARD -s 10.127.0.0/16 -j ACCEPT""")
            #print """iptables -A FORWARD -s %s/32 -d %s/32 -i eth1 -o eth0 -m comment --comment 'rule %s - allow access between endpoints' -j ACCEPT""" % (source_ip, destination_ip, count)
            os.popen("""iptables -A FORWARD -s %s/32 -d %s/32 -i eth1 -o eth0 -m comment --comment 'rule %s - allow access between endpoints' -j ACCEPT""" % (source_ip, destination_ip, count))
            test_type = ""
            for ip in ip_range:
                count = count + 1
                os.popen("""iptables -A FORWARD -s %s/32 -d %s/32 -i eth1 -o eth0 -m comment --comment 'iptables rule %s --> without match' -j ACCEPT""" % (ip, destination_ip, count))
        elif (test_type == "middle_rule"): 
            print "We are going to create %s iptables rules and the allowing rule is in the middle" % (count_rules)
            os.popen("""iptables-restore < /root/testes/iptables-original""")
            os.popen("""iptables -A INPUT -s 10.127.0.0/16 -j ACCEPT""")
            os.popen("""iptables -A OUTPUT -s 10.127.0.0/16 -j ACCEPT""")
            os.popen("""iptables -A FORWARD -s 10.127.0.0/16 -j ACCEPT""")
            test_type = ""
            for ip in ip_range:
                if (len(ip_range) % 2 != 0) and (count == len(ip_range) / 2):
                    #os.popen("iptables -A FORWARD -s %s/32 -d 10.224.76.198/32 -i eth1 -o eth0 -m comment --comment 'iptables rule %s --> without match' -j ACCEPT" % (ip,count))
                    os.popen("""iptables -A FORWARD -s %s/32 -d %s/32 -i eth1 -o eth0 -m comment --comment 'rule %s - allow access between endpoints' -j ACCEPT""" % (source_ip, destination_ip, count + 1)) 
                    count = count + 1
                elif (len(ip_range) % 2 == 0) and (count == len(ip_range) / 2):
                    #os.popen("iptables -A FORWARD -s %s/32 -d 10.224.76.198/32 -i eth1 -o eth0 -m comment --comment 'iptables rule %s --> without match' -j ACCEPT" % (ip,count))
                    os.popen("""iptables -A FORWARD -s %s/32 -d %s/32 -i eth1 -o eth0 -m comment --comment 'rule %s - allow access between endpoints' -j ACCEPT""" % (source_ip, destination_ip, count + 1)) 
                    count = count + 1
                else:
                    os.popen("""iptables -A FORWARD -s %s/32 -d %s/32 -i eth1 -o eth0 -m comment --comment 'iptables rule %s --> without match' -j ACCEPT""" % (ip, destination_ip, count))
                    count = count + 1
        elif (test_type == "last_one_rule"):
            print "We are going to create %s iptables rules and the allowing rule is the last one" % (count_rules)
            os.popen("""iptables-restore < /root/testes/iptables-original""")
            os.popen("""iptables -A INPUT -s 10.127.0.0/16 -j ACCEPT""")
            os.popen("""iptables -A OUTPUT -s 10.127.0.0/16 -j ACCEPT""")
            os.popen("""iptables -A FORWARD -s 10.127.0.0/16 -j ACCEPT""")
            test_type = ""
            for ip in ip_range:
                if (count == len(ip_range) - 1):
                    os.popen("""iptables -A FORWARD -s %s/32 -d %s/32 -i eth1 -o eth0 -m comment --comment 'iptables rule %s --> without match' -j ACCEPT""" % (ip, destination_ip, count))
                    os.popen("""iptables -A FORWARD -s %s/32 -d %s/32 -i eth1 -o eth0 -m comment --comment 'rule %s - allow access between endpoints' -j ACCEPT""" % (source_ip, destination_ip, count + 1))
                    break
                else:
                    os.popen("""iptables -A FORWARD -s %s/32 -d %s/32 -i eth1 -o eth0 -m comment --comment 'iptables rule %s --> without match' -j ACCEPT""" % (ip, destination_ip, count))
                    count = count + 1              
        else:
            print """You need to choose first_rule, middle_rule or last_one_rule"""
    except Exception:
        sys.exit("something went wrong") 
    return True



def auth(host):
    count = 0
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    while count <= 2:
        username = raw_input("Usuario: ")
        password = getpass.getpass("Senha: ")
        ssh.connect(host, username, password)
        try:
            stdin,stdout,stderr = ssh.exec_command('ls')
            if stderr.channel.recv_exit_status() != 0:
                print stderr.read()
            else:
                print stdout.read()
        except Exception:
            print "Authentication error"
            count = count + 1
    sys.exit("Authentication failed. Please verify your credentials.\n")


def create_result_file(qtd_rules,test_step):
    httperf = str(qtd_rules) + "-iptables-rules-httperf.csv-" + str(test_step)
    rtt = str(qtd_rules) + "-iptables-rules-rtt.csv-" + str(test_step)
    throughput = str(qtd_rules) + "-iptables-rules-throughput.csv-" + str(test_step)
    #test_exec = "/bin/bash 250a20000-iptables-rules-benchmarking.sh %s %s %s" % (httperf, rtt, throughput)
    result = int(subprocess.check_output(["/bin/bash", "250a20000-iptables-rules-benchmarking.sh", httperf, rtt, throughput]))
    if result == 10:
        return result
    else:
        print "Create result file ERROR"



if __name__ == "__main__":
    #rules = int(raw_input("How many rules do you wanna create? "))
    test_step = [250, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000]
    test_type = ["first_rule", "middle_rule", "last_one_rule"]
    source_ip = "10.170.3.22"
    destination_ip = "10.170.3.26"
    for value in test_type:
        #test_type = raw_input("Where do you want to insert the allowing rule (first_rule, middle_rule or last_one_rule)? ")
        for qtd_rules in test_step:
            end_ip = how_many_rules(qtd_rules)
            ip_range = source_ipRange("10.0.0.0", end_ip)
            #source_ip = raw_input("Please inform traffic generator's ip address. Eg.: 10.224.70.50 \n ")
            #destination_ip = raw_input("Please inform traffic receptor's ip address. Eg.: 10.224.76.198 \n ")
            out = iptables_forward_rules(source_ip, destination_ip, value)
            #import pdb; pdb.set_trace()
            if out == True:
                print out
                if create_result_file(qtd_rules,value) == 10:
                    continue
            else:            
                print "Main ERROR"

	
