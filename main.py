# ===
# About: Upgrade Cipher
# Author: Zaid Mukaddam <zaidmukaddam@proton.me>
# Keywords: [basic, flask]
#
# Setup:
# FILE requirements.txt EOF
# flask
# simple-websocket
# h2o-nitro[web]
# EOF
# RUN python -m pip install -r requirements.txt
# ENV FLASK_APP main.py
# ENV FLASK_ENV development
# START python -m flask run
# ===

import simple_websocket
import os
from flask import Flask, request, send_from_directory
from h2o_nitro import View, box, option, row, Theme, header
from h2o_nitro_web import web_directory
from pymongo import MongoClient
from dotenv import load_dotenv
import re

load_dotenv()

client = MongoClient(
    os.getenv("MONGO_HOST"),
)

db = client['test-database']
user_db = db['user_data']
encrypt_db = db['encrypt_data']

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


key = 100


class Login:
    def __init__(self, name, email, region) -> None:
        self.email = email
        self.name = name
        self.region = region


class State:
    def __init__(self) -> None:
        self.login = Login("Zaid", "example@mail.com", "Asia")


def main(view: View):
    view.set(
        theme=Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#42a5f5',
            accent_color_name='blue',
        )
    )
    view.context['state'] = State()
    damn = view(
        '''
        # Upgrade Cipher
        ---
        - Enter the data
        - Encryption
        - Decryption

        Choose an option that best suits your situation.
        ''',
        # box('Pick a theme', value=theme_name, options=theme_names),
        box(
            [
                option('create-account', 'Create Account',
                   caption="Create Account to login further", selected=True),
                option('login', 'Login', caption="Login to continue"),
            ],
        )
    )

    if damn == "create-account":
        name, email, password, region, action = view(
            '''
            # Create your account

            ''',
            box('Full name', placeholder='Boaty McBoatface'),
            row(
                box('Email', placeholder='you@company.com', icon='Mail'),
                box('Password', value='pa55w0rd', password=True)
            ),
            box('Region', mode='menu', options=[
                'Africa', 'Asia', 'Australia', 'Europe', 'North America', 'South America',
            ]),
            box(['Create'])
        )

        # create a dictionary of the user's input
        user_input = {
            "username": name,
            "email": email,
            "password": encode(password),
            "region": region
        }

        # store the user's input to a mongodb collection
        user_db.insert_one(user_input)

    email_1, password1 = view(
        '''
        # Login
        ---

        - Enter your email
        - Enter your password
        ''',
        box('Email', placeholder="example@mail.com"),
        box('Password', placeholder='pa55w0rd', password=True)
    )

    while email_1 == "":
        email_1 = view(
            "Please enter your email",
            box('Email', placeholder="example@mail.com"),
            popup=True
        )
        # password validation with regex for 8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special character
        if password1 == "" or re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password1) is None:
            password1 = view(
                "Please enter your password",
                box('Password', placeholder='pa55w0rd', password=True),
                popup=True
            )

    try:
        # get the user's input from the mongodb collection
        returndb = user_db.find_one(filter={"email": email_1})
    except:
        view("No account found")
        view.jump(main)

    name_re, email_re, password_re, region_re = returndb["username"], returndb[
        "email"], returndb["password"], returndb["region"]

    decoded_str = decode(password_re)

    # one line if condition to check if the user's input is correct
    valid = password1 == decoded_str

    if not valid and email_1 == email_re:
        view(
            """
            # Error
            ---
            - Invalid password
            """, mode="md"
        )

    view.context['state'].login = Login(name_re, email_1, region_re)

    view.jump(afterLogin)


def encrypt(view: View):
    email: Login = view.context['state'].login.email
    thetext = view(f'''
    # Encryption
    ---
    ''',
        box(
            'Enter the data to be encrypted',
            placeholder='I hate Apples!'
        )
    )

    e_data = {
        "email": email,
        "data": encode(thetext)
    }

    encrypt_db.insert_one(e_data)

    view.jump(afterLogin)


def decrypt(view: View):
    email: Login = view.context['state'].login.email
    re_endb = encrypt_db.find(filter={"email": email})
    # create a string which appends all the data in the collection
    f = {}
    for i, data in enumerate(re_endb):
        f[i] = data["data"]

    view(
        '''
        # Showing the data
        ''',
        box(
            mode='table',
            headers=[
                header('S.No'), header('Data', width=400)
            ],
            options=[
                option(str(i), options=(str(i+1), decode(f[i]))) for i in f
            ]
        )
    )

    view.jump(afterLogin)


def afterLogin(view: View):
    name: Login = view.context['state'].login.name
    region: Login = view.context['state'].login.region
    action = view(
        f'''
        # Welcome
        ---
        - Welcome to the world of encryption, {name}
        - You are logged in from {region}
        ''',
        box([
            option('encrypt', 'Encrypt',
                   caption="Encrypt and store personal data", selected=True),
            option('decrypt-view', 'View data',
                   caption="View your personal data"),
        ])
    )

    if action == "encrypt":
        view.jump(encrypt)
    if action == "decrypt-view":
        view.jump(decrypt)


nitro = View(
    main,
    title='Upgrade Cipher!',
    caption='v1.0',
    routes=[
        option(main),
        option(afterLogin),
        option(encrypt),
        option(decrypt)
    ]
)


app = Flask(__name__, static_folder=web_directory, static_url_path='')


@app.route('/')
def home_page():
    return send_from_directory(web_directory, 'index.html')


@app.route('/nitro', websocket=True)
def socket():
    ws = simple_websocket.Server(request.environ)
    try:
        nitro.serve(ws.send, ws.receive)
    except simple_websocket.ConnectionClosed:
        pass
    return ''


if __name__ == '__main__':
    app.run(debug=True, port=3000, host="0.0.0.0")
