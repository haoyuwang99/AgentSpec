# scenest BNF grammar rules
```
<scenario> ::= CreateScenario”{”<map>; 
<ego vehicle>;
<npc vehicles>;
<pedestrians>;
<obstacles>;
[<Env>];
<traffic>;”}”

<map> ::= load(<map name>)
<map name> ::= “””<string>”””
<string> ::= <input character>|<string><input character>
//input character is the set of basic characters encoded by ASCII
<input character> ::= <letter> | <digit> | <symbol>
<letter> ::= a|…|z|A|…|Z
<digit> ::= 0|<non zero digit>
<non zero digit> ::= 1|…|9
<symbol> ::= " " | "~" | "`" | "!" | "@" | "#" | "$" | "%" | "^" | "&" | "*" | "(" | ")" | "_" | "-" | "+" | "=" | "\" | "|" | "]" | "}" | " [" | "{" | ";" | ":" | "’" | "”" | "/" | "?" | ">" | "<" | "," | "."


<ego vehicle> ::= AV“(”<parameter_list_ego>|*”)”
//<parameter_list_ego>|*: describe the parameters explicitly or all parameters are generated randomly
<parameter_list_ego> ::= <state>,<state>[,<vehicle type>]
	//first <state> is the initial state of the ego vehicle
	//second <state> is the target state of the ego vehicle
	//without <vehicle type>, use the default one.
<state> ::= “(”<position>[,[<heading>][,<speed>]]”)”
// the format can be: (position), (position, heading), (position, heading, speed), (position, ,speed)
<position> ::= [<coordinate frame>]<coordinate>
<coordinate frame> ::= IMU | ENU | WGS84
	// IMU: vehicle coordinate system, right-forward-up, origin is the position of the vehicle
// ENU: east-north-up, map origin is the origin of the coordinate
// WGS84: world geodetic system
// default coordinate frame: ENU
<coordinate> ::= “(”<real value>, <real value>”)” | <lane ID> “-““>” <real value>
// <lane ID> -> <real value>: the distance of the point to the start point of /////<lane ID> is <string> that consists real value
<real value> ::= <signal><non negative value>
<signal> ::= + | -
<non negative value> ::= <number>“.”<number>
<number>::= <digit>|<number><digit>
<lane ID> ::= "<string>"

<heading> ::= <real value> <unit> [related to <direction>] 
            |<real value> pi <unit> [related to <direction>] 
// default value: the direction to the lane where the position is on
<unit> ::= deg | rad
<direction> ::= <predefined direction>
<predefined direction> ::= <lane ID>-><real value>|EGO|<npc identifier>|<ego identifier>|<pedestrian identifier>
	// the reference system for lane <lane ID> and AV is shown as:


<speed> ::= <real value>

<vehicle type> ::= “(”<type>[,[<color>][,<material>]]”)” 
//currently, we do not consider material
<type> ::= <specific type>|<general type>
<specific type> ::= “””<string>”””
//model of the vehicle
<general type> ::= car|bus|Van|truck|bicycle|motorbicycle|tricycle
<color> ::= <color list>|<rgb color>
<color list> ::= red|green|blue|black|white
<rgb color> ::= “(“<rgb_value>,<rgb_value>,<rgb_value>“)”
<rgb_value> ::= <digit>|<non zero digit><digit>|1<digit><digit>|2<digit_2><digit>|25<digit_3>
<digit_2> ::= 0|…|4
<digit_3> ::= 0|…|5


<npc vhielces> ::= ”{”<multiple npc vehicles>”}”
<multiple npc vehicles> = <npc vehicle>|<multiple npc vehicles>,<npc vehicle>
<npc vehicle> ::= Vehicle”(”<parameter_list_npc>|*”)”
<parameter_list_npc> ::= <state> [,[<vehicle motion>] [,[<state>] [,<vehicle type>]]] 
//first <state> is the initial state of a vehicle
//second <state> is the target state of a vehicle
//default motion: uniform form motion along paths
<vehicle motion> ::= <uniform motion>|<waypoint motion>
<uniform motion> ::= <uniform index>”(”< state>”)”
	// move with the given speed in <state>
<uniform index> ::= uniform|Uniform|U|u
<waypoint motion> ::= <waypoint index>”(”<state_list>”)”
<waypoint index> ::= Waypoint|W|WP|waypoint|w|wp
<state_list>::='('<multi states>')'
<multi states> ::= <state>|<multi states>,<state>


<pedestrians> ::= ”{”[<multiple pedestrians>]”}”
<multiple pedestrians> = <pedestrian>|<multiple pedestrians>,<pedestrian>

<pedestrian> ::= Pedestrian”(”<parameter_list_ped>|*”)”
<parameter_list_ped> ::= <state>[,[<pedestrian motion>][,[< state>][,<pedestrian type>]]] 
//default motion: uniform motion along the crosswalk with the same direction of the nearest lane parallel with the crosswalk.
<pedestrian motion> ::= <uniform motion>|<waypoint motion>

<pedestrian type> ::= “(”<height>,<color>”)” 
//color means the color of cloth
<height> ::= <real value>


<obstacles> ::= “{“[<multiple obstacles>]”}”
<multiple obstacles> ::= <obstacle>|<multiple obstacles>,<obstacle>
<obstacle> ::= Obstacle”(”<parameter_list_obs>|*”)”
<parameter_list_obs> ::= <position>[,<shape>]
<shape> ::= <sphere> | <box> | <cone> | <cylinder>
<sphere> ::=”(“sphere, <non negative value>”)”
<box> ::= “(“box, <non negative value>, <non negative value>, <non negative value>”)”
<cone> ::= “(“cone, <non negative value>, <non negative value>, <non negative value>”)”
<cylinder> ::= “(“cylinder, <non negative value>, <non negative value>, <non negative value>”)”


<Env> ::= Environment“(“<parameter_list_env>|*”)”
<parameter_list_env> ::= <time>,<weather>
<time> ::= <hour>:<minute>
<hour> ::= <digit>|1<digit>|2<digit3>
<digit3> ::= 0|…|3
<minute> ::= <digit5><digit>
<digit5> ::= 0|…|5

<weather> ::= “{”<weather statements>”}”
<weather statements> ::= <weather statement>|<weather statements>,<weather statement>
<weather statement> ::= “‘”<kind>:“’” <weather continuous index>|<weather discrete level>;
<kind> ::= sunny|rain|snow|fog|wetness 
//this should be set based on simulator capability
<weather continuous index> ::= <proper fraction>|1
<proper fraction> ::= 0.<number>
<weather discrete level> ::= light|middle|heavy


<traffic> ::= “{”[<traffic statement>]”}”

<traffic statement> ::= <intersection traffic>, <lane traffic>
<intersection traffic> ::= <meta intersection traffic>|< intersection traffic>,<meta intersection traffic> 
<meta intersection traffic> ::= Intersection“(”<intersection ID>, <traffic light>, <stop sign>, <crosswalk> “)”
<intersection ID> ::= <signal><number>
<traffic light> ::= 0|1
<stop sign> ::= 0|1
<crosswalk> ::= 0|1
<lane traffic>::= <speed limitation>|<lane traffic>, <speed limitation>
<speed limitation> ::= SpeedLimit“(”<lane ID>, <speed range>”)”
<speed range> ::= “(”<non negative value>, <non negative value>”)”



// this it the main entry of this grammar.
<assignments>::=<assignment>|<assignments>','<assignment>
<assignment statement> ::= <identifier> = <assignment expression>';'

<identifier> ::= <first character>|<variable name>,<character>
<character>::=<first character>|<digit>
<first character>::=<letter>|“_”

//declare <trace>
<trace assignment> ::= Trace <trace> = EXE(<scenario>)
<trace> ::= <identifier>
	// EXE(<scenario>） will perform the execution of autoware and generate the required trace
// the parser needs to check whether <trace> is consistent with the definition <trace class>

//perception related assertions
<detection assertion> ::= <trace> |= G <detection statement>
<detection statement> ::= <single detection>|<detection statement>&<single detection>
<single detection> ::= <agent detection>|<traffic detection>

<agent detection> ::= <agent visible statement> & <agent error statement> 
<agent visible statement> ::= <agent ground distance> <= <sensing range>
<agent ground distance> ::= dis“(”<ego-state>, <agent ground truth>“)”	
   //dis “(”<agent state>, <agent state>“)” =d(position in <agent state>, position in <agent state>)
<ego-state> ::= <trace >“[ego]”
<agent ground truth> ::= <trace >“[truth]” “[<agent identifier>]”
<agent identifier> ::= <npc identifier>|<pedestrian identifier>|<obstacle identifier>
<sensing range> ::= <non negative value>

<agent error statement> ::= <agent error> <= <error threshold>
<agent error> ::= diff “(”<agent state>, <agent ground truth>“)”
// diff “(”<agent state>, <agent ground truth>“)”=  
w1*error(position) + w2* error(velocity) + w3* error(size)
<agent state> ::= <trace >“[perception]”“[<agent identifier>]”

<traffic detection> ::= <trace > [perception]“[traffic]”== <trace> “[truth]”“[traffic]”

// safety assertions
<safety assertion> ::= <trace> |= G <safety statement>
<safety statement> ::= <single safety statement>|<safety statement> & < single safety statement>
<single safety statement> ::= <agent detection> & <agent safety statement>
< agent safety statement> ::= dis“(”<ego-state>, <agent state>“)” >= <safety radius>
<safety radius> ::= <non negative value>

// intersection statement
<intersection assertion> ::= <trace> |= G <red light statement>
<red light statement> ::= “(”<traffic detection> & <red light>“)” -> “(”~<ego speed> U “(”<traffic detection>&<green light> “)”“)”
<red light> ::= <trace >“[traffic]”==red
<ego speed> ::= norm“(”<ego velocity>“)”
	//the 2-norm of <ego velocity>
<green light> ::= <trace >“[traffic]” == green

//lane statement
<speed constraint assertion> ::= <trace> |= G <speed statement>
<speed statement> ::= “(”<traffic detection> & <speed limitation checking> & <speed violation>“)” -> F “[”0, <time duration> “]”~<speed violation>
<speed limitation checking > ::= <trace>“[traffic]”==<speed range>
<speed violation> ::= <speed> < <trace > “[traffic]”“[0]” | 
<speed> > <trace > “[traffic]”“[1]”
<time duration> ::= <non negative value>
```
