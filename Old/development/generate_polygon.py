
import time

data = [
    [38.8781548838115,-77.3764300346375],
    [38.8795413373583,-77.3796486854553],
    [38.877570226617,-77.3796057701111],
    [38.8764343074595,-77.3767948150635],
    [38.8769521552097,-77.3733186721802],
    [38.8783720409729,-77.3724174499512],
    [38.8798420104618,-77.3733830451965],
    [38.8809945789057,-77.3758506774902],
    [38.8809611713878,-77.3782968521118],
    [38.8795413373583,-77.3796486854553]
]

def open_file():
    global f
    if var == 1:
        filename = 'test.poly'
    else:
        filename = 'test.fen'
    try:
        f = open(filename, 'w+')  # Write to file, if file doesn't exist, create new
    except FileNotFoundError as e:
        print(e)

def create_file():
    for i in data:
        toAdd = str(i[0]) + " " + str(i[1])
        f.write(toAdd + "\n")
    f.close()

if __name__ == "__main__":
    global var
    var = input("Create polygon (1) or geofence (2)? ")
    open_file()
    create_file()
