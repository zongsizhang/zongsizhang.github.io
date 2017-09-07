# Classifier

## Decision Boundary
In a statistic-classification problem, a decision boundary is a hyperplane that partition vector space into two sets, one for each class.

## Navie Bayes
Actually minimum error rate, which is equal to maximize posterior probability. Assuming that every feature independent.

### train
go through every record, calculate P(xi|yi).
Time complexity: O(np), n = number of records, p = number of features
Space Complexity: O(pl), l = number of labels

### Test
For every record, extract all value of features, calculate P(yi | x) for every label, and return the label with maximum probability.
Time complexity: O(np)


### Bayes Network (Belief Network)


