from pathlib import Path
import joblib


def load_model(model_name):
    model_names = {
        'CatBoost': 'catboost_model.pkl',
        'LogisticRegression': 'model_log.pkl',
        'DecisionTreeClassifier': 'model_tree.pkl',
    }
    model_file = model_names[model_name]
    current_file_path = Path(__file__).resolve()
    project_root = current_file_path.parents[4]
    models_directory = project_root / 'models_weights'
    full_model_path = models_directory / model_file
    if not full_model_path.exists():
        raise FileNotFoundError(f"Model file not found at {full_model_path}")
    return joblib.load(full_model_path)


def load_vectorizer():
    current_file_path = Path(__file__).resolve()
    project_root = current_file_path.parents[4]
    models_directory = project_root / 'models_weights'
    full_model_path = models_directory / 'tfidf_vectorizer.pkl'
    if not full_model_path.exists():
        raise FileNotFoundError(f"Vectorizer file not found at {full_model_path}")
    return joblib.load(full_model_path)
