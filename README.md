# TinyUSB USB Audio Capture Examples for Alif Semiconductor Ensemble E7

USB Audio Class 2.0 (UAC2) capture ("microphone") examples for the
[Alif Semiconductor](https://www.alifsemi.com) Ensemble **E7 DevKit**
(`AE722F80F55D5LS`), built on [TinyUSB](https://github.com/hathach/tinyusb).

The repository contains the same USB audio demo in three flavours — bare-metal,
FreeRTOS and Zephyr — so that the Alif Ensemble USB device controller can be
exercised from each of those environments. All three enumerate as a 1-channel,
16-bit, 48 kHz USB microphone and stream a synthetic test signal to the host
over an isochronous IN endpoint.

| | |
|---|---|
| **Target device** | Alif Ensemble `AE722F80F55D5LS`, Cortex-M55 HP and HE cores |
| **Target board** | Alif Ensemble E7 DevKit (`DevKit-E7`, Generation 2 variant) |
| **USB stack** | TinyUSB, Alif Ensemble device controller driver (`dcd_ensemble.c`) |
| **USB class** | USB Audio Class 2.0, isochronous IN (capture only) |
| **Published by** | Sirin Software, with Alif Semiconductor's permission |
| **Status** | Development snapshot, provided as-is — see below |

---

## Publication and collaboration statement

These examples were developed as part of the collaboration between **Sirin
Software** and **Alif Semiconductor**, and are published by Sirin Software with
Alif Semiconductor's permission.

This repository is **not** an official Alif Semiconductor examples repository.

## Snapshot / As-Is

> This repository provides **development snapshots** for the Alif Semiconductor
> Ensemble platform. They are provided **as-is** for demonstration and development
> purposes and should be considered snapshots rather than finalized demos.
>
> Customer support is not provided for these snapshots. Future finalized versions
> may be supported separately.

---

## Examples at a glance

| Example | What it demonstrates | Environment | Build system |
|---|---|---|---|
| [`audio_test`](#audio_test-bare-metal) | UAC2 microphone streaming a synthetic ramp signal over isochronous IN | Bare metal (super-loop) | CMSIS solution (`csolution`) |
| [`audio_test_freertos`](#audio_test_freertos) | The same UAC2 device with the TinyUSB device stack running in a FreeRTOS task | FreeRTOS (CMSIS-FreeRTOS 11.2.0 pack) | CMSIS solution (`csolution`) |
| [`audio_test_zephyr`](#audio_test_zephyr) | The same UAC2 device with TinyUSB (not Zephyr's own USB stack) on Zephyr | Zephyr RTOS | `west` / CMake |

All three examples share the same USB behaviour, descriptors and test signal.
They differ only in how the TinyUSB device task and the LED blinker are
scheduled.

---

## Target Setup Requirements

### Hardware

- **Alif Ensemble E7 DevKit Gen2**
- **2× Micro-USB cables** (one included with the DevKit)
- A **host computer** (Linux, macOS or Windows) with terminal emulation software
- Optional: **JTAG debugger**, such as SEGGER J-Link or Arm ULINKpro

### USB Connections

The DevKit provides two Micro-USB interfaces used by the examples:

#### PRG USB

Connect a USB cable from the host computer to the **PRG USB** connector.

This interface provides a two-channel USB-to-UART adapter:
- used by the SETOOLS applications to program images into MRAM.
- used for example debug output. The examples configure it as 115200 baud, 8-N-1.

#### SoC USB

Connect the second USB cable from the host computer to the SoC USB connector.

This interface is connected directly to the Ensemble SoC and is used by the USB examples
for communication with the host computer.

### GPIO used by the examples

| Function | Board definition | GPIO |
|---|---|---|
| Status LED | `BOARD_LEDRGB1_R_*` | GPIO port 6, pin 2 (RGB LED 1, red) |

---

## Getting started

Clone with submodules

```bash
git clone --recurse-submodules <repository-url>
```
Pick a build flow

| Flow | Examples | Section |
|---|---|---|
| CMSIS solution (`csolution` / VS Code) | `audio_test`, `audio_test_freertos` | [below](#a-cmsis-solution-build-vs-code--cmsis-toolbox) |
| Zephyr / `west` | `audio_test_zephyr` | [below](#b-zephyr-build) |

---

## CMSIS solution build (VS Code / CMSIS-Toolbox)

This is the flow the repository is primarily set up for. It builds the
bare-metal and FreeRTOS examples.

### Prerequisites

- VS Code with the recommended extensions:
  `arm.environment-manager`, `arm.cmsis-csolution`,
  `ms-vscode.cpptools-extension-pack`, `marus25.cortex-debug`.
- The tools installed by the Arm Environment Manager: CMake ≥ 3.28.4,
  Ninja ≥ 1.12.0,`arm-none-eabi-gcc` ≥ 13.2.1-0, CMSIS-Toolbox ≥ 2.6.1.
- CMSIS packs (installed by the task below): `ARM::CMSIS@6.2.0`,
  `ARM::CMSIS-FreeRTOS@11.2.0`, `AlifSemiconductor::Ensemble@2.0.2`.
- For the Security Toolkit programming tasks: the Alif Security Toolkit
  (SETOOLS) installed locally.

Setting up the Alif VS Code environment itself is documented by Alif in the
[VS Code Getting Started Template](https://github.com/alifsemi/alif_vscode-template);
follow that first.

### Build

1. Open the repository folder in VS Code (**File → Open Folder**).
2. When the **Arm Environment Activation** prompt appears, choose
   **Allow For Current Workspace**.
3. **F1 → Tasks: Run Task → First time pack installation** (only needed once
   per machine; it runs `cpackget` to install the three CMSIS packs listed above).
4. **F1 → CMSIS: Manage Solution Settings** and select
   - a target type: `E7-HP` (Cortex-M55 High Performance core) or `E7-HE`
     (High Efficiency core), and
   - a project: `audio_test` (bare metal) or `audio_test_freertos`.
5. Build with the CMSIS extension's build (hammer) button, or
   **F1 → Tasks: Run Task → cmsis-csolution.build: Build**.

Build types are `release` (`-O speed`) and `debug` (`-O none`).
GCC is the selected compiler.

### Output location

```
out/<project>/<target>/<build-type>/<project>.elf
out/<project>/<target>/<build-type>/<project>.bin
```

for example `out/audio_test/E7-HP/release/audio_test.elf`.

### Program the board

Two paths are pre-configured in [`.vscode/tasks.json`](.vscode/tasks.json):

**Alif Security Toolkit (writes to MRAM)**

**F1 → Tasks: Run Task → Program with Security Toolkit**.
Variants for selecting a COM port and for installing debug stubs are provided
as separate tasks.

**pyOCD over CMSIS-DAP**

**F1 → Tasks: Run Task → CMSIS Load** (or `CMSIS Load+Run`). Related tasks:
`CMSIS Run`, `CMSIS Erase`, `CMSIS TargetInfo`.

### Debug

[`.vscode/launch.json`](.vscode/launch.json) provides a J-Link configuration
("Alif Ensemble Debug (Cortex-Debug)", using
[`.alif/JLinkDevices.xml`](.alif/JLinkDevices.xml) and RTT console) and pyOCD
gdb launch/attach configurations for the M55_HP and M55_HE cores.

---

## B. Zephyr build

### Requirements

- [Zephyr SDK 0.16.9](https://github.com/zephyrproject-rtos/sdk-ng/releases/tag/v0.16.9)
- The `west` tool
- Python 3 with the Zephyr dependencies installed
- Access to the Alif Zephyr tree referenced by the manifest (see the note above)

### Install the Zephyr SDK

```bash
cd ~
wget https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.16.9/zephyr-sdk-0.16.9_linux-x86_64.tar.xz
tar xvf zephyr-sdk-0.16.9_linux-x86_64.tar.xz
cd zephyr-sdk-0.16.9
./setup.sh
```

### Build

Builds are supported for the two RTSS cores: **rtss_hp** and **rtss_he**.

```bash
python3 -m venv .venv
source ./.venv/bin/activate

pip install -U west
cd audio_test_zephyr/
west init -l .
cd ../
west update
pip install -r zephyr/scripts/requirements.txt

cd audio_test_zephyr/
west build -b alif_e7_dk/ae722f80f55d5xx/rtss_hp
```

`west update` places the Zephyr tree at the repository root (`zephyr/`), which
is where [`audio_test_zephyr/CMakeLists.txt`](audio_test_zephyr/CMakeLists.txt)
expects it. The build uses TinyUSB compiled from `lib/tinyusb` (see
[`audio_test_zephyr/cmake/tinyusb_sources.cmake`](audio_test_zephyr/cmake/tinyusb_sources.cmake))
rather than Zephyr's own USB device stack, and the board overlays in
[`audio_test_zephyr/boards/`](audio_test_zephyr/boards) enable the `alif,xhci`
USB controller node.

### Program the board

To program the board using the Alif Security Toolkit in VS Code:

1. Open the compiled binary file (`build/zephyr/zephyr.bin`) in VS Code so it is the active editor tab.

2. Press **F1 → Tasks: Run Task**, then choose the appropriate target core:
- Program opened binary file to M55_HE
- Program opened binary file to M55_HP

---

## Examples in detail

### `audio_test` (bare metal)

A USB Audio Class 2.0 capture device (a "microphone")
on the Alif Ensemble USB device controller, driven by TinyUSB with no operating
system: `main()` initialises the board and the TinyUSB device stack and then
runs `tud_task()`, the LED blinker and an (empty) audio task in a super-loop.

Audio data is produced inside the audio class callbacks rather than from a real
audio peripheral: `tud_audio_tx_done_pre_load_cb()` hands the current buffer to
`tud_audio_write()`, and `tud_audio_tx_done_post_load_cb()` refills it with an
incrementing 16-bit counter. The host therefore receives a continuously rising
ramp (a sawtooth) instead of microphone audio. The example also implements the
UAC2 control requests for mute, volume, sample-rate range and clock validity.

This example is the smallest end-to-end check that the Ensemble USB device
controller, the TinyUSB port and isochronous IN transfers work: no audio codec,
I2S or external hardware is involved, and the expected data is exactly
predictable, so a wrong or dropped packet is easy to see in a host recording.

**Run.**

1. Program the board and reset it.
2. Connect the board's **SoC USB** device connector to the host.
3. The host should enumerate a USB audio input device named **MicNode**.
4. Record from it, or run the plotting script described in
   [Checking the audio stream](#checking-the-audio-stream-on-the-host).

**Expected result.**

- The status LED blinks at **250 ms** while the device is not mounted,
  **1000 ms** once the host has enumerated and configured it, and **2500 ms**
  while the bus is suspended.
- The host lists a 1-channel, 16-bit, 48 kHz capture device called `MicNode`.
- Recorded samples form a rising ramp that wraps around, not silence and not
  noise.
- No trace output is printed by default: TinyUSB logging is off
  (`CFG_TUSB_DEBUG 0`). Raising `CFG_TUSB_DEBUG` in `tusb_config.h` sends
  TinyUSB's log to the trace UART.

---

### `audio_test_freertos`

The same UAC2 capture device as `audio_test`, with the
TinyUSB device stack running inside a FreeRTOS task instead of a super-loop.
`main()` creates a `blinky` task (priority 1) and a `usbd` task (priority
`configMAX_PRIORITIES - 1`) and starts the scheduler; the `usbd` task calls
`tusb_init()` and then loops on `tud_task()`. Tasks are created statically when
`configSUPPORT_STATIC_ALLOCATION` is enabled and dynamically otherwise. The
audio data path and the descriptors are identical to the bare-metal example.

This example shows the RTOS integration points — where the device
stack must be initialised relative to the scheduler, what task priority the USB
task needs, and which FreeRTOS features the TinyUSB port relies on — for a
class with hard timing requirements.

**Target hardware, connections, USB identity, expected LED behaviour, expected
host behaviour.** Same as [`audio_test`](#audio_test-bare-metal).

---

### `audio_test_zephyr`

The same UAC2 capture device again, this time on Zephyr,
still using TinyUSB as the USB stack (Zephyr's own USB device stack is
not used). `main()` creates a `usbd` thread at
`K_HIGHEST_APPLICATION_THREAD_PRIO - 1` with a 4 KiB stack and a `k_timer` that
drives the LED; the thread initialises TinyUSB and loops on `tud_task()`.

This example shows how to bring the Alif TinyUSB port into a Zephyr
application — the device tree overlay for the Ensemble USB controller, the
board/BSP wiring, and the CMake glue that compiles TinyUSB inside a Zephyr
build.

**Run and expected result.**

Same USB behaviour and LED patterns as the other
two examples: a `MicNode` 1-channel 16-bit 48 kHz capture device producing a
ramp signal, with the LED period reflecting mount/suspend state. Console output
depends on the Zephyr board configuration and is not produced by the example
itself.

---

## Checking the audio stream on the host

[`test/plot_audio_samples.py`](test/plot_audio_samples.py) records a short
buffer from the device and plots it, so the ramp signal can be inspected
visually. It needs the PortAudio runtime plus `sounddevice`, `matplotlib` and
`numpy`:

```bash
$ sudo apt install libportaudio2
$ pip3 install sounddevice matplotlib numpy
$ python3 test/plot_audio_samples.py
```

(The package name above is the Debian/Ubuntu one.) The captured samples are
also written to `Output.csv` in the working directory.

The script picks an input device by name per platform: `micnode` on Linux,
`Microphone (MicNode), Windows WASAPI` on Windows and `MicNode` on macOS. If it
raises `ValueError: No input device matching`, your host names the device
differently — uncomment the `print(sd.query_devices())` line near the top of the
script to list the available devices and adjust the name.

---

## Licensing

This repository contains software from multiple sources and under multiple
applicable licences. **No single licence covers the whole repository.**

- **TinyUSB source and TinyUSB-derived source** (the example sources under
  `audio_test*/src/`, `test/plot_audio_samples.py`, the CMake support files
  under `audio_test_zephyr/cmake/`, and the `lib/tinyusb` submodule except where
  noted): MIT Licence — see [`LICENSE-MIT.txt`](LICENSE-MIT.txt) and the notices
  in the individual files. The copyright notices name Ha Thach (tinyusb.org),
  Reinhard Panhuber, Jerzy Kasenberg and HiFiPhile.
- **Alif Semiconductor material** (the Ensemble device controller driver and
  Alif BSP inside `lib/tinyusb`, the `lib/alif_common-app-utils` submodule, the
  CMSIS pack configuration under `audio_test*/RTE/`, and the project scaffolding
  derived from the Alif VS Code template): the Alif Semiconductor Software
  License Agreement — see [`LICENSE-ALIF.txt`](LICENSE-ALIF.txt) and the
  notices in the individual files.
- **Other third-party components** (Arm CMSIS under Apache-2.0, the FreeRTOS
  kernel configuration under MIT, Zephyr under Apache-2.0, host-side Python
  packages): see [`THIRD_PARTY_NOTICES.txt`](THIRD_PARTY_NOTICES.txt) and the
  components' own licence files.

Modifications developed for the Alif Semiconductor platform are marked as such
in the affected files; they do not replace the upstream copyright or licence
notices in those files, which continue to apply to the original material.

---

## Support and issues

This repository is a **published snapshot**. It is maintained on a best-effort
basis by Sirin Software and is not covered by an Alif Semiconductor
customer-support commitment.

- Questions or problems with the content of **this repository** can be raised
  through this repository's issue tracker on GitHub. Opening an issue here does
  not create any support obligation for Alif Semiconductor.
- Questions about **Alif Semiconductor devices, SDKs, packs or tools** belong in
  Alif's own support channels; see [alifsemi.com](https://www.alifsemi.com).
- Questions about **TinyUSB itself** belong upstream at
  [hathach/tinyusb](https://github.com/hathach/tinyusb).

---

## References

- [Alif Ensemble E7 DevKit documentation](https://alifsemi.com/support/kits/ensemble-e7devkit/)
- [Alif VS Code Getting Started Template](https://github.com/alifsemi/alif_vscode-template)
- [TinyUSB documentation](https://docs.tinyusb.org)
- [Zephyr documentation](https://docs.zephyrproject.org)
- [CMSIS-Toolbox](https://github.com/Open-CMSIS-Pack/cmsis-toolbox)
