# Api info created by alinas 
# When you upload it to GitHub and then deploy it to Vercel, the link will look like this : https://api-test-info.vercel.app/{uid} Example: https://api-test-info.vercel.app/7909163333 and d'ont say src is mine because i'will fuck uyou in bed
 # by xAlInAs
from flask import Flask, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
import requests

from secret import key, iv
import uid_generator_pb2
from zitado_pb2 import Users

app = Flask(__name__)

session = requests.Session()

UID = "4844157514"
PASSWORD = "03B9B199CB9B8C0EFE3B83524D749A1AB559D454BCECBAAA82B7B41B3FF5380A"


def hex_to_bytes(hex_string):
    return bytes.fromhex(hex_string)


def create_protobuf(saturn_, garena):
    message = uid_generator_pb2.uid_generator()
    message.saturn_ = saturn_
    message.garena = garena
    return message.SerializeToString()


def protobuf_to_hex(protobuf_data):
    return binascii.hexlify(protobuf_data).decode()


def decode_hex(hex_string):
    byte_data = binascii.unhexlify(hex_string.replace(' ', ''))
    users = Users()
    users.ParseFromString(byte_data)
    return users


def encrypt_aes(hex_data, key, iv):
    key = key.encode()[:16]
    iv = iv.encode()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(bytes.fromhex(hex_data), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return binascii.hexlify(encrypted_data).decode()


def apis(idd, token):
    if not token:
        return None

    try:
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Expect': '100-continue',
            'X-Unity-Version': '2018.4.11f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': 'OB53',
            'Authorization': f'Bearer {token}',
        }

        try:
            data = bytes.fromhex(idd)
        except Exception:
            return None

        response = requests.post(
            'https://clientbp.ggpolarbear.com/GetPlayerPersonalShow',
            headers=headers,
            data=data,
            timeout=15
        )

        if not response or not response.content:
            return None

        return response.content.hex()

    except Exception:
        return None

def token(uid, password):
    try:
        response = session.get(
            "https://api-get-jwt-by-alinas.vercel.app/get",
            params={"uid": uid, "password": password},
            timeout=5
        )

        data = response.json()
        return data.get("token")

    except Exception:
        return None


@app.route('/<uid>', methods=['GET'])
def main(uid):
    try:
        # تحويل UID
        try:
            saturn_ = int(uid)
        except Exception:
            return jsonify({
                "error": "Invalid UID"
            }), 400

        garena = 1

        # protobuf
        protobuf_data = create_protobuf(saturn_, garena)
        hex_data = protobuf_to_hex(protobuf_data)

        # AES Encrypt
        encrypted_hex = encrypt_aes(hex_data, key, iv)

        # Get Token
        tokenn = token(UID, PASSWORD)

        if not tokenn:
            return jsonify({
                "error": "Token generation failed"
            }), 500

        # External API
        infoo = apis(encrypted_hex, tokenn)

        if not infoo:
            return jsonify({
                "error": "API request failed"
            }), 500

        # Decode protobuf response
        try:
            users = decode_hex(infoo)
        except Exception as e:
            return jsonify({
                "error": "Decode failed",
                "details": str(e),
                "raw_response": infoo[:500]
            }), 400

        result = {}

        # basicinfo
        if users.basicinfo:
            result["basicinfo"] = []

            for user_info in users.basicinfo:
                result["basicinfo"].append({
                    "username": user_info.username,
                    "region": user_info.region,
                    "level": user_info.level,
                    "Exp": user_info.Exp,
                    "bio": users.bioinfo[0].bio if users.bioinfo else None,
                    "banner": user_info.banner,
                    "avatar": user_info.avatar,
                    "brrankscore": user_info.brrankscore,
                    "BadgeCount": user_info.BadgeCount,
                    "likes": user_info.likes,
                    "lastlogin": user_info.lastlogin,
                    "csrankpoint": user_info.csrankpoint,
                    "csrankscore": user_info.csrankscore,
                    "brrankpoint": user_info.brrankpoint,
                    "createat": user_info.createat,
                    "OB": user_info.OB
                })

        # claninfo
        if users.claninfo:
            result["claninfo"] = []

            for clan in users.claninfo:
                result["claninfo"].append({
                    "clanid": clan.clanid,
                    "clanname": clan.clanname,
                    "guildlevel": clan.guildlevel,
                    "livemember": clan.livemember
                })

        # clanadmin
        if users.clanadmin:
            result["clanadmin"] = []

            for admin in users.clanadmin:
                result["clanadmin"].append({
                    "idadmin": admin.idadmin,
                    "adminname": admin.adminname,
                    "level": admin.level,
                    "exp": admin.exp,
                    "brpoint": admin.brpoint,
                    "lastlogin": admin.lastlogin,
                    "cspoint": admin.cspoint
                })

        result["Owners"] = [
            "DRAGON TELEGRAM : @DRAGONX1M"
        ]

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "fatal_error": str(e)
        }), 500


if __name__ == "__main__":
    app.run()

# FuCk YoU 🙂