#!/usr/bin/env bash
set -x

SOURCE1=$(pactl get-default-sink)
SOURCE2=$(pactl get-default-source)
echo ${SOURCE1} ${SOURCE2}

pactl load-module module-null-sink sink_name=mywiretap1 channels=2 sink_properties=device.description="wiretap1" rate=16000
pactl load-module module-null-sink sink_name=mywiretap2 channels=1 sink_properties=device.description="wiretap2" rate=16000
#pactl load-module module-null-sink sink_name=output channels=2 sink_properties=device.description="output" rate=16000
pactl load-module module-loopback sink=mywiretap1 source="${SOURCE1}.monitor" remix=yes channels=2
pactl load-module module-loopback sink=mywiretap2 source="${SOURCE2}" remix=yes
#pactl load-module module-combine-sink sink_name=combine1 sink_properties=device.description=combine1 slaves=mywiretap1,mywiretap2 channels=2 resample_method=src-sinc-best-quality
#pactl load-module module-combine-sink sink_name=combine2 sink_properties=device.description=combine2 channels=4 resample_method=src-sinc-best-quality slaves=mywiretap1,mywiretap2,${SOURCE1},alsa_output.usb-Elite_Silicon_USB_Audio_Device-00.analog-stereo #,${SOURCE2}.monitor
#,mywiretap2,mywiretap1 channels=3 resample_method=src-sinc-best-quality
#pactl load-module module-combine-sink sink_name=combine3 sink_properties=device.description=combine3 slaves=mywiretap2 # ${SOURCE1} #,mywiretap2,mywiretap1 channels=3 resample_method=src-sinc-best-quality
#pactl load-module module-remap-source source_name=remap master=outout remix=no

