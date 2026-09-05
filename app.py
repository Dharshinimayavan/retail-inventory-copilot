import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from google import genai
from dotenv import load_dotenv

load_dotenv()
# -----------------------------
# Sample Retail Data
# -----------------------------
PRODUCTS = [
    {
        "id": 1,
        "product": "Wireless Mouse",
        "category": "Electronics",
        "stock": 8,
        "monthly_sales": 145,
        "price": 799
    },
    {
        "id": 2,
        "product": "Mechanical Keyboard",
        "category": "Electronics",
        "stock": 65,
        "monthly_sales": 42,
        "price": 2499
    },
    {
        "id": 3,
        "product": "USB-C Cable",
        "category": "Accessories",
        "stock": 12,
        "monthly_sales": 210,
        "price": 499
    },
    {
        "id": 4,
        "product": "Laptop Stand",
        "category": "Accessories",
        "stock": 4,
        "monthly_sales": 95,
        "price": 1299
    },
    {
        "id": 5,
        "product": "Bluetooth Speaker",
        "category": "Electronics",
        "stock": 85,
        "monthly_sales": 18,
        "price": 1999
    },
    {
        "id": 6,
        "product": "Webcam",
        "category": "Electronics",
        "stock": 25,
        "monthly_sales": 76,
        "price": 2999
    }
]


# -----------------------------
# Deterministic Analysis
# -----------------------------
def analyze_inventory():

    low_stock = []
    overstock = []

    for p in PRODUCTS:

        # Low stock rule
        if p["stock"] <= 10:
            low_stock.append(p)

        # Overstock rule
        if p["stock"] >= 60 and p["monthly_sales"] < 50:
            overstock.append(p)

    top_products = sorted(
        PRODUCTS,
        key=lambda x: x["monthly_sales"],
        reverse=True
    )[:3]

    return {
        "low_stock": low_stock,
        "overstock": overstock,
        "top_products": top_products
    }


# -----------------------------
# Clean Gemini Response
# -----------------------------
def clean_ai_response(text):

    if not text:
        return "No AI response was generated."

    text = text.replace("### ", "")
    text = text.replace("## ", "")
    text = text.replace("# ", "")
    text = text.replace("**", "")
    text = text.replace("---", "")
    text = text.replace("* ", "- ")

    return text.strip()


# -----------------------------
# Gemini AI
# -----------------------------
def ask_gemini(question):

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:

        return {
            "answer":
            "Gemini API key is not configured. Showing data-based analysis instead.",

            "evidence":
            "Local retail dataset"
        }

    try:

        client = genai.Client(
            api_key=api_key
        )

        inventory_analysis = analyze_inventory()

        prompt = f"""
You are a retail sales and inventory assistant.

Answer ONLY using the retail data provided below.
Do not invent numbers, products, sales values, or stock values.

Retail data:
{json.dumps(PRODUCTS, indent=2)}

Deterministic analysis:
{json.dumps(inventory_analysis, indent=2)}

Manager question:
{question}

Requirements:

1. Give a clear and direct answer.
2. Mention actual numbers from the provided data.
3. Explain the evidence behind the answer.
4. If the data cannot answer the question, clearly say:
   "The available data is insufficient to answer this."
5. Recommend an action when appropriate.
6. Use plain text only.
7. Do not use Markdown formatting.
8. Do not use symbols such as ###, **, *, or ---.
9. Use simple numbered sections when useful.
10. Keep the answer concise and easy for a retail manager to understand.
"""

        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt
        )

        clean_answer = clean_ai_response(
            response.text
        )

        return {
            "answer": clean_answer,
            "evidence":
            "Retail dataset + deterministic inventory analysis"
        }

    except Exception as e:

        print(
            "GEMINI ERROR:",
            repr(e)
        )

        return {
            "answer":
            "AI service is temporarily unavailable. Please try again.",

            "evidence":
            "Local retail dataset remains available"
        }


# -----------------------------
# HTML Dashboard
# -----------------------------
HTML = """
<!DOCTYPE html>
<html>

<head>

    <meta charset="UTF-8">

    <title>
        Retail Sales & Inventory Copilot
    </title>

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f4f7fb;
            color: #172033;
        }

        header {
            background: #172033;
            color: white;
            padding: 25px 50px;
        }

        header h1 {
            margin: 0;
        }

        header p {
            margin-bottom: 0;
            color: #cbd5e1;
        }

        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }

        .card h3 {
            margin-top: 0;
        }

        .number {
            font-size: 35px;
            font-weight: bold;
        }

        .section {
            background: white;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            padding: 14px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }

        th {
            background: #f8fafc;
        }

        .low {
            color: #dc2626;
            font-weight: bold;
        }

        .over {
            color: #d97706;
            font-weight: bold;
        }

        input {
            width: 75%;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }

        button {
            padding: 15px 22px;
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
        }

        button:hover {
            background: #1d4ed8;
        }

        #answer {
            margin-top: 20px;
            padding: 20px;
            background: #f8fafc;
            border-radius: 10px;
            white-space: pre-wrap;
            line-height: 1.6;
        }

        @media(max-width: 800px) {

            .cards {
                grid-template-columns: 1fr;
            }

            input {
                width: 100%;
                margin-bottom: 10px;
            }

        }

    </style>

</head>


<body>


<header>

    <h1>
        🛍️ Retail Sales & Inventory Copilot
    </h1>

    <p>
        AI-powered decision support for retail managers
    </p>

</header>


<div class="container">


    <!-- Dashboard Cards -->

    <div class="cards">


        <div class="card">

            <h3>
                Products
            </h3>

            <div
                class="number"
                id="productCount"
            >
                -
            </div>

        </div>


        <div class="card">

            <h3>
                Low Stock
            </h3>

            <div
                class="number"
                id="lowStock"
            >
                -
            </div>

        </div>


        <div class="card">

            <h3>
                Overstock
            </h3>

            <div
                class="number"
                id="overStock"
            >
                -
            </div>

        </div>


    </div>


    <!-- Inventory -->

    <div class="section">

        <h2>
            📦 Inventory Overview
        </h2>


        <table>

            <thead>

                <tr>

                    <th>
                        Product
                    </th>

                    <th>
                        Category
                    </th>

                    <th>
                        Stock
                    </th>

                    <th>
                        Monthly Sales
                    </th>

                    <th>
                        Status
                    </th>

                </tr>

            </thead>


            <tbody
                id="inventoryTable"
            ></tbody>

        </table>

    </div>


    <!-- AI Copilot -->

    <div class="section">


        <h2>
            🤖 Ask the Copilot
        </h2>


        <p>
            Ask questions using normal language.
        </p>


        <input
            id="question"
            placeholder="Example: Which products need attention today?"
        >


        <button onclick="askQuestion()">
            Ask AI
        </button>


        <div id="answer">

            Your AI answer will appear here.

        </div>


    </div>


</div>


<script>


async function loadDashboard() {

    const response =
        await fetch("/api/dashboard");

    const data =
        await response.json();


    document.getElementById(
        "productCount"
    ).innerText =
        data.products.length;


    document.getElementById(
        "lowStock"
    ).innerText =
        data.analysis.low_stock.length;


    document.getElementById(
        "overStock"
    ).innerText =
        data.analysis.overstock.length;


    const table =
        document.getElementById(
            "inventoryTable"
        );


    table.innerHTML = "";


    data.products.forEach(p => {

        let status = "Healthy";

        let className = "";


        if (p.stock <= 10) {

            status = "LOW STOCK";

            className = "low";

        }


        if (
            p.stock >= 60 &&
            p.monthly_sales < 50
        ) {

            status = "OVERSTOCK";

            className = "over";

        }


        table.innerHTML += `

            <tr>

                <td>
                    ${p.product}
                </td>

                <td>
                    ${p.category}
                </td>

                <td>
                    ${p.stock}
                </td>

                <td>
                    ${p.monthly_sales}
                </td>

                <td class="${className}">
                    ${status}
                </td>

            </tr>

        `;

    });

}



async function askQuestion() {

    const question =
        document.getElementById(
            "question"
        ).value;


    if (!question.trim()) {

        alert(
            "Please enter a question."
        );

        return;

    }


    document.getElementById(
        "answer"
    ).innerText =
        "Analyzing retail data...";


    try {

        const response =
            await fetch(
                "/api/ask",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question:
                            question
                    })
                }
            );


        const data =
            await response.json();


        document.getElementById(
            "answer"
        ).innerText =

            data.answer +

            "\\n\\nEvidence: " +

            data.evidence;

    }

    catch (error) {

        document.getElementById(
            "answer"
        ).innerText =
            "Unable to connect to the AI service.";

    }

}


loadDashboard();

</script>


</body>

</html>
"""

# -----------------------------
# HTTP Server
# -----------------------------
class Handler(BaseHTTPRequestHandler):

    # -------------------------
    # Send JSON Response
    # -------------------------
    def send_json(self, data):

        body = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(body))
        )

        self.end_headers()

        self.wfile.write(body)


    # -------------------------
    # GET Requests
    # -------------------------
    def do_GET(self):

        path = urlparse(self.path).path

        if path == "/":

            body = HTML.encode("utf-8")

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )

            self.send_header(
                "Content-Length",
                str(len(body))
            )

            self.end_headers()

            self.wfile.write(body)

        elif path == "/api/dashboard":

            self.send_json({
                "products": PRODUCTS,
                "analysis": analyze_inventory()
            })

        else:

            self.send_response(404)
            self.end_headers()


    # -------------------------
    # POST Requests
    # -------------------------
    def do_POST(self):

        path = urlparse(self.path).path

        if path == "/api/ask":

            try:

                length = int(
                    self.headers.get(
                        "Content-Length",
                        0
                    )
                )

                body = self.rfile.read(length)

                data = json.loads(body)

                result = ask_gemini(
                    data.get(
                        "question",
                        ""
                    )
                )

                self.send_json(result)

            except Exception:

                self.send_json({

                    "answer":
                        "Invalid request. Please try again.",

                    "evidence":
                        "Local retail dataset"

                })

        else:

            self.send_response(404)
            self.end_headers()


# -----------------------------
# Start Application
# -----------------------------
if __name__ == "__main__":

    server = HTTPServer(
        ("0.0.0.0", 8000),
        Handler
    )

    print("Retail Copilot running at:")

    print("http://localhost:8000")

    server.serve_forever()