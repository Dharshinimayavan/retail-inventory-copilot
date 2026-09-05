TRACK_ID=PS03

Retail - Sales and Inventory Copilot

An AI-powered retail assistant that helps store managers understand sales and inventory data, identify products that need attention, and receive practical, data-grounded recommendations through natural-language questions.

Problem Statement

Small retail businesses often have sales and inventory data but lack an easy way to turn that data into actionable decisions. Managers may need to manually inspect stock levels, sales performance, and overstocked products before deciding what to restock or promote.

Solution

Retail Sales & Inventory Copilot combines deterministic inventory analysis with Google Gemini to provide a simple conversational interface for retail decision-making.

The system:

Displays product and inventory information in a dashboard.

Detects low-stock products.

Detects potential overstocked products.

Identifies top-selling products.

Accepts natural-language questions from a manager.

Uses Gemini to convert the computed data into a clear business-oriented answer.

Grounds AI responses in the local retail dataset and deterministic analysis.

Provides evidence with the response.

Gracefully handles Gemini/API failures instead of inventing results.

Key Features

1. Inventory Dashboard

Provides an overview of:

Total number of products

Low-stock products

Overstocked products

Product-wise stock levels

Monthly sales

Product prices

Inventory status

2. Deterministic Inventory Analysis

Business rules are calculated by Python before the AI response is generated.

Current rules include:

Low Stock: stock level <= 10

Overstock: stock level >= 60 and monthly sales < 50

Top Sellers: products ranked by monthly sales

This keeps important numerical calculations deterministic rather than leaving them entirely to the LLM.

3. AI Retail Copilot

Managers can ask questions such as:

Which products need attention today?

Which product has the highest sales?

Which products are overstocked?

What should I restock first?

What action should I take for slow-moving inventory?

Gemini generates the final explanation using the supplied retail data and calculated analysis.

4. Grounded Responses

The AI is instructed to:

Use only the provided retail dataset and computed analysis.

Report actual numbers from the dataset.

Avoid unsupported assumptions.

Clearly state when the available data is insufficient.

Provide recommendations based on the available evidence.

Architecture

                +----------------------+
                |    Retail Manager    |
                +----------+-----------+
                           |
                           | Natural-language question
                           v
                +----------------------+
                |   Python Web Server   |
                |       app.py          |
                +----------+-----------+
                           |
              +------------+------------+
              |                         |
              v                         v
   +---------------------+   +----------------------+
   | Local Retail Data   |   | Deterministic        |
   | Product / Sales /   |-->| Inventory Analysis   |
   | Inventory Records   |   | Low / Over / Top     |
   +---------------------+   +----------+-----------+
                                        |
                                        v
                              +----------------------+
                              |    Google Gemini     |
                              | Grounded Explanation |
                              +----------+-----------+
                                         |
                                         v
                              +----------------------+
                              | Answer + Evidence    |
                              +----------------------+

Technology Stack

Backend: Python

Web Server: Python http.server

Frontend: HTML, CSS, JavaScript

AI: Google Gemini API

SDK: google-genai

Data: Local in-memory retail dataset

Port: 8000

Project Structure

retail-inventory-copilot/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore

Sample Dataset

The prototype uses a small local retail dataset containing products such as:

Product

Category

Stock

Monthly Sales

Price

Wireless Mouse

Electronics

8

145

799

Mechanical Keyboard

Electronics

65

42

2499

USB-C Cable

Accessories

12

210

499

Laptop Stand

Accessories

4

95

1299

Bluetooth Speaker

Electronics

85

18

1999

Webcam

Electronics

25

76

2999

Installation

1. Clone the repository

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd retail-inventory-copilot

2. Install dependencies

python -m pip install -r requirements.txt

3. Configure Gemini API Key

Set the API key as an environment variable named:

GEMINI_API_KEY

Do not hard-code the API key in app.py or commit it to GitHub.

4. Run the application

python app.py

Open:

http://localhost:8000

Example Queries

Try these questions in the Retail Copilot:

Which products need attention today?

Which product has the highest sales?

Which products are overstocked and what should I do?

What should I restock first?

Error Handling

If the Gemini service is unavailable or the API key is not configured, the application does not fabricate an AI answer. It falls back to data-based analysis and indicates that the AI service is unavailable.

Security

The Gemini API key is read from the GEMINI_API_KEY environment variable.

Never commit API keys, passwords, or other secrets to the repository.

Recommended .gitignore entries:

.env
__pycache__/
*.pyc
.venv/

Hackathon Alignment

This project is designed for PS03 - Retail: Sales and Inventory Copilot.

The application focuses on answering natural-language questions using store/catalogue/sales/stock information, identifying stock risks and sales patterns, and recommending actions using available data.

Demo

Demo Video

Add the final demo video link here:

<YOUR_DEMO_VIDEO_URL>

Repository

<YOUR_GITHUB_REPOSITORY_URL>

Future Enhancements

Upload CSV files for real retail datasets.

Add historical sales trends and charts.

Add store-wise inventory analysis.

Add demand forecasting.

Add reorder quantity recommendations.

Add downloadable inventory reports.

Add role-based access for store managers and staff.

Conclusion

Retail Sales & Inventory Copilot turns raw retail data into simple, actionable insights. By combining deterministic business rules with grounded Gemini-generated explanations, it helps managers identify inventory risks and make faster, data-driven decisions.