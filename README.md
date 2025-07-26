# water_project

This project is a **Streamlit-based web application** for calculating **wall and bulk chlorine decay coefficients** in water distribution systems. It supports both **manual input** and **CSV dataset upload**, making it useful for water quality engineers and researchers.

---

## **Features**

* **Two Decay Models:**

  * **Wall Decay Coefficient (k<sub>w</sub>)** — accounts for pipe material and water chemistry.
  * **Bulk Decay Coefficient (k<sub>b</sub>)** — influenced by water quality parameters.
* **Dual Input Modes:**

  * **Upload Dataset:** Process bulk data from CSV files.
  * **Manual Input:** Perform individual calculations.
* **Automatic Correction Factors:**

  * Adjusts decay coefficients based on pH, iron, nitrite, manganese, and hydrogen sulfide levels.
* **Interactive UI:** Built with **Streamlit**, providing real-time calculations.
* **Download Results:** Export processed datasets (CSV) with decay results.
* **Contact Time Calculation:** Automatically computes residence/contact time based on pipe length and flow velocity.

---

## **Tech Stack**

* **Frontend/UI:** Streamlit
* **Backend/Logic:** Python (NumPy, Pandas, Math library)
* **Libraries:**

  * `streamlit`
  * `pandas`
  * `numpy`
  * `math`

---

## **Project Structure**

```
Chlorine-Decay-Calculator/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## **Key Formulas**

1. **Contact Time (hrs):**

   $$
   t = \frac{L}{V \cdot 3600}
   $$

   Where:
   *L = Pipe Length (m)*
   *V = Velocity (m/s)*

2. **Base Decay Coefficient (k<sub>b</sub>):**

   $$
   k_b = -\frac{\ln(C / C_0)}{t}
   $$

   Where:
   *C = Final Chlorine (PPM)*
   *C<sub>0</sub> = Initial Chlorine (PPM)*
   *t = Contact Time (hrs)*

3. **Wall Decay Coefficient (k<sub>w</sub>):**

   $$
   k_w = - \frac{D}{4t} \cdot \ln \left(\frac{C}{C_0}\right)
   $$

   Where:
   *D = Pipe Diameter (m)*

4. **Correction Factors:**
   Final *k<sub>w</sub>* is adjusted by multiple factors: pH, iron, nitrite, manganese, and hydrogen sulfide.

---

## **Installation & Setup**

### **1. Clone the repository**

```bash
git clone https://github.com/rahulpihub/water_project.git
cd water_project
```

### **2. Create and activate a virtual environment** (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### **3. Install dependencies**

```bash
pip install -r requirements.txt
```

*(If `requirements.txt` is not created, use: `pip install streamlit pandas numpy`)*

### **4. Run the Streamlit app**

```bash
streamlit run app.py
```

---

## **Usage**

1. **Choose Mode:** Select **Upload Dataset** or **Manual Input** from the sidebar.
2. **Wall Decay:** Input pipe length, diameter, velocity, and chemistry values to compute k<sub>w</sub>.
3. **Bulk Decay:** Enter chlorine concentration data and chemical factors to compute k<sub>b</sub>.
4. **Export Results:** Download the computed dataset as CSV.

---

## **CSV Dataset Requirements**

For **Upload Dataset** mode, your CSV must include:

* `Velocity m/s` (column name)
* `Length (m)` and `Diameter (mm)`
* `Final Chlorine (PPM)`
* Optional: `pH`, `Iron`, `Nitrite`, `Manganese`, `Hydrogen Sulfide`

---


