#!/bin/bash
# Streamlit을 Tailscale 네트워크에서 접근 가능하게 실행

cd /Users/prodigyduck/git/financing

# 가상환경 활성화
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Streamlit 실행 (모든 인터페이스에서 리스닝)
streamlit run src/presentation/app.py --server.address 0.0.0.0 --server.port 8501
