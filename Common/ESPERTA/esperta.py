import numpy as np
from sklearn.metrics import confusion_matrix, f1_score


class esperta_original:
    """
    Authors: Mirko Stumpo,Tommaso Torda,Tommaso Alberti, Monica Laurenza.
    The original ESPERTA logistic-model. The class given below does take into
    account the training rule of the logistic model. For this reason, you
    must set the weights a priori. The original optimal set of weights
    can be found in Laurenza et. al (2009).

    e.g.:
    Given the set of weights, in order to initialize the model do the following:

    esperta = esperta_original(weights, threshold=0.5)

    now, given the test set xtest:

    predictions = esperta.predict(xtest)
    
    where xtest for esperta is a list: [Nexp,1,log10(X), log10(R), log10(X)*log10(R)] where Nexp, are the number of examples, 1 is for the bias of the model, X is the integrated X-ray flux and R is the integrated radio flux R

    the models for s1 and s2 data and for the three interval of longitude w20-120, e40-19, e120-41, are:
    
    esperta_s1_w20_120 = esperta_original([-6.07,-1.75, 1.14, 0.56], 0.28) 
    esperta_s2_w20_120 = esperta_original([-6.07,-1.75, 1.14, 0.56], 0.35)

    esperta_s1_e40_19 = esperta_original([-7.44,-2.99, 1.21, 0.69], 0.28) 
    esperta_s2_e40_19 = esperta_original([-7.44,-2.99, 1.21, 0.69], 0.28)
    
    esperta_s1_e120_41 = esperta_original([-5.02,-1.74, 0.64, 0.40], 0.23) 
    esperta_s2_e120_41 = esperta_original([-5.02,-1.74, 0.64, 0.40], 0.23)
    """

    def __init__(self, weights, threshold):
        """
        In order to create an instance of esperta_original, you must set
        the weights and the threshold/decision rule
        """
        self.weights = weights
        self.threshold = threshold

    def prob(self, x):
        """
        Logistic probability function.

        x : 1D-array; input variables concerning the i-th point

        return: probability that the point x is a SEP event.
        """
        w = self.weights
        return 1 / (1 + np.exp(-np.dot(w, x)))

    def predict(self, xtest):
        """
        Prediction rule based on the threshold/decision rule

        xtest: 2D-array (n_test, n_features); the whole test set

        return: predicted labels for each point in xtest aggiungi 15 minuti in cui è acceso
        """

        eps = self.threshold
       

        pred = np.zeros(len(xtest))
      
        k = 0

        for xx in xtest:

            p = self.prob(xx)
         
            if p > eps:
                pred[k] = 1
            k +=1
        return pred


def ConfMatrix(predictions, true_labels):
    return confusion_matrix(predictions, true_labels)


def get_scores(predictions, true_labels):
    """
    Use confusion matrix in order to get the scores of the model.
    """
    C = ConfMatrix(predictions, true_labels)
    POD_score = (C[1][1] /
                      (C[1][1] +
                       C[0][1]))
    FAR_score = (C[1][0] /
                      (C[1][1] +
                       C[1][0]))

    f1 = f1_score(true_labels, predictions)    #harmonic mean between POD & FAR
    return POD_score, FAR_score, f1