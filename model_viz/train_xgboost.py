# This script needs these libraries to be installed:
#   numpy, xgboost

import wandb

import numpy as np
import xgboost as xgb


# setup parameters for xgboost
param = {
    "objective" : "multi:softmax",
    "eta" : 0.1,
    "max_depth": 6,
    "nthread" : 4,
    "num_class" : 6
}

# start a new wandb run to track this script
wandb.init(
    # set the wandb project where this run will be logged
    project="my-awesome-project",

    # track hyperparameters and run metadata
    config=param
)

# download data from wandb Artifacts and prep data
wandb.use_artifact('wandb/intro/dermatology_data:v0', type='dataset').download('.')
data = np.loadtxt(
    "./dermatology.data", delimiter=",",
    converters={33: lambda x: int(x == "?"), 34: lambda x: int(x) - 1},
)
sz = data.shape

train = data[: int(sz[0] * 0.7), :]
test = data[int(sz[0] * 0.7) :, :]

train_X = train[:, :33]
train_Y = train[:, 34]

test_X = test[:, :33]
test_Y = test[:, 34]

xg_train = xgb.DMatrix(train_X, label=train_Y)
xg_test = xgb.DMatrix(test_X, label=test_Y)
watchlist = [(xg_train, "train"), (xg_test, "test")]

# add another config to the wandb run
num_round = 100
wandb.config["num_round"] = 100
wandb.config["data_shape"] = sz

# pass custom callback to log metrics to wandb
class WandbCallback(xgb.callback.TrainingCallback):
    def after_iteration(self, model, epoch, evals_log):
        for eval_set, metrics in evals_log.items():
            for metric, values in metrics.items():
                wandb.log({f"{eval_set}_{metric}": values[-1]})
        return False

bst = xgb.train(
    param, xg_train, num_round, evals=watchlist,
    callbacks=[WandbCallback()]
)

# get prediction
pred = bst.predict(xg_test)
error_rate = np.sum(pred != test_Y) / test_Y.shape[0]

# log your test metric to wandb
wandb.summary["Error Rate"] = error_rate

# [optional] finish the wandb run, necessary in notebooks
wandb.finish()
      