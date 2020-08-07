# ArmPi Qemu Image
https://github.com/waldo-irc/ArmPi

#### A qemu/chroot whose sole purpose it is to reverse engineer ARM Binaries.

#### NOTES
1. It is old and will be updated soon.  It was made with an RPI Zero in mind for portability but will likely be upgraded to an RPI4.
2. The QEMU image is slow due to memory limiates, theres are 2 PDB files, one thats quite limited and another one with an unknown limit.  The unknown one could feasibly go pretty high to speed it up in QEMU.
3. The CHROOT is fast but the web portal doesn't work.  Does run binaries with no issues in GDB GEF.
4. Bugs here or there to resolves
5. Plans to move to node as it's faster and more compact than PHP

![ArmPI Image](https://raw.githubusercontent.com/waldo-irc/ArmPi/master/chroot.png)