document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("queryForm");
  const input = document.getElementById("siteName");
  const loading = document.getElementById("loading");
  const responseText = document.getElementById("responseText");

  form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const userInput = input.value.trim();
      if (!userInput) return;

      loading.style.display = "block";
      responseText.textContent = "";

      try {
          const response = await fetch("/ask", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
              },
              body: JSON.stringify({ message: userInput }),
          });

          if (response.ok) {
              const data = await response.json();
              responseText.textContent = data.response;
          } else {
              responseText.textContent = "حدث خطأ أثناء جلب الاستجابة.";
          }
      } catch (error) {
          responseText.textContent = "حدث خطأ في الاتصال بالخادم.";
      } finally {
          loading.style.display = "none";
          input.value = "";
      }
  });
});