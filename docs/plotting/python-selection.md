# Python科研绘图选型记忆
依据：通用建模图型阅读与Matplotlib官方文档，2026-11-01。先问要回答什么问题，再检查数据结构，最后选图。

|研究问题|合适图型|最小数据结构|Python实现方向|
|---|---|---|---|
|一个量随时间/连续自变量如何变化|折线/点线图|x、y、series_id；x的顺序有物理意义|Axes.plot；未排序散点用scatter|
|多个模型/条件的轨迹有何差异|多曲线，条件较多则分面|x、value、model、scenario、initial_state|subplots或GridSpec；统一比较用共同轴范围|
|模型贴合参考值到什么程度|上方对照曲线，下方残差联图|x、reference、prediction、residual，指标定义|sharex子图、plot、axhline；必要时区间带|
|估计的不确定性如何变化|中心线+区间带|x、estimate、lower、upper、区间构造方法|plot+fill_between；缺失位置保留断点|
|总量由哪些组件构成|堆叠柱/随时间连续构成的堆叠面积|group/time、component、value，数值同单位且可相加|bar的bottom累计；连续过程才考虑stackplot|
|多个方案的终值/增幅如何排序|水平条形图|category、outcome、baseline、gain定义|barh、axvline、直接标签；条形通常含零|
|哪个参数变化影响较大且方向如何|龙卷风式正负条形+参数扫描曲线|parameter、low/base/high及响应差、相同扰动尺度|barh正负值、零线；扫描用plot，按预先定义的影响量排序|
|扰动如何影响输出|输入与输出上下配对分面|time、input、baseline_output、perturbed_output|GridSpec、sharex；真实阶跃用step/stairs|
|两种单位的同时间输入输出如何对齐|优先上下联图；必要时双Y|共同time、两个有单位的量|subplots；必要时twinx并清楚标注对应关系|
|两个因素怎样共同影响一个输出|热图+等高线|x轴、y轴、Z网格或可解释的XYZ样本|pcolormesh/contour；不规则样本考虑tricontour|
|接近重叠的轨迹差异在哪里|局部放大或独立差值图|原坐标、两组输出、放大范围或差值|inset_axes/差值子图；保留主图上下文|
|如何解释方法/物理结构|流程/机制图|节点、边、方向、含义、证据|按任务选择图示工具；不伪装成数值曲线|

## 数据准备
推荐长表：
    time, scenario, initial_state, model, component, value, unit
区间数据：
    time, estimate, lower, upper, interval_type, level, source
参数扫描：
    parameter, parameter_value, baseline_value, response, scenario
二维响应：
    factor_x, factor_y, response, unit

同一图中模型和参考值要有共同定义、单位和对齐规则。不同时间采样可以显式插值，但保留方法与原始数据；缺失不是零。

## 画图前后必须讲清楚
- 组件组成数据可相加；若归一化为100%，明确已从绝对量改为占比。
- 区间可能是SD、SE、置信区间、预测区间或分位带；逐项注明。不能从漂亮阴影推断含义。
- 消融固定其余条件；敏感性声明参数扰动幅度；前后对比用可比的数据与轴尺度。
- 多面板共用颜色、线型和排序。为不同单位设置独立标签；不调双轴制造相关性。
- 保存原始表、变换规则、绘图脚本、版本、输出尺寸和图件来源。原论文曲线不作为本次新增实测数据。
- 本次学习没有重建任何实验数据，也没有运行拟合或重新绘制定量曲线。

## 官方参考
- https://matplotlib.org/stable/plot_types/
- https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.fill_between.html
- https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.bar.html
