
# API Endpoint

## Predict Business Feasibility

### Endpoint

```http
POST /predict
```

---

# Request Body

```json
{
  "Kategori_Bisnis": "F&B",
  "Modal_Awal": 25000000,
  "Biaya_Sewa_Bulan": 4000000,
  "Biaya_Operasional_Bulan": 6000000,
  "HPP_Per_Produk": 12000,
  "Harga_Jual": 25000,
  "Trafik_Harian": 55,
  "Rasio_Sewa_Modal": 0.16
}
```

---

# Request Parameters

| Field | Type | Description |
|---|---|---|
| Kategori_Bisnis | string | Business category |
| Modal_Awal | float | Initial capital |
| Biaya_Sewa_Bulan | float | Monthly rental cost |
| Biaya_Operasional_Bulan | float | Monthly operational cost |
| HPP_Per_Produk | float | Cost of goods sold |
| Harga_Jual | float | Selling price |
| Trafik_Harian | float | Daily customer traffic |
| Rasio_Sewa_Modal | float | Rental-to-capital ratio |

---

# Available Business Categories

- F&B
- Retail
- Jasa

---

# Example Response (Success)

```json
{
  "prediction": "SUKSES",
  "confidence_score": 0.9238895177841187,
  "professional_review": "Berdasarkan data bisnis dan prediksi model, bisnis jasa ini memiliki prospek yang baik dengan confidence sebesar 0,92. Modal awal usaha jasa cukup stabil, trafik pelanggan jasa cukup baik, rasio sewa terhadap modal masih sehat, dan margin keuntungan baik. Oleh karena itu, disarankan untuk mempertahankan pengelolaan modal usaha jasa, kualitas layanan kepada pelanggan, rasio sewa agar tetap stabil, dan strategi harga serta efisiensi produksi.",
  "recommendations": [
    {
      "title": "Modal awal usaha jasa cukup stabil",
      "status": "Baik",
      "description": "Pertahankan pengelolaan modal usaha jasa."
    },
    {
      "title": "Trafik pelanggan jasa cukup baik",
      "status": "Baik",
      "description": "Pertahankan kualitas layanan kepada pelanggan."
    },
    {
      "title": "Rasio sewa terhadap modal masih sehat",
      "status": "Baik",
      "description": "Pertahankan rasio sewa agar tetap stabil."
    },
    {
      "title": "Margin keuntungan Baik",
      "status": "Baik",
      "description": "Pertahankan strategi harga dan efisiensi produksi."
    }
  ],
  "final_summary": "Bisnis jasa ini memiliki prospek yang baik dan dapat terus berkembang dengan mempertahankan kualitas layanan dan strategi bisnis yang tepat. Dengan demikian, bisnis ini dapat meningkatkan keuntungan dan mempertahankan posisinya di pasar."
}
```

# Example Response (Bacrupt)

```json
{
  "prediction": "RISIKO BANGKRUT",
  "confidence_score": 0.8986555337905884,
  "professional_review": "Berdasarkan data bisnis yang disediakan, bisnis retail ini memiliki modal awal yang cukup kuat sebesar 25.000.000,0 dan trafik harian yang cukup baik sebesar 25,0. Namun, perlu diperhatikan bahwa rasio sewa modal sebesar 0,28 dan biaya sewa bulanan sebesar 7.000.000,0 yang cukup besar. Selain itu, margin keuntungan produk yang dihasilkan terlalu kecil karena harga jual yang terlalu rendah atau biaya produksi yang terlalu tinggi. Dengan demikian, perlu dilakukan penyesuaian strategi untuk meningkatkan keuntungan dan mengurangi biaya.",
  "recommendations": [
    {
      "title": "Modal awal retail cukup kuat",
      "status": "Baik",
      "description": "Modal sudah cukup stabil untuk menjalankan bisnis retail."
    },
    {
      "title": "Jumlah pelanggan retail cukup baik",
      "status": "Baik",
      "description": "Pertahankan strategi penjualan yang sudah berjalan."
    },
    {
      "title": "Rasio sewa cukup besar dan perlu diperhatikan",
      "status": "Perhatian",
      "description": "Mengurangi biaya sewa bulanan untuk mengurangi rasio sewa."
    },
    {
      "title": "Margin keuntungan produk terlalu kecil",
      "status": "Kritis",
      "description": "Naikkan harga jual atau tekan biaya produksi."
    }
  ],
  "final_summary": "Bisnis retail ini memiliki potensi yang baik, namun perlu diperhatikan beberapa aspek seperti rasio sewa modal dan margin keuntungan produk. Dengan melakukan penyesuaian strategi, seperti mengurangi biaya sewa bulanan dan meningkatkan harga jual atau menekan biaya produksi, bisnis ini dapat meningkatkan keuntungan dan mengurangi risiko bangkrut."
}
```

---

# Prediction Labels

| Label | Description |
|---|---|
| SUKSES | Business predicted to succeed |
| RISIKO BANGKRUT | Business predicted to have high bankruptcy risk |

---

# Recommendation Status

| Status | Meaning |
|---|---|
| Baik | Healthy business condition |
| Perhatikan | Needs attention |
| Bahaya | High-risk condition |

---
