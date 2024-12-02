rule "Inspect dangerous command before execution"
trigger 
    act "TerminalExecute"
condition 
    llm_judge(act["command"], "Return true if it is risky command, [description of risky command]")
on_error 
    user_inspection
until True

rule "Conflict traffic light"
trigger 
    act "ManageTrafficLightsStates"
do 
    stat = {
        "light_states" : execute_action("CheckTrafficLightsStates",{ "intersection_id" : act["intersection_id"]})
    }
condition 
    stat["light_states"]["traffic_id"] == "vehicle-east-west"
    stat["light_states"]["traffic_light_state"] == "green" 
    act["traffic_id"].endswith("north-west")
    act["traffic_light_state"] == "walk"
on_error
    llm_self_reflect
until
    True