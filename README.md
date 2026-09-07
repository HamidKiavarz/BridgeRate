# BridgeRate

BridgeRate predicts bridge deck condition ratings from California National Bridge Inventory (NBI) data. The main workflow is in `BridgeRate.ipynb`, which prepares bridge features, trains AutoGluon Tabular XGBoost classifiers, and exports model reports/evaluation summaries.

## Repository Contents

- `BridgeRate.ipynb` - Google Colab notebook for training and evaluating deck rating models.
- `Meta_Data.xlsx` - project metadata/reference workbook.
- `Statics.xlsx` - project statistics workbook.
- `Model_Results/` - exported CSV reports and evaluation summaries.
- `requirements.txt` - Python dependencies for running the notebook outside Colab.

## Data Requirements

The notebook expects yearly California NBI workbooks named like:

```text
California2024.xlsx
California2023.xlsx
...
California1992.xlsx
```

By default, these files are read from Google Drive:

```text
/content/drive/My Drive/BridgeResearchProject/NBIDataCollected
```

Saved AutoGluon models and generated reports are written to:

```text
/content/drive/My Drive/BridgeResearchProject/PredictModels
```

If you run locally instead of in Colab, update `DRIVE_ROOT`, `DATA_DIR`, and `OUT_DIR` in the notebook.

## Modeling Workflow

The notebook:

1. Loads selected NBI columns from yearly California Excel files.
2. Engineers bridge features including `Age`, `Reconstructed`, `ADT`, `Curb_Width`, and `Deck_Area`.
3. Renames NBI fields into modeling-friendly feature names.
4. Uses `DECK_COND_058` as the target label `Deck_Rate`.
5. Keeps deck rating classes `4, 5, 6, 7, 8, 9`.
6. Trains cumulative models from `2024` back to earlier years.
7. Saves classification reports, confusion matrices, and holdout-year summaries.

The current included `eval_2025_SUMMARY.csv` shows the best listed model span as `2024-2021`, with accuracy about `0.8589` and weighted F1 about `0.8513`.

## Running In Colab

1. Open `BridgeRate.ipynb` in Google Colab.
2. Confirm the yearly NBI Excel files exist in the expected Google Drive folder.
3. Run the install/mount cell.
4. Edit the settings cell if needed:
   - `START_YEAR`
   - `END_YEAR`
   - `TEST_YEAR`
   - `DATA_DIR`
   - `OUT_DIR`
5. Run the training and evaluation cells.

## Running Locally

Create an environment and install dependencies:

```bash
pip install -r requirements.txt
```

Then open the notebook with Jupyter and update the data/output paths to local folders before running.

## Notes

Raw NBI workbooks and saved AutoGluon model directories can become large, so they are intentionally excluded from git by `.gitignore`. The small exported CSV summaries in `Model_Results/` are suitable to keep in the repository.
