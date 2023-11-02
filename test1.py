from datetime import datetime
tenfile = "quan.txt"
tenfile = tenfile.split('.')[0]
outputFile = f"./outputCSV/{tenfile}"
extension = datetime.now()
extension = extension.strftime('(%Hh%Mm %d-%m-%Y)')
with open(outputFile + extension + ".csv", "a") as f:
    f.write("")
fileNames = outputFile + extension + ".csv"