
import sys
sys.path.append("..")

from utils.exceptions import NotFittedError, MissingFeatureError

class DecisionTreeClassifier:
    def __init__(self, max_depth=100, min_size=3):
        self.max_depth = max_depth
        self.min_size = min_size
        self.required_features = set()
        self.isfit = False

    def fit(self, X, y):
        self.X = X
        self.y = y
        self.labels = y.unique()
        root = self._get_split(X.index)
        self._split(root, self.max_depth, self.min_size, 1)
        self.tree = root
        self.isfit = True
        del self.X
        del self.y

    def predict(self, X):
        self._validate(X)
        predictions = []
        for idx in X.index:
            y_hat = self._descend_tree(self.tree, X.loc[idx])
            predictions.append(y_hat)

        return predictions

    def _pivot(self, dataset, series, pivot):
        left = dataset[series <= pivot].index
        right = dataset[series>pivot].index

        return left, right

    def _gini_index(self, group_indices):
        label_groups = [self.y.loc[index_group].value_counts(normalize=True) 
                        for index_group in group_indices]
        group_sizes = [len(group) for group in group_indices]
        total_size = sum(group_sizes)
        weighted_score = 0
        for idx in range(len(label_groups)):
            group_size = group_sizes[idx]
            if not group_size:
                continue 
            score = (label_groups[idx] ** 2).sum()
            weighted_score += (1-score) * (group_size/total_size)
        return weighted_score            


    def _get_split(self, indices):
        X = self.X.loc[indices]
        unique  = [X[column].unique() for column in X.columns]
        total_columns = X.shape[1]
        groups = []
        best_score = None
        for idx in range(total_columns):
            column = X.columns[idx]
            for val in unique[idx]:
                left_split, right_split = self._pivot(X, X[column], val)
                gini_score = self._gini_index([left_split, right_split])
                if not best_score:
                    best_score = gini_score
                    best_column = column
                    best_val = val
                    best_split = (left_split, right_split)
                else:
                    if gini_score < best_score:
                        best_score = gini_score
                        best_column = column
                        best_val = val
                        best_split = (left_split, right_split)
                        
        self.required_features.add(best_column)
        
        return  {'column':best_column, 'split_value': best_val, 'score': best_score, 'split': best_split}

    def _to_terminal(self, split_indices):
        labels = self.y.loc[split_indices]

        return labels.value_counts().idxmax()

    def _split(self, node, max_depth, min_size, depth):
        left, right = node['split']
        del node['split']
        if not len(left) or not len(right):
            node['left'] = node['right'] = self._to_terminal(left.append(right))
            return
        if depth >= self.max_depth:
            node['left'], node['right'] = self._to_terminal(left), self._to_terminal(right)
            return
        if len(left) <= self.min_size:
            node['left'] = self._to_terminal(left)
        else:
            node['left'] = self._get_split(left)
            self._split(node['left'], max_depth, min_size, depth+1)
        if len(right) <= self.min_size:
            node['right'] = self._to_terminal(right)
        else:
            node['right'] = self._get_split(right)
            self._split(node['right'], max_depth, min_size, depth+1)

    def _descend_tree(self, node, row):
        if row[node['column']] <= node['split_value']:
            if isinstance(node['left'], dict):
                return self._descend_tree(node['left'], row)
            else:
                return node['left']

        else:
            if isinstance(node['right'], dict):
                return self._descend_tree(node['right'], row)
            else:
                return node['right']
            
    def _validate(self, X):
        for column in self.required_features:
            if column not in X.columns:
                raise MissingFeatureError(f'The following feature is required: {column}')



