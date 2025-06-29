import torch

if torch.cuda.is_available():
    print("CUDA 可用，GPU 数量：", torch.cuda.device_count())
    print("当前使用的 GPU 设备索引：", torch.cuda.current_device())
    print("GPU 设备名称：", torch.cuda.get_device_name(0))
else:
    print("CUDA 不可用，无法使用 GPU。")
