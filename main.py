import time

sbox = [
    [
        "63", "7c", "77", "7b", "f2", "6b", "6f", "c5", "30", "01", "67", "2b",
        "fe", "d7", "ab", "76"
    ],
    [
        "ca", "82", "c9", "7d", "fa", "59", "47", "f0", "ad", "d4", "a2",
        "af", "9c", "a4", "72", "c0"
    ],
    [
        "b7", "fd", "93", "26", "36", "3f", "f7", "cc", "34", "a5", "e5",
        "f1", "71", "d8", "31", "15"
    ],
    [
        "04", "c7", "23", "c3", "18", "96", "05", "9a", "07", "12", "80",
        "e2", "eb", "27", "b2", "75"
    ],
    [
        "09", "83", "2c", "1a", "1b", "6e", "5a", "a0", "52", "3b", "d6",
        "b3", "29", "e3", "2f", "84"
    ],
    [
        "53", "d1", "00", "ed", "20", "fc", "b1", "5b", "6a", "cb", "be",
        "39", "4a", "4c", "58", "cf"
    ],
    [
        "d0", "ef", "aa", "fb", "43", "4d", "33", "85", "45", "f9", "02",
        "7f", "50", "3c", "9f", "a8"
    ],
    [
        "51", "a3", "40", "8f", "92", "9d", "38", "f5", "bc", "b6", "da",
        "21", "10", "ff", "f3", "d2"
    ],
    [
        "cd", "0c", "13", "ec", "5f", "97", "44", "17", "c4", "a7", "7e",
        "3d", "64", "5d", "19", "73"
    ],
    [
        "60", "81", "4f", "dc", "22", "2a", "90", "88", "46", "ee", "b8",
        "14", "de", "5e", "0b", "db"
    ],
    [
        "e0", "32", "3a", "0a", "49", "06", "24", "5c", "c2", "d3", "ac",
        "62", "91", "95", "e4", "79"
    ],
    [
        "e7", "c8", "37", "6d", "8d", "d5", "4e", "a9", "6c", "56", "f4",
        "ea", "65", "7a", "ae", "08"
    ],
    [
        "ba", "78", "25", "2e", "1c", "a6", "b4", "c6", "e8", "dd", "74",
        "1f", "4b", "bd", "8b", "8a"
    ],
    [
        "70", "3e", "b5", "66", "48", "03", "f6", "0e", "61", "35", "57",
        "b9", "86", "c1", "1d", "9e"
    ],
    [
        "e1", "f8", "98", "11", "69", "d9", "8e", "94", "9b", "1e", "87",
        "e9", "ce", "55", "28", "df"
    ],
    [
        "8c", "a1", "89", "0d", "bf", "e6", "42", "68", "41", "99", "2d",
        "0f", "b0", "54", "bb", "16"
    ]
]



def converttobinary(a):
    return oc(bin(ord(a) ^ key).replace("0b", "").zfill(8)[::-1])


def oc(c):
    r = ""
    for i in range(len(c)):
        if (c[i] == '1'):
            r += '0'
        else:
            r += '1'
    return division(r)


def division(k):
    val1 = ""
    val2 = ""

    for i in range(len(k)):
        if (i <= 3):
            val1 += k[i]
        else:
            val2 += k[i]

    a = int(val1, 2)
    b = int(val2, 2)

    return (sbox[a][b])


def encode(data):

    arr = ""

    for i in range(len(data)):
        x = converttobinary(data[i])
        arr += x

    arr = arr + data[len(data):]

    return arr


def doc(c):
    r = ""
    for i in range(len(c)):
        if (c[i] == '1'):
            r += '0'
        else:
            r += '1'
    return r


def sboxs(a):
    for i in range(len(sbox)):
        for j in range(len(sbox)):
            if (sbox[i][j] == a):
                k = bin(i).replace("0b", "").zfill(4)
                l = bin(j).replace("0b", "").zfill(4)
                final = k + l
                final = doc(final)
                final = final[::-1]
                final = chr(int(final, 2) ^ key)
                return final


def decode(arr):
    decoded_string = ""
    for i in range(0, len(arr), 2):
        joining = ""
        if i == len(arr) - 1:
            joining = arr[i]
        else:
            j, k = arr[i:i + 2]
            joining = j + k
        decoded_string = decoded_string + sboxs(joining)
    return decoded_string


def print_string(s):
    print("--------------------ENCRYPTED/DECRYPTED STRING-------------------")
    print()
    print(s)
    print()


def store_decoded_str(s):
    fd = open("decode.dec", mode="w")
    fd.write(s)
    fd.close()


def store_encoded_str(s):
    fd = open("encode.enc", mode="w")
    fd.write(s)
    fd.close()


key = int(input("Enter key: "))

encoded_str = ""
decoded_str = ""
choice = -1

print("|-------------------ENCRYPTION/DECRYPTION--------------------|")
print("|  Choose your option:                                       |")
print("|  Press 1 to enter the data                                 |")
print("|  Press 2 to enter the file name                            |")
print("|  press 3 for encryption                                    |")
print("|  press 4 for decryption                                    |")
print("|  press 5 to exit                                           |")
print("|------------------------------------------------------------|")
"""file handeling code for decoding check if file exist and it is not empty"""

while choice != 5:

    choice = int(input("ENTER CHOICE: "))
    # print(choice)
    print()
    start_time = time.time()

    if (choice == 1):
        y = input("Enter your data: ")
        f = open("your_data.txt", mode="w")
        f.write(y)
        f.close()
        f = open("your_data.txt", mode="r")
        data = f.read()

    elif (choice == 2):
        y = input("Enter file name:  ")
        f = open(y, mode="r")
        data = f.read()

    elif choice == 3:

        print("ENCRPTING DATA ...")
        # call encryption function

        encoded_str = encode(data)
        print_string(encoded_str)
        print(
            "---------------ENCRYPTED FILE SAVED IN THE DIRECTORY-------------------"
        )
        print()
        print("--- Time to encrypt %s seconds ---" %
              (time.time() - start_time))
        store_encoded_str(encoded_str)
        print()
        print("-------------------------------------------------------------")
        print()
        print("To decrypt press 4")
        print()

    elif choice == 4:
        # call decryption function
        print("DECRYPTING STRING PLEASE WAIT...")
        print()
        if len(encoded_str) == 0:
            print("encrypt the data first then decrypt!! try again!!")
            break

        decoded_str = decode(encoded_str)
        print_string(decoded_str)
        print("---------------SAVING DECRYPTED FILE-------------------")
        print()
        print("--- Time to decrypt %s seconds ---" %
              (time.time() - start_time))
        store_decoded_str(decoded_str)
        print()
        print("-------------------------------------------------------------")
        print()

    elif choice == 5:
        break
    else:
        print("Entered wrong choice!!try again!!")
