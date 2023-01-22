import pandas as pd
import os
import sys

def Normalize(norm_input_dataset,nCol,weights):
    for j in range(1,nCol):
        temp=0
        for i in range(0,len(norm_input_dataset)):
            temp = temp +  norm_input_dataset.iloc[i,j]**2
        temp = temp**0.5
        for i in range(0,len(norm_input_dataset)):
            norm_input_dataset.iloc[i,j]= (norm_input_dataset.iloc[i,j] / temp)*weights[j-1]
    return norm_input_dataset

def calculate(norm_input_dataset,nCol,impact):
    ideal_best = norm_input_dataset.max()
    ideal_best = (ideal_best.values)[1:]
    ideal_worst = norm_input_dataset.min()
    ideal_worst = (ideal_worst.values)[1:]
    for i in range(1, nCol):
        if impact[i-1] == '-':
            ideal_best[i-1], ideal_worst[i-1] = ideal_worst[i-1], ideal_best[i-1]
    return ideal_best, ideal_worst

def topsis(norm_input_dataset, input_dataset, nCol, weights, impact):
    norm_input_dataset = Normalize(norm_input_dataset, nCol, weights)
    ideal_best,ideal_worst = calculate(norm_input_dataset,nCol,impact)
    performance_score =[]
    for i in range(len(norm_input_dataset)):
        s_p = 0
        s_n = 0
        for j in range(1,nCol):
            s_p = s_p + (ideal_best[j-1] - norm_input_dataset.iloc[i,j])**2
            s_n = s_n + (ideal_worst[j-1] - norm_input_dataset.iloc[i,j])**2
        s_p = s_p**0.5
        s_n = s_n**0.5
        performance_score.append(s_n/(s_p+s_n))
    input_dataset['Topsis Score'] = performance_score
    input_dataset['Rank'] = (input_dataset['Topsis Score'].rank(
    method='max', ascending=False))
    input_dataset = input_dataset.astype({"Rank": int})
    input_dataset.to_csv(sys.argv[4], index=False)

def main():
    if len(sys.argv) != 5:
        print("Number of arguments should be 5")
        exit(1)
    elif not os.path.isfile(sys.argv[1]):
        print(f"{sys.argv[1]} Does not exist")
        exit(1)
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f"Wrong format, {sys.argv[1]} is not csv")
        exit(1)
    else:
        input_dataset, norm_input_dataset = pd.read_csv(
            sys.argv[1]), pd.read_csv(sys.argv[1])
        nCol = len(norm_input_dataset.columns.values)
        if nCol < 3:
            print("Input file have less then 3 columns")
            exit(1)
        for i in range(1, nCol):
            pd.to_numeric(input_dataset.iloc[:, i], errors='coerce')
            input_dataset.iloc[:, i].fillna(
                (input_dataset.iloc[:, i].mean()), inplace=True)
        try:
            weights = [int(i) for i in sys.argv[2].split(',')]
        except:
            print("error in weights array")
            exit(1)
        impact = sys.argv[3].split(',')
        for i in impact:
            if not (i == '+' or i == '-'):
                print("error in impact array")
                exit(1)
        if nCol != len(weights)+1 or nCol != len(impact)+1:
            print(
                "number of weights, number of impacts and number of columns are not same")
            exit(1)
        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("output file extension is incorrect")
            exit(1)
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])
        topsis(norm_input_dataset, input_dataset, nCol, weights, impact)

if __name__ == "__main__":
    main()