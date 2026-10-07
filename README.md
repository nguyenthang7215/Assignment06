# Assignment 06 - Multimodal Search System for E-Commerce

This project is a multimodal e-commerce search prototype implemented with a three-layer architecture. It supports text search, simulated voice search, image-similarity search, ranking, evaluation, and optional multimodal and order-search extensions.

## Requirements

- Python 3.10 or later; Python 3.12 is recommended.
- NumPy.
- Pillow.
- Flask.
- Optional advanced modes use PyTorch, torchvision, and scikit-learn from `code/requirements-advanced.txt`.

## Installation

On Windows PowerShell:

```powershell
cd code
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Running the Program

Run the complete demonstration:

```powershell
python main.py demo
```

Run the local web interface, then open <http://127.0.0.1:5000>:

```powershell
python web.py
```

Run an individual search mode:

```powershell
python main.py text "black running shoes"
python main.py voice "find running shoes under 110 dollars"
python main.py image "dataset/images/nike_black_running_shoes.png"
python main.py multimodal "black shoes" "dataset/images/nike_black_running_shoes.png"
python main.py order "find my order O001"
```

Generate the experimental-evaluation files in `code/results/`:

```powershell
python evaluate.py
```

Run the automated tests:

```powershell
python -m unittest discover -s tests -v
```

The current suite has 13 passing tests. `evaluate.py` checks 10 controlled queries, including a negative brand-and-price case. These results do not establish production accuracy.

## Optional Advanced Modes

Install `requirements-advanced.txt`, then set any of these PowerShell environment variables before starting the app:

```powershell
$env:SEARCH_IMAGE_ENCODER = "mobilenet"
$env:SEARCH_VECTOR_BACKEND = "sqlite"
$env:SEARCH_TEXT_MODE = "semantic"
python web.py
```

MobileNet downloads official pretrained weights on first use. The SQLite vector store persists vectors but performs an exact scan. The semantic mode uses TF-IDF with truncated SVD on the ten-product catalog, so relatedness can be weak. A compatible browser can capture speech through the Web Speech API; typed transcripts remain available.

Regenerate the sample images if necessary:

```powershell
python scripts/generate_sample_images.py
```

## Project Structure

```text
code/
|-- main.py                     # CLI entry point
|-- web.py                      # Flask website
|-- app_factory.py              # Dependency composition root
|-- evaluate.py                 # Experimental evaluation
|-- presentation/               # Presentation Layer
|-- application/                # Application/Intelligence Layer
|-- data_access/                # Data Layer repositories and vector index
|-- domain/                     # Shared domain objects
|-- dataset/
|   |-- products.json           # Ten product records
|   |-- orders.json             # Sample orders
|   `-- images/                 # Ten sample product images
|-- results/                    # Generated evaluation files
|-- scripts/                    # Sample-data utilities
`-- tests/                      # Automated tests
|-- templates/, static/         # Website markup, styles, and JavaScript
```

The assignment handout shows two folders named `data/`: one for repository source files and one for dataset files. This implementation uses `data_access/` and `dataset/` to remove that naming ambiguity while preserving the required Data Layer responsibilities.

## Limitations

- Voice search simulates speech-to-text by accepting a transcript.
- The image encoder uses color histograms and a 3-by-3 spatial grid rather than a deep-learning embedding.
- The dataset is small and controlled; its success rate is not representative of production accuracy.
- VectorIndex is stored in memory rather than in a vector database.
- The local web interface and order lookup do not include user authentication.
