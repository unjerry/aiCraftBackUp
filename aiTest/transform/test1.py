import torch
import torch.nn as nn

if __name__ == "__main__":
    transformer_model = nn.Transformer(nhead=16, num_encoder_layers=12)
    src = torch.rand((512))
    tgt = torch.rand((512))  # What is tgt??
    out = transformer_model(src, tgt)
    print(src.shape, tgt.shape, out.shape)
