# Origin科研绘图选型记忆
2026-11-01。与Python共享“研究问题-图型-数据结构”的判断，软件实现与可编辑工程分别记录。

|用途|Origin图型/组织方式|工作表或矩阵数据要求|
|---|---|---|
|多模型/多条件轨迹|Line或Line+Symbol；多层/合并多面板|A列X，B及之后各列Y；长表需按group拆分或使用索引绘图|
|模型-参考对照与残差|上层叠加曲线，下层残差，共享X|X、reference、prediction、residual；残差先按明确口径计算|
|估计区间|中心线+上下界两曲线之间填充|X、center、lower、upper；lower/upper不是普通Y误差值|
|组件构成|Stacked Column/Bar；连续过程可考虑Stacked Area|分类/时间X，各组件独立Y列，单位相同，可相加|
|方案/消融终值比较|Horizontal Bar，加参考线和标签|类别、response、baseline、gain；通常从零起算|
|正负敏感性排名|以零为基准的左右水平条形/龙卷风式|参数类别、low响应差、high响应差；同一基准与扰动定义|
|参数扫描|Line+Symbol分面|扫描参数X，各响应Y；多个参数面板不要混淆单位|
|输入与输出扰动配对|上下多层并链接X轴|共同time及input、baseline_output、perturbed_output|
|两个量共用时间但单位不同|优先上下联图；必要时Double-Y|time、left_Y、right_Y及单位，记录每条曲线所属轴|
|二维响应热图/等高线|Contour Color Fill/Heatmap|指定X、Y、Z的三列，或有坐标范围的Z矩阵|
|局部放大|Inset Layer或差值子图|保留同一原始数据和明确放大范围|
|方法/物理结构图|独立图示，不套用数值绘图模型|节点、连线、变量与解释，而不是强行生成XY表|

## 容易混淆的情况
- 从上下界曲线填充区域时，要保留lower/upper的定义与区间水平。统计拟合软件自动生成的拟合置信带，与外部模型提供的状态估计区间不是同一来源。
- 纵向误差列通常保存误差幅度，不能直接把“上界”整列当成Y误差；上界减中心、中心减下界才是相应幅度，且可能不对称。
- 原案例二维热图+等高线不是3D Surface。确需曲面时也需要有意义的XYZ或矩阵坐标，不能用外观生成缺失的响应值。
- XYZ转矩阵涉及网格化/插值；保存原XYZ、算法、网格范围与缺失区策略。官方亦支持从XYZ直接绘制等高线/曲面。
- 双Y轴的一层/两层实现随Origin版本与图模板而异；检查实际窗口和图层，不能把两个轴混当一个标度。

## 自动化与交付
先用read_origin_session读取真实工程，再导入/编辑。当前可见MCP的create_plot支持X/Y列与误差列参数，且有create_double_y_plot；不能因为plot_type接受字符串就声称所有复杂图型均已验证。
复杂图型按实际工具能力或本机界面完成，并检查最终图层与数据绑定。本次只建立选图记忆，未声称生成Origin工程。
只有真实保存了OPJU及对应工作表后，才称为可编辑Origin交付；另留源CSV和导出图。

## 官方参考
- https://docs.originlab.com/quick-help/xyz-contour-surface/
- https://docs.originlab.com/quick-help/fill-area-two-curve/
- https://docs.originlab.com/quick-help/create-double-y/
