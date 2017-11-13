 #!/bin/bash

cliente05='10.170.3.22'
servidor05='10.170.3.26'

#cliente06='10.240.116.140'
#servidor06='10.240.116.142'

#cliente08='10.240.116.135'
#servidor08='10.240.116.145'

#cliente=$cliente05
#servidor=$servidor05
#cadeia='cadeia-uma-vnf'

typeset -i i END
let END1=1000 i=1
let END2=16

sshpass -p "ChangeMe" ssh -o StrictHostKeyChecking=no root@${cliente05} export servidor05='10.170.3.26'

for ((i=0; i<=END2; i++)); do
    #echo Starting HTTPERF test...
    sshpass -p "ChangeMe" ssh -o StrictHostKeyChecking=no root@${servidor05} killall -1 httperf -2 iperf -3 python
    sshpass -p "ChangeMe" ssh -o StrictHostKeyChecking=no root@${servidor05} screen -dmS http$cadeia "python -m SimpleHTTPServer $(($i+20000))"
    #sshpass -p "ChangeMe" ssh -o StrictHostKeyChecking=no root@${servidor06} killall -1 httperf -2 iperf -3 python
    #sshpass -p "ChangeMe" ssh -o StrictHostKeyChecking=no root@${servidor06} screen -dmS http$cadeia "python -m SimpleHTTPServer $(($i+20000))"
    if [ $i -lt $END2 ]; then
        sshpass -p "ChangeMe" ssh root@${cliente05} "httperf --server $servidor05 --port $(($i+20000)) --num-conns=1000 -v 2> /dev/null | grep 'Connection rate'" | awk '{print $3;}' | tr '\n' ',' >> $1
        #sshpass -p "ChangeMe" ssh root@${cliente05} "httperf --server $servidor05 --port $(($i+20000)) --num-conns=1000 -v 2> /dev/null | grep 'Connection rate'" | awk '{print $3;}' | tr '\n' ',' >> leo-10a20000regras-iptables-onenode-HTTPERF.csv
        #sshpass -p "ChangeMe" ssh root@${cliente05} "httperf --server $servidor06 --port $(($i+20000)) --num-conns=1000 -v 2> /dev/null | grep 'Connection rate'" | awk '{print $3;}' | tr '\n' ',' >> leo-10a20000regras-iptables-twonodes-HTTPERF.csv
    #    echo HTTPERF Test $i na port $(($i+20000))
        sleep 1
    else
    #    echo HTTPERF Test $i on port $(($i+20000))
        sshpass -p "ChangeMe" ssh root@${cliente05} "httperf --server $servidor05 --port $(($i+20000)) --num-conns=1000 -v 2> /dev/null | grep 'Connection rate'" | awk '{print $3;}' >> $1
        #sshpass -p "ChangeMe" ssh root@${cliente05} "httperf --server $servidor05 --port $(($i+20000)) --num-conns=1000 -v 2> /dev/null | grep 'Connection rate'" | awk '{print $3;}' >> leo-10a20000regras-iptables-onenode-HTTPERF.csv
        #sshpass -p "ChangeMe" ssh root@${cliente05} "httperf --server $servidor06 --port $(($i+20000)) --num-conns=1000 -v 2> /dev/null | grep 'Connection rate'" | awk '{print $3;}' >> leo-10a20000regras-iptables-twonodes-HTTPERF.csv
        sleep 1
    fi
    sleep 3
done



   #sshpass -p "ChangeMe" ssh -o StrictHostKeyChecking=no root@${cliente05} export servidor05='10.170.3.26'
   #sshpass -p "ChangeMe" ssh -o StrictHostKeyChecking=no root@${cliente05} export servidor06='10.240.116.142'

 #nc-latency
   #echo Starting nc-latency test on chain $i ...
   for j in {1..100}; do
      if [ $j -lt 100 ]; then
         { sshpass -p "ChangeMe" ssh root@${cliente05} "time nc -zw 5 $servidor05 $(($i+20000))"; } |& grep real | awk '{print $2;}' | tr '\n' ',' >> $2
         #{ sshpass -p "ChangeMe" ssh root@${cliente05} "time nc -zw 5 $servidor05 $(($i+20000))"; } |& grep real | awk '{print $2;}' | tr '\n' ',' >> leo-10a20000regras-iptables-onenode-RTT.csv
         #{ sshpass -p "ChangeMe" ssh root@${cliente05} "time nc -zw 5 $servidor06 $(($i+20000))"; } |& grep real | awk '{print $2;}' | tr '\n' ',' >> leo-10a20000regras-iptables-twonodes-RTT.csv
      else
         { sshpass -p "ChangeMe" ssh root@${cliente05} "time nc -zw 5 $servidor05 $(($i+20000))"; } |& grep real | awk '{print $2;}' >> $2
         #{ sshpass -p "ChangeMe" ssh root@${cliente05} "time nc -zw 5 $servidor05 $(($i+20000))"; } |& grep real | awk '{print $2;}' >> leo-10a20000regras-iptables-onenode-RTT.csv
         #{ sshpass -p "ChangeMe" ssh root@${cliente05} "time nc -zw 5 $servidor06 $(($i+20000))"; } |& grep real | awk '{print $2;}' >> leo-10a20000regras-iptables-twonodes-RTT.csv
      fi
    #  if [ $(($j % 10)) -eq 0 ]; then
    #     echo chain-$i nc $j/100
    #  fi
      sleep 1
   done

   sshpass -p "ChangeMe" ssh -o StrictHostKeyChecking=no root@${servidor05} killall python
   sshpass -p "ChangeMe" ssh -o StrictHostKeyChecking=no root@${servidor06} killall python

   #tacker sfc-classifier-create --name classifierNSHflow-$(($i+20000)) --chain cadeia-uma-vnf --match source-port=0,dest_port=$(($i+20000)),protocol=17 

# iperf
   #echo Starting IPERF Test on chain $i ...
   sshpass -p "ChangeMe" ssh -o StrictHostKeyChecking=no root@${servidor05} screen -dmS iperf${i} "iperf -su -p $(($i+20000))"
   #sshpass -p "ChangeMe" ssh -o StrictHostKeyChecking=no root@${servidor06} screen -dmS iperf${i} "iperf -su -p $(($i+20000))"
   sleep 5
   bw=1000m
   for j in {1..10}; do
      if [ $j -lt 10 ]; then
         sshpass -p "ChangeMe" ssh root@${cliente05} "iperf -c $servidor05 -p $(($i+20000)) -b ${bw} -u -m -l 1470 | grep '%)'" | awk '{print $7;}' | tr '\n' ',' >> $3
         #sshpass -p "ChangeMe" ssh root@${cliente05} "iperf -c $servidor05 -p $(($i+20000)) -b ${bw} -u -m -l 1470 | grep '%)'" | awk '{print $7;}' | tr '\n' ',' >> leo-10a20000regras-iptables-onenode-THROUGHPUT.csv
         #sshpass -p "ChangeMe" ssh root@${cliente05} "iperf -c $servidor06 -p $(($i+20000)) -b ${bw} -u -m -l 1470 | grep '%)'" | awk '{print $7;}' | tr '\n' ',' >> leo-10a20000regras-iptables-twonodes-THROUGHPUT.csv
      else
         sshpass -p "ChangeMe" ssh root@${cliente05} "iperf -c $servidor05 -p $(($i+20000)) -b ${bw} -u -m -l 1470 | grep '%)'" | awk '{print $7;}' >> $3
         #sshpass -p "ChangeMe" ssh root@${cliente05} "iperf -c $servidor05 -p $(($i+20000)) -b ${bw} -u -m -l 1470 | grep '%)'" | awk '{print $7;}' >> leo-10a20000regras-iptables-onenode-THROUGHPUT.csv
         #sshpass -p "ChangeMe" ssh root@${cliente05} "iperf -c $servidor06 -p $(($i+20000)) -b ${bw} -u -m -l 1470 | grep '%)'" | awk '{print $7;}' >> leo-10a20000regras-iptables-twonodes-THROUGHPUT.csv
      fi
     # echo IPERF $j/10
      sleep 3
   done

# Final Test Flag
  #iptables-restore < /root/testes/iptables-original
  #echo Iptables restaurado
  echo 10
