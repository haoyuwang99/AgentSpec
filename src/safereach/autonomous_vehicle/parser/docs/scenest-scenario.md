## 语言描述
+ [scenest场景介绍](#jump1)
+ [如何解析获取场景](#jump2)
+ [与场景有关的AST对象](#jump3)
  
*关于语言的断言文法，请参考[scenest assertion](./scenest-assertion.md)*

*关于语言的所有合法描述，请参考[scenest BNF文法](./scenest-grammar.md)*

*关于所有API的描述，请参考[scenest reference](./scenest-reference.md)*
### <span id="jump1">*scenest语言中的场景由以下几个部分组成:*</span>

### 1. 场景（scenario）
一个场景包含7个组成部分:
``地图（map）``，``控制车辆（ego vehicle）``，``NPC车辆（npc vehicles）[可选]``，``行人（pedestrians)[可选]``，``障碍物（obstacles）[可选]``，``环境（environment）[可选]``，``交通（traffic）[可选]``,<br />通过``CreateScenario``来创建一个场景：
```
/*以下通过CreateScenario创造一个scenario的场景，参数分别为
	map：地图
	ego_vehicle:控制车辆
	npc_vehicles:NPC车辆
	pedestrians：行人
	obstacles：障碍物
	env：环境
	traffic：交通
	以上所有的对象将在接下来一一介绍
*/
/*
	允许默认的参数，通过‘{}’指定。例如
	scenario=CreateScenario{
		load(map);
		ego_vehicle;
		{};//默认npc_vehicles
		{}; //默认pedestrians
		{};//默认obstacles
		{};//默认environment
		{};//默认traffic
	};
*/
scenario=CreateScenario{
	load(map);
	ego_vehicle;
	npc_vehicles;
	pedestrians;
	obstacles;
	env;
	traffic;
};
```
### 2. 地图对象(map)
只需指定加载的地图的名字：
> ``map="San Francisco"; //这将加载一个地图，地图为旧金山，地图的名字为map``

### 3. 控制车辆（ego vehicle）
控制车辆由关键字‘AV’指定，控制车辆由三个部分组成分别是``初始状态（state）``，``目标状态（state）``，``车辆类型（vehicle type）[可选]``<br />

```
/* 以下指定了一个名字为ego_vehicle的控制车辆,初始状态由ego_init_state指定，
	目标状态由ego_target_state指定，类型信息由vehicle_type指定*/


ego_vehicle=AV(ego_init_state,ego_target_state,vehicle_type);
```
#### 3.1 状态（state）
状态表示一辆车（控制车辆或者NPC车辆）或者行人的状态信息，由三个部分组成：``位置（position）``，``朝向（heading）[可选]``，``速度（speed）[可选]``<br />
位置有两种表示方法：坐标与相对于车道（lane）的表示方法，位置还可以设置``坐标参考系（coordinate frame）``,共有三种：``IMU,ENU[默认],WSG84``<br />
坐标可以有二维坐标，也可以设置第三维坐标（**注意:为了可以解析，第三个维度必须加上正负号**）
例如：
```
pos=(1,2,+1);//表示坐标为（1,2,+1）的一点
pos=(1,2,-10);//表示坐标为（1,2,-10）的一点
```
朝向:朝向可以设置相对于某个*NPC*车辆，某个形容，可以相对于某个具体的车道，也可以相对于控制车辆
```
ego_init_position=(2,3); //表示坐标为（2,3）的一点
ego_init_position2=".5"->6; //表示相对于车道5距离为6的一点
heading=34 deg related to EGO;//表示相对于控制车辆34度的方向
speed=35; //表示34的速度
ego_init_state=(ego_init_position,heading,speed);//表示一个初始状态，由初始位置，初始朝向，初始速度组成
ego_target_position=(2,4);
ego_target_state=(ego_target_position);//表示目标状态

```
#### 3.2 车辆类型（vehicle type）<br />
车辆类型由三个部分组成：``具体类型（type），颜色（color）[可选]，材料（material）[目前不支持，但保留，可选]``
具体类型：具体类型可以是``car,bus,truck``等等，也可以是字符串自定义的类型<br />
颜色：支持RGB表达或者预制的颜色，例如``red，blue``等等
```
type=bus;//表示一辆大巴
color=(255,0,0);
vehicle_type=(type,color);//表示控制车辆类型，由具体类型和颜色组成
```
### 4. NPC车辆（NPC vehicles）<br />
你可以设置多个``NPC车辆（NPC vehicle）``共同组成多个NPC车辆列表，
单个NPC车辆由关键字``Vehicle``指定，由以下几个部分组成：``初始状态（state），运动路径（vehicle motion），目标状态（state），车辆类型（vehicle type）``<br />
#### 4.1 运动路径（vehicle motion）<br />
运动路径可以指定为``uniform motion``与``waypoint motion``，前者指定一个状态，后者指定一系列的状态来控制NPC车辆的运动轨迹,
```
	statelist=(state1,state2，state3); //表示一系列的状态，由state1,state2,state3组成
	uniform=U(state); //表示以给定的状态匀速运动
	waypoint=WP(statelist);//表示一系列的状态运动
	npc1=Vehicle(state1,uniform,state2,vehicle_type);//表示一辆NPC车辆
	npc_vehicles={npc1,npc2};//表示多辆NPC车辆
```
### 5. 行人（pedestrians）
你可以设置多个``行人（pedestrian）``，每一个行人由``Pedestrian``关键字指定，并由``初始状态（state），行人路径（pedestrian motion），目标状态（state），行人类型（pedestrian type）``组成
#### 5.1 行人路径
行人路径与``vehicle motion``一样设置
#### 5.2 行人类型（pedestrian type）
行人类型由``高度（height）``与``颜色（color）``组成
```
height=1.8;
color=white;
pedestrian_type=(height,color);//表示一个身高1.8,颜色为白色的行人类型
pedestrian1=Pedestrian(state1,uniform,state2,pedestrian_type);//表示一个行人
pedestrians={pedestrian1,pedestrian2};//表示多个行人
```
### 6. 障碍物(obstacles)
你可以设置多个``障碍物（obstacle）``，每个障碍物由关键字``Obstacle``指定，并由``位置（position），形状（shape）``组成
#### 6.1 形状（shape）
形状只有预设的形状：``球（sphere），立方体（box），圆锥（cone），圆柱（cylinder）``
```
position=(1,2);
box_shape=(box,1,1,1);//表示一个立方体障碍物，长宽高为1,1,1
obstacle1=Obstacle(position,box_shape);//构造一个障碍物
obstacles={obstacle1,obstacle2};//表示多个障碍物
```
### 7. 环境（environment）
环境由关键字``Environment``指定，并由``时间（time），天气（weathers）``组成
#### 7.1 天气（weathers）
你可以制定多个``天气（weather）``条件，格式如下
``kind:value``或者``kind:level``
其中``kind``可以是``sunny,rain,snow,fog,wetness``,``value``介于0-1之间用来描述程度，或者使用``light，middle，heavy``来指定等级（level）
```
time=12:00;
weather1=rain:0.1;
weather2=fogness:middle;
weathers={weather1,weather2};//指定多个天气条件
env=Environment(time,weathers);//指定环境
```
### 8. 交通（traffic）<br />
交通由车道``交互交通情况（intersection traffic）``与``车道限速（speed limitation）``组成
车道交互交通情况可以指定交汇路口的``交通灯（traffic light），停止信号（stop sign），人行横道（crosswalk）``<br />
格式如下：``Intersection(intersection id,traffic light,stop sign,crosswalk)``<br />
车道（lane）的限速情况：``SpeedLimit(lane id,(speed-min,speed-max)``
```
intersection1=Intersection(3,0,0,0);
intersection2=Intersection(6,1,1,0);
speedlimit1=(".1",(80,120));//表示车道".1"的限速情况
traffic={intersection1,intersection2,speedlimt1};
```
### 其它
注释：允许行内与块内注释，以``//``和``/**/``方式声明
## 一个完整的实例
 下面是一个完整的实例：
 ```
	map = "San Francisco";//地图名字
	ego_init_position = (4.5, 214);
	ego_target_position = (4.5, -200);
	ego_init_state = (ego_init_position);
	ego_target_state = (ego_target_position);
	car_model = "Lincoln MKZ 2017";//车辆具体类型
	car_color = (255, 0, 0);
	vehicle_type = (car_model, car_color);//使用car_model,car_color来标识车辆类型（vehicle type）
	ego_vehicle = AV(ego_init_state, ego_target_state, vehicle_type);//创建一个ego vehicle
	npc_init_state = (".1"->0.0, ,1.5) ;//创造一个状态，该状态有一个位置为".1"->0.0，默认朝向，，速度为1.5
	motion = U(npc_init_state);//使用npc_init_state来创造一个uniform motion
	npc1 = Vehicle(npc_init_state, motion);//使用motion和npc_init_state来创造一个npc1
	npc_init_state2 = ("2"->0.0, ,1.0);//创造npc_init_state2状态
	npc_state = (("2"->0.0, , 1.0), ("2"->50.0, ,1.0));//创造状态列表（state list），该列表有两个匿名状态组成
	npc2 =Vehicle(npc_init_state2, Waypoint(npc_state), ("4"->100, ,0.0), vehicle_type);//创造第二辆npc2
	heading = 45 deg related to EGO;
	npc_init_state3 = ((9.5, 114), heading, 0.0);
	npc3 = Vehicle(npc_init_state3);//创造第三辆npc3

	npc = {npc1, npc2, npc3};//创造npc车辆，共有三辆车

	pedestrian_type = (1.65, black);
	pedestrian = Pedestrian(((19,13), ,0.5), , ((0,13), ,0), pedestrian_type);//创造一个行人
	pedestrians={pedestrian};//创造行人列表，只有一个行人
	time = 10:00;
	weather = {rain: 0.1};
	env = Environment(time, weather);//添加天气信息

	speed_range = (0,20);
	speed_limit = SpeedLimit(".5", speed_range);
	i1 = Intersection(1, 1, 0, 1);
	traffic = {i1,speed_limit};//创造traffic约束

	scenario = CreateScenario{load(map);
						ego_vehicle;
						npc;
						pedestrians;
						{};//默认的障碍物（obstacles）
						env;
						traffic;
	};//使用map,ego_vehicle,npc,pedestrians,env,traffic来创建一个场景，名字为scenario
 ```
## <span id="jump2">如何解析代码(**只是一个初步的功能**)</span>

```python
from parser.ast import Parse
from parser.ast import AST,ASTDumper
ast:AST=Parse("input.txt")  #调用Parse函数解析输入，并返回AST（包含所有的解析后的信息）对象
```
### ``与场景有关的AST类``
当已经完成了对于输入的解析之后，所有的有用的信息以及一些对于信息操作的相关函数都储存在``AST``对象中，
例如：你可以通过成员函数``get_ast_tree()``来返回AST对象中包含的数据结构，所有的数据结构都封装为一个列表（list）通过此函数返回，例如
```python
from parser.ast import Parse
from parser.ast import AST,ASTDumper
ast:AST=Parse("input.txt")
nodes=ast.get_ast_tree()#此nodes为一个列表，是对于输入文件的代码的解析后的结果
```
如果你想看到解析后的``AST``长什么样子，通过``ASTDumper``对象将他们打印出来，<u>目前更加友好的打印方式还未开发</u>
```python
	dumper=ASTDumper(ast)
	dumper.dump()
```
例如``input.txt``文件含有如下内容
```
map = "San Francisco";
ego_init_position = (4.5, 214); 
ego_target_position = (4.5, -200);
ego_init_state = (ego_init_position);
ego_target_state = (ego_target_position);

car_model = "Lincoln MKZ 2017";
car_color = (255, 0, 0);
vehicle_type = (car_model, car_color);
ego_vehicle = AV(ego_init_state, ego_target_state, vehicle_type);

scenario1 = CreateScenario{load(map);
			        ego_vehicle;
			        {}; // no other vehicles;
			        {}; // no pedestrians;
			        {}; // no obstacles;
			        {}; // default environment
			        {}; // no traffic constraints
};
```
那么打印之后的输出如下
```
-Map:[name:map][map:"San Francisco"]
-Position:[name:ego_init_position][kind:ENU]
  -(4.5,214)
-Position:[name:ego_target_position][kind:ENU]
  -(4.5,-200)
-State:[name:ego_init_state]
  -Position:ego_init_position
  -Heading:[default]
  -Speed:[default]
-State:[name:ego_target_state]
  -Position:ego_target_position
  -Heading:[default]
  -Speed:[default]
-Type:[name:car_model]
  -"Lincoln MKZ 2017"
-Color:[name:car_color]
  -(255, 0, 0)
-VehicleType:[name:vehicle_type]
  -Type:car_model
  -Color:car_color
-EgoVehicle:[name:ego_vehicle]
  -State:ego_init_state
  -State:ego_target_state
  -VehicleType:vehicle_type
-Scenario:[name:scenario1]
  -Map:map
  -EgoVehicle:ego_vehicle
  -NPCVehicles:[default]
  -Pedestrians:[default]
  -Obstacles:[default]
  -Environment:[default]
  -Traffic:[default]
```
### <span id="jump3">AST对象</span>
从上图可以看出，有非常多的对象，下面简单描述所有的对象
#### Map
对应与一个地图，例如声明一个地图，会生成一个``Map``对象
```
map_name="Beijing";
```
#### Lane
Lane表示一个车道，车道由一个字符串组成，字符串如下形式“road_id.lane_id”,其中road_id与lane_id都为整数，且road_id可选
例如：
```
lane="1.0";// 表示道路标识为1,车道表示为0的Lane对象
lane2=".3";// 表示车道表示为3的Lane对象
```
可以通过``get_map_name()``来获得地图对象的内容
#### Position
对应着一个二维平面上的点，``Position``还有一个参数是``参考系（coordinate frame）``，共有三种方式``IMU,ENU,WGS83``，不过不加指定的话，默认为``ENU``，位置有两种设置方式，第一种是传统的点坐标的方式，还可以设定以某一车道为参考，某一距离的点，例如：
```
position1=(1,2);//设置一个坐标为（1,2）的点，默认的coordinate frame为ENU
position2=IMU ".1"->1;//设置一车道".1"为参考，距离为1的点，coordinate frame为IMU
```
可以通过``get_frame()``来获取对应的参考系，返回的是一个枚举值类型``CoordinateFrame``，如果返回的是空值（``None``）的话，则是默认的参考系``ENU``
#### Heading
对应着一个朝向，允许弧度（rad）和角度（deg）制，可以指明想对于某一点的偏转角度或者想对于某个车道或者想对于车辆自身，也允许指定关键字*pi*，来表示180度。

例如：

```
heading0=50 deg;//定义了一个朝向，相对于的方向默认
heading1=50 deg related to ".4"->0.0;//定义了一个朝向，想对于点".4"->0.0偏转50度
heading2=50 deg related to EGO;//定义了一个朝向，想对于控制车辆偏转50度
heading3=pi rad related to EGO;//定义了一个朝向，想对于控制车辆偏转180度
```
它们的打印结果如下：
```
-Heading:[name:heading0][angle:50 deg]
  -direction:[default]
-Heading:[name:heading1][angle:50 deg]
  -Lane:[anonymous][laneID:.4]
  -0.0
-Heading:[name:heading2][angle:50 deg]
  -direction:EGO
-Heading:[name:heading3][angle:pi rad]
  -direction:EGO
```
通过``get_raw_heading_angle（）``来获得角度，通过``get_unit()``来获得角度的单位，
通过``get_direction()``来获得方向，会返回一个``Predefined Direction``对象，当然也会返回一个空值，所以需要用``has_direction()``来判断是否取默认的方向
#### Speed
对应着速度，可以通过``get_speed_value()``来获取速度值
```
speed=12;//定义了速度为12,名字为speed
```
#### State
一个状态类包括``Position``，``Heading``[可选]，``Speed``[可选]成员，注意可选的成员在使用时需要判断是否不为空，通过``has_heading()``和``has_speed（）``判断
#### VehiceType
对应着车辆类型，车辆类型拥有一个``Type``，``Color``[可选]，``Material``[目前无意义，可选]成员，分别是
``Type``可以是``SpecificType``（自定义的车辆类型）或者``GeneralType``（限定了车辆的具体种类），
``Color``可以是``RGBColor``（以RGB值给出的颜色），或者``ColorList``（预制的颜色）
```
specific_type="Lincoln MKZ 2017";//自定义车辆，为Lincoln MKZ 2017
general_type=bus;//定义了车辆为大巴
rgb_color=(255,0,0);
color_list=white;
```
下面是允许的合法值
|GeneralType|ColorList|
|---|---|
|car|red|
|bus|green|
|Van|blue|
|truck|black|
|bicycle|white|
|motorbicycle||
|tricycle||
通过``get_type()``，``get_color()``成员函数来获得对应的``Type``和``Color``
#### EgoVehicle
对应着控制车辆信息，一个``EgoVehicle``对象拥有``State``，``State``，``VehicleType``[可选]，
前一个``State``表示初始状态，后一个``State``表示目标状态
通过``get_first_state(),get_second_state(),get_vehicle_type()``来获得相应的对象

#### StateList
包含多个``State``对象，通过``get_states()``成员函数来获取一个list列表，该列表包含多个``State``对象
```
state_list=(state1,state2,state3);//假设state1,state2,state3已经定义为State对象，那么这里state_list表明生成一个StateList对象
```
#### UniformMotion，WaypointMotion
对应着NPC车辆或者行人的规划路径，一个``UniformMotion``拥有一个``State``，而一个``WaypointMotion``拥有一个``StateList``对象
#### NPCVehicle
对应着一辆NPC车辆的信息，一个``NPCVehicle``拥有``State``，``VehicleMotion``[可选]，``State``[可选]，``VehicleType``[可选]对象，其中``VehicleMotion``可以通过``get_motion()``来获得一个``UniformMotion``或者``WaypointMotion``对象

#### NPCVehicles
该对象包含多个``NPCVehicle``对象
#### PedestrianType
对应着行人的类型，拥有一个``Height``，``Color``对象，表示身高与行人颜色
```
height=1.8;
color=white;
pedestrian_type=(height,color);//生成一个行人
```
#### Pedestrian
对应者一个行人，一个``Pedestrian``拥有``State``，``PedestrianMotion``[可选]，``State``[可选]，``PedestrianType``[可选]对象，其中``PedestrianMotion``可以通过``get_motion()``来获得一个``UniformMotion``或者``WaypointMotion``对象

#### Pedestrians
该对象包含多个``Pedestrian``对象
#### Shape
表示一个障碍物形状，内置的形状有``box，cone,cylinder,sphere``，它们的合法代码如下：
```
box=(box,1,2,3);//表示一个长为1,宽为2,高为3的立方体
cone=(cone,1,1);//表示一个半径为1,高为1的圆锥
cylinder=(cylinder,1,1);//表示一个半径为1,高为1的圆柱
sphere=(sphere,1);//表示一个半径为1的球
```
#### Obstacle
表示一个障碍物，一个障碍物拥有一个``Position``，和``Shape``[可选]对象

#### Obstacles
该对象包含多个``Obstacle``对象

#### Weather
用来描述某一项天气，合法的描述如下，可以使用值来描述，生成一个WeatherContinuousIndex对象，
或者使用程度来描述，生成一个``WeatherDiscreteLevel``对象
|Weather|WeatherContinuousIndex|WeatherDiscreteLevel|
|---|---|--|
|sunny|0.0-1.0之间|light,middle或者heavy|
|rain|0.0-1.0之间|light,middle或者heavy|
|snow|0.0-1.0之间|light,middle或者heavy|
|foggy|0.0-1.0之间|light,middle或者heavy|
|wetness|0.0-1.0之间|light,middle或者heavy|
#### Weathers
要描述多个``Weather``，使用``Weathers``对象，例如：
```
weather1=foggy:0.7;
weather2=sunny:0.1;
weathers={weather1,weather2};//生成Weathers对象，包含多个Weather对象
```
#### Environment
对应着环境，环境对象拥有一个``Weathers``（天气情况），``Time``（时间）


#### IntersectionTraffic
对应着``intersection``的交通情况，可以通过``get_id()``来获取对应的``intersection``的``id``
#### SpeedLimitation
对应着车道限速情况，拥有一个``SpeedRange``对象，表示限速范围，拥有一个``Lane``，表示对应的车道
，例如：
```
speedrange=(80,120);//表示限速范围为（80,120）
speedlimit=SpeedLimit(".2",speedrange);//表示车道".2"的限速为speedrange所描述
```
#### Traffic
表示交通约束，一个Traffic拥有多个``SpeedLimitation``和``IntersectionTraffic``对象

#### Scenario
表示一个场景，一个场景拥有7个对象，分别是``Map``,``EgoVehicle``,``NPCVehicles``[可选],``Pedestrians``[可选],``Obstacles``[可选],``Environment``[可选],``Traffic``[可选]
<br />通过成员函数``get_map(),get_ego_vehicle(),get_npc_vehicles(),get_pedestrians(),get_obstacles(),get_environment(),get_traffic()``来获得对应的内容,
<br />在``AST``对象中，可以通过``get_scenarios()``来获得所有解析好的``Scenario``对象列表