#!/usr/bin/env python3
"""
簡單的應用程式啟動腳本
"""

import os
from app_simple import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 