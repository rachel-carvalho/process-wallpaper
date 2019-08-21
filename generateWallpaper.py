import re
from PIL import Image
from wordcloud import WordCloud
import json

commandList = []

def to_mb(text):
    number = float(text[:-1])
    if text.count('M') > 0:
        return number
    if text.count('G') > 0:
        return number * 1024
    if text.count('K') > 0:
        return number / 1024

with open("top.out", "r") as topFile:
    allText = topFile.read()
    allText = allText[allText.rfind('Processes: '):]
    lines = allText.split("\n")

    reg = "\d+[GMK]?"

    all = re.findall(reg, lines[6])

    used = to_mb(all[0])
    unused = to_mb(all[2])
    total = used + unused

    topOutput = lines[9:]

    for line in topOutput[:-1]:
        line = re.sub(r'\s+', ' ', line).strip()
        fields = line.split(" ")

        try:
            if fields[1].count("/") > 0:
                command = fields[1].split("/")[0]
            else:
                command = fields[1]

            cpu = float(fields[3].replace(",", "."))
            mem = to_mb(fields[2].replace("+", "")) / total * 100.0

            if command != "top":
                commandList.append((command, cpu, mem))
        except:
            pass


commandDict = {}

for command, cpu, mem in commandList:
    if command in commandDict:
        commandDict[command][0] += cpu
        commandDict[command][1] += mem
    else:
        commandDict[command] = [cpu + 1, mem + 1]

resourceDict = {}

for command, [cpu, mem] in commandDict.items():
    resourceDict[command] = (cpu ** 2 + mem ** 2) ** 0.5

configJSON = json.loads(open("config.json", "r").read())

wc = WordCloud(
    background_color = configJSON["wordcloud"]["background"],
    width = int(configJSON["resolution"]["width"] - 2 * configJSON["wordcloud"]["margin"]),
    height = int(configJSON["resolution"]["height"] - 2 * configJSON["wordcloud"]["margin"])
).generate_from_frequencies(resourceDict)

wc.to_file('wc.png')

wordcloud = Image.open("wc.png")
wallpaper = Image.new('RGB', (configJSON["resolution"]["width"], configJSON["resolution"]["height"]), configJSON["wordcloud"]["background"])
wallpaper.paste(
    wordcloud,
    (
        configJSON["wordcloud"]["margin"],
        configJSON["wordcloud"]["margin"]
    )
)
wallpaper.save("wallpaper.png")
