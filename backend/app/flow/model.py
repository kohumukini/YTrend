import torch
import joblib
import torch.nn as nn
import numpy as np
from pathlib import Path
from .logger import logger

INPUT_SIZE = 9
HIDDEN_SIZE = 32
NUM_LAYERS = 1
DROPOUT = 0.2
WINDOW_SIZE = 42

MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "models"

class StockLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, dropout):
        super(StockLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, dropout=dropout if num_layers > 1 else 0.0, batch_first=True)
        self.regressor = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 1)
        )
        for name, param in self.named_parameters():
            if 'weight_ih' in name:
                nn.init.xavier_uniform_(param)
            elif 'weight_hh' in name:
                nn.init.orthogonal_(param)
            elif 'bias' in name:
                nn.init.zeros_(param)
                total = param.size(0)
                quarter = total // 4
                param.data[quarter:quarter*2] = 1.0

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        last_time_step = lstm_out[:, -1, :]
        return self.regressor(last_time_step)


def load_models():
    try:
        pred_model = StockLSTM(INPUT_SIZE, HIDDEN_SIZE, NUM_LAYERS, DROPOUT)
        pred_model.load_state_dict(torch.load(
            MODELS_DIR / "lstm_pred_model.pth",
            map_location=torch.device("cpu"),
            weights_only=True
        ))
        pred_model.eval()

        class_model = StockLSTM(INPUT_SIZE, HIDDEN_SIZE, NUM_LAYERS, DROPOUT)
        class_model.load_state_dict(torch.load(
            MODELS_DIR / "lstm_class_model.pth",
            map_location=torch.device("cpu"),
            weights_only=True
        ))
        class_model.eval()

        scaler = joblib.load(MODELS_DIR / "scaler.pkl")
        y_mean = float(np.load(MODELS_DIR / "y_mean.npy")[0])
        y_std = float(np.load(MODELS_DIR / "y_std.npy")[0])

        logger.info("[model] Models and artifacts loaded successfully")
        return pred_model, class_model, scaler, y_mean, y_std

    except Exception as e:
        logger.error(f"[model] Failed to load models: {type(e).__name__}: {e}")
        raise