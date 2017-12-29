from glob import glob


for f in glob('logs/*'):
    print("opening file: {}".format(f))
    with open(f, 'r') as file:
        print(file.read())
