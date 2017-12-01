#!python3
'''This module provides all of the interaction with scikit-learn and
performs the logistic regressions'''
import numpy
from sklearn import linear_model
from sklearn.metrics import log_loss

def create_school_array(base_table):
    '''Returns a numpy array that can be fed to the regression tool where
    base_table is a Table with the reduced data-set but all columns'''
    # First order of business is get a reduced table:
    reduced_table = list(base_table.get_columns(['GPA', 'ACT', 'Y']))
    return numpy.array(reduced_table)

def create_standard_array(base_table,ACTcase='ACT25'):
    '''Returns a numpy array that can be fed to the regression tool where
    base_table is a Table with the reduced data-set but all columns'''
    # First order of business is get a reduced table:
    reduced_table = list(base_table.get_columns(['GPA', 'ACT', 'Y', ACTcase]))
    diff_table = [[x[0], x[1]-x[3], x[2]] for x in 
                  reduced_table if isinstance(x[3],float)]
    return numpy.array(diff_table)


def run_lregression(data):
    '''Returns the logistic regression results for the passed numpy array
    where the first columns are the independent variables and the final
    column is the outcome (Y)'''
    lr = linear_model.LogisticRegression(C=10000000000, solver='newton-cg')
    X = data[:,:-1]
    Y = data[:,-1]
    lr.fit(X, Y)
    GPAcoef = lr.coef_[0][0]
    ACTcoef = lr.coef_[0][1]
    intercept = lr.intercept_[0]
    score = lr.score(X,Y)
    loss = log_loss(Y, lr.predict_proba(X))
    # now create some sensitivity stats
    # first find the average gpa of points near 50/50
    preds = lr.predict_proba(X)
    gpa_yes = []
    for i in range(len(preds)):
        if (preds[i][0] > 0.35) and (preds[i][0] < 0.65):
            gpa_yes.append(X[i,0])

    # then calculate the ACT that corresponds to this average
    avg_yes_gpa = numpy.mean(gpa_yes)
    avg_act_yes = (-intercept - avg_yes_gpa*GPAcoef)/ACTcoef

    # next, build a sensitivity matrix and check the predictions
    X_check = numpy.array([[avg_yes_gpa, avg_act_yes],
                           [avg_yes_gpa+0.05, avg_act_yes+.5],
                           [avg_yes_gpa+0.1, avg_act_yes+1]])
    pred_check = lr.predict_proba(X_check)


    return [Y.sum(), GPAcoef, ACTcoef, intercept, score, loss,
            avg_yes_gpa, avg_act_yes, pred_check[0][1],pred_check[1][1],
            pred_check[2][1]]

