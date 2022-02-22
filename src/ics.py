import sys

if sys.argv[1] != "-add" and sys.argv[1] != "-read" and sys.argv[1] != "-help":
    print("ERROR: Unknown Command. Type -help for more information")
elif sys.argv[1] == "-help":
    print("Commands:")
    print("-add [link]\tadds a link to ical_links.txt")
    print("-read\t\treads all ical links stored in ical_links.txt")
elif sys.argv[1] == "-add" and len(sys.argv) != 3:
    print("Usage: python ics.py -add [link]")
elif sys.argv[1] == "-add":
    # writing to file
    file1 = open('ical_links.txt', 'w')
    L = file1.readlines()
    L.append(sys.argv[2])
    file1.writelines(L)
    file1.close()
    print("Added Link to Source File")
elif sys.argv[1] == "-read":
    import ics_reader