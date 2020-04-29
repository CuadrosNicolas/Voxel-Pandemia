import os
import time


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(
            f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap


def exec_base():
    os.system("go run base/main.go > output_basic.txt")


def exec_main():
    os.system("go run main/main.go > output_main.txt")


def main():
    exec_base()
    exec_main()
    # Use diff on results from each program to verify the main algorithm validity.
    os.system("diff ./output_main.txt ./output_basic.txt")
    os.system("rm ./output_*")


if __name__ == "__main__":
    main()
