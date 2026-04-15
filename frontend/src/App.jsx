import { useState } from "react";
import { predictPrice } from "./api";

function App() {
  const [form, setForm] = useState({
    brand: 0,
    year: 2020,
    mileage: 50000,
    fuel: 0
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: Number(e.target.value) });
  };

  const handlePredict = async () => {
    try {
      const res = await predictPrice(form);
      setResult(res.data.predicted_price);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h1>🚗 Car Price Predictor</h1>

      <input name="brand" placeholder="Brand (0,1,2)" onChange={handleChange} />
      <br /><br />

      <input name="year" placeholder="Year" onChange={handleChange} />
      <br /><br />

      <input name="mileage" placeholder="Mileage" onChange={handleChange} />
      <br /><br />

      <input name="fuel" placeholder="Fuel (0=Petrol,1=Diesel)" onChange={handleChange} />
      <br /><br />

      <button onClick={handlePredict}>
        Predict Price
      </button>

      {result && (
        <h2 style={{ marginTop: "20px" }}>
          💰 Predicted Price: {result} $
        </h2>
      )}
    </div>
  );
}

export default App;