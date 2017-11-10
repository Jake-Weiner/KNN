import random
import csv
import pandas as pd
import math

def loadDataset(filename, split, trainingSet=[] , testSet=[]):
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for x in range(len(dataset)-1):
            for y in range(4):
                dataset[x][y] = float(dataset[x][y])
                if random.random() < split:
                    trainingSet.append(dataset[x])
                else:
                    testSet.append(dataset[x])


    return trainingSet,testSet

#$calculates
def euclideanDistance(instance1, instance2, start,end):
    distance = 0
    for x in range(start,end):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)

def standardise(non_standardised,min_0,max_0,min_1,max_1,min_2,max_2,min_3,max_3):
    standardised = [(non_standardised[0] - min_0)/(max_0 - min_0),(non_standardised[1] - min_1)/(max_1 - min_1),
                    (non_standardised[2] - min_2) / (max_2 - min_2),(non_standardised[3] - min_3)/(max_3 - min_3)]
    return standardised

def poll(points_close):
    categories = {}
    for point in points_close:

        try:
            categories[point[4]] = categories[point[4]] + 1
            break
        except KeyError:
            categories[point[4]] = 0


    category_assigned = None
    for key, value in sorted(categories.iteritems(), key=lambda (k, v): (v, k),reverse=True):
        category_assigned = key
        break
    return category_assigned

def main():
    trainingSet, testSet = loadDataset(r'C:/Users/weineja/Documents/KNN/iris.data.txt' , 0.66)
    df_all = pd.read_csv(r'C:/Users/weineja/Documents/KNN/iris.data.txt',header = None)
    row_count = df_all.shape[0]
    column_count = df_all.shape[1]
    max_0 = df_all[0].max()
    min_0 = df_all[0].min()
    max_1 = df_all[1].max()
    min_1 = df_all[1].min()
    max_2 = df_all[2].max()
    min_2 = df_all[2].min()
    max_3 = df_all[3].max()
    min_3 = df_all[3].min()

    for test_point in testSet:
        euclidean_distances = []
        for train_point in trainingSet:
            euclidean_distances.append((train_point,euclideanDistance(standardise(test_point,min_0,max_0,min_1,max_1,min_2,max_2,min_3,max_3),
                                                                      standardise(train_point,min_0,max_0,min_1,max_1,min_2,max_2,min_3,max_3),0,4)))
        euclidean_distances_sorted = sorted(euclidean_distances, key=lambda train: train[1])
        top_k = []
        for i in range(0,10):
            top_k.append(euclidean_distances_sorted[i][0])

        print ('category of point is {}, assigned category is {}'.format(test_point[4],poll(top_k)))


if __name__ == "__main__":
    main()