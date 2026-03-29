import os


def save_settings(email: str, password: str, label: str = "투자"):
    # Minimal function: write to .env for tests
    with open(".env", "w") as f:
        f.write(f"GOOGLE_KEEP_EMAIL={email}\n")
        f.write(f"GOOGLE_KEEP_PASSWORD={password}\n")
        f.write(f"KEEP_LABEL={label}\n")
