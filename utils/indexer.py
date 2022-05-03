content = []
index = 1
with open('audios.csv', encoding="utf-8") as fp:
    content = fp.readlines() # Skipping first line of the file (usually contains information about end-to-end encryption)
    #content.insert(index, line)
    #index += 1
print(len(content))
with open('audios2.csv', 'w') as file_handler:
    index = 1
    for item in content:
        file_handler.write("{},{}".format(index, item))
        index += 1