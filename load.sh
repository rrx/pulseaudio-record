#!/usr/bin/env bash
set -x

SINK=$(pactl get-default-sink)
SOURCE=$(pactl get-default-source)
echo DEFAULT_SINK: ${SOURCE1}
echo DEFAULT_SOURCE: ${SOURCE2}

pactl load-module module-null-sink sink_name=mywiretap1 channels=2 sink_properties=device.description="wiretap1" rate=16000
pactl load-module module-null-sink sink_name=mywiretap2 channels=1 sink_properties=device.description="wiretap2" rate=16000
pactl load-module module-loopback sink=mywiretap1 source="${SINK}.monitor" remix=yes channels=2
pactl load-module module-loopback sink=mywiretap2 source="${SOURCE}" remix=yes
