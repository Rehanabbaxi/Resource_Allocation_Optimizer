import os
from dotenv import load_dotenv
from groq import Groq
import random
import datetime
import pandas as pd
import streamlit as st
import plotly.express as px

# Load environment variables
load_dotenv()

# Initialize the client for Llama (Groq API)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Initialize session state variables
if "logs" not in st.session_state:
    st.session_state["logs"] = []
if "total_bandwidth" not in st.session_state:
    st.session_state["total_bandwidth"] = 100
if "allocated_bandwidth" not in st.session_state:
    st.session_state["allocated_bandwidth"] = {}

def simulate_request():
    """Simulates a new bandwidth request."""
    service_types = ["healthcare", "education", "emergency_services"]
    new_request = {
        "service_type": random.choice(service_types),
        "bandwidth_needed": random.randint(5, 20),
        "timestamp": datetime.datetime.now().strftime("%d/%m/%Y %I:%M %p")  
    }
    st.session_state["logs"].append(new_request)
    prioritize_requests_with_llm()

# def prioritize_requests_with_llm():
#     """Assign priorities using the Llama model via Groq API."""
#     for log in st.session_state["logs"]:
#         if "priority" not in log:  # Skip if already processed
#             # Prepare input text for Llama model
#             input_text = (
#                 f"Service Type: {log['service_type']}, Bandwidth Needed: {log['bandwidth_needed']} Mbps, "
#                 f"Timestamp: {log['timestamp']}"
#             )

#             # Call the Llama model
#             response = client.chat.completions.create(
#                 messages=[
#                     {"role": "user", "content": input_text}
#                 ],
#                 model="llama-3.3-70b-versatile",
#             )

#             # Extract priority score (adjust based on API response structure)
#             log["priority"] = float(response.choices[0].message.content.strip())



def prioritize_requests_with_llm():
    """Assign priorities using the Llama model via Groq API."""
    for log in st.session_state["logs"]:
        if "priority" not in log:  # Skip if already processed
            # Prepare input text for Llama model
            input_text = (
                f"Analyze the following service request and assign a numerical priority score (1 = highest priority, 10 = lowest priority):\n\n"
                f"Service Type: {log['service_type']}\n"
                f"Bandwidth Needed: {log['bandwidth_needed']} Mbps\n"
                f"Timestamp: {log['timestamp']}\n"
                f"Urgency Level: Based on its type, provide a priority score.\n\n"
                f"Reply with: Priority Score: [score]\n"
            )

            # Call the Llama model
            response = client.chat.completions.create(
                messages=[
                    {"role": "user", "content": input_text}
                ],
                model="llama-3.3-70b-versatile",
            )

            # Parse priority score from response
            response_text = response.choices[0].message.content.strip()

            # Look for a line starting with "Priority Score:"
            try:
                for line in response_text.splitlines():
                    if "Priority Score:" in line:
                        # Extract the numeric value
                        log["priority"] = float(line.split(":")[1].strip())
                        break
                else:
                    log["priority"] = 10.0  # Default low priority if no score is found
            except Exception as e:
                st.error(f"Failed to extract priority score: {e}")
                log["priority"] = 10.0  # Default low priority on failure




def allocate_bandwidth():
    """Allocates bandwidth based on priorities."""
    total_capacity = st.session_state["total_bandwidth"]
    allocated_bandwidth = {}

    # Sort logs by priority (lower priority value = higher priority)
    sorted_logs = sorted(st.session_state["logs"], key=lambda x: x.get("priority", float('inf')))
    
    for log in sorted_logs:
        service_type = log["service_type"]
        if log["bandwidth_needed"] <= total_capacity:
            # Allocate bandwidth
            allocated_bandwidth[service_type] = allocated_bandwidth.get(service_type, 0) + log["bandwidth_needed"]
            total_capacity -= log["bandwidth_needed"]
            log["fulfilled"] = True
        else:
            # Log unfulfilled requests
            log["fulfilled"] = False

    # Update session state
    st.session_state["allocated_bandwidth"] = allocated_bandwidth
    st.session_state["remaining_bandwidth"] = total_capacity

def display_dashboard():
    """Displays the Streamlit dashboard for testing the backend."""
    st.title("Resource Allocation Optimizer")

    st.header("Bandwidth Summary")
    st.metric("Total Bandwidth", f"{st.session_state['total_bandwidth']} Mbps")
    st.metric("Remaining Bandwidth", f"{st.session_state.get('remaining_bandwidth', 0)} Mbps")

    st.button("Simulate New Request", on_click=simulate_request)

    st.header("Service Logs")
    if st.session_state["logs"]:
        df_logs = pd.DataFrame(st.session_state["logs"])
        st.dataframe(df_logs)

        # Timeline chart for requests
        df_logs['timestamp'] = pd.to_datetime(df_logs['timestamp'], format="%d/%m/%Y %I:%M %p")
        fig_timeline = px.scatter(df_logs, x='timestamp', y='priority', color='service_type',
                                  title="Request Timeline",
                                  labels={"priority": "Priority Score"})
        st.plotly_chart(fig_timeline)
    else:
        st.write("No service requests logged yet.")

    st.header("Bandwidth Allocation")
    allocate_bandwidth()
    if st.session_state["allocated_bandwidth"]:
        df_allocation = pd.DataFrame.from_dict(st.session_state["allocated_bandwidth"], orient="index", columns=["Allocated Bandwidth"])
        df_allocation.reset_index(inplace=True)
        df_allocation.rename(columns={"index": "Service Type"}, inplace=True)
        st.dataframe(df_allocation)

        # Bar chart for bandwidth allocation
        fig_allocation = px.bar(df_allocation, x="Service Type", y="Allocated Bandwidth", color="Service Type",
                                title="Bandwidth Allocation")
        st.plotly_chart(fig_allocation)
    else:
        st.write("No bandwidth allocated yet.")

# Run the dashboard
display_dashboard()
