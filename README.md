# FDC-project

export DISPLAY=$(grep nameserver /etc/resolv.conf | awk '{print $2}'):0.0  