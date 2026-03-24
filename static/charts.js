const BASE_SUGAR = nutrients.sugar || 0;
function updateSugar(val){
  document.getElementById("sugarValue").innerText = val;

  let baseSugar = BASE_SUGAR;
  let newSugar = baseSugar - val;

  let risk = "Unhealthy";

  if (newSugar <= 25) {
      risk = "Healthy";
  } else if (newSugar <= 50) {
      risk = "Moderate";
  }

  document.getElementById("predictedRisk").innerText = risk;
}