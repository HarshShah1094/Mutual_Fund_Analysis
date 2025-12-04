## Mutual Fund NAV Analysis – Console Application

This project is a simple Python console application that reads mutual fund NAV data from a CSV file and performs basic analysis.

- **Task 2 – Data Ingestion**: Read and process NAV data from a CSV file (`MF1.csv`).  
- **Task 3 – Analysis & Computation**:  
  - Calculate 7‑year CAGR (Compound Annual Growth Rate) for each mutual fund.  
  - Display the **top 2** and **bottom 2** funds by CAGR.  
  - Detect days where a fund’s NAV changed by more than **±5%** compared to the previous NAV and print those swings.

---

## 1. Requirements and Dependencies

- **Python**: Version 3.8 or later is recommended.
- **Python packages**:
  - `pandas`

### 1.1. Installing Python packages

From a terminal (PowerShell on Windows), run:

```bash
pip install pandas
```

If you have multiple Python versions, you may need to use `pip3` instead of `pip`.

---

## 2. Project Files

- `MF1.csv` – Input dataset containing NAV history.  
  - Expected columns: `Fund Name`, `Date`, `NAV`  
  - Date format: `DD-MM-YYYY` (for example `26-11-2018`).
- `mutual_fund_analysis.py` – Main console application that implements Task 2 and Task 3.

---

## 3. How to Run the Program (Step‑by‑Step)

1. **Open PowerShell** (or any terminal) on your system.
2. **Navigate to the project folder**:
3. **(First time only) Install dependencies**:

   ```bash
   pip install pandas
   ```

4. **Run the Python program**:

   ```bash
   python mutual_fund_analysis.py
   ```

5. When prompted with:

   ```text
   Enter path to NAV CSV file (e.g. MF1.csv):
   ```

   type:

   ```text
   MF1.csv
   ```

   and press Enter.

6. The program will:
   - Read and validate the CSV file (Task 2).  
   - Compute the **7‑year CAGR** for each fund and display the **top 2** and **bottom 2** funds (Task 3.1 & 3.2).  
   - Detect and print all **NAV swings > ±5%**, listing fund name, date, and percentage change (Task 3.3).

---

## 4. Notes

- If the CSV has invalid dates or NAV values, those rows are skipped and a short message is printed.  
- You can point the program to any other CSV file with the same column format by entering its path when prompted.



