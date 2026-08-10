def sample_mlp_params(rng):
    if QUICK_MODE:
        hidden_options = [(32,), (64, 32)]
        max_iters = [120, 180]
    elif FAST_MODE:
        hidden_options = [(64, 32), (128, 64), (128, 64, 32), (256, 128)]
        max_iters = [250, 350]
    else:
        hidden_options = [(64, 32), (128, 64), (128, 64, 32), (256, 128), (256, 128, 64)]
        max_iters = [300, 450, 650]
    return {
        "hidden_layer_sizes": hidden_options[int(rng.randint(len(hidden_options)))],
        "alpha": float(rng.choice([1e-6, 1e-5, 1e-4, 1e-3])),
        "learning_rate_init": float(rng.choice([1e-4, 3e-4, 5e-4, 1e-3, 2e-3])),
        "batch_size": int(rng.choice([32, 64, 128])),
        "max_iter": int(rng.choice(max_iters)),
    }


def build_mlp(params):
    return MLPRegressor(
        random_state=SEED,
        activation="relu",
        solver="adam",
        early_stopping=True,
        n_iter_no_change=12,
        validation_fraction=0.1,
        **params
    )

