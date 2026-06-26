import torch
import joblib
import torch.nn as nn
import numpy as np
from pathlib import Path
from .logger import logger

# Training Configuration
INPUT_SIZE = 9
HIDDEN_SIZE = 32
NUM_LAYERS = 1
DROPOUT = 0.2

MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "models"

class StockLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, dropout, is_classification = False):
        super(StockLSTM, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.dropout = dropout
        self.is_classification = is_classification

        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, dropout=dropout if num_layers > 1 else 0.0, batch_first=True)
        self.regressor = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 1)
        )
        self.sigmoid = nn.Sigmoid()

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
        out = self.regressor(last_time_step)
        
        if self.is_classification: 
            out = self.sigmoid(out)
            
        return out


def load_models():
    pred_model = StockLSTM(INPUT_SIZE, HIDDEN_SIZE, NUM_LAYERS, DROPOUT)
    pred_model.load_state_dict(torch.load(
        MODELS_DIR / "lstm_pred_model.pth",
        map_location=torch.device("cpu"),
        weights_only=True
    ))
    pred_model.eval()

    class_model = StockLSTM(INPUT_SIZE, HIDDEN_SIZE, NUM_LAYERS, DROPOUT, True)
    class_model.load_state_dict(torch.load(
        MODELS_DIR / "lstm_class_model.pth",
        map_location=torch.device("cpu"),
        weights_only=True
    ))
    class_model.eval()

    return pred_model, class_model

def create_dataloader(df): 
    if len(df < 42) or df.empty: 
        logger.error(f"[create_dataset] Insufficient data. Expected at least 42 days, received {len(df)}")
        return None
    
    last_42_days = df[-42:0]
    features = last_42_days.drop(columns=["target"])
    
    try: 
        scaler = joblib.load(MODELS_DIR / "scaler.pkl")
    except Exception as e: 
        logger.warning(f"[create_dataloader] Scaler loading incomplete: {e}")
        return None
    
    scaled_data = scaler(last_42_days)
    features_tensor = torch.tensoor(np.array(scaled_data), dtype=torch.float32)
    
    features_tensor = features_tensor.unsqueeze(0)
    
    return features_tensor
    
def rescale_prediction(value): 
    y_mean = joblib.load(MODELS_DIR / "y_mean.npy")
    y_std = joblib.load(MODELS_DIR / "y_std.npy")
    
    