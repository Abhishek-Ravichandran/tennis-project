import numpy as np

from sklearn import linear_model, naive_bayes, svm, decomposition
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score
from overview import init_stats
from featureExtraction import getBaseline
import csv
import exceptions
import matplotlib.pyplot as plt

# Load the data
# Features
features = 'features.csv'
# Winners
winners = 'data/match_winner.csv'

match_players, valid_matches, num_matches, surfaces, handedness = init_stats(0)


X = np.zeros((1165, 102))
winner_vects = []

ct = 0
with open(features) as features_csv:
    cr = csv.reader(features_csv)
    featureVectorMap1 = getBaseline()
    
    for row in cr:
        # Strip off match id and winner label
        X[ct][:] = np.array(row[2:] + featureVectorMap1[row[0]])
        winner = row[1].replace('_', ' ').strip()
        if winner == match_players[row[0]]['player1'].strip():
            winner_vects.append(1)
        elif winner == match_players[row[0]]['player2'].strip():
            winner_vects.append(2)
        else:
            print row[0], winner, match_players[row[0]]['player1'], match_players[row[0]]['player2']
            raise
        ct += 1
y = np.array(winner_vects)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

# Set up the pipeline
pca = decomposition.PCA()
logistic = linear_model.LogisticRegression()
gaussian_nb = naive_bayes.GaussianNB()
svm_gaussian = svm.SVC()
pipe = Pipeline(steps=[('pca', pca), 
    # ('gaussianNB', gaussian_nb)
    ('svm', svm_gaussian)
    # ('logistic', logistic)
    ])

#Parameters of pipelines can be set using '__' separated parameter names:

estimator = GridSearchCV(pipe,
                         dict(pca__n_components=[48, 49, 50, 51]
                              , svm__C=[400, 450, 500, 550], svm__gamma=[.003, .005, .008]
                              #, logistic__C=[1, 6, 10, 60, 100]
                              ))
estimator.fit(X_train, y_train)

print "train", accuracy_score(y_train, estimator.predict(X_train))
print "test", accuracy_score(y_test, estimator.predict(X_test))

print estimator.best_estimator_

# plt.axvline(estimator.best_estimator_.named_steps['pca'].n_components,
#             linestyle=':', label='n_components chosen')
# plt.legend(prop=dict(size=12))
# plt.show()


# pca.fit(X_train)
# plt.figure(1, figsize=(4, 3))
# plt.clf()
# plt.axes([.2, .2, .7, .7])
# plt.plot(pca.explained_variance_, linewidth=2)
# plt.axis('tight')
# plt.xlabel('n_components')
# plt.ylabel('explained_variance_')

# plt.savefig('pca_graph.png')
