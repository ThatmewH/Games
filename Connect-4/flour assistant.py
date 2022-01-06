percentages = [0.03, 0.02, 0.02, 0.01, 0.70]

while True:
    RDW = input("RDW: ")
    Factor = 1.7
    for x in range(10):
        print()
    grams = float(RDW) / float(Factor)
    totalDoughWeighr = 0
    print("Flower: ", RDW)
    print("Grahms: ", grams)
    print("=================")
    for percent in percentages:
        print(str(percent*100) + "%:      " + str((percent) * int(grams)))
        totalDoughWeighr += (percent) * int(grams)
    print("=================")
    print("Total DW: " + str(totalDoughWeighr+int(grams)))
    print()
