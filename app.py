"""Independent demonstrations of simulated service status and guide retrieval."""

import streamlit as st

from connectivity_support_agent.service_status import get_service_status
from connectivity_support_agent.troubleshooting import get_troubleshooting_guide

st.title("Connectivity Support Agent")
st.info(
    "Simulated service data and demonstration guides. These are independent lookup "
    "tools, not yet an AI agent. Model integration is not implemented."
)

with st.container(key="service_section"):
    st.header("Service status")
    with st.form("service_status"):
        zone = st.text_input("Zone", key="service_zone")
        submitted = st.form_submit_button("Check service", key="service_submit")

    with st.container(key="service_result"):
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

with st.container(key="guide_section"):
    st.header("Troubleshooting guides")
    symptom_ids = {
        "Cannot connect to Wi-Fi": "wifi_unavailable",
        "Connected without internet access": "connected_no_internet",
        "Slow connection": "slow_connection",
        "Other symptom": "other",
    }
    with st.form("troubleshooting_guides"):
        selection = st.selectbox(
            "Symptom", ["Select a symptom", *symptom_ids], key="guide_symptom"
        )
        guide_submitted = st.form_submit_button(
            "Get troubleshooting guide", key="guide_submit"
        )

    with st.container(key="guide_result"):
        if guide_submitted:
            if selection == "Select a symptom":
                st.error("Select a symptom.")
            else:
                guide = get_troubleshooting_guide(symptom_ids[selection])
                if guide["status"] == "found":
                    st.subheader(guide["title"])
                    st.write(guide["message"])
                    st.markdown(
                        "\n".join(
                            f"{index}. {step['instruction']}"
                            for index, step in enumerate(guide["steps"], start=1)
                        )
                    )
                else:
                    st.warning(guide["message"])
                with st.expander("Guide structured result"):
                    st.json(guide)
