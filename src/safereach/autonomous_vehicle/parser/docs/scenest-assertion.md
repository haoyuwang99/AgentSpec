# 语言描述
+ [断言（assertions）](#jump1)
+ [如何解析获取断言](#jump2)
+ [与断言有关的AST对象](#jump3)
  
*关于语言的场景文法，请参考[scenest scenario](./scenest-scenario.md)*

*关于语言的所有合法描述，请参考[scenest BNF文法](./scenest-grammar.md)*

*关于所有API的描述，请参考[scenest reference](./scenest-reference.md)*
## <span id="jump1">*scenest语言中的断言由以下几个部分组成*</span>

### 1 规划路径（Trace） 
 每一个场景都对应一条规划路径，例如，通过语法
 ```
 Trace trace=EXE(scenario);
 ```
 表示将场景*scenario*关联到名字为*trace*的路径上。
 规划路径代表着车辆一系列的状态
 <br />规划路径某一时刻的状态包括控制车辆的状态，NPC车辆的状态等等
 <br />我们可以获取这些信息，取如下形式
 ```
 <ego-state> =<trace-id>[ego]
 ```
 例如：
 ```
    ego-state=trace[ego];
 ```
表示将规划路径*trace*控制车辆信息赋值给变量*ego-state*
<br />把一辆*NPC*车辆，一个障碍物，或者一个行人对象都称为一个agent对象，
因此也可以获取它们的信息，例如：
```
agent-state=trace[perception][agent-name];
```
上面的代码中，解析器将会寻找名字为*agent-name*的对象，可以是一个NPC车辆，一个障碍物，或者一个行人
，并把规划路径*trace*的有关的**感知**信息信息赋值给变量*agent-state*.
也可以获取**实际**状态，例如：
```
agent-ground-truth=trace[truth][agent-name];
```
上面的代码中，解析器将会寻找名字为*agent-name*的对象，可以是一个NPC车辆，一个障碍物，或者一个行人
，并把规划路径*trace*有关的**实际**信息信息赋值给变量*agent-ground-truth*.

有关perception与truth的概念，请参考*autoware自动驾驶*

### 2 断言（Assertion）
断言表示期望一条规划路径上满足的某些性质。

断言的语义基于[MTL operators](https://github.com/mvcisback/py-metric-temporal-logic)
### 2.1 检测断言（Detection Assertion）
检测断言分为关于agent的检测断言（Agent Detection）与交通感知断言（Traffic Detection）
#### 2.1.1 关于agent的检测断言（Agent Detection）
分为agent感知断言与agent误差断言，通过以下方法规定一个感知断言
> ```dis(<ego-state>,<agent-ground-truth>)<= <sensing-range>```

其中，*ego-state*表示控制车辆的状态，*agent-ground-truth*表示某个*agent*实际状态，它们必须
在感知范围内，*sensing-range*是一个实数

*agent-ground-truth*是*agent*实际状态，语法在上面以给出
相比之前的*agent-state*，这里只需要把*perception*换成*truth*

agent误差断言表示，表示感知与实际的误差范围在允许范围之内，取如下形式：
```
diff(<agent-state,agent-ground-truth)<= <threshold>
```
其中，*agent-state*与*agent-ground-truth*上面已给出定义，这个断言表示的是感知到的agent状态和实际的agent状态误差小于等于*threshold*表示的值
#### 2.1.2 交通感知断言(Traffic Detection)
表示感知与实际的交通情况相同，取如下形式：
```
<trace-id>[perception][traffic]==<trace-id>[truth][traffic]
```
### 2.2 安全断言（Safety Assertion）
安全断言由关于agent的检测断言与安全距离断言组成，
表示安全的距离断言取如下形式：
```
dis(<ego-state>,<agent-state>)>= <safety-radius>
```
表示感知到的*ego*车辆与*agent*对象，距离必须满足给定的要求，*safety-radius*给出表示安全距离的实数
### 2.3 交通断言（Intersection Assertion）
如下形式：
```
(<traffic-detection>&<red-light>)->(~<ego-speed>U(<traffic-detection>&<green-light>))
<red-light> ::=<trace-id>[traffic]==red
<green-light> ::=<trace-id>[traffic]==green
<ego-speed> ::=norm(<ego-velocity)
<ego-velocity> ::=<coordinate>
```
其中，*traffic-detection*上面已给出，而*red-light*与*green-light*表示检测到红灯与绿灯状况。*ego-speed*表示*ego*车辆的速度，[*coordinate*](./scenest-scenario.md)在场景文法中已给出。

此断言表示，检测的交通状况断言，在遇到红灯的情况下，*ego-speed*表示的速度一定为0,直到
检测的交通状况为绿灯
### 2.4 速度约束断言（Speed Constraint Assertion）
取如下形式：
```
(<traffic-detection>&<speed-limitation-checking>&<speed-violation>)->F[0,<time-duration>]~<speed-violation> 
<speed-limitation-checking>::=<trace-id>[traffic]==<speed-range>
<speed-violation>::=<speed><trace-id>[traffic][0]
```
其中，[*speed-range*与*speed*](./scenest-scenario.md)在之前的场景文法中已给出

该断言表示，检测到的交通断言，如果存在速度检查（*speed-limitation-checking*）以及速度违反检测(*speed-violation*)的限制，则在时刻0到由实数*time-duration*给定的值时刻之内不能违反第二个速度违反断言
### 3. 断言附加到规划路径上
   四种断言（检测断言，安全断言，交通路口断言，速度约束断言）在描述之后，必须附加到给出的规划路径上，表示在这个规划路径上断言生效，通过下面的方式：
   ```
   <trace-id>|=G<detection-assertion> //<detection-assertion>表示检测断言，假设在此之前已给出
   <trace-id>|=G<safety-assertion> //<safety-assertion>表示安全断言，假设在此之前已给出
   <trace-id>|=G<intersection-assertion> //<intersection-assertion>表示交通路口断言，假设在此之前已给出
   <trace-id>|=G<speed-constraint-assertion> //<speed-constraint-assertion>表示速度约束断言，假设在此之前已给出
   ```
## <span id="jump2">*如何解析获取断言*</span>
下面是一个例子，包含了以上所有的断言内容：
```
Trace trace=EXE(scenario);// 由场景scenario给出一个执行路径trace
ego_vehicle_state= trace[ego];// 从场景中提取控制车辆信息
npc_vehicle1= trace[perception][npc1];//从场景提取名字为npc1的感知信息
npc_vehicle1_ground= trace[truth][npc1];//从场景提取名字为npc1的实际信息
npc_vehicle2= trace[perception][npc2];//从场景提取名字为npc2的感知信息
npc_vehicle2_ground = trace[truth][npc2];//从场景提取名字为npc2的实际信息
npc_vehicle3= trace[perception][npc3];//从场景提取名字为npc3的感知信息
npc_vehicle3_ground =  trace[truth][npc3];//从场景提取名字为npc3的实际信息
pedestrian_truth = trace[perception][pedestrian];//从场景提取名字为pedestrian的感知信息
pedestrian_ground = trace[truth][pedestrian];//从场景提取名字为pedestrian的实际信息

dis1 = dis(ego_vehicle_state, npc_vehicle1_ground);
error = diff(npc_vehicle1, npc_vehicle1_ground);
perception_detection = dis1<= 0.1 & error <= 0.1;//定义一个包含agent感知断言与agent误差断言的检测断言
trace |=G perception_detection ;// 断言附加到路径上
trace |=G dis1<= 0.1 & error <= 0.1 & dis(ego_vehicle_state, npc_vehicle1)>= 0.1 ; //定义一个包含agent感知断言，agent误差断言和安全距离断言的安全断言，并附加到路径上
intersection_assertion=(trace[perception][traffic]==trace[truth][traffic]
	&trace[traffic]==red)->(~norm((100,100))U(trace[perception][traffic]==trace[truth][traffic]
	&trace[traffic]==green));//定义一个交通断言
trace |=G intersection_assertion;// 断言附加到路径上
// speed constraint assertion
speed_constraint_assertion=(trace[perception][traffic]==trace[truth][traffic]
	&trace[traffic]==(100,200)&120<trace[traffic][0])
	->F[0,2]~120<trace[traffic][0];//定义一个速度约束断言
trace |=G speed_constraint_assertion;// 断言附加到路径上
```
解析后，打印如下：
```
-Trace:[name:trace][scenario:scenario]
-EgoState:ego_vehicle_state=trace[ego]
-AgentState:npc_vehicle1=trace[perception][npc1]
-AgentGroundTruth:npc_vehicle1_ground=trace[truth][npc1]
-AgentState:npc_vehicle2=trace[perception][npc2]
-AgentGroundTruth:npc_vehicle2_ground=trace[truth][npc2]
-AgentState:npc_vehicle3=trace[perception][npc3]
-AgentGroundTruth:npc_vehicle3_ground=trace[truth][npc3]
-AgentState:pedestrian_truth=trace[perception][pedestrian]
-AgentGroundTruth:pedestrian_ground=trace[truth][pedestrian]
-AgentGroundDistance:dis1=
  -dis(  npc_vehicle1_ground,  ego_vehicle_state)
-AgentError:error=
  -diff(  npc_vehicle1,  npc_vehicle1_ground)
-DetectionAssertion:perception_detection=
  -AgentVisibleDetectionAssertion:
    dis1
    <=0.1
  -AgentErrorDetectionAssertion:
    error
    <=0.1
-AssignAssertionToTrace:
  -trace:trace
  -assertion:perception_detection
-AssignAssertionToTrace:
  -trace:trace
  -SafetyAssertion:=
    -AgentVisibleDetectionAssertion:
      dis1
      <=0.1
    -AgentErrorDetectionAssertion:
      error
      <=0.1
    -AgentSafetyAssertion:
      dis(      ego_vehicle_state,      npc_vehicle1)>=0.1
-IntersectionAssertion:intersection_assertion=
  -TrafficDetectionAssertion:trace[perception][traffic]==trace[truth][traffic]
  &
  -RedLightState:trace[traffic]=red
  ->
  ~
  -EgoSpeed:norm((100.0, 100.0))
  U
  -TrafficDetectionAssertion:trace[perception][traffic]==trace[truth][traffic]
  &
  -GreenLightState:trace[traffic]=green
-AssignAssertionToTrace:
  -trace:trace
  -assertion:intersection_assertion
-SpeedConstraintAssertion:speed_constraint_assertion=
  -TrafficDetectionAssertion:trace[perception][traffic]==trace[truth][traffic]
  &
  -SpeedLimitationChecking:trace[traffic]==(100.0, 200.0)
  &
  -SpeedViolation:120.0<trace[traffic][0]
  ->F[0,2.0]
  ~
  -SpeedViolation:120.0<trace[traffic][0]
-AssignAssertionToTrace:
  -trace:trace
  -assertion:speed_constraint_assertion
```
## <span id="jump3">*与断言有关的AST对象*</span>
### Trace
表示一条规划路径，拥有一个场景对象，以及所有的关于此规划路径的断言对象
### EgoState
表示规划路径的控制车辆信息，例如，下面代码构造一个*EgoState*对象
```
ego_state=trace[ego];//ego是关键字
```
### AgentState
表示规划路径的*agent*的感知信息，例如，下面代码构造一个*AgentState*对象
```
agent_state=trace[perception][agent_name];// agent名字为agent_name
```
### AgentGroundTruth
表示规划路径的*agent*的实际信息，例如，下面代码构造一个*AgentGroundTruth*对象
```
agent_ground=trace[truth][agent_name];// agent名字为agent_name
```
### AgentGroundDistance
属于agent感知断言的前一部分
### AgentVisibleDetectionAssertion
*agent*感知断言，一个*agent*感知断言，拥有一个*AgentGroundDistance*与感知范围（是一个实数）
例如，通过下面代码构造一个*AgentVisibleDetectionAssertion*对象
```
dis1 = dis(ego_vehicle_state, npc_vehicle1_ground);//构造一个AgentGroundDistance对象
error = diff(npc_vehicle1, npc_vehicle1_ground);
perception_detection = dis1<= 0.1 & error <= 0.1;//下面代码会构造一个AgentVisibleDetectionAssertion对象，注意还会构造其它对象
```
### AgentError
属于*agent*误差断言的前一部分
### AgentErrorDetectionAssertion
*agent*误差断言，一个*agent*误差断言，拥有一个*AgentError*与误差阈值（是一个实数）
例如，通过下面代码构造一个*AgentErrorDetectionAssertion*对象
```
dis1 = dis(ego_vehicle_state, npc_vehicle1_ground);
error = diff(npc_vehicle1, npc_vehicle1_ground);//构造一个AgentError对象
perception_detection = dis1<= 0.1 & error <= 0.1;//下面代码会构造一个AgentErrorDetectionAssertion对象，注意还会构造其它对象
```
### AgentSafetyAssertion
表示安全距离断言，例如
``
 dis(ego_vehicle_state, npc_vehicle1)>= 0.1
``
就会构造一个*AgentSafetyAssertion*对象，表示控制车辆与感知到的*agent*对象必须大于或等于一个安全范围
### TrafficDetectionAssertion
表示交通感知断言，一般是如下形式``trace[perception][traffic]==trace[truth][traffic]``
### RedLightState
表示感知到了红灯，取如下形式``trace[traffic]==red``
### GreenLightState
表示感知到了绿灯，取如下形式``trace[traffic]==green``
### EgoSpeed
表示控制车辆速度对象
### IntersectionAssertion
表示交通断言，一个交通断言拥有两个*TrafficDetectionAssertion*对象，一个*RedLightState*和一个*GreenLightState*对象，和一个*EgoSpeed*对象
### SpeedLimitationChecking
表示速度检查（限速）对象
### SpeedViolation
表示速度违反对象
### SpeedConstraintAssertion
表示速度约束对象，一个速度约束对象拥有两个*SpeedViolation*对象，一个*TrafficDetectionAssertion*对象，一个*SpeedLimitationChecking*和一个*SpeedViolation*对象，和一个时刻（表示从0时刻到该时刻的间隔）