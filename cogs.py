import csv

from scipy.stats import pearsonr



def calcPearsonCor(file):
    file = open(str(file) + '.csv')
    csvreader = csv.reader(file)
    year = []
    pricePerSqFt = []

    for row in csvreader:
        year.append(row[4])
        pricePerSqFt.append(row[-1])

    year = year[1:]
    pricePerSqFt = pricePerSqFt[1:]

    for i in range(len(year)):
        year[i] = int(year[i])
    for i in range(len(pricePerSqFt)):
        money = pricePerSqFt[i][1:].replace(',', '')
        pricePerSqFt[i] = float(money)

    corr, _ = pearsonr(year, pricePerSqFt)
    print('Pearsons correlation: %.3f' % corr)


if __name__ == "__main__":
    calcPearsonCor('propertyData')

