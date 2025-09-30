import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4
class MyCustomError(Exception):
    """A custom exception raised for specific error conditions."""
    pass

'''
def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data("shopping.csv")
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")
'''

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    checkFile = checkValidFile(filename)
    if checkFile != "":
       raise MyCustomError(checkFile)

    months = {"Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5, 
              "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11} 
    intColumns = {0, 2, 4, 11, 12, 13, 14}  # Columns with integer values
    floatColumns = {1, 3, 5, 6, 7, 8, 9} # Columns with float values

    # Results that will be tupled
    evidenceList = []
    labels = []

    # Reading through file
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skipping the first line
        # Getting evidence & label for each user
        for row in reader:
            evidence = []
            index = 0
            # Adding to the evidence list
            while index < 17:
                if index in intColumns:
                    evidence.append(int(row[index]))
                elif index in floatColumns:
                    evidence.append(float(row[index]))
                # 10 represents the column index of month
                elif index == 10:
                    userMonth = row[index]
                    evidence.append(months[userMonth])
                # 15 represents the column index of visitorType
                elif index == 15:
                    returner = checkReturningVisitor(row[index])
                    evidence.append(returner)
                # 16 represents the column index of weekend
                elif index == 16:
                    weekendVisit = checkWeekendVisitor(row[index])
                    evidence.append(weekendVisit)
            
                index += 1
            evidenceList.append(evidence)
            label = checkPurchase(row[17])
            labels.append(label)
        
    return (evidenceList, labels)

def checkValidFile(filename) -> str:
    """
    This method will essentially check if the given CSV file is valid for
    training based on shopping data. If the file has all matching columns, then
    the file is valid, and True is returned. Otherwise, False is returned.
    """
    columns = ['Administrative', 'Administrative_Duration', 'Informational', 
                'Informational_Duration', 'ProductRelated', 
                'ProductRelated_Duration', 'BounceRates', 'ExitRates', 
                'PageValues', 'SpecialDay', 'Month', 'OperatingSystems', 
                'Browser', 'Region', 'TrafficType', 'VisitorType', 'Weekend',
                'Revenue']

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)

        # Loop goes through the top element in the reader, and checks if the 
        # columns are valid
        for row in reader:
            if len(row) != 18:
                return f"File has wrong column length: {len(row)} (Should be 18)"
            
            for i in range(18):
                if columns[i] != row[i]:
                    return f"File has incorrect column name {row[i]} (Should be {columns[i]})"

            break

        return ""

def checkReturningVisitor(visitType) -> int:
    """
    Simple helper method that checks if the user is returning to the website, 
    or if it's their first time. If the user's returning, 1 is returned.
    Otherwise, 0 is returned
    """
    if visitType == "Returning_Visitor":
        return 1
    return 0

def checkWeekendVisitor(isWeekend) -> int:
    """
    Simple helper method that checks if the user is visiting the website on the
    weekend, or if it's a weekday. If it's the weekend, 1 is returned. 
    Otherwise, 0 is returned.
    """
    
    if isWeekend == "TRUE":
        return 1
    return 0

def checkPurchase(revenue):
    """
    Simple helper method that checks if the user ended up making a purchase. If
    They did, then 1 is returned. Otherwise, 0 is returned.
    """
    if revenue == "TRUE":
        return 1
    return 0


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    model = KNeighborsClassifier(n_neighbors = 1)
    model.fit(evidence, labels)
    
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    
    positiveLabel, negativeLabel, correctPositive, correctNegative = 0, 0, 0, 0

    # Counting the positive & negative labels, and the amount of correct 
    # predictions
    for i in range(len(labels)):
        if labels[i] == 1:
            positiveLabel += 1
            if predictions[i] == 1:
                correctPositive += 1
        
        else:
            negativeLabel += 1
            if predictions[i] == 0:
                correctNegative += 1
    
    sensitivity = correctPositive / positiveLabel
    specificity = correctNegative / negativeLabel

    return (sensitivity, specificity)


def splitTrainTest(evidence, labels, testSize=TEST_SIZE):
    """
    Simple method that returns the data split into a training dataset and a 
    test dataset.
    """

    return train_test_split(evidence, labels, test_size=testSize, random_state = 42)


if __name__ == "__main__":
    main()
