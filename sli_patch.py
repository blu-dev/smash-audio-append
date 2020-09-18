import zlib
import sys
import os
import struct

def readu64le(file):
    return struct.unpack(b"<Q", file.read(8))[0]

def readu32le(file):
    return struct.unpack(b"<I", file.read(4))[0]

def gen_hash40(label):
    return (len(label) << 32) | zlib.crc32(bytes(label, 'utf8'))

filepath = input("Enter the filepath to soundlabelinfo.sli: ")
assert os.path.exists(filepath), "File not found: " + str(filepath)
sli = open(filepath, u'rb+')
if sli.read(3) != b"SLI":
    print("Invalid file. No SLI header")
    exit()
sli.seek(4)
if readu32le(sli) != 0x01:
    print("Invalid file. Improper SLI header")
    exit()
sli.seek(8)
count = readu32le(sli)
new_sound_label = input("Enter the new sound label: ")
new_hash = gen_hash40(new_sound_label)
new_index = int(input("Enter the index of the new sound label in the NUS3Bank: "))
comp_label = input("Enter a comparable sound label (from the same NUS3Bank): ")
comp_hash = gen_hash40(comp_label)
new_offset = 0
comp_offset = 0
sli.seek(0xC)
for x in range(0, count):
    sli.seek(0x10 * x + 0xC)
    hash40 = readu64le(sli)
    if hash40 == comp_hash:
        comp_offset = x
    elif hash40 == new_hash:
        print("The new sound label already exists in the table.")
        exit()
    elif (hash40 > new_hash) and (new_offset == 0):
        new_offset = x
    if (comp_offset != 0) and (new_offset != 0):
        break
if comp_offset == 0:
    print("The comparable sound label could not be found in the table.")
    exit()
if new_offset == 0:
    new_offset = count
sli.seek(0)
original_data = sli.read()
sli.close()
comp_data = original_data[(0xC + 0x10 * comp_offset + 0x8):(0xC + 0x10 * comp_offset + 0xC)]
extension_index = filepath.find('.')
if extension_index == -1:
    sli = open(filepath + "_appended", u'wb+')
else:
    sli = open(filepath[:extension_index] + "_appended" + filepath[extension_index:], u'wb+')
sli.write(b"SLI")
sli.write(struct.pack(b"B", 0))
sli.write(struct.pack(b"<I", 0x1))
sli.write(struct.pack(b"<I", count + 1))
if new_offset == count:
    sli.write(original_data[0xC:])
    sli.write(struct.pack(b"<Q", new_hash))
    sli.write(comp_data)
    sli.write(struct.pack(b"<I", new_index))
else:
    sli.write(original_data[0xC:(0xC + 0x10 * new_offset)])
    sli.write(struct.pack(b"<Q", new_hash))
    sli.write(comp_data)
    sli.write(struct.pack(b"<I", new_index))
    sli.write(original_data[(0xC + 0x10 * new_offset):])
print("Added sound label", new_sound_label, "(", hex(new_hash), ") to", filepath, "owo")
