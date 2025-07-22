from setuptools import setup, find_packages

setup(
    name="whisper-notebook",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask>=3.1.1",
        "gunicorn>=23.0.0",
        "openai-whisper>=20240930",
        "numpy>=1.26.4",
        "torch>=2.7.1",
        "tqdm>=4.67.1",
        "ffmpeg-python",
        "Werkzeug>=3.0.0"
    ],
    python_requires=">=3.8",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)