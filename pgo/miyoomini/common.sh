# common.sh: env for lrbench runs; fix 1200 MHz and pause the frontend + screentest unless TRAIN=1
export LD_LIBRARY_PATH=/mnt/SDCARD/Koriki/lib:/lib:/config/lib:/customer/lib LR_RATE=48000 LR_KEYS=1 LR_SYSDIR=/mnt/SDCARD/BIOS
CF=/sys/devices/system/cpu/cpu0/cpufreq; G=$(cat $CF/scaling_governor)
SM=$(pidof simplemenu); ST=$(pidof screentest)
start() { [ -z "$TRAIN" ] && { echo userspace > $CF/scaling_governor; echo 1200000 > $CF/scaling_setspeed; }
  [ -n "$SM" ] && kill -STOP $SM; [ -n "$ST" ] && kill -STOP $ST; }
stop() { [ -n "$ST" ] && kill -CONT $ST; [ -n "$SM" ] && kill -CONT $SM; [ -z "$TRAIN" ] && echo $G > $CF/scaling_governor; }
