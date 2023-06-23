import asyncio
import pulsectl_asyncio
import pulsectl
import signal
from contextlib import suppress
from asyncio_channel import create_channel


def print_events(ev):
    print('Pulse event:', ev)
    print(dir(ev))
    ### Raise PulseLoopStop for event_listen() to return before timeout (if any)
    # raise pulsectl.PulseLoopStop
    if ev.facility == pulsectl.PulseEventFacilityEnum.sink_input:
        print("input")
    elif ev.facility == pulsectl.PulseEventFacilityEnum.source_output:
        source_output = pulse.source_list()[ev.index]
        print("output", source_output)


async def display(ch, source_name, sink_name, N=30):
    source_level = 0
    sink_level = 0

    print("Monitor", source_name, sink_name)

    async for msg in ch:
        (name, level) = msg
        if name == source_name:
            source_level = level
        elif name == sink_name:
            sink_level = level
        else:
            continue

        print('\x1b[2K\x1b[0E', end='')  # return to beginning of line
        source_num_o = round(source_level * N)
        sink_num_o = round(sink_level * N)
        print('MIC', 'O' * source_num_o + '-' * (N-source_num_o), end='', flush=True)
        print('/', 'X' * sink_num_o + '-' * (N-sink_num_o), end='', flush=True)

        
async def listen(ch, pulse: pulsectl_asyncio.PulseAsync, name: str):
    async for level in pulse.subscribe_peak_sample(name, rate=5):
        await ch.put((name, level))

 
async def main():
    ch = create_channel()
    async with pulsectl_asyncio.PulseAsync('listener') as pulse:
        # Get name of monitor_source of default sink
        server_info = await pulse.server_info()
        default_sink_info = await pulse.get_sink_by_name(server_info.default_sink_name)
        default_source_info = await pulse.get_source_by_name(server_info.default_source_name)
        sink_name = default_sink_info.monitor_source_name
        source_name = default_source_info.name

        cleanup = []
        try:

            # Start listening/monitoring task
            source_task = loop.create_task(listen(ch, pulse, source_name))
            sink_task = loop.create_task(listen(ch, pulse, sink_name))
            display_task = loop.create_task(display(ch, source_name, sink_name))

            tasks = [source_task, sink_task, display_task]

            #output_mod = await pulse.module_load('module-null-sink', args='sink_name=mywiretap1 channels=2 sink_properties=device.description="wiretap1"')
            #cleanup.append(output_mod)

            #output_mod = await pulse.module_load('module-null-sink', args='sink_name=mywiretap2 channels=2 sink_properties=device.description="wiretap2"')
            #cleanup.append(output_mod)

            #output_mod = await pulse.module_load('module-loopback', args='sink=mywiretap1 channel_map=mono,mono source=%s' % source_name)
            #cleanup.append(output_mod)
            #output_mod = await pulse.module_load('module-loopback', args='sink=mywiretap1 channel_map=mono,mono source=%s' % sink_name)
            #cleanup.append(output_mod)

            # register signal handlers to cancel listener when program is asked to terminate
            # Alternatively, the PulseAudio event subscription can be ended by breaking/returning from the `async for` loop
            for sig in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
                for task in tasks:
                    loop.add_signal_handler(sig, task.cancel)

            with suppress(asyncio.CancelledError):
                await asyncio.gather(*tasks)
                print()

        finally:
            for mod in reversed(cleanup):
                print("unloading %s" % mod)
                await pulse.module_unload(mod)

        print("EXIT1")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
print("EXIT2")



