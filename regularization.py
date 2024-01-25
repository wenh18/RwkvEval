import re
def extract_id_act_text(v):
    llm_input = ''
    try:
        llm_id, llm_action, llm_input = re.findall(
            "id=(N/A|-?\d+)(?:.|\\n)*(?:-|,)\s?action=(N/A|\w+)(?:.|\\n)*(?:-|,)\s?input text=\"?'?(N/A|\w+)\"?'?",
            v,
        )[0]
        if llm_id == "N/A":
            llm_id = -1
        else:
            llm_id = int(llm_id)
        if "tapon" in llm_action.lower():
            llm_action = "tap"
        elif "none" in llm_action.lower():
            llm_action = "N/A"
        elif "click" in llm_action.lower():
            llm_action = "tap"
        elif "input" in llm_action.lower():
            llm_action = "input"
        assert llm_action in ["tap", "input", "N/A"]
    except:
        try:
            llm_id, llm_action = re.findall(
                "id=(N/A|-?\d+)(?:.|\\n)*(?:-|,)\s?action=(N/A|\w+)", v.lower(), flags=re.S
            )[0]
            llm_id = int(llm_id)
            if (
                "tapon" in llm_action.lower()
                or "check" in llm_action.lower()
                or "uncheck" in llm_action.lower()
            ):
                llm_action = "tap"
            elif "none" in llm_action.lower():
                llm_action = "N/A"
            assert llm_action in ["tap", "input", "N/A"]
        except:
            try:
                llm_id, llm_action, llm_input = re.findall(
                    "Action: (N/A|\w+)\\nid=(-?\d+)\\ninput text=(N/A|\w+)", v
                )[0]
                llm_id = int(llm_id)
            except:
                return -1, '', ''
                # llm_id, llm_action, llm_input = eval(
                #     input(
                #         v + "\nPlease input id, action, and text: "
                #     )
                # )
                # llm_id = int(llm_id)
                # llm_action = ["tap", "input", "N/A"][
                #     int(llm_action)
                # ]
                # try:
                #     if int(llm_input) == -1:
                #         llm_input = "N/A"
                # except:
                #     pass
            
    return llm_id, llm_action, llm_input
