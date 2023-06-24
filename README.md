Some scripts for recording with PulseAudio on Linux

Take the default speaker, and the default microphone, and reduce them down to a single stereo channel.  The left channel is a mixed version of the stereo speaker, and the right channel is the microphone.  The resulting channel can be recorded using ffmpeg.

```
# Setup PulseAudio channels
make channels

# record to MP3
make record
```

Some helpful references:
- https://trac.ffmpeg.org/wiki/AudioChannelManipulation


