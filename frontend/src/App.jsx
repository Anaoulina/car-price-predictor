import { useState } from "react";
import axios from "axios";

function App() {
  const [formData, setFormData] = useState({
    brand: 'DACIA',
    year: 2020,
    mileage: 100000,
    fuel: 'Diesel'
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: (name === 'year' || name === 'mileage') ? Number(value) : value
    });
  };

  const handlePredict = async () => {
    try {
      // تأكد أن الرابط هو اللي خدام فيه الباك-أند ديالك
      const res = await axios.post("http://127.0.0.1:8000/predict", formData);
      setResult(res.data.predicted_price);
    } catch (err) {
      console.error(err);
      alert("Error: Check if Backend is running!");
    }
  };

  // --- Inline Styles (باش يتقاد الديزاين 100% بلا مشاكل CSS خارجية) ---
  const styles = {
    body: {
      backgroundColor: '#0f172a',
      minHeight: '100vh',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      fontFamily: 'Segoe UI, sans-serif',
      margin: 0
    },
    card: {
      backgroundColor: '#1e293b',
      padding: '30px',
      borderRadius: '15px',
      width: '350px',
      boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.5)',
      color: 'white'
    },
    title: {
      textAlign: 'center',
      color: '#38bdf8',
      marginBottom: '25px',
      fontSize: '24px'
    },
    inputGroup: {
      marginBottom: '15px',
      display: 'flex',
      flexDirection: 'column',
      gap: '5px'
    },
    label: {
      fontSize: '14px',
      color: '#94a3b8',
      fontWeight: '600'
    },
    input: {
      padding: '12px',
      borderRadius: '8px',
      border: '1px solid #334155',
      backgroundColor: '#0f172a',
      color: 'white',
      fontSize: '16px'
    },
    button: {
      width: '100%',
      padding: '12px',
      backgroundColor: '#38bdf8',
      border: 'none',
      borderRadius: '8px',
      color: '#0f172a',
      fontWeight: 'bold',
      fontSize: '16px',
      cursor: 'pointer',
      marginTop: '10px'
    },
    result: {
      marginTop: '20px',
      padding: '15px',
      backgroundColor: 'rgba(56, 189, 248, 0.1)',
      borderRadius: '10px',
      textAlign: 'center',
      border: '1px solid #38bdf8'
    }
  };

  return (
    <div style={styles.body}>
      <div style={styles.card}>
        <h1 style={styles.title}>🚗 Car Price Predictor</h1>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Brand</label>
          <input name="brand" value={formData.brand} onChange={handleChange} style={styles.input} />
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Year</label>
          <input name="year" type="number" value={formData.year} onChange={handleChange} style={styles.input} />
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Mileage (KM)</label>
          <input name="mileage" type="number" value={formData.mileage} onChange={handleChange} style={styles.input} />
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Fuel</label>
          <input name="fuel" value={formData.fuel} onChange={handleChange} style={styles.input} />
        </div>

        <button onClick={handlePredict} style={styles.button}>Predict Price</button>

        {result && (
          <div style={styles.result}>
            <span style={{ fontSize: '14px', color: '#94a3b8' }}>Estimated Price:</span>
            <div style={{ fontSize: '22px', fontWeight: 'bold', color: '#38bdf8', marginTop: '5px' }}>
              {Number(result).toLocaleString()} DH
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;