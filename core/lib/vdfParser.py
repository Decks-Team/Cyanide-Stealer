import re
import json

def convert(t: str):

    t = re.sub(r"//.*\n", "", t)
    t = t.replace("\\\"", "\"")
    t = re.sub(r"[\{\[\}\]]", "", t)
    t = re.sub(r"(\w+)", r'"\1"', t)
    t = re.sub(r"\"(\w+)\"\s+\"(.+)\"", r'"\1": "\2",', t)
    t = re.sub(r",$", "", t)
    t = "{" + t + "}"

    config_dict = json.loads(t)

    return config_dict