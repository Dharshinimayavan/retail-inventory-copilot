TRACK_ID=PS03

# Retail - Sales and Inventory Copilot

An AI-powered retail assistant that helps store managers understand sales and inventory data, identify products that need attention, and receive practical, data-grounded recommendations through natural-language questions.

## Live Demo

https://retail-inventory-copilot.onrender.com/

## Problem Statement

Small retail businesses often have sales and inventory data but lack an easy way to turn that data into actionable decisions.

Managers may need to manually inspect stock levels, sales performance, and overstocked products before deciding what to restock or promote.

This manual process can be time-consuming and may make it difficult to quickly identify products that require immediate attention.

## Solution

Retail Sales & Inventory Copilot combines deterministic inventory analysis with Google Gemini to provide a simple conversational interface for retail decision-making.

The system:

- Displays product and inventory information in a dashboard.
- Detects low-stock products.
- Detects potential overstocked products.
- Identifies top-selling products.
- Accepts natural-language questions from a manager.
- Uses Gemini to convert computed data into a clear business-oriented answer.
- Grounds AI responses in the local retail dataset and deterministic analysis.
- Provides evidence with the response.
- Gracefully handles Gemini/API failures instead of inventing results.

## Key Features

### 1. Inventory Dashboard

Provides an overview of:

- Total number of products
- Low-stock products
- Overstocked products
- Product-wise stock levels
- Monthly sales
- Product prices
- Inventory status

### 2. Deterministic Inventory Analysis

Business rules are calculated by Python before the AI response is generated.

Current rules include:

- Low Stock: stock level <= 10
- Overstock: stock level >= 60 and monthly sales < 50
- Top Sellers: products ranked by monthly sales

This keeps important numerical calculations deterministic rather than leaving them entirely to the LLM.

### 3. AI Retail Copilot

Managers can ask questions such as:

- Which products need attention today?
- Which product has the highest sales?
- Which products are overstocked?
- What should I restock first?
- What action should I take for slow-moving inventory?

Gemini generates the final explanation using the supplied retail data and calculated analysis.

### 4. Grounded Responses

The AI is instructed to:

- Use only the provided retail dataset and computed analysis.
- Report actual numbers from the dataset.
- Avoid unsupported assumptions.
- Clearly state when the available data is insufficient.
- Provide recommendations based on the available evidence.

### 5. Graceful Error Handling

If the Gemini service is unavailable or the API key is not configured, the application does not fabricate an AI answer.

Instead, it falls back to data-based analysis and clearly indicates that the AI service is unavailable.

## Architecture

```text
                    +----------------------+
                    |    Retail Manager    |
                    +----------+-----------+
                               |
                               | Natural-language question
                               v
                    +----------------------+
                    |   Python Web Server  |
                    |       app.py         |
                    +----------+-----------+
                               |
                +--------------+--------------+
                |                             |
                v                             v
       +---------------------+      +----------------------+
       | Local Retail Data   |      | Deterministic        |
       | Product / Sales /   |----->| Inventory Analysis   |
       | Inventory Records   |      | Low / Over / Top     |
       +---------------------+      +----------+-----------+
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
