The Resource Allocation Optimizer is a prototype system designed to dynamically manage and prioritize bandwidth allocation in public sector networks, focusing on underserved regions. By leveraging the power of AI through Groq's Llama model and an interactive dashboard, this project demonstrates an efficient, real-time solution for optimizing resource distribution in critical sectors like healthcare, education, and emergency services.

Key Features

Simulated Network Requests: Generates and manages service requests for bandwidth from sectors like healthcare, education, and emergency services.

AI-Driven Priority Assignment: Uses the Groq Llama model to analyze service requests and assign numerical priority scores based on urgency and bandwidth needs.

Dynamic Bandwidth Allocation: Allocates available bandwidth in real-time based on the AI-assigned priorities to ensure critical services are prioritized.

Interactive Dashboard: Built with Streamlit, the dashboard visualizes service requests, priority assignments, and bandwidth allocations using real-time data and dynamic charts.

Scalable Design: Provides a modular framework that can be adapted for real-world network optimization.

Technologies Used

Programming Language: Python

AI Integration: Groq Llama API

Frontend Framework: Streamlit

Visualization: Plotly for interactive charts

Data Management: Pandas for handling and processing data

Environment Management: dotenv for secure environment variable handling

Use Case

The project is tailored for public sector networks where resources are scarce and efficient distribution is critical. By simulating bandwidth requests and optimizing allocation with AI, this system can:

Ensure uninterrupted connectivity for emergency services.

Prioritize educational services during peak hours.

Dynamically adjust allocations to address real-time demands.

How It Works

Simulated Requests: The system generates service requests with details like bandwidth needed, service type, and urgency.

AI Analysis: The Llama model processes each request and assigns a priority score based on its importance.

Allocation: Bandwidth is allocated based on priorities, ensuring critical services receive sufficient resources.

Visualization: The dashboard provides real-time updates on requests, priorities, and allocations, enabling users to monitor and interact with the system.

Future Enhancements

Integration with real-world network data for live testing.

Advanced AI models for more nuanced priority assessment.

Improved UI for enhanced user experience.

Support for decentralized networks and blockchain-based transparency.
