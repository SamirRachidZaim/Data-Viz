import random

import wandb

# Define model configurations
models = [
    {
        "learning_rate": 0.025,
        "architecture": "CNN",
        "dataset": "CIFAR-100",
        "epochs": 20,
    },
    {
        "learning_rate": 0.025,
        "architecture": "VAE",
        "dataset": "CIFAR-100",
        "epochs": 20,
        "vae_latent_dim": 128,
        "vae_beta": 1.0,
    },
    {
        "learning_rate": 0.025,
        "architecture": "RandomForest",
        "dataset": "CIFAR-100",
        "random_forest_trees": 2000,
    },
]

# Train each model
for config in models:
    run = wandb.init(
        # Set the wandb entity where your project will be logged (generally your team name).
        entity="samir-rachid-zaim-allen",
        # Set the wandb project where this run will be logged.
        project="my-awesome-project",
        # Track hyperparameters and run metadata.
        config=config,
    )
    
    # Simulate training.
    epochs = config.get("epochs", 10)
    offset = random.random() / 5
    for epoch in range(2, epochs):
        acc = 1 - 2**-epoch - random.random() / epoch - offset
        loss = 2**-epoch + random.random() / epoch + offset

        # Log metrics to wandb.
        run.log({"acc": acc, "loss": loss})

    # Finish the run and upload any remaining data.
    run.finish()


