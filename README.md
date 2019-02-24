# Graph Transformation System

**小组成员及分工**：

- 肖宇晗：图变换问题建模、A*算法实现、启发式蒙特卡洛的尝试
- 陈树银：图变换问题建模、随机算法与MCTS算法对广搜的优化、图匹配部分优化



------

### 项目介绍：

####  项目要求

1. 实现Graph Transformation和基本的搜索策略（DFS/BFS），使得对于任何给定的问题模型和问题实例，可以通过图变换得到一个满足目标的实例，并能判断无解的情况
2. 采用前述模型来描述某一个问题，问题的类型不限，但应该对于搜索具有一定的复杂性，给出问题的模型，以及若干复杂程度不等的实例
3. 尝试给出**问题无关**的搜索优化策略，使得对于不同的问题，都可以在一定程度上减少搜索的时间（或空间）



####  模型格式说明

模型包含`metamodel.json`、`rules.json`、`goal.json`以及任意文件名的json格式实例模型

#####  metamodel.json

一个json对象，其中包含

- `classes`：json数组，包含问题中所有的类，每一个类中包含
  - `id`：必须，不与其他类id重复，类的唯一标识
- `relations`：json数组，包含问题中所有的关系，每一个关系中包含
  - `id`：必须，不与其他关系id重复，关系的唯一标识
  - `source`：必须，为某一类的id，表示关系的源端
  - `target`：必须，为某一类的id，表示关系的目标端
  - `name`：可选，关系的名称，用于展示，如不包含该字段，将用id字段展示

#####  rules.json

所有的规则组成的json数组，每一个规则包含

- `id`：必须，不与其他规则id重复，规则的唯一标识
- `lhs`：必须，规则的左部（用于匹配），包含一个[对象图](#obj_diagram)
- `rhs`：必须，规则的右部（用于替换左部），包含一个[对象图](#obj_diagram)
- `nacs`：可选，规则的negative application conditions（用于限制规则的适用条件，如果任意一个nac被匹配，则无法apply该rule），包含一个nac的json数组，nac为[对象图](#obj_diagram)的形式
  - `lhs`、`rhs`、`nac`中的对象id只表示他们之间的点（对象）映射关系，**并不具有实际含义**。在与某一实例图匹配的时候，只需考虑类和关系是否匹配
  - `lhs`和`rhs`、`lhs`和`nac`中相同id的对象表示为同一个对象（“会被保留的对象”），只出现于`lhs`的对象为“会被删除的对象”，只出现于`rhs`的对象为“将要新增的对象”
  - 由morphism的定义可知，一旦确定点（对象）的映射关系，边（关系实例）的映射关系亦可确定，即两侧源、目标和类型均相同的关系实例被视为是identical的，若在另一侧找不到对应的关系实例，则被视为是新增/删除的

#####  goal.json

目标的json对象，包含

- `graph`：可选，满足目标所需要匹配的[对象图](#obj_diagram)
- `nacs`：可选，目标的negative application conditions（如果任意一个nac被匹配，则视为没有满足目标）
  - `graph`与`nacs`不应同时为空，否则goal将没有意义
  - 与规则类似，`graph`和`nac`中的对象id没有实际含义，只表示`graph`与`nac`之间的映射关系



#####  实例模型

一个[对象图](#obj_diagram)

##### <a name="obj_diagram">对象图</a>

一个json对象，包含

- `objects`：必须，json数组，包含对象图中所有的对象，每一个对象包含
  - `id`：必须，不与其他对象id重复，对象的唯一标识
  - `type`：必须，为metamodel中某一个类的id，对象的类型
  - `name`：可选，对象的别名，用于展示，如不包含该字段，将用id字段展示
- `relations`：可选，json数组，包含对象图中所有的关系实例，每一个关系实例包含
  - `type`：必须，为metamodel中某一个关系的id，关系实例的类型
  - `source`：必须，为某一对象的id，表示关系的源端
  - `target`：必须，为某一对象的id，表示关系的目标端
    - 关系实例**不能**包含id，一个关系实例应该是由上述三个字段唯一确定的





------

### 程序框架：

* 图建模：`GraphBuilding.py`
* 图变换：`GraphTransformer.py`
* 图匹配：`GraphMatch.py`
* 问题输入与输出：`Input.py`、`Output.py`
* 图问题的算法：`GraphAlgorithm.py`



------

### 程序说明：

* **图建模：`GraphBuilding.py`**

  封装了`Edge`、`Node`、`Graph`三个类，并进行了类的相关测试。

  ![](https://ws3.sinaimg.cn/large/006tKfTcly1fsb3roiargj30f20a2aa3.jpg)



* **图变换：`GraphTransformer.py`**

  封装了`Rule`、`Transformer`类，定义了`getDiff`函数，并进行了相关测试。

  ![](https://ws2.sinaimg.cn/large/006tKfTcly1fsb3s0bxvpj30q00s8t9h.jpg)



* **图匹配：`GraphMatch.py`**

  封装了`Match`类，并进行了相关测试。

  ![](https://ws1.sinaimg.cn/large/006tKfTcly1fsb3sb01qnj30p20g0dgb.jpg)



* **问题输入与输出：`Input.py`、`Output.py`**

  * `Input.py`

    ![](https://ws3.sinaimg.cn/large/006tKfTcly1fsb3ufkm2ej30ow0du74k.jpg)

  * `Output.py`

    ![](https://ws1.sinaimg.cn/large/006tKfTcly1fsb3v6gehyj30su04cq2x.jpg)



* **图问题的算法：`GraphAlgorithm.py`**

  一共做了四次优化：

  * 广搜：**`GraphAlgorithm_0.py`**中的`bfs`函数部分（搭配`GraphMatch_0.py`）
  * 广搜 + 图匹配剪枝：**`GraphAlgorithm_0.py`**中的`bfs`函数部分（搭配`GraphMatch.py`）
  * 随机 + 图匹配剪枝：**`GraphAlgorithm.py`**中的`bfs`函数部分
  * A* + 图匹配剪枝：**`GraphAlgorithm_0.py`**中的`aStar`函数部分
  * MCTS + 图匹配剪枝：写了代码，但bug未能完全解决…...

**图匹配方面的优化：**

* 暴力：先检查点类型，得到匹配之后check任意两点间边类型是否相同；

* 剪枝（VF2）：检查点类型时check边类型是否满足条件从而进行剪枝；

  效果：有一点效果，但不是非常显著

**搜索算法的优化：**

* **随机**：拉斯维加斯算法，仅在广搜的基础上做了少许改动，随机选取下一层结点，对问题无关有一点效果； 
* **A***：`f(x)=g(x)+h(x)`，以`f(x)`为选择下一层结点的依据，值越小，优先级越高；
  * `g(x)`：当前图状态距离原图的“距离”
  * `h(x)`：当前图状态距离goal的“距离”
* **MCTS**：主要使用UCT算法

**关于随机算法：**

选用拉斯维加斯算法的初衷并不是指望它会比广搜有多明显的效果，如果说广搜是一种盲目搜索，那么拉斯维加斯也只是一个基于概率的盲目搜索而已。之所以尝试它，出于以下几点原因：

* 启发式搜索其实是非常依赖于具体问题的特性的。一个启发式搜索写得怎么样，取决于其启发式函数的设计；而启发式函数的设计好坏，又取决于对问题特征的提取。成功与否，皆在于启发式函数。我们所要研究的问题是给出与问题无关的优化策略，那么在这种情况下，启发式搜索很难有普适性的明显效果。所以在一开始做project时，对启发式并不看好。
* 大家基本都采用启发式搜索，这样会不会限制了我们的优化思路？由于问题的特性与启发式搜索的适用条件存在一定矛盾，我们是否可以寻找一个更恰当的突破口，弱化搜索策略的适用要求，使其与我们的问题更为贴切？
* 因此我们想到的是将概率结合进来。概率论知识在生活中有着相当强大的普适性。我们希望能将它应用到我们的优化策略中，加以调整，从而比启发式搜索拥有更好的普适性。拉斯维加斯便是我们最开始的尝试。其实从数学上分析，拉斯维加斯平均下来得到的结果是一个期望值，而广搜得到的是一个确定值，极其依赖于实例的特性（如果实例足够好，广搜效果将是最好的，上来就能搜出结果）。即使是最简单的随机算法，都会比广搜具有更好的普适性，在适用性上有更理想的效果。

**关于A*算法**

虽说对A*并不是很看好，但我们还是做出尝试，希望能从图结构的共同特征中提取出一些有用的信息来支撑起我们的启发式函数。同时，也为我们将问题的启发性与策略的普适性结合起来做一个铺垫。

- 准备工作：

 * 很简单，利用python内置的heapq维护一个优先队列
- 启发式函数：
 * `f = g + h`，关于`g`，我们使用的是精确图编辑距离，即现图与goal的差距，应该严格删掉多少边，删去多少点，加多少点，加多少边，把这些严格计算好得出的编辑距离。这一步在我们的GraphTransformer里已经做好，是在进行图变换的过程中顺便完成的，不需额外花去时间，搜索算法直接使用结果就可。由于是精确图编辑距离，且几乎没有花费额外的时间代价，所以这一部分已经没有多少可优化的空间。关于`h`，我们使用的是近似图编辑距离。我们主要考虑了以下几种实现方案：

     * Manhattan distance：
     * Diagonal distance(这里为表示方便，以方格图中的Diagonal distance为例)：
    ![image](https://wx1.sinaimg.cn/mw690/0071tMo1ly1fshqkrviy4j30d202rwee.jpg)
     * Euclidean distance
 ![image](https://wx1.sinaimg.cn/mw690/0071tMo1ly1fshqlt2hlfj309f02twee.jpg)
 综合考虑之后，我们选择使用Euclidean distance。这三个距离衡量一开始都是针对方格图的问题而被应用于启发式搜索的，所以存在一个转换使用的问题。选用Euclidean distance的原因有二。一是Euclidean distance转换到图问题上比较方便，Diagonal距离存在一个参数D2，需要遍历一遍邻图取最小的图变换代价，时间代价太过高昂；二来实现上比较简单直观(效果稍微比Manhattan distance稍微好一点点)，主要是计算点数之差与边数之差。
 在实现A*时，我们还阅读了一些关于Fast computation of graph edit distance的论文，希望能有更好的图编辑距离算法，例如BSS-GED。其伪代码如下：
        ![image](https://wx1.sinaimg.cn/mw690/0071tMo1ly1fshqn8w2dqj308r0gc0uf.jpg) 
 迫于代码水平，没有能在考试周之前实现。 
 * 在进行了如上的启发式函数设计后，发现效果并不是特别明显，对于有些特征很不好的问题（例如过河问题），A*的表现甚至不如广搜。因此，结合输入中的nac条件，尝试将nac的个数作为一个参数代入启发式函数中。我们对nac的估值是分为两部分的，一部分是在匹配rule的左图时记录匹配到的rule.nac的数目，另一部分是在计算现图与goal的近似图编辑距离时，记录现图中有多少个goal的nac。最后发现对于八数码问题，后者的nac数目更有效。并且对于有nac的输入来说，效果非常明显。具体情况在后文的表格中有展示。 
* 对`A*`的改进思路与问题： 
 在得出一些结果之后，考虑对`A*`本身进行优化。之前有看过`Dynamic A* and Lifelong Planning A*`以及`Dynamic Weighting`，所以考虑是否可以在`g`或`h`的前面加上一个系数，该系数与搜索的结点或搜索时间存在一个函数关系。但由于不同的问题搜索结点数与搜索时间大相径庭，很难给出这么一个普适性的函数，故该想法存在很大的问题，没有能够得到实现。


**关于MCTS树搜索算法的实现思路：**

共分4个步骤：

* 扩展(Expansion)：在当前获得的统计结果不足以计算出下一个步骤时，随机选择一个子步骤；
* 模拟(Simulation)：模拟进入下一步；
* 反向传播(Back-Propagation)：根据结束的结果，计算对应路径上统计记录的值；
* 选举(selection)：根据当前获得所有子步骤的统计结果，选择一个最优的子步骤

UCT算法过程：

* 首先，初始状态下，所有的子步骤都没有统计数据；

  ![](https://ws4.sinaimg.cn/large/006tKfTcly1fsbxz2j2xdj30a5057weh.jpg)

* 先做**扩展(Expansion)**，随机选择一个子步骤，不停的**模拟(Simulation)**，直到游戏结束。然后**反向传播(Back-Propagation)**，记录扩展步骤的统计数据；

  ![](https://ws4.sinaimg.cn/large/006tKfTcly1fsby062znwj308s0damxd.jpg)

* 多次**扩展(Expansion)**之后，达到了**选举(selection)**的条件，开始**选举(selection)**，选出最优的一个子步骤；

  ![](https://ws1.sinaimg.cn/large/006tKfTcly1fsby16zjxcj30cc05mt8s.jpg)

* 继续**扩展(Expansion)**，**模拟(Simulation)**，**反向传播(Back-Propagation)**；

  ![](https://ws1.sinaimg.cn/large/006tKfTcly1fsby0uwh7vj30fq0dfwf1.jpg)

其中关于结点选择：

在树向下遍历时的节点选择通过选择最大化某个量来实现，我们常常使用UCB公式用来计算：

![](https://ws2.sinaimg.cn/large/006tKfTcly1fsby2vmxuqj305k020a9u.jpg)

其中 $v_i$是节点估计的值，$n_i$ 是节点被访问的次数，而 N 则是其父节点已经被访问的总次数，C 是可调整参数。



**关于MCTS树搜索算法的思考：**

* 这也是在写完代码之后发现的：针对较难的八数码问题，问题的复杂性不在于其搜索树的宽度，而在于树的深度，如果采用给定时间作为模拟出口的话，那么在选取时很容易出现各结点评价值均为0的现象，那么此时MCTS方法就退化成了一般随机算法，且效果可能还会差于广搜。基于这一点，肖宇晗同学认为可以将启发式函数估值结合到MCTS方法中，从而避免出现均为0的情况；





------

### 程序测试：

**问题**：共选取了7个具体问题

* 推箱子：样例
* 过河问题：直接借用的其他组测试用的JSON
* 句法分析（简单）：直接借用的其他组测试用的JSON
* 句法分析（进阶）：直接借用的其他组测试用的JSON
* 四数码（3021）：
* 八数码（简单）：
* 八数码（进阶）：

**测试结果：**

![](https://ws2.sinaimg.cn/large/006tKfTcly1fshx6yxd2gj31280fugo8.jpg)

![](https://ws3.sinaimg.cn/large/006tKfTcly1fshx8go2i7j312a0fy779.jpg)



**结果说明：**

* 除八数码（进阶）问题外，其他问题均测试100次以上取均值（随机算法测试次数更多）得到表中数据；

* 八数码（进阶）的广搜（未加剪枝）没有跑，预计耗时较长且毫无意义，主要比较的是加了剪枝优化的广搜。因为比较耗时且广搜的搜索效果不存在不稳定性，所以优化算法只运行了一次；

* 句法分析问题中主要是剪枝起到良好效果，随机只是在剪枝的基础上对广搜进行一点优化；

* 随机算法对广搜算法有优化效果，效果不是很显著；

* `A*`算法在过河问题上（该问题的特征不是很适合我们的A*）表现较差，而在八数码问题上表现良好。待搜索结点数越多，表现越好；对于拥有nac（尤其是goal的nac）的问题，表现尤为突出。

  

  

------

### 遇到的问题及方案（这里只是一个陈列，特定算法的具体问题在上面已有提及）：

* 问题：图问题的建模是个比较细致的工作， 因为在图变换问题中属于底层基础部分，所以必须做到尽可能少bug，且接口实现要简单良好，避免在后期调试时带来更多困扰；

  方案：两个人（陈树银和肖宇晗）同时写一份建模的文件，交流并相互补充取较完善的一份；

* 问题：前期工作中建立的八数码模型存在一定问题，导致后期的算法一直无法得到八数码问题的解；

  方案：仔细分析调试之后发现了JSON中的存在的问题，并参考了其他组的JSON模型，修改之后得到新的八数码模型后，算法能够正常运行得到解；

* 问题：算法方面，起初A*一直表现不好，广搜对于复杂问题又耗时太久，搜索结点数一直降不下来

  方案：在继续修改A*算法的同时，进行其他的算法改进，如随机算法、MCTS;



### 感想：

* 图的底层实现至关重要，无论是建模还是变换匹配等，都是会影响后期算法的运行，导致出现一些难调的bug，非常耗时间和精力。

* 算法优化时发现启发式搜索策略要想实现问题无关的性能优化是很困难的，然而随机化的策略似乎具备了实现这种要求得到特征，但初步的随机算法效果不是非常显著。为此，在写完A*和拉斯维加斯后，我们将两者特征结合起来，由此进行MCTS的探索。

* MCTS算法是一种比较高级的随机算法，通常适用于组合博弈问题，本来想通过一定的变换用于此处的图变换问题的求解，但是实现的时候发现传统的蒙特卡洛局限性比较大，可以考虑将UCB公式中的Vi替换为h的某种形式。这样，UCB公式的左部具有启发性，右部与结点访问次数有关（与问题关系很小），具有普适性，即所谓的启发式蒙特卡洛搜索，将启发性与普适性结合在一起。

  

------

### 参考文献：
【1】Chen X, Huo H, Huan J, et al. Fast Computation of Graph Edit Distance[J]. arXiv preprint arXiv:1709.10305, 2017.

【2】徐周波,张鵾,宁黎华,古天龙.图编辑距离概述[J].计算机科学,2018,45(04):11-18. 

【3】http://theory.stanford.edu/~amitp/GameProgramming/

【4】Huttenlocher D P, Klanderman G A, Rucklidge W J. Comparing images using the Hausdorff distance[J]. IEEE Transactions on pattern analysis and machine intelligence, 1993, 15(9): 850-863.







