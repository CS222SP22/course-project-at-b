import sys

if len(sys.argv) != 2:
    print("Usage: " + argv[0] + "[link]")
else:
    L = [sys.argv[1]]
    # writing to file
    file1 = open('lines.txt', 'w')
    file1.writelines(L)
    file1.close()