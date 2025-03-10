#!/bin/bash
echo "启动后端服务器..."
source venv_py39/bin/activate
export PYTHONPATH=$PYTHONPATH:$(pwd)
python simple_fastapi.py
