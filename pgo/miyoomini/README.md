# PGO profile for the Miyoo Mini build (Koriki)

`profile/` is the GCC 8.3 profile (`.gcda`) of `snes9x2005_plus` (blargg APU) running six
games for 2400 frames each with buttons pressed: Star Fox, Yoshi's Island, Super Mario World,
Donkey Kong Country, Kirby Super Star and Super Mario Kart (SuperFX, SuperFX 2, SA-1 and
DSP-1 included). The `.gcda` of objects that never ran (Cx4, S-DD1, SETA, OBC1, cheats...)
were deleted (`prune_gcda.py`), so GCC compiles them as usual instead of as cold code.

    make platform=miyoomini USE_BLARGG_APU=1          # PGO + LTO (default)
    make platform=miyoomini USE_BLARGG_APU=1 PGO=0    # LTO only

Measured (guest instructions under qemu-arm, 1200 frames after 60 of boot; video and audio
CRCs identical between the builds), speed against the plain -O2 build:

| Game | PGO + LTO |
|---|---|
| Yoshi's Island (Rev 1) | +10 % |
| Super Mario World | +12 % |
| Stunt Race FX | +11 % |
| Super Metroid | +9 % |
| F-Zero | +8 % |
| Super Mario RPG | +10 % |

## Recording it again (after changing the sources)

The profile can be recorded on the console or under `qemu-arm` (user mode): emulation is
deterministic, so both give the same counters (checked: the qemu profile builds a core with
exactly the same instruction count as the one recorded on a Miyoo Mini Plus).

1. `make clean; make platform=miyoomini USE_BLARGG_APU=1 PGO=generate PGO_DIR=/tmp/pgo_snes`
2. `arm-linux-gnueabihf-gcc -O2 -I libretro-common/include -o lrbench pgo/miyoomini/lrbench.c -ldl`
3. Run every game of `snes_train.lst` for 2400 frames with `LR_RATE=48000 LR_KEYS=1`:
   on the console copy the core, `lrbench`, `common.sh`, `snes.sh` and `snes_train.lst` to `/tmp/sb`
   and run `TRAIN=1 /tmp/sb/snes.sh /tmp/sb/snes_train.lst 2400 /tmp/sb/snes9x2005_plus_libretro.so`;
   with qemu: `qemu-arm -L <sysroot> ./lrbench snes9x2005_plus_libretro.so <rom> 2400 <core .opt>`.
4. `python3 pgo/miyoomini/prune_gcda.py /tmp/pgo_snes`, replace `profile/` with it,
   `make clean` and build again.

`snes.sh LIST FRAMES core...` without `TRAIN=1` is the benchmark on the console (1200 MHz
fixed, SimpleMenu paused); `lrbench` prints fps and CRCs of the video and audio output.
