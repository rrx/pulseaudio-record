FILENAME = $(shell date +'%FT%H%M%S')

default:

setup:
	python patest.py

record3:
	ffmpeg \
		-fflags nobuffer -flags low_delay -strict experimental -async 1 \
		-thread_queue_size 4096 \
		-channel_layout mono -ac 1 -f pulse -i mywiretap1.monitor \
		-thread_queue_size 4096 \
		-channel_layout mono -f pulse -i mywiretap2.monitor \
		-filter_complex "[0:a][1:a]join=inputs=2:channel_layout=stereo[a]" -map "[a]" out-$(FILENAME).mp3

clean:
	rm *.wav


