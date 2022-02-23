import sys
import ics_reader

filename = 'ical_links.txt'

if sys.argv[1] != "-add" and sys.argv[1] != "-read" and sys.argv[1] != "-help":
    print("ERROR: Unknown Command. Type -help for more information")
elif sys.argv[1] == "-help":
    print("Commands:")
    print("-add [link]\tadds a link to %s" % filename)
    print("-read\t\treads all ical links stored in %s" % filename)
elif sys.argv[1] == "-add" and len(sys.argv) != 3:
    print("Usage: python ics.py -add [link]")
elif sys.argv[1] == "-add":
    # writing to file
    file1 = open(filename, 'a')
    file1.writelines(sys.argv[2])
    file1.close()
    print("Added Link to Source File")
elif sys.argv[1] == "-read":
    try:
        ofs = open(filename, 'r')
    except IOError:
        print ("Could not open %s, please create file!" % filename)
    else:
        read_lines = ofs.readlines()
        event_strings = ics_reader.ReadICal(read_lines)
        for line in event_strings:
            print(line + '\n')