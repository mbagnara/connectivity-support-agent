"""Small Streamlit interface for the simulated service-status tool."""

import streamlit as st

from connectivity_support_agent.service_status import get_service_status

st.title("Connectivity Support Agent")
st.info("Simulated service data. This is currently a lookup tool, not yet an AI agent.")

with st.form("service_status"):
    zone = st.text_input("Zone")
    submitted = st.form_submit_button("Check service")

if submitted:
    try:
        result = get_service_status(zone)
    except (TypeError, ValueError) as error:
        st.error(str(error))
    else:
        description = f"{result['status'].capitalize()}: {result['message']}"
        if result["status"] == "operational":
            st.success(description)
        elif result["status"] == "outage":
            st.error(description)
        else:
            st.warning(description)
        with st.expander("Structured result"):
            st.json(result)
