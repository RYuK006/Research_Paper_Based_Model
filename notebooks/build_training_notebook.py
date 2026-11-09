"""
Builds notebooks/train_research_lm.ipynb via nbformat.
Configured for Google Colab Free T4 + 5TB Google Drive + Auto-Resume Sharded QLoRA.
"""

from pathlib import Path
import nbformat as nbf


def generate_research_lm_notebook(output_path: str = "notebooks/train_research_lm.ipynb") -> None:
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "accelerator": "GPU",
        "colab": {
            "gpuType": "T4",
            "provenance": [],
        },
        "language_info": {
            "name": "python",
            "version": "3.10",
        },
    }

    cells = []

    # Title & Architecture
    cells.append(nbf.v4.new_markdown_cell(
        "# ⚡ Guaranteed Baseline QLoRA Training on Google Colab T4\n"
        "\n"
        "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RYuK006/Research_Paper_Based_Model/blob/main/notebooks/train_research_lm.ipynb)\n"
        "\n"
        "> **Model Target**: `Qwen2.5-7B-Instruct` 4-bit (with 3B fallback) + LoRA $r=16, \\alpha=32$\n"
        "> **Hardware Budget**: Free Colab T4 (16 GB VRAM, ~12 GB RAM, ~100 GB ephemeral disk) + 5 TB Google Drive\n"
        "> **Fault Tolerance**: Automatic resumption from Google Drive `manifest.json` on Colab disconnect\n"
        "> **Evaluation**: Pre-cutoff training vs. post-cutoff held-out perplexity & 10 historical discovery completions\n"
        "\n"
        "---"
    ))

    # Cell 1: Mount Google Drive
    cells.append(nbf.v4.new_markdown_cell(
        "### Step 1: Mount Google Drive\n"
        "Google Drive stores our authoritative checkpoints, tokenized shards (1-5 GB each), 4-bit base model snapshot, and `manifest.json`."
    ))
    cells.append(nbf.v4.new_code_cell(
        "# Mount Google Drive\n"
        "try:\n"
        "    from google.colab import drive\n"
        "    drive.mount('/content/drive')\n"
        "    print('Google Drive mounted successfully.')\n"
        "except Exception as e:\n"
        "    print(f'Drive mount notice: {e}')"
    ))

    # Cell 2: Check Hardware
    cells.append(nbf.v4.new_markdown_cell(
        "### Step 2: Verify GPU & Ephemeral Local Disk\n"
        "All active training occurs strictly on fast ephemeral local disk (`/content/local_training`)."
    ))
    cells.append(nbf.v4.new_code_cell(
        "!nvidia-smi\n"
        "!df -h /content"
    ))

    # Cell 3: Install Unsloth / PEFT
    cells.append(nbf.v4.new_markdown_cell(
        "### Step 3: Install High-Performance Unsloth / PEFT Libraries"
    ))
    cells.append(nbf.v4.new_code_cell(
        "!pip install -q --no-deps \"xformers<0.0.27\" \"trl<0.9.0\" peft accelerate bitsandbytes\n"
        "!pip install -q \"unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git\""
    ))

    # Cell 4: Clone Repo
    cells.append(nbf.v4.new_markdown_cell(
        "### Step 4: Clone Research Codebase & Prepare Environment"
    ))
    cells.append(nbf.v4.new_code_cell(
        "import os\n"
        "if not os.path.exists('Research_Paper_Based_Model'):\n"
        "    !git clone https://github.com/RYuK006/Research_Paper_Based_Model.git\n"
        "%cd Research_Paper_Based_Model"
    ))

    # Cell 5: Launch Resilient Training Loop
    cells.append(nbf.v4.new_markdown_cell(
        "### Step 5: Execute Resilient Training Loop (`colab/train.py`)\n"
        "- Streams shards one-by-one to fast ephemeral disk.\n"
        "- Checkpoints written locally, verified on Drive, then `manifest.json` is updated.\n"
        "- Re-running 'Run all' after a disconnect automatically detects the latest checkpoint and resumes seamlessly."
    ))
    cells.append(nbf.v4.new_code_cell(
        "!python colab/train.py \\\n"
        "    --model-id \"unsloth/Qwen2.5-7B-Instruct-bnb-4bit\" \\\n"
        "    --fallback-model-id \"unsloth/Qwen2.5-3B-Instruct-bnb-4bit\" \\\n"
        "    --drive-root \"/content/drive/MyDrive/Model_Training\" \\\n"
        "    --local-root \"/content/local_training\" \\\n"
        "    --db-path \"data/papers.db\" \\\n"
        "    --cutoff-year 2004 \\\n"
        "    --max-steps 1000 \\\n"
        "    --checkpoint-interval 50"
    ))

    # Cell 6: Held-Out Evaluation
    cells.append(nbf.v4.new_markdown_cell(
        "### Step 6: Held-Out Evaluation on Post-Cutoff Literature\n"
        "- Computes perplexity reduction on held-out post-cutoff papers.\n"
        "- Completes 10 historical discovery prefixes (e.g., $(La,Y)H_{10}$ at 160 GPa)."
    ))
    cells.append(nbf.v4.new_code_cell(
        "import json\n"
        "eval_path = '/content/local_training/held_out_eval_results.json'\n"
        "if os.path.exists(eval_path):\n"
        "    with open(eval_path, 'r', encoding='utf-8') as f:\n"
        "        results = json.load(f)\n"
        "    print(f'Base Model Perplexity:      {results[\"base_perplexity\"]:.2f}')\n"
        "    print(f'Fine-Tuned Perplexity:     {results[\"finetuned_perplexity\"]:.2f} (-{results[\"perplexity_reduction_pct\"]}%)')\n"
        "    print('\\nTop Discovery Completions:')\n"
        "    for c in results[\"completions\"][:3]:\n"
        "        print(f'Prompt: {c[\"prompt\"]}')\n"
        "        print(f'Generated: {c[\"completion\"]}\\n')\n"
        "else:\n"
        "    print('Evaluation results not found yet. Run Step 5 first.')"
    ))

    nb.cells = cells

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"Generated {out_file} successfully via nbformat.")


if __name__ == "__main__":
    generate_research_lm_notebook()
