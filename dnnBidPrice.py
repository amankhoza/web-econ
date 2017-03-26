import pandas as pd
import tensorflow as tf
import os

tf.logging.set_verbosity(tf.logging.INFO)


FEATURES = ['weekday', 'hour', 'region', 'city', 'slotwidth', 'slotheight', 'slotprice']
LABELS = ['bidprice']


def input_fn(data_set, label):
    feature_cols = {k: tf.constant(data_set[k].values, shape=[len(data_set), 1])
                    for k in FEATURES}
    labels = tf.constant(data_set[label].values)
    return feature_cols, labels


class MultiLabelRegressor:

    def __init__(self, input_fn, feature_cols, labels):
        self.input_fn = input_fn
        self.feature_cols = feature_cols
        self.labels = labels

    def fit(self, data_set):
        self.regressors = {}
        for label in self.labels:
            # Build 2 layer fully connected DNN with 10, 10 units respectively.
            regressor = tf.contrib.learn.DNNRegressor(feature_columns=self.feature_cols,
                                                      hidden_units=[10, 10])
            # Fit
            regressor.fit(input_fn=lambda: self.input_fn(data_set, label), steps=5000)
            self.regressors[label] = regressor

    def evaluate(self, data_set):
        for label in self.labels:
            # Score accuracy
            ev = self.regressors[label].evaluate(input_fn=lambda: self.input_fn(data_set, label), steps=1)
            loss_score = ev["loss"]
            print("Loss for "+label+": {0:f}".format(loss_score))

    def predict(self, data_set):
        predictions = {}
        for label in self.labels:
            regressor = self.regressors[label]
            prediction = regressor.predict(input_fn=lambda: input_fn(data_set, label))
            predictions[label] = list(prediction)
        return predictions


def main(unused_argv):
    os.system('reset')

    # Load datasets
    training_set = pd.read_csv("validation.csv")
    # test_set = pd.read_csv("validation.csv")
    # prediction_set = pd.read_csv("test.csv")
    prediction_set = pd.read_csv("validation.csv")

    # Feature cols
    feature_cols = [tf.contrib.layers.real_valued_column(k)
                    for k in FEATURES]

    multiRegressor = MultiLabelRegressor(input_fn, feature_cols, LABELS)
    multiRegressor.fit(training_set)
    # multiRegressor.evaluate(test_set)
    predictions = multiRegressor.predict(prediction_set)

    for label in LABELS:
        actual = predictions[label]
        preds = list(prediction_set[label].values)
        combined = zip(actual, preds)
        print('Actual \t\t Prediction \t\t Diff')
        totalDiff = 0
        for pair in combined:
            diff = abs(pair[0]-pair[1])
            totalDiff += diff
            print('{:.2f} \t\t {:.2f} \t\t {:.2f}'.format(pair[0], pair[1], diff))
        avgDiff = float(totalDiff) / float(len(combined))
        print('Average diff = {}\n'.format(avgDiff))


if __name__ == "__main__":
    tf.app.run()
