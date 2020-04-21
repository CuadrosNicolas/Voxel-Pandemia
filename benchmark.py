import os
import time

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap

@timing
def exec_base():
    os.system("python3 main_base.py > output_basic.txt")

@timing
def exec_main():
    os.system("python3 main.py > output_main.txt")

def main():
    exec_base()
    exec_main()
    os.system("rm ./output_*")

if __name__ == "__main__":
    main()