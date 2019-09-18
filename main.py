import os
import sys
import time

def read_buf(file_path):
    buf = []
    sz = 0
    with open (file_path) as f:
        for line in f.readlines():
            if sz > SIZE_BOUND:
                yield buf
                buf = []
                sz = 0
            else:
                sz += len (line)
                buf.append(line)
    if len(buf) > 0:
        yield buf


def write_buf (path, buf):
    with open (path, 'a') as f:
        f.write("".join(buf))


if __name__ == '__main__':
    SIZE_BOUND = 1 * 2 ** 20 # File size for split
    # SIZE_BOUND = 128 # File size for split
    path = sys.argv[1]
    if not os.path.exists(path):
        print("Bad path" )
        exit(1)
    res_dir = path + "\\" + str(time.time())
    print (res_dir)
    try:
        os.mkdir(res_dir)
    except OSError:
        print("Creation of the directory failed")
    print (f"Result directory is {res_dir}")

    for file in os.listdir(path):
        filename = os.fsdecode(file)
        if filename.endswith('.trc') and os.stat(path +"\\"+ filename).st_size > 1024:
            print (os.stat(path +"\\"+ filename).st_size )
            buf_num = 1
            for buf in  read_buf  (path +"\\"+ filename):
                f_name = f"{res_dir}\\{filename}_part_{buf_num}"
                write_buf(f_name, buf)
                buf_num += 1


