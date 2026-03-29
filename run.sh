#!/bin/bash
# Streamlit 실행 스크립트

cd /Users/prodigyduck/git/financing

# 가상환경 활성화
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# PYTHONPATH 설정 (src 폴더 포함)
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Streamlit 실행
echo "" | streamlit run src/presentation/app.py --server.address 0.0.0.0 --server.port 8504
